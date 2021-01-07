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

pp = PrettyPrinter(indent=4)
@app.route('/', methods=['GET', 'POST'])
def gif_search():
    """Show a form to search for GIFs and show resulting GIFs from Tenor API."""
    if request.method == 'POST':
        

        return render_template('home.html', **context)
    else:
        response = requests.get(GENRE_URL)
        result = json.loads(response.content).get('genres')
        #pp.pprint(result)
        return render_template('home.html', context**)





if __name__ == '__main__':
    app.config['ENV'] = 'development'
    app.run(debug=True)
