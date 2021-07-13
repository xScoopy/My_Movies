# MYMDB
Web-app designed to assist with transforming a stack of physical DvD's into a visual collection. 

## How to use - basic
Currently hosted on CapRover/Docker VPS here: https://my-movies.dev.jleary.me

Single MongoDB Atlas cluster in use, shared among users at present. 

## How to use - advanced
### Pre-requisites:
- API Key from themoviedb.org
- MongoDB Atlas DB User/password
- MongoDB connection string (found on your atlas cluster page)
- Python 3.8
- pip3 installer

### Instructions:

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


### Demo
![alt text](mymdb_giphy.gif "Demo Giphy")

#### Background
My step-father was obsessed with movies, and would treat himself to a new DvD once a week on Tuesdays. Over time, his little collection turned into thousands of movies piled up in his basement. With a little bit of work up front, I'm hoping we can make him an easily searchable database of his very own movies. 

I'm a big believer in making the little things in life just a tad bit easier. Not every idea needs to change the world. Helping one person save a few minutes here and there leaves an impact. 
