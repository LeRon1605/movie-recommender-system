import pandas as pd
import numpy as np
import math
from ContentBased import ContentBased
from utils import get_movie_name

from sortedcontainers import SortedList
class MatrixFactorizationRecommenderSystem:
    def __init__(self):
        self.df = pd.read_csv('../dataset/rating_final.csv')
        self.contentBasedModel = ContentBased()  
        self.user_to_movie = {}
        self.movie_to_user = {}
        self.movie_user_rating = {}
        self.bias_movie = {}
        self.bias_user = {}
        self.recommend_history = {}

        df_user = pd.read_csv('../dataset/user_final.csv')

        for row in df_user.values:
            id, _ = row
            self.user_to_movie[id] = []
            self.bias_user[id] = 0

        for row in self.df.values:
            movie_id, user_id, rate = row
            if movie_id not in self.user_to_movie:
                self.user_to_movie[user_id] = [movie_id]
            else:
                self.user_to_movie[user_id].append(movie_id)
            
            if movie_id not in self.movie_to_user:
                self.movie_to_user[movie_id] = [user_id]
            else:
                self.movie_to_user[movie_id].append(user_id)

            self.movie_user_rating[(movie_id, user_id)] = rate

        self.average = np.mean(list(self.movie_user_rating.values()))

        for user_id in self.user_to_movie:
            rates = []
            for movie_id in self.user_to_movie[user_id]:
                rates.append(self.movie_user_rating[(movie_id, user_id)] - self.average)
            self.bias_user[user_id] = np.mean(rates)

        for movie_id in self.movie_to_user:
            rates = []
            for user_id in self.movie_to_user[movie_id]:
                rates.append(self.movie_user_rating[(movie_id, user_id)] - self.average)
            self.bias_movie[movie_id] = np.mean(rates)

        self.k = 30
        self.W = dict.fromkeys(self.user_to_movie.keys())
        self.U = dict.fromkeys(self.movie_to_user.keys())

        self.saved_average = np.copy(self.average)
        self.saved_bias_movie = self.bias_movie.copy()
        self.saved_bias_user = self.bias_user.copy()
        self.saved_w = self.W.copy()
        self.saved_u = self.U.copy()
    
    def dump(self):
        self.df = pd.read_csv('../dataset/rating_final.csv')
        self.user_to_movie = {}
        self.movie_to_user = {}
        self.movie_user_rating = {}
        self.bias_movie = {}
        self.bias_user = {}

        df_user = pd.read_csv('../dataset/user_final.csv')

        for row in df_user.values:
            id, _ = row
            self.user_to_movie[id] = []
            self.bias_user[id] = 0

        for row in self.df.values:
            movie_id, user_id, rate = row
            if movie_id not in self.user_to_movie:
                self.user_to_movie[user_id] = [movie_id]
            else:
                self.user_to_movie[user_id].append(movie_id)
            
            if movie_id not in self.movie_to_user:
                self.movie_to_user[movie_id] = [user_id]
            else:
                self.movie_to_user[movie_id].append(user_id)

            self.movie_user_rating[(movie_id, user_id)] = rate

        average = np.mean(list(self.movie_user_rating.values()))

        for user_id in self.user_to_movie:
            rates = []
            for movie_id in self.user_to_movie[user_id]:
                rates.append(self.movie_user_rating[(movie_id, user_id)] - average)
            self.bias_user[user_id] = np.mean(rates)

        for movie_id in self.movie_to_user:
            rates = []
            for user_id in self.movie_to_user[movie_id]:
                rates.append(self.movie_user_rating[(movie_id, user_id)] - average)
            self.bias_movie[movie_id] = np.mean(rates)

        for user_id in self.W.keys():
            self.W[user_id] = np.random.randn(self.k)
        for movie_id in self.U.keys():
            self.U[movie_id] = np.random.randn(self.k)

        self.saved_average = np.copy(self.average)
        self.saved_bias_movie = self.bias_movie.copy()
        self.saved_bias_user = self.bias_user.copy()
        self.saved_w = self.W.copy()
        self.saved_u = self.U.copy()

    def fit(self, epoch, learning_rate, weight):
        self.dump()

        for i in range(0, epoch):
            loss = 0    
            
            for movie_id, user_id in self.movie_user_rating:
                rate = self.movie_user_rating[(movie_id, user_id)]

                predict_rating = self.average + self.bias_movie[movie_id] + self.bias_user[user_id] + np.dot(self.W[user_id], self.U[movie_id])
                
                error = rate - predict_rating

                self.average = self.average + learning_rate * error

                self.bias_movie[movie_id] += learning_rate * (error - weight * self.bias_movie[movie_id])
                self.bias_user[user_id] += learning_rate * (error - weight * self.bias_user[user_id])
                
                saved_w = np.copy(self.W[user_id])
                saved_u = np.copy(self.U[movie_id])

                self.W[user_id] += learning_rate * (2 * error * saved_u - weight * saved_w)
                self.U[movie_id] += learning_rate * (2 * error * saved_w - weight * saved_u)

                loss += error ** 2


            loss = loss / len(self.movie_user_rating)
            rmse = math.sqrt(loss)

            print(f'Epoch: {i + 1}/{epoch}')
            print('Loss: ' , loss, 'RMSE: ', rmse)

        self.saved_average = self.average
        self.saved_bias_movie = self.bias_movie
        self.saved_bias_user = self.bias_user
        self.saved_w = self.W
        self.saved_u = self.U
        
        self.recommend_history = {}

    def get_rating_with_bias(self, user_id, movie_id):
        return np.dot(self.saved_w[user_id], self.saved_u[movie_id]) + self.saved_average + self.saved_bias_movie[movie_id] + self.saved_bias_user[user_id]
    
    def recommend_matrix_factorization_with_bias(self, user_id, n = 10):
        recommend_list = SortedList()
        
        for movie_id in self.movie_to_user.keys():
            if (movie_id, user_id) not in self.movie_user_rating:
                rating = self.get_rating_with_bias(user_id, movie_id)
                sim = []
                for movie_id_user_rated in self.user_to_movie[user_id]:
                    sim.append(self.contentBasedModel.get_movie_similarities(movie_id_user_rated, movie_id))

                adjust = 0
                if (user_id, movie_id) in self.recommend_history:
                    adjust = self.recommend_history[(user_id, movie_id)] * 0.3

                recommend_list.add((np.mean(sim) * rating - adjust, get_movie_name(movie_id)))
                if len(recommend_list) > n:
                    del recommend_list[0]

        result = []
        for score, (movie_id, movie_name, movie_poster) in list(recommend_list):
            if (user_id, movie_id) in self.recommend_history:
                self.recommend_history[(user_id, movie_id)] += 1
            else:
                self.recommend_history[(user_id, movie_id)] = 0
            result.append({
                'id': movie_id,
                'name': movie_name,
                'score': round(score, 2),
                'poster': movie_poster
            })
        
        return result