from flask_restful import Resource, reqparse
from models.user import UserModel
from flask import make_response, render_template


class UserConfirm(Resource):
    @classmethod
    def get(cls, user_id: int):
        user = UserModel.find_user(user_id)

        if not user:
            return {'message': f'User id {user_id} not found.'}, 404

        try:
            user.active = True
            user.save_user()
            headers = {'Content-type': 'text/html'}
            return make_response(render_template('user_confirm.html', email=user.email), 200, headers)
        except Exception as ex:
            return {'message': f'An error ocurred when trying to create hotel: {ex}'}, 500
