from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

import geocoder
import urllib.request
from urllib.parse import urljoin
import requests
import json

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = 'users'
    uid = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(100))
    lastname = db.Column(db.String(100))
    email = db.Column(db.String(120), unique=True)
    pwdhash = db.Column(db.String(54))

    def __init__(self, firstname, lastname, email, password):
        self.firstname = firstname.title()
        self.lastname = lastname.title()
        self.email = email.lower()
        self.set_password(password)

    def set_password(self, password):
        self.pwdhash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.pwdhash, password)


# p = Place()
# places = p.query('1600 Amphitheater Parkway Mountain View CA')
class Place(object):
    def meters_to_walking_time(self, meters):
        # 80 meters is one minute walking time
        return int(meters / 80)

    def wiki_path(self, slug):
        return urljoin("http://en.wikipedia.org/wiki/", slug.replace(' ', '_'))

    def address_to_latlng(self, address):
        g = geocoder.google(address)
        return g.lat, g.lng

    def query(self, address):
        lat, lng = self.address_to_latlng(address)

        lat = 37.422
        lng = -122.084

        S = requests.Session()

        URL = "https://en.wikipedia.org/w/api.php"

        print(lat, lng)

        PARAMS = {
            "format": "json",
            "list": "geosearch",
            "gscoord": f'{lat}|{lng}',
            "gslimit": "20",
            "gsradius": "5000",
            "action": "query"
        }

        R = S.get(url=URL, params=PARAMS)
        DATA = R.json()

        PLACES = DATA['query']['geosearch']

        print(PLACES)

        places = []

        for place in PLACES:
            name = place['title']
            meters = place['dist']
            lat = place['lat']
            lng = place['lon']

        wiki_url = self.wiki_path(name)
        walking_time = self.meters_to_walking_time(meters)

        d = {
            'name': name,
            'url': wiki_url,
            'time': walking_time,
            'lat': lat,
            'lng': lng
        }

        places.append(d)

        return places
