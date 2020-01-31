from flask import Flask
from flask_restful import Api
from resources.hotel import Hotel, Hotels

APP = Flask(__name__)
APP.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///hotels.db'
APP.config['SQLALCHEMY_TACK_MODIFICATIONS'] = False
API = Api(APP)


@APP.before_first_request
def create_database():
    DATABASE.create_all()


API.add_resource(Hotels, '/hotels')
API.add_resource(Hotel, '/hotel/<int:hotel_id>')

if __name__ == '__main__':
    from sql_alchemy import DATABASE
    DATABASE.init_app(APP)
    APP.run(debug=True)
