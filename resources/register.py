from flask_restful import Resource, reqparse
from models.user import UserModel
import traceback


class UserRegister(Resource):
    def post(self):
        attributes = reqparse.RequestParser()
        attributes.add_argument('email', type=str, required=True,
                                help="The field 'email' cannot be left blank.")
        attributes.add_argument('password', type=str, required=True,
                                help="The field 'password' cannot be left blank.")
        attributes.add_argument('active', type=bool)

        data = attributes.parse_args()

        if UserModel.find_by_email(data['email']):
            return {'message': f"The email '{data['email']}' already exists."}, 400

        user = UserModel(**data)
        user.active = False  # Security

        try:
            user_id = user.save_user()
            user.send_confirmation_email()
            return {'message': f'User {user_id} created successfully!'}, 201
        except Exception as ex:
            user.delete_user()
            traceback.print_exc()
            return {'message': f'An internal server error has occured: {ex}.'}, 500
