from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import csv
import time
import pandas as pd
import threading

csv_path = './dataset/movie.csv'

page_per_genre = 1

urls = [
    # 'https://www.imdb.com/search/title/?genres=adventure&sort=user_rating,desc&title_type=feature&num_votes=25000,&pf_rd_m=A2FGELUUNOQJNL&pf_rd_p=94365f40-17a1-4450-9ea8-01159990ef7f&pf_rd_r=YNTYFE4J51JTTVJEWBRF&pf_rd_s=right-6&pf_rd_t=15506&pf_rd_i=top',
    # 'https://www.imdb.com/search/title/?genres=fantasy&sort=user_rating,desc&title_type=feature&num_votes=25000,&pf_rd_m=A2FGELUUNOQJNL&pf_rd_p=94365f40-17a1-4450-9ea8-01159990ef7f&pf_rd_r=YNTYFE4J51JTTVJEWBRF&pf_rd_s=right-6&pf_rd_t=15506&pf_rd_i=top',
    'https://www.imdb.com/search/title/?genres=animation&sort=user_rating,desc&title_type=feature&num_votes=25000,&pf_rd_m=A2FGELUUNOQJNL&pf_rd_p=94365f40-17a1-4450-9ea8-01159990ef7f&pf_rd_r=YNTYFE4J51JTTVJEWBRF&pf_rd_s=right-6&pf_rd_t=15506&pf_rd_i=top',
    # 'https://www.imdb.com/search/title/?genres=action&sort=user_rating,desc&title_type=feature&num_votes=25000,&pf_rd_m=A2FGELUUNOQJNL&pf_rd_p=94365f40-17a1-4450-9ea8-01159990ef7f&pf_rd_r=YNTYFE4J51JTTVJEWBRF&pf_rd_s=right-6&pf_rd_t=15506&pf_rd_i=top',
    # 'https://www.imdb.com/search/title/?genres=drama&sort=user_rating,desc&title_type=feature&num_votes=25000,&pf_rd_m=A2FGELUUNOQJNL&pf_rd_p=94365f40-17a1-4450-9ea8-01159990ef7f&pf_rd_r=YNTYFE4J51JTTVJEWBRF&pf_rd_s=right-6&pf_rd_t=15506&pf_rd_i=top',
    # 'https://www.imdb.com/search/title/?genres=sci_fi&sort=user_rating,desc&title_type=feature&num_votes=25000,&pf_rd_m=A2FGELUUNOQJNL&pf_rd_p=94365f40-17a1-4450-9ea8-01159990ef7f&pf_rd_r=YNTYFE4J51JTTVJEWBRF&pf_rd_s=right-6&pf_rd_t=15506&pf_rd_i=top',
    # 'https://www.imdb.com/search/title/?genres=animation&sort=user_rating,desc&title_type=tv_series,mini_series&num_votes=5000,&pf_rd_m=A2FGELUUNOQJNL&pf_rd_p=015e490c-cb1b-4813-8798-a957282ed1f4&pf_rd_r=7ZQB5WZC4PXX67DQJN56&pf_rd_s=right-6&pf_rd_t=15506&pf_rd_i=toptv',
    # 'https://www.imdb.com/search/title/?genres=romance&sort=user_rating,desc&title_type=feature&num_votes=25000,&pf_rd_m=A2FGELUUNOQJNL&pf_rd_p=94365f40-17a1-4450-9ea8-01159990ef7f&pf_rd_r=VA7KJ198KYDATR75M4VN&pf_rd_s=right-6&pf_rd_t=15506&pf_rd_i=top&ref_=chttp_gnr_16',
    # 'https://www.imdb.com/search/title/?genres=family&sort=user_rating,desc&title_type=feature&num_votes=25000,&pf_rd_m=A2FGELUUNOQJNL&pf_rd_p=94365f40-17a1-4450-9ea8-01159990ef7f&pf_rd_r=D0AV71R4VZND8XBJPGPB&pf_rd_s=right-6&pf_rd_t=15506&pf_rd_i=top&ref_=chttp_gnr_8',
    # 'https://www.imdb.com/search/title/?genres=family&sort=user_rating,desc&title_type=feature&num_votes=25000,&pf_rd_m=A2FGELUUNOQJNL&pf_rd_p=94365f40-17a1-4450-9ea8-01159990ef7f&pf_rd_r=D0AV71R4VZND8XBJPGPB&pf_rd_s=right-6&pf_rd_t=15506&pf_rd_i=top&ref_=chttp_gnr_8',
    # 'https://www.imdb.com/search/title/?title_type=feature&num_votes=25000,&genres=animation&sort=user_rating,desc&start=201&ref_=adv_nxt',
    # 'https://www.imdb.com/search/title/?genres=music&sort=user_rating,desc&title_type=feature&num_votes=25000,&pf_rd_m=A2FGELUUNOQJNL&pf_rd_p=94365f40-17a1-4450-9ea8-01159990ef7f&pf_rd_r=D0AV71R4VZND8XBJPGPB&pf_rd_s=right-6&pf_rd_t=15506&pf_rd_i=top&ref_=chttp_gnr_13',
    # 'https://www.imdb.com/search/title/?genres=animation&title_type=tv_series,mini_series&pf_rd_m=A2FGELUUNOQJNL&pf_rd_p=4bb13f2c-7ee0-413a-ae38-5cf423b577a4&pf_rd_r=3BY5FBA7X3ER8Y9MWWE3&pf_rd_s=right-6&pf_rd_t=15506&pf_rd_i=tvmeter',
    # 'https://www.imdb.com/search/title/?genres=adventure&title_type=tv_series,mini_series&pf_rd_m=A2FGELUUNOQJNL&pf_rd_p=4bb13f2c-7ee0-413a-ae38-5cf423b577a4&pf_rd_r=3BY5FBA7X3ER8Y9MWWE3&pf_rd_s=right-6&pf_rd_t=15506&pf_rd_i=tvmeter',
    # 'https://www.imdb.com/search/title/?genres=action&title_type=tv_series,mini_series&pf_rd_m=A2FGELUUNOQJNL&pf_rd_p=4bb13f2c-7ee0-413a-ae38-5cf423b577a4&pf_rd_r=3BY5FBA7X3ER8Y9MWWE3&pf_rd_s=right-6&pf_rd_t=15506&pf_rd_i=tvmeter',
    # 'https://www.imdb.com/search/title/?genres=sci_fi&title_type=tv_series,mini_series&pf_rd_m=A2FGELUUNOQJNL&pf_rd_p=4bb13f2c-7ee0-413a-ae38-5cf423b577a4&pf_rd_r=3BY5FBA7X3ER8Y9MWWE3&pf_rd_s=right-6&pf_rd_t=15506&pf_rd_i=tvmeter',
    # 'https://www.imdb.com/search/title/?genres=musical&title_type=tv_series,mini_series&pf_rd_m=A2FGELUUNOQJNL&pf_rd_p=4bb13f2c-7ee0-413a-ae38-5cf423b577a4&pf_rd_r=3BY5FBA7X3ER8Y9MWWE3&pf_rd_s=right-6&pf_rd_t=15506&pf_rd_i=tvmeter',
    # 'https://www.imdb.com/search/title/?genres=drama&title_type=tv_series,mini_series&pf_rd_m=A2FGELUUNOQJNL&pf_rd_p=4bb13f2c-7ee0-413a-ae38-5cf423b577a4&pf_rd_r=3BY5FBA7X3ER8Y9MWWE3&pf_rd_s=right-6&pf_rd_t=15506&pf_rd_i=tvmeter',
    # 'https://www.imdb.com/search/title/?genres=fantasy&title_type=tv_series,mini_series&pf_rd_m=A2FGELUUNOQJNL&pf_rd_p=4bb13f2c-7ee0-413a-ae38-5cf423b577a4&pf_rd_r=3BY5FBA7X3ER8Y9MWWE3&pf_rd_s=right-6&pf_rd_t=15506&pf_rd_i=tvmeter',
    # 'https://www.imdb.com/search/title/?genres=comedy&title_type=tv_series,mini_series&pf_rd_m=A2FGELUUNOQJNL&pf_rd_p=4bb13f2c-7ee0-413a-ae38-5cf423b577a4&pf_rd_r=3BY5FBA7X3ER8Y9MWWE3&pf_rd_s=right-6&pf_rd_t=15506&pf_rd_i=tvmeter',
    # 'https://www.imdb.com/search/title/?genres=comedy&sort=user_rating,desc&title_type=feature&num_votes=25000,&pf_rd_m=A2FGELUUNOQJNL&pf_rd_p=94365f40-17a1-4450-9ea8-01159990ef7f&pf_rd_r=XJRVBNHADCZ9HJCG5JH0&pf_rd_s=right-6&pf_rd_t=15506&pf_rd_i=top&ref_=chttp_gnr_5'
]

