from flask_restful import Resource, reqparse
from models.hotel import HotelModel
from models.site import SiteModel
from flask_jwt_extended import jwt_required


def getInformations() -> dict:
    args = reqparse.RequestParser()

    args.add_argument('name', type=str, required=True,
                      help="The field 'nome' cannot be left blank.")
    args.add_argument('stars', type=float)
    args.add_argument('dayly', type=float)
    args.add_argument('city', type=str)
    args.add_argument('site_id', type=int, required=True,
                      help='Every hotel needs to be linked with a site.')

    return args.parse_args()


class Hotels(Resource):
    def get(self) -> dict:
        return {'data': HotelModel.get_all()}

    @jwt_required
    def post(self) -> dict:
        data = getInformations()

        if not SiteModel.find_by_id(data.get('site_id')):
            return {'message': 'The hotel must be associated to a valid site id.'}, 400

        hotel = HotelModel(**data)

        try:
            hotel_id = hotel.save_hotel()
            return {'message': f'Hotel {hotel_id} create with success!', 'data': hotel.json()}, 201
        except Exception as ex:
            return {'message': f'An error ocurred when trying to create hotel: {ex}'}, 500


class Hotel(Resource):
    def get(self, hotel_id: int) -> dict:
        hotel = HotelModel.find_hotel(hotel_id)

        if hotel:
            return {'message': f'Hotel {hotel_id} found.', 'data': hotel.json()}, 200

        return {'message': 'Hotel not found.', 'data': {}}, 404

    @jwt_required
    def put(self, hotel_id: int) -> dict:
        data = getInformations()

        if not SiteModel.find_by_id(data.get('site_id')):
            return {'message': 'The hotel must be associated to a valid site id.'}, 400

        wanted_hotel = HotelModel.find_hotel(hotel_id)

        if wanted_hotel:
            try:
                wanted_hotel.update_hotel(**data)
                wanted_hotel.save_hotel()
                return {'message': f'Hotel {hotel_id} updated with success', 'data': wanted_hotel.json()}, 200
            except Exception as ex:
                return {'message': f'An error ocurred when trying to update hotel: {ex}'}, 500

        try:
            hotel = HotelModel(**data)
            hotel.save_hotel()
            return {'message': f'Hotel {hotel_id} created with success', 'data': hotel.json()}, 201
        except Exception as ex:
            return {'message': f'An error ocurred when trying to create hotel: {ex}'}, 500

    @jwt_required
    def delete(self, hotel_id: int) -> dict:
        hotel = HotelModel.find_hotel(hotel_id)

        if hotel:
            try:
                hotel.delete_hotel()
                return {'message': f'Hotel {hotel_id} has been deleted with success!', 'data': hotel.json()}, 200
            except Exception as ex:
                return {'message': f'An error ocurred when trying to delete hotel: {ex}'}, 500

        return {'message': 'Hotel not found.', 'data': {}}, 404
