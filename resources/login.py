from flask_restful import Resource, reqparse
from models.user import UserModel
from flask_jwt_extended import create_access_token
from werkzeug.security import safe_str_cmp


class UserLogin(Resource):
    @classmethod
    def post(cls):
        attributes = reqparse.RequestParser()
        attributes.add_argument(
            'email', type=str, required=True, help="The field 'email' cannot be left blank.")
        attributes.add_argument('password', type=str, required=True,
                                help="The field 'password' cannot be left blank.")

        data = attributes.parse_args()

        user = UserModel.find_by_email(data['email'])

        if user and safe_str_cmp(user.password, data['password']):
            token = create_access_token(identity=user.user_id)
            return {'message': 'Welcome!', 'access_token': token}, 200

        return {'message': 'The email or password is incorrect'}, 401