def thread_handler(url):
    driver = webdriver.Edge()

    df = pd.read_csv(csv_path)
    driver.get(url)
    new_movie_count = 0

    for i in range(0, page_per_genre):
        time.sleep(2)

        next_page_element = driver.find_elements(By.CLASS_NAME, 'next-page')[-1]

        actions = ActionChains(driver)
        actions.move_to_element(next_page_element).perform()

        time.sleep(5)

        movie_list_element = driver.find_element(By.CLASS_NAME, 'lister-list').find_elements(By.CLASS_NAME, 'mode-advanced')
        
        count = 0
        movies = []

        for row in movie_list_element:
            try:
                poster_column = row.find_element(By.CLASS_NAME, 'lister-item-image').find_element(By.TAG_NAME, 'img')
                title_column = row.find_element(By.CLASS_NAME, 'lister-item-header').find_element(By.TAG_NAME, 'a')
                rating_column = row.find_element(By.CLASS_NAME, 'ratings-bar').find_element(By.TAG_NAME, 'strong')
                
                poster_url = poster_column.get_attribute('src')
                movie_title = title_column.text
                movie_url = title_column.get_attribute('href')[0:title_column.get_attribute('href').index('?') - 1]
                movie_id = movie_url[movie_url.rindex('/') + 1:]
                movie_rating = rating_column.text

                if (movie_id not in df['id'].values):
                    movies.append([movie_id, movie_title, movie_url, poster_url, movie_rating])
                    new_movie_count += 1
            except Exception as e:
                print(str(e))
                continue

            count += 1
            if count % 50 == 0:
                print('Process ' + str(count) + ' movies...')

        driver.execute_script('arguments[0].click();', next_page_element)
    print('New movie inserted: ' + str(new_movie_count))
    with open(csv_path, 'a', newline='') as f:
        writer = csv.writer(f)
        for data in movies:
            writer.writerow(data)
    time.sleep(2)
    driver.quit()

for url in urls:
    th = threading.Thread(target=thread_handler, args=[url])
    th.start()