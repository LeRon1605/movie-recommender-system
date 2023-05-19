import pandas as pd
import uuid

user_csv_path = '../dataset/user_final.csv'
movie_csv_path = '../dataset/movie_final.csv'
rating_csv_path = '../dataset/rating_final.csv'

df_movie = pd.read_csv(movie_csv_path)

def get_user_by_username(username):
    df_user = pd.read_csv(user_csv_path)
    user = df_user[df_user['username'] == username]
    if len(user) > 0:
        return (user.values[0][0], user.values[0][1])
    else:
        return (None, None)
    
def is_user_exist(username):
    df_user = pd.read_csv(user_csv_path)
    user = df_user[df_user['username'] == username]
    return len(user) > 0

def create_user(username):
    df_user = pd.read_csv(user_csv_path)
    
    user = {
        'id': uuid.uuid1().hex,
        'username': username
    }

    df_user = df_user.append(user, ignore_index = True)
    df_user.to_csv(user_csv_path, index = False)

def is_movie_exist(movie_id):
    df_user = pd.read_csv(movie_csv_path)
    user = df_user[df_user['id'] == movie_id]
    return len(user) > 0
    
def insert_rate(user_id, movie_id, rate_score):
    df_rating = pd.read_csv(rating_csv_path)

    rate = df_rating[(df_rating['movie_id'] == movie_id) & (df_rating['user_id'] == user_id)]

    if len(rate) > 0:
        df_rating.loc[(df_rating['movie_id'] == movie_id) & (df_rating['user_id'] == user_id, 'rate')] = rate
        df_rating.to_csv(rating_csv_path, index = False)
    else:
        rating = {
            'movie_id': movie_id,
            'user_id': user_id,
            'rate': rate_score
        }

        df_rating = df_rating.append(rating, ignore_index = True)
        df_rating.to_csv(rating_csv_path, index = False)

def get_movie_name(movie_id):
    movie = df_movie[df_movie['id'] == movie_id]
    if len(movie) > 0:
        return (movie.values[0][0], movie.values[0][1], movie.values[0][2])
    else:
        return (None, None)

def get_recommend(user_id):
    pass