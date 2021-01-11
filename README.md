# MYMDB
Web-app designed to assist with transforming a stack of physical DvD's into a visual collection. 

## How to use - basic
Currently hosted on Heroku here:
Single MongoDB Atlas cluster in use, shared among users at present. 

## How to use - advanced
### Pre-requisites:
- API Key from themoviedb.org
- MongoDB Atlas DB User/password
- MongoDB connection string (found on your atlas cluster page)
- Python 3.8
- pip3 installer

1. Download files to project directory
2. Create .env file in project root. 
3. Enter Mongo credentials and API key in this format: 
`MONGODB_USERNAME=<your mongodb user>`
`MONGODB_PASSWORD=<your mongodb user password>`
`API_KEY=<your api key here>`
4. Replace connection string on line 30 of `app.py` with your MONGODB atlas connection string. 
5. install requirements in project directory.(virtual environment recommended):
`pip3 install -r requirements.txt`
6. Replace footer with Personalized information if desired. 

