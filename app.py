from flask import Flask, request, redirect, render_template, url_for
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from pymongo import MongoClient
from dotenv import load_dotenv
import os

#API setup

app = Flask(__name__)

# Get the API key from the '.env' file
load_dotenv()
API_KEY = os.getenv('API_KEY')