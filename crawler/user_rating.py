from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.action_chains import ActionChains
import time
import pandas as pd
import threading
import csv
import numpy as np

csv_path = './dataset/rating.csv'
df = pd.read_csv('./dataset/rating_clean.csv')
df1 = pd.read_csv('./dataset/rating.csv')
users1 = set(df['user_id'].unique())
users2 = set(df1['user_id'].unique())
users = list(users2.difference(users1))
movies = df['movie_id'].unique()

current_user_index = 230
number_of_thread = 5
number_of_review_per_page = 100
number_of_review_per_user = 300

def get_url(index):
    return f"https://www.imdb.com/user/{users[index]}/ratings?ref_=nv_usr_rt_4"

def thread_handler(url):
    global current_user_index

    new_row_count = 0

    rating_df = pd.read_csv(csv_path)
    rating_df['composite'] = rating_df['user_id'] + rating_df['movie_id']
    
    data = []
    
    edge_option = Options()
    edge_option.add_argument("--headless")
    
    driver = webdriver.Edge(options=edge_option)
    driver.get(url)

    time.sleep(3)

    try:
        number_of_review = int(driver.find_element(By.ID, 'lister-header-current-size').text.replace(',', ''))

        if number_of_review < number_of_review_per_user:
            total_scroll = int(number_of_review / number_of_review_per_page)
        else:
            total_scroll = int(number_of_review_per_user / number_of_review_per_page)

        if total_scroll > 0:
            for i in range (0, total_scroll):
                if total_scroll > 1:
                    load_more_element = driver.find_elements(By.CLASS_NAME, 'next-page')[0]
                    actions = ActionChains(driver)
                    actions.move_to_element(load_more_element).perform()
                    time.sleep(1)

                rating_list_element = driver.find_element(By.ID, 'ratings-container').find_elements(By.CLASS_NAME, 'lister-item')
                for row in rating_list_element:
                    try:
                        movie_element = row.find_element(By.CLASS_NAME, 'lister-item-header').find_element(By.TAG_NAME, 'a')
                        rating_element = row.find_element(By.CLASS_NAME, 'ipl-rating-star__rating')

                        user_id = users[current_user_index]
                        movie_url = movie_element.get_attribute('href')[0:movie_element.get_attribute('href').index('?') - 1]
                        movie_id = movie_url[movie_url.rindex('/') + 1:]
                        rating = rating_element.text

                        if movie_id in movies and ((user_id + movie_id) not in rating_df['composite']):
                            data.append([movie_id, user_id, rating])
                            new_row_count += 1
                    except Exception as e:
                        continue
                if total_scroll > 1:
                    driver.execute_script('arguments[0].click();', load_more_element)
                    time.sleep(5)

    except Exception as e:
        print(e)
    
    print('New row inserted: ' + str(new_row_count))

    with open(csv_path, 'a', newline='') as f:
        writer = csv.writer(f)
        for row in data:
            writer.writerow(row)

    if current_user_index < len(users):
        current_user_index += 1
        th = threading.Thread(target=thread_handler, args=[get_url(current_user_index)])
        th.start()
        
    driver.quit()

for i in range(0, number_of_thread):
    th = threading.Thread(target=thread_handler, args=[get_url(current_user_index)])
    current_user_index += 1
    th.start()

# print(np.where(users == 'ur87808462'))