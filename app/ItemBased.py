import pandas as pd
import numpy as np
from sortedcontainers import SortedList
from utils import get_movie_name
import math

from ContentBased import ContentBased
class ItemBased:
    def __init__(self):
        self.contentBasedModel = ContentBased() 
        self.df = pd.read_csv('../dataset/rating_final.csv')
        self.user_to_movie = {}
        self.movie_to_user = {}
        self.movie_user_rating = {}
        self.recommend_history = {}

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

        self.k_neighbor = 20
        self.limit_neighbor = 5
        self.neighbors = {}
        self.averages = {}
        self.deviations = {}
        self.similarities = {}

        for movie_id_i in self.movie_to_user.keys():
            self.similarities[movie_id_i] = []

            # get all user who rated for movie_id_i
            user_rated_movie_i = self.movie_to_user[movie_id_i]

            # get all rating of users gave for movie_id_i
            rating_user_for_movie_i = [
                self.movie_user_rating[(movie_id_i, user_id)] for user_id in user_rated_movie_i]

            # calculate avarage rating of all user gave for movie_id_i
            avg_rating_movie_i = np.mean(rating_user_for_movie_i)

            self.averages[movie_id_i] = avg_rating_movie_i
            
            sorted_list = SortedList()
            for movie_id_j in self.movie_to_user.keys():
                if movie_id_j == movie_id_i:
                    continue

                # get all user who rated for movie_id_j
                user_rated_movie_j = self.movie_to_user[movie_id_j]

                common_users = list(set(user_rated_movie_i).intersection(set(user_rated_movie_j)))

                if len(common_users) < self.limit_neighbor:
                    continue

                # get all rating of users gave for movie_id_j
                rating_user_for_movie_j = [self.movie_user_rating[(movie_id_j, user_id)] for user_id in user_rated_movie_j]

                # calculate avarage rating of all user gave for movie_id_j
                avg_rating_movie_j = np.mean(rating_user_for_movie_j)
                
                deviation = 0
                sigmoid_i = 0
                sigmoid_j = 0

                for user_id in common_users:
                    dev_i = (self.movie_user_rating[(movie_id_i, user_id)] - avg_rating_movie_i)
                    dev_j = (self.movie_user_rating[(movie_id_j, user_id)] - avg_rating_movie_j)
                    deviation += dev_i * dev_j
                    sigmoid_i += dev_i * dev_i
                    sigmoid_j += dev_j * dev_j

                s_ij = deviation / (math.sqrt(sigmoid_i) * math.sqrt(sigmoid_j))
                sorted_list.add((s_ij, movie_id_j))
                self.similarities[movie_id_i].append((s_ij, movie_id_j))

            self.similarities[movie_id_i] = sorted(self.similarities[movie_id_i], key = lambda x: x[1])
    
    def fit(self):
        self.df = pd.read_csv('../dataset/rating_final.csv')
        self.user_to_movie = {}
        self.movie_to_user = {}
        self.movie_user_rating = {}

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

        self.k_neighbor = 20
        self.limit_neighbor = 5
        self.neighbors = {}
        self.averages = {}
        self.deviations = {}
        self.similarities = {}

        for movie_id_i in self.movie_to_user.keys():
            self.similarities[movie_id_i] = []

            # get all user who rated for movie_id_i
            user_rated_movie_i = self.movie_to_user[movie_id_i]

            # get all rating of users gave for movie_id_i
            rating_user_for_movie_i = [
                self.movie_user_rating[(movie_id_i, user_id)] for user_id in user_rated_movie_i]

            # calculate avarage rating of all user gave for movie_id_i
            avg_rating_movie_i = np.mean(rating_user_for_movie_i)

            self.averages[movie_id_i] = avg_rating_movie_i
            
            sorted_list = SortedList()
            for movie_id_j in self.movie_to_user.keys():
                if movie_id_j == movie_id_i:
                    continue

                # get all user who rated for movie_id_j
                user_rated_movie_j = self.movie_to_user[movie_id_j]

                common_users = list(set(user_rated_movie_i).intersection(set(user_rated_movie_j)))

                if len(common_users) < self.limit_neighbor:
                    continue

                # get all rating of users gave for movie_id_j
                rating_user_for_movie_j = [self.movie_user_rating[(movie_id_j, user_id)] for user_id in user_rated_movie_j]

                # calculate avarage rating of all user gave for movie_id_j
                avg_rating_movie_j = np.mean(rating_user_for_movie_j)
                
                deviation = 0
                sigmoid_i = 0
                sigmoid_j = 0

                for user_id in common_users:
                    dev_i = (self.movie_user_rating[(movie_id_i, user_id)] - avg_rating_movie_i)
                    dev_j = (self.movie_user_rating[(movie_id_j, user_id)] - avg_rating_movie_j)
                    deviation += dev_i * dev_j
                    sigmoid_i += dev_i * dev_i
                    sigmoid_j += dev_j * dev_j

                s_ij = deviation / (math.sqrt(sigmoid_i) * math.sqrt(sigmoid_j))
                sorted_list.add((s_ij, movie_id_j))
                self.similarities[movie_id_i].append((s_ij, movie_id_j))

            self.similarities[movie_id_i] = sorted(self.similarities[movie_id_i], key = lambda x: x[1])

    def predict(self, movie_id_i, user_id):
        if movie_id_i not in self.movie_to_user or user_id not in self.user_to_movie:
            return None

        # calculate average rating of all users who rated movie_id_i
        avg_rating_movie_i = self.averages[movie_id_i]

        # calculate the predicted rating for movie_id_i by user_id
        predicted_rating = avg_rating_movie_i

        similarity_sum = 0
        weighted_rating_sum = 0
        limit_neighbors = 15
        count = 0

        for similarity, neighbor_movie_id in self.similarities[movie_id_i]:
            if count > limit_neighbors:
                break
            
            if (neighbor_movie_id, user_id) in self.movie_user_rating:
                weighted_rating_sum += similarity * (self.movie_user_rating[(neighbor_movie_id, user_id)] - self.averages[neighbor_movie_id])
                similarity_sum += abs(similarity)
                count += 1

        if (similarity_sum == 0):
            return predicted_rating
        return predicted_rating + (weighted_rating_sum / similarity_sum)
    
    def recommend(self, user_id, n = 24):
        recommend_list = SortedList()
        
        for movie_id in self.movie_to_user.keys():
            if (movie_id, user_id) not in self.movie_user_rating:
                rating = self.predict(movie_id, user_id)
                sim = []
                for movie_id_user_rated in self.user_to_movie[user_id]:
                    sim.append(self.contentBasedModel.get_movie_similarities(movie_id_user_rated, movie_id))

                adjust = 0
                if (user_id, movie_id) in self.recommend_history:
                    adjust = self.recommend_history[(user_id, movie_id)] * 0.2

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