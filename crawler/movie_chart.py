from selenium import webdriver
from selenium.webdriver.common.by import By
import csv
import pandas as pd

csv_path = './dataset/movie.csv'

urls = [
    # 'https://www.imdb.com/chart/bottom',
    # 'https://www.imdb.com/chart/toptv',
    # 'https://www.imdb.com/chart/tvmeter',
    # 'https://www.imdb.com/chart/top-english-movies',
    # 'https://www.imdb.com/chart/top',
    'https://www.imdb.com/chart/moviemeter'
]

driver = webdriver.Edge()
for url in urls:
    df = pd.read_csv(csv_path)

    driver.get(url)
    
    movie_list_element = driver.find_element(By.CLASS_NAME, 'lister-list').find_elements(By.TAG_NAME, 'tr')
    count = 0
    new_movie_count = 0
    movies = []

    for row in movie_list_element:
        try:
            poster_column = row.find_element(By.CLASS_NAME, 'posterColumn').find_element(By.TAG_NAME, 'img')
            title_column = row.find_element(By.CLASS_NAME, 'titleColumn').find_element(By.TAG_NAME, 'a')
            rating_column = row.find_element(By.CLASS_NAME, 'imdbRating').find_element(By.TAG_NAME, 'strong')
            
            movie_title = title_column.text
            movie_url = title_column.get_attribute('href')[0:title_column.get_attribute('href').index('?') - 1]
            movie_id = movie_url[movie_url.rindex('/') + 1:]
            poster_url = poster_column.get_attribute('src')
            movie_rating = rating_column.text

            if (movie_id not in df['id'].values):
                movies.append([movie_id, movie_title, movie_url, poster_url, movie_rating])
                new_movie_count += 1
        except:
            pass

        count += 1
        if count % 50 == 0:
            print('Process ' + str(count) + ' movies...')

    print('New movie inserted: ' + str(new_movie_count))

    with open(csv_path, 'a', newline='') as f:
        writer = csv.writer(f)
        for data in movies:
            writer.writerow(data)

driver.quit()