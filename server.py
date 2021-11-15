from flask import Flask, request, send_from_directory, Response
from flask_cors import CORS
import postgres
import main as resto
import logging
from os import getenv
import sys

# set the project root directory as the static folder, you can set others.
app = Flask(__name__, static_url_path='')
CORS(app, resources=r'/*')
logging.basicConfig(level=logging.INFO)

@app.route('/<file>')
def get_file(file):
    return send_from_directory('./', file)

@app.route('/')
def get_index():
    return send_from_directory('./', "index.html" )    

@app.route('/missingflurry.js')
def get_missing_flurries():
    cur = postgres.init()
    missingflurry = postgres.get_restaurants(cur)
    return Response(missingflurry, mimetype='application/javascript')
    
@app.route('/refresh')
def refresh():
    restaurants = resto.load_restaurants()
    limit = int(getenv("LIMIT") ) if getenv("LIMIT") else None
    restaurants_menu = resto.get_unavailable_menu(restaurants[:limit])
    cur = postgres.init()
    status = postgres.save_restaurants(cur,restaurants_menu)
    return status

@app.route('/health')
def health():
    cur = postgres.init()
    health = postgres.healthcheck(cur)
    if health == 1 :
        return "ok", 200
    else :
        return "not ok", 500

if __name__ == "__main__":
    app.run()
