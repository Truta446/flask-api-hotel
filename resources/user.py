from flask_restful import Resource
from models.user import UserModel
from flask_jwt_extended import jwt_required


class User(Resource):
    def get(self, user_id: int) -> dict:
        user = UserModel.find_user(user_id)

        return {'message': f'User {user_id} found.', 'data': user.json()}, 200

    @jwt_required
    def delete(self, user_id: int) -> dict:
        user = UserModel.find_user(user_id)

        if user:
            try:
                user.delete_user()
                return {'message': f'User {user_id} has been deleted with success!', 'data': user.json()}, 200
            except Exception as ex:
                return {'message': f'An error ocurred when trying to delete user: {ex}'}, 500

        return {'message': 'User not found.', 'data': {}}, 404
