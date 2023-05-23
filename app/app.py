from flask import Flask, request, make_response, jsonify
from apscheduler.schedulers.background import BackgroundScheduler
from utils import get_user_by_username, is_user_exist, create_user, is_movie_exist, insert_rate, get_movies
from MatrixFactorization import MatrixFactorizationRecommenderSystem
from ContentBased import ContentBased

app = Flask(__name__)

@app.after_request 
def after_request(response):
    header = response.headers
    header['Access-Control-Allow-Origin'] = '*'
    header['Access-Control-Allow-Headers'] = '*'
    header['Access-Control-Allow-Methods'] = '*'
    # Other headers can be added here if needed
    return response


matrix_factorization_rs = MatrixFactorizationRecommenderSystem()
content_based_model = ContentBased()
def fit_matrix():
    print('Begin fit matrix')
    matrix_factorization_rs.fit(100, 0.01, 0.2)
    print('End fit matrix')

scheduler = BackgroundScheduler(daemon=True)
scheduler.add_job(fit_matrix, 'interval', seconds = 3 * 60)
scheduler.start()

@app.route('/login', methods = ['POST'])
def login():
    response = make_response()

    data = request.get_json()
    username = data['username']

    user_id, username = get_user_by_username(username)

    if user_id is not None:
        response.set_cookie('user_id', str(user_id))
        response.set_cookie('username', str(username))

        return jsonify({
            'user_id': str(user_id),
            'username': str(username)
        }), 200
    else:
        return jsonify({
            'message': 'Username does not exist.',
        }), 404
    
@app.route('/register', methods = ['POST'])
def register():
    response = make_response()

    data = request.get_json()
    username = data['username']

    if is_user_exist(username):
        return jsonify({
            'message': 'Username already exist',
        }), 400
    else:
        create_user(username)
        return jsonify({
            'message': 'Register account successfully',
        }), 200

@app.route('/rate', methods = ['POST'])
def rate():
    data = request.get_json()
    user_id = data['user_id']

    if user_id:
        movie_id = data['movie_id']
        rate = data['rate']

        if is_movie_exist(movie_id):
            insert_rate(user_id, movie_id, rate)
            return jsonify({
                'message': 'Rated movie successfully',
            }), 200
        else:
            return jsonify({
                'message': 'Movie does not exist',
            }), 404
    else:
        return jsonify({
            'message': 'Please login',
        }), 401

@app.route('/matrix-factorization', methods = ['POST'])
def recommend():
    data = request.get_json()
    user_id = data['user_id']

    if user_id:
        return jsonify(matrix_factorization_rs.recommend_matrix_factorization_with_bias(user_id, 12)), 200
    else:
        return jsonify({
            'message': 'Please login',
        }), 401
    
@app.route('/content-based', methods = ['POST'])
def recommend_content_based():
    data = request.get_json()
    movie_id = data['movie_id']
    result = content_based_model.recommend(movie_id)
    return jsonify(result), 200

@app.route('/movies', methods = ['GET'])
def get_all_movies():
    result = get_movies()
    return jsonify(result), 200


if __name__ == '__main__':
    matrix_factorization_rs.fit(5, 0.01, 0.2)
    app.run()