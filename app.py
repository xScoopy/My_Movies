import json
import os
from pprint import PrettyPrinter

import requests
from dotenv import load_dotenv
from flask import Flask, redirect, render_template, request, url_for
from pymongo import MongoClient

# API setup

app = Flask(__name__)

# Get the API key from the '.env' file
load_dotenv()
API_KEY = os.getenv('API_KEY')

# API endpoints required in application
BASE_URL = 'https://api.themoviedb.org/3/'
GENRE_URL = f'{BASE_URL}genre/movie/list?api_key={API_KEY}&language=en-US'
MOVIE_URL = f'{BASE_URL}discover/movie'
DETAIL_URL = f'{BASE_URL}movie/'
SEARCH_URL = f'{BASE_URL}search/movie'
ACTOR_URL = f'{BASE_URL}people'
UPCOMING_URL = f'{BASE_URL}movie/upcoming'

#initialization of PrettyPrinter for troubleshooting
pp = PrettyPrinter(indent=4)

# Mongo Connection(Replace if running your own mongo cluster or local mongodb)
MONGODB_USERNAME = os.getenv('MONGODB_USERNAME')
MONGODB_PASSWORD = os.getenv('MONGODB_PASSWORD')
client = MongoClient(
    f"mongodb+srv://{MONGODB_USERNAME}:{MONGODB_PASSWORD}@webcluster.jdw9h.mongodb.net/mydb?retryWrites=true&w=majority")
db = client.test


@app.route('/', methods=['GET', 'POST'])
def home_page():
    """Shows a form to search for movies, then shows results beneath the form."""
    if request.method == 'POST':
        genre = request.form.get('pick_genre')
        title = request.form.get('pick_title')
        genre_response = requests.get(GENRE_URL)
        genre_result = json.loads(genre_response.content).get('genres')
        # if a user selects a genre and not a custom title into the form
        if not title:
            response = requests.get(MOVIE_URL,
                                    {
                                        'api_key': API_KEY,
                                        'with_genres': genre

                                    }
                                    )
            result = json.loads(response.content).get('results')
            context = {
                'movies': result,
                'results': genre_result
            }
            return render_template('home.html', **context, )
        #If a user enters a custom title and NOT a dropdown genre
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
    #If homepage is loaded without a form submission, shows upcoming films
    else:
        response = requests.get(GENRE_URL)
        result = json.loads(response.content).get('genres')
        upcoming_response = requests.get(UPCOMING_URL, 
        {
            'api_key':API_KEY,
            'language':'en-us',
            'page': 1,
            'region' : 'US'
        })
        upcoming_result = json.loads(upcoming_response.content).get('results')
        context = {
            'results': result,
            'upcoming' : upcoming_result
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
    #if POST request, add movie to the db
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
        #Check's if the movie being added already exists in the database
        check_movie = db.movies.find_one({'db_id': movie_id})
        #If it doesn't already exist, add it, otherwise return an error message and redirect to their previous search results.
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
    #If a GET request is made, just find all movies in the db and send them to the template for rendering
    else: 
        result = db.movies.find()
        context = {
            'movies': result
        }
        return render_template('my_collection.html', **context)

@app.route('/delete/<movie_id>', methods=['POST'])
def delete_movie(movie_id):
    '''Deletes a movie from the user's collection (will not remove it from the TMDB database)'''
    db.movies.delete_one({
        'db_id': movie_id
    })
    return redirect(url_for('my_collection'))


if __name__ == '__main__':
    app.config['ENV'] = 'development'
    app.run(debug=True)
