from sql_alchemy import DATABASE

# pylint: disable=no-member


class SiteModel(DATABASE.Model):
    __tablename__ = 'sites'

    site_id = DATABASE.Column(DATABASE.Integer, primary_key=True)
    url = DATABASE.Column(DATABASE.String(80))
    hotels = DATABASE.relationship('HotelModel')

    def __init__(self, url: str) -> None:
        self.url = url

    def json(self) -> dict:
        return {
            'site_id': self.site_id,
            'url': self.url,
            'hotels': [hotel.json() for hotel in self.hotels]
        }

    @classmethod
    def find_site(cls, url: str):

        site = cls.query.filter_by(url=url).first()

        if site:
            return site

        return None

    def save_site(self):
        DATABASE.session.add(self)
        DATABASE.session.commit()
        return self.site_id

    def delete_site(self):
        [hotel.delete_hotel() for hotel in self.hotels]
        DATABASE.session.delete(self)
        DATABASE.session.commit()
