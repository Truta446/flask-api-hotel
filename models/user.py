from sql_alchemy import DATABASE
from flask import request, url_for
from requests import post

MAILGUN_DOMAIN = DOMAIN
MAILGUN_API_KEY = API_KEY
FROM_TITLE = 'NO-REPLY'
FROM_EMAIL = 'no-reply@restapi.com'

# pylint: disable=no-member


class UserModel(DATABASE.Model):
    __tablename__ = 'users'

    user_id = DATABASE.Column(DATABASE.Integer, primary_key=True)
    email = DATABASE.Column(DATABASE.String(40), nullable=False, unique=True)
    password = DATABASE.Column(DATABASE.String(40), nullable=False)
    active = DATABASE.Column(DATABASE.Boolean, default=False)

    def __init__(self, email: str, password: str, active: bool) -> None:
        self.email = email
        self.password = password
        self.active = active

    def json(self) -> dict:
        return {
            'user_id': self.user_id,
            'email': self.email,
            'active': self.active
        }

    def send_confirmation_email(self):
        link = request.url_root[:-1] + \
            url_for('userconfirm', user_id=self.user_id)
        return post(f'https://api.mailgun.net/v3/{MAILGUN_DOMAIN}/messages',
                    auth=('api', MAILGUN_API_KEY),
                    data={
                        'from': f'{FROM_TITLE} <{FROM_EMAIL}>',
                        'to': self.email,
                        'subject': 'Confirmação de cadastro',
                        'text': f'Confirme seu cadastro clicando no link a seguir: {link}',
                        'html': f'<html>\
                            <p>Confirme seu cadastro clicando no link a seguir: <a href="{link}">CONFIRMAR E-MAIL</a></p>\
                        </html>'
                    })

    @classmethod
    def find_user(cls, user_id: int):
        return cls.query.filter_by(user_id=user_id).first_or_404(description=f'User not found: {user_id}.')

    @classmethod
    def find_by_email(cls, email: str):
        email_find = cls.query.filter_by(email=email).first()

        if email_find:
            return email_find

        return None

    def save_user(self) -> int:
        DATABASE.session.add(self)
        DATABASE.session.commit()
        return self.user_id

    def delete_user(self):
        DATABASE.session.delete(self)
        DATABASE.session.commit()
