from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.action_chains import ActionChains
import time
import pandas as pd
import threading
import csv
import numpy as np

csv_path = './dataset/movie_additional1.csv'
df = pd.read_csv('./dataset/movie_final.csv')
df1 = pd.read_csv(csv_path)

movies = list(set(df['id']).difference(set(df1['id'])))

print(movies)
print(len(movies))

current_movie_index = 0
number_of_thread = 5

def get_url(index):
    return f"https://www.imdb.com/title/{movies[index]}"

def thread_handler(url):
    global current_movie_index
    
    data = []
    
    edge_option = Options()
    # edge_option.add_argument("--headless")
    edge_option.add_argument("--window-size=2560,1440")
    
    driver = webdriver.Edge(options=edge_option)
    driver.get(url)

    time.sleep(3)

    try:
        elements = driver.find_element(By.CLASS_NAME, 'sc-52d569c6-0').find_elements(By.CLASS_NAME, 'ipc-inline-list__item')
        
        if len(elements) > 3:
            _, releaseYear, limitRate, duration = elements
        else:
            releaseYear, limitRate, duration = elements
        poster = driver.find_element(By.CSS_SELECTOR, '.ipc-media.ipc-media--poster-27x40.ipc-image-media-ratio--poster-27x40.ipc-media--baseAlt.ipc-media--poster-l.ipc-poster__poster-image.ipc-media__img').find_element(By.TAG_NAME, 'img')
        genres = driver.find_element(By.CLASS_NAME, 'sc-52d569c6-4').find_element(By.CLASS_NAME, 'ipc-chip-list__scroller').find_elements(By.TAG_NAME, 'a')
        languages = driver.find_element(By.CSS_SELECTOR, 'li[data-testid="title-details-languages"]').find_elements(By.TAG_NAME, 'a')
        origins = driver.find_element(By.CSS_SELECTOR, 'li[data-testid="title-details-origin"]').find_elements(By.TAG_NAME, 'a')
        elements = driver.find_element(By.CLASS_NAME, 'sc-52d569c6-3').find_elements(By.CLASS_NAME, 'ipc-metadata-list__item')
        origins = '|'.join([origin.text for origin in origins])
        languages = '|'.join([language.text for language in languages])
        companies = driver.find_element(By.CSS_SELECTOR, 'li[data-testid="title-details-companies"]').find_element(By.CLASS_NAME, 'ipc-metadata-list-item__content-container').find_elements(By.TAG_NAME, 'a')
        companies = '|'.join([company.text for company in companies])
        if len(genres) > 0:
            genres = '|'.join([genre.text for genre in genres])
        else:
            genres = '|'

        if len(elements) > 1:
            directors = elements[0].find_elements(By.TAG_NAME, 'a')
            directors = '|'.join([director.text for director in directors])
        else:
            directors = '|'
        if len(elements) > 2:
            writers = elements[1].find_elements(By.TAG_NAME, 'a')
            writers = '|'.join([writer.text for writer in writers])
        else:
            writers = '|'
       
        actors = driver.find_elements(By.CLASS_NAME, 'sc-bfec09a1-1')
        if len(actors) > 0:
            actors = '|'.join([actor.text for actor in actors])
        else:
            actors = '|'

    
        name = driver.find_element(By.CLASS_NAME, 'sc-afe43def-1').text
        data.append([url[url.rindex('/') + 1:], name, poster.get_attribute('src'), directors, writers, genres, actors, releaseYear.text, limitRate.text, duration.text, languages, origins, companies])
        # print(genres, actors, writers, directors, releaseYear.text, limitRate.text, duration.text, poster.get_attribute('src'))
        with open(csv_path, 'a', newline='') as f:
            writer = csv.writer(f)
            for row in data:
                writer.writerow(row)
    except Exception as e:
        print(e)

    if current_movie_index < len(movies):
        current_movie_index += 1
        th = threading.Thread(target=thread_handler, args=[get_url(current_movie_index)])
        th.start()
        
    driver.quit()

for i in range(0, number_of_thread):
    th = threading.Thread(target=thread_handler, args=[get_url(current_movie_index)])
    # current_movie_index += 1
    th.start()