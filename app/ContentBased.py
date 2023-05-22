import numpy as np
import pandas as pd
from sortedcontainers import SortedList
class ContentBased:
    def __init__(self):
        df = pd.read_csv('../dataset/movie_final.csv')

        for i in range(0, len(df)):
            time = df['duration'][i]
            try:
                df['duration'][i] = int(time[:time.index('h')]) * 60
            except:
                df['duration'][i] = int(time[:time.index('m')])

            if len(time.split(' ')) > 1:
                df['duration'][i] += int(time.split(' ')[1][:time.split(' ')[1].index('m')])

        self.movies = {}
        for row in df.values:
            id, name, poster, directors, writers, genres, actors, releaseYear, limit, duration, language, origin = row
            self.movies[id] = {
                'name': name,
                'poster': poster,
                'directors': directors,
                'genres': genres,
                'actors': actors,
                'releaseYear': releaseYear,
                'limit': limit,
                'duration': duration,
                'writers': writers,
                'language': language,
                'origin': origin
            }

    def get_sim_director(self, movie_id_i, movie_id_j):
        director_i = set(self.movies[movie_id_i]['directors'])
        director_j = set(self.movies[movie_id_j]['directors'])

        return 0.125 * (len(director_i.intersection(director_j)) / len(director_i.union(director_j)))

    def get_sim_writer(self, movie_id_i, movie_id_j):
        writer_i = set(self.movies[movie_id_i]['writers'])
        writer_j = set(self.movies[movie_id_j]['writers'])

        return 0.125 * (len(writer_i.intersection(writer_j)) / len(writer_i.union(writer_j)))

    def get_sim_actor(self, movie_id_i, movie_id_j):
        actor_i = set(self.movies[movie_id_i]['actors'])
        actor_j = set(self.movies[movie_id_j]['actors'])

        return 0.125 * (len(actor_i.intersection(actor_j)) / len(actor_i.union(actor_j)))

    def get_sim_releaseYear(self, movie_id_i, movie_id_j):
        releaseYear_i = int(self.movies[movie_id_i]['releaseYear'])
        releaseYear_j = int(self.movies[movie_id_j]['releaseYear'])

        diff = abs(releaseYear_i - releaseYear_j)
        if diff < 3:
            return 0.05
        elif diff < 5:
            return 0.05 * 0.8
        elif diff < 10:
            return 0.05 * 0.5
        elif diff < 20:
            return 0.05 * 0.3
        return 0

    def get_sim_genres(self, movie_id_i, movie_id_j):
        genres_i = set(self.movies[movie_id_i]['genres'])
        genres_j = set(self.movies[movie_id_j]['genres'])

        return 0.35 * (len(genres_i.intersection(genres_j)) / len(genres_i.union(genres_j)))

    def get_sim_limit(self, movie_id_i, movie_id_j):
        limit_i = self.movies[movie_id_i]['limit']
        limit_j = self.movies[movie_id_j]['limit']
        if limit_i == limit_j:
            return 0.025
        return 0

    def get_sim_duration(self, movie_id_i, movie_id_j):
        duration_i = float(self.movies[movie_id_i]['duration'])
        duration_j = float(self.movies[movie_id_j]['duration'])

        diff = abs(duration_i - duration_j)
        if diff < 15:
            return 0.125
        elif diff < 30:
            return 0.125 * 0.8
        elif diff < 60:
            return 0.125 * 0.6
        elif diff < 90:
            return 0.125 * 0.3
        return 0

    def get_sim_language(self, movie_id_i, movie_id_j):
        language_i = self.movies[movie_id_i]['language']
        language_j = self.movies[movie_id_j]['language']
        if language_i == language_j:
            return 0.05
        return 0

    def get_sim_origin(self, movie_id_i, movie_id_j):
        origin_i = self.movies[movie_id_i]['origin']
        origin_j = self.movies[movie_id_j]['origin']
        if origin_i == origin_j:
            return 0.025
        return 0

    def get_movie_similarities(self, movie_id_i, movie_id_j):
        sim_director = self.get_sim_director(movie_id_i, movie_id_i)
        sim_writer = self.get_sim_writer(movie_id_i, movie_id_j)
        sim_genre = self.get_sim_genres(movie_id_i, movie_id_j)
        sim_actor = self.get_sim_actor(movie_id_i, movie_id_j)
        sim_releaseYear = self.get_sim_releaseYear(movie_id_i, movie_id_j)
        sim_duration = self.get_sim_duration(movie_id_i, movie_id_j)
        sim_limit = self.get_sim_limit(movie_id_i, movie_id_j)
        sim_language = self.get_sim_language(movie_id_i, movie_id_j)
        sim_origin = self.get_sim_origin(movie_id_i, movie_id_j)

        return sim_director + sim_genre + sim_actor + sim_releaseYear + sim_duration + sim_limit + sim_writer + sim_language + sim_origin

    def recommend(self, movie_id):
        k = 24
        list = SortedList()
        for id in self.movies.keys():
            if (id == movie_id):
                continue
            sim = self.get_movie_similarities(movie_id, id)
            list.add((sim, id))
            if len(list) > k:
                del list[0]

        result = []
        for score, id in list:
            result.append({
                'id': id,
                'name': self.movies[id]['name'],
                'poster': self.movies[id]['poster'],
                'score': round(score, 2)
            })

        return result


