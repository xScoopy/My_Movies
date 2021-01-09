from flask import Flask, request, redirect, render_template, url_for
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from pymongo import MongoClient
from pprint import PrettyPrinter
from dotenv import load_dotenv
import json
import os
import requests

# API setup

app = Flask(__name__)

# Get the API key from the '.env' file
load_dotenv()
API_KEY = os.getenv('API_KEY')
GENRE_URL = f'https://api.themoviedb.org/3/genre/movie/list?api_key={API_KEY}&language=en-US'
MOVIE_URL = f'https://api.themoviedb.org/3/discover/movie'
DETAIL_URL = f'https://api.themoviedb.org/3/movie/'
SEARCH_URL = f'https://api.themoviedb.org/3/search/movie'
pp = PrettyPrinter(indent=4)
MONGODB_PASSWORD = os.getenv('MONGODB_PASSWORD')
# Mongo Connection

client = MongoClient(
    f"mongodb+srv://scoopy:{MONGODB_PASSWORD}@webcluster.jdw9h.mongodb.net/mydb?retryWrites=true&w=majority")
db = client.test
# print(client.server_info())


@app.route('/', methods=['GET', 'POST'])
def home_page():
    """Shows a form to search for movies, then shows results beneath the form."""
    if request.method == 'POST':
        genre = request.form.get('pick_genre')
        title = request.form.get('pick_title')
        genre_response = requests.get(GENRE_URL)
        genre_result = json.loads(genre_response.content).get('genres')
        if not title:
            response = requests.get(MOVIE_URL,
                                    {
                                        'api_key': API_KEY,
                                        'with_genres': genre

                                    }
                                    )
            result = json.loads(response.content).get('results')
            # pp.pprint(result)
            context = {
                'movies': result,
                'results': genre_result
            }
            return render_template('home.html', **context, )
        else:
            response = requests.get(SEARCH_URL,
                                    {
                                        'api_key': API_KEY,
                                        'query': title
                                    })
            result = json.loads(response.content).get('results')
            context = {
                'movies': result,
                'results': genre_result
            }
            return render_template('home.html', **context)
    else:
        response = requests.get(GENRE_URL)
        result = json.loads(response.content).get('genres')
        # pp.pprint(result)
        context = {
            'results': result
        }
        return render_template('home.html', **context)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/movie/<movie_id>')
def movie_details(movie_id):
    '''Display in-depth movie details'''
    response = requests.get(f'{DETAIL_URL}{movie_id}',
                            {
                                'api_key': API_KEY,

                            })
    result = json.loads(response.content)
    context = {
        'result': result
    }
    return render_template('movie.html', **context)


@app.route('/my_collection', methods=['GET', 'POST'])
def my_collection():
    '''Add a movie to the database on POST, or show all movies in db on GET'''
    if request.method == 'POST':
        movie_id = request.form.get('movie_id')
        new_movie = {
            'db_id': movie_id,
            'title': request.form.get('movie_title'),
            'genres': request.form.get('movie_genre'),
            'image': request.form.get('movie_poster'),
            'runtime': request.form.get('movie_run'),
            'description': request.form.get('movie_description')
        }
        check_movie = db.movies.find_one({'db_id': movie_id})
        if not check_movie:
            db.movies.insert_one(new_movie)
            result = db.movies.find()
            context = {
                'movies': result
            }
            return render_template('my_collection.html', **context)
        else:
            response = requests.get(f'{DETAIL_URL}{movie_id}',
                                    {
                                        'api_key': API_KEY,

                                    })
            result = json.loads(response.content)
            context =   {
                        'error_message': "This movie is already in your collection.",
                        'result' : result
                        }
            return render_template('movie.html', **context, movie_id=movie_id)
    else: 
        result = db.movies.find()
        context = {
            'movies': result
        }
        return render_template('my_collection.html', **context)

@app.route('/delete/<movie_id>', methods=['POST'])
def delete_movie(movie_id):
    db.movies.delete_one({
        'db_id': movie_id
    })
    return redirect(url_for('my_collection'))


if __name__ == '__main__':
    app.config['ENV'] = 'development'
    app.run(debug=True)
