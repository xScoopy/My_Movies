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
SEARCH_URL = f'https://api.themoviedb.org/3/search/movie'
pp = PrettyPrinter(indent=4)


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
                'movies':result, 
                'results':genre_result
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


if __name__ == '__main__':
    app.config['ENV'] = 'development'
    app.run(debug=True)
