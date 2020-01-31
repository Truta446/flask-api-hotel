from sql_alchemy import DATABASE


class HotelModel(DATABASE.Model):
    __tablename__ = 'hotels'

    hotel_id = DATABASE.Column(DATABASE.Integer, primary_key=True)
    name = DATABASE.Column(DATABASE.String(50))
    stars = DATABASE.Column(DATABASE.Float(precision=1))
    dayly = DATABASE.Column(DATABASE.Float(precision=2))
    city = DATABASE.Column(DATABASE.String(80))

    def __init__(self, name: str, stars: float, dayly: float, city: str) -> None:
        self.name = name
        self.stars = stars
        self.dayly = dayly
        self.city = city

    def json(self) -> dict:
        return {
            'hotel_id': self.hotel_id,
            'name': self.name,
            'stars': self.stars,
            'dayly': self.dayly,
            'city': self.city
        }

    @classmethod
    def find_hotel(cls, hotel_id: int):
        hotel = cls.query.filter_by(hotel_id=hotel_id).first()

        if hotel:
            return hotel

        return None

    def save_hotel(self):
        DATABASE.session.add(self)
        DATABASE.session.commit()
        return self.hotel_id

    def update_hotel(self, name: str, stars: float, dayly: float, city: str) -> None:
        self.name = name
        self.stars = stars
        self.dayly = dayly
        self.city = city

    def delete_hotel(self):
        DATABASE.session.delete(self)
        DATABASE.session.commit()

    @classmethod
    def get_all(cls) -> list:
        return [hotel.json() for hotel in cls.query.all()]
