from flask_restful import Resource, reqparse
from models.site import SiteModel
from flask_jwt_extended import jwt_required


class Site(Resource):
    def get(self) -> dict:
        return {'sites': [site.json() for site in SiteModel.query.all()]}

    @jwt_required
    def post(self) -> dict:
        args = reqparse.RequestParser()

        args.add_argument('url', type=str, required=True,
                          help="The field 'url' cannot be left blank.")

        body = args.parse_args()

        url = body['url']

        if SiteModel.find_site(url):
            return {'message': f'The site "{url}" already exists.'}, 400

        try:
            site = SiteModel(url)
            site_id = site.save_site()
            return {'message': f'Site create successfully: id = {site_id}.', 'data': site.json()}, 200
        except Exception as ex:
            return {'message': f'An internal error occurs when trying to create a new site: {ex}.'}, 500

    @jwt_required
    def delete(self, site_id: int) -> dict:
        site = SiteModel.find_site(site_id)

        if site:
            try:
                site.delete_user()
                return {'message': f'User {site_id} has been deleted with success!', 'data': site.json()}, 200
            except Exception as ex:
                return {'message': f'An error ocurred when trying to delete user: {ex}'}, 500

        return {'message': 'User not found.', 'data': {}}, 404
