import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter

df_movie = pd.read_csv('./crawler/dataset/movie.csv')
df_rating = pd.read_csv('./crawler/dataset/rating.csv')

df_rating['composite'] = df_rating['user_id'] + df_rating['movie_id'] + df_rating['rate'].apply(str)

user_id_count = Counter(df_rating['user_id'])
movie_ids_count = Counter(df_rating['movie_id'])

number_of_user = 10000
number_of_movie = 500

user_ids = [u for u, c in user_id_count.most_common(number_of_user)]
movie_ids = [m for m, c in movie_ids_count.most_common(number_of_movie)]

df_small = df_rating[df_rating['user_id'].isin(user_ids) & df_rating['movie_id'].isin(movie_ids)].copy()
df_small = df_small.drop_duplicates(keep='last')

print(len(df_small) / (number_of_user * number_of_movie))
# print(len(df_rating['composite'].unique()))

# temp_df = df_rating.drop_duplicates(keep='last').groupby('movie_id').count().sort_values(by='rate', ascending=False)
# temp_df['rate'] = temp_df['rate'].apply(int)
# a = temp_df.where((temp_df.rate < 600) & (temp_df.rate > 100))
# a = a.loc[a.rate.isnull() == False]
# print(a['rate'].sum())
# print(a)