from flask import Flask, jsonify
from flask_restful import Api, reqparse
from flask_jwt_extended import JWTManager, jwt_required
import sqlite3
from resources.hotel import Hotel, Hotels
from models.hotel import HotelModel
from resources.user import User
from resources.register import UserRegister
from resources.login import UserLogin
from resources.logout import UserLogout
from resources.site import Site
from helpers.filters import normalize_data, consult_with_city, consult_without_city
from blacklist import BLACKLIST
from sql_alchemy import DATABASE

# pylint: disable=no-member

APP = Flask(__name__)
APP.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///hotels.db'
APP.config['SQLALCHEMY_TACK_MODIFICATIONS'] = False
APP.config['JWT_SECRET_KEY'] = '3QeCxTBPT7KeYEMMqp'
APP.config['JWT_BLACKLIST_ENABLED'] = True
API = Api(APP)
JWT = JWTManager(APP)


@APP.before_first_request
def create_database():
    DATABASE.create_all()


@JWT.token_in_blacklist_loader
def verify_blacklist(token):
    return token['jti'] in BLACKLIST


@JWT.revoked_token_loader
def invalid_token():
    return jsonify({'message': 'You have been logged out.'}), 401


@APP.route('/complex_hotel_search', methods=['POST'])
@jwt_required
def complex_hotel_search():
    body = reqparse.RequestParser()

    body.add_argument('city', type=str)
    body.add_argument('min_stars', type=float)
    body.add_argument('max_stars', type=float)
    body.add_argument('min_dayly', type=float)
    body.add_argument('max_dayly', type=float)
    body.add_argument('limit', type=int)
    body.add_argument('offset', type=int)

    data = body.parse_args()

    valid_data = {key: data[key] for key in data if data[key] is not None}

    search_params = normalize_data(**valid_data)

    connection = sqlite3.connect('hotels.db')
    cursor = connection.cursor()

    result = []

    modify_data = tuple([search_params[key] for key in search_params])

    if search_params.get('city'):
        result = cursor.execute(consult_with_city, modify_data)
    else:
        result = cursor.execute(consult_without_city, modify_data)

    hotels = []
    for line in result:
        hotels.append({
            'hotel_id': line[0],
            'name': line[1],
            'stars': line[2],
            'dayly': line[3],
            'city': line[4]
        })

    return {'message': 'Result return successfully!', 'data': hotels}, 200


@APP.route('/complex_hotel_search_optimized', methods=['POST'])
@jwt_required
def complex_hotel_search_optimized():
    body = reqparse.RequestParser()

    body.add_argument('city', type=str)
    body.add_argument('min_stars', type=float)
    body.add_argument('max_stars', type=float)
    body.add_argument('min_dayly', type=float)
    body.add_argument('max_dayly', type=float)
    body.add_argument('limit', type=int)
    body.add_argument('offset', type=int)

    data = body.parse_args()

    valid_data = {key: data[key] for key in data if data[key] is not None}

    search_params = normalize_data(**valid_data)

    result = HotelModel.query.filter(HotelModel.city == search_params['city'], HotelModel.stars >= search_params['min_stars'], HotelModel.stars <= search_params['max_stars'],
                                     HotelModel.dayly >= search_params['min_dayly'], HotelModel.dayly <= search_params['max_dayly']).order_by('dayly').limit(search_params['limit']).offset(search_params['offset'])

    hotels = [hotel.json() for hotel in result]

    return {'message': 'Result return successfully!', 'data': hotels}, 200


API.add_resource(Hotels, '/hotels')
API.add_resource(Hotel, '/hotel/<int:hotel_id>')
API.add_resource(User, '/user/<int:user_id>')
API.add_resource(UserRegister, '/signup')
API.add_resource(UserLogin, '/signin')
API.add_resource(UserLogout, '/signout')
API.add_resource(Site, '/site')

if __name__ == '__main__':
    from sql_alchemy import DATABASE
    DATABASE.init_app(APP)
    APP.run(debug=True)
