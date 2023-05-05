from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.action_chains import ActionChains
import time
import pandas as pd
import threading
import csv

csv_path = './dataset/rating.csv'
df = pd.read_csv('./dataset/movie.csv')
current_movie_index = 370
number_of_thread = 20
number_of_review_per_page = 25
number_of_review_per_movie = 300

WINDOW_SIZE = '1920,1080'


def get_url(index):
    return f"https://www.imdb.com/title/{df['id'][index]}/reviews"

def thread_handler(url):
    global current_movie_index

    new_row_count = 0

    rating_df = pd.read_csv(csv_path)
    rating_df['composite'] = rating_df['user_id'] + rating_df['movie_id']
    
    data = []
    
    edge_option = Options()
    edge_option.add_argument("--headless")
    
    driver = webdriver.Edge(options=edge_option)
    driver.get(url)

    # time.sleep(10)

    number_of_review_element = driver.find_elements(By.CLASS_NAME, 'header')[1].find_element(By.TAG_NAME, 'span')
    number_of_review = int(number_of_review_element.text.split(' ')[0].replace(',', ''))

    if number_of_review < number_of_review_per_movie:
        total_scroll = int(number_of_review / number_of_review_per_page)
    else:
        total_scroll = int(number_of_review_per_movie / number_of_review_per_page)

    if total_scroll > 0:
        load_more_element = driver.find_element(By.ID, 'load-more-trigger')
        for i in range (0, total_scroll):
            actions = ActionChains(driver)
            actions.move_to_element(load_more_element).perform()
            time.sleep(1)
            driver.execute_script('arguments[0].click();', load_more_element)
            time.sleep(5)

    rating_list_element = driver.find_element(By.CLASS_NAME, 'lister-list').find_elements(By.CLASS_NAME, 'lister-item')
    
    for row in rating_list_element:
        try:
            rating_element = row.find_element(By.CLASS_NAME, 'rating-other-user-rating').find_element(By.TAG_NAME, 'span')
            user_element = row.find_element(By.CLASS_NAME, 'display-name-link').find_element(By.TAG_NAME, 'a')

            user_url = user_element.get_attribute('href')[0:user_element.get_attribute('href').index('?') - 1]
            user_id = user_url[user_url.rindex('/') + 1:]
            movie_id = df['id'][current_movie_index]
            rating = rating_element.text

            if (user_id + movie_id) not in rating_df['composite']:
                data.append([movie_id, user_id, rating])
                new_row_count += 1
        except Exception as e:
            continue

    print('New row inserted: ' + str(new_row_count))

    with open(csv_path, 'a', newline='') as f:
        writer = csv.writer(f)
        for row in data:
            writer.writerow(row)

    if current_movie_index < len(df['id']):
        current_movie_index += 1
        th = threading.Thread(target=thread_handler, args=[get_url(current_movie_index)])
        th.start()
        
    driver.quit()

for i in range(0, number_of_thread):
    th = threading.Thread(target=thread_handler, args=[get_url(current_movie_index)])
    th.start()