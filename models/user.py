from sql_alchemy import DATABASE

# pylint: disable=no-member


class UserModel(DATABASE.Model):
    __tablename__ = 'users'

    user_id = DATABASE.Column(DATABASE.Integer, primary_key=True)
    email = DATABASE.Column(DATABASE.String(40))
    password = DATABASE.Column(DATABASE.String(40))

    def __init__(self, email: str, password: str) -> None:
        self.email = email
        self.password = password

    def json(self) -> dict:
        return {
            'user_id': self.user_id,
            'email': self.email
        }

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
