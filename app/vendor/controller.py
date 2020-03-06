import requests
from flask import jsonify, request
from flask_restx import Resource, Namespace, reqparse
from flask_jwt_extended import (
    jwt_required, create_access_token,
    get_jwt_identity
)

from .model import Vendor
from .schema import VendorSchema

api = Namespace('Vendor')


@api.route('/')
class VendorResource(Resource):
    parser = reqparse.RequestParser()
    @jwt_required
    def get(self):
        identity = get_jwt_identity()
        print(identity)
        vendor = Vendor.find_by_uid(identity)
        print(vendor)
        if vendor:
            output = VendorSchema().dump(vendor).data
            print(output)
            return jsonify(output)
        return 'Vendor Not Found'

    def post(self):
        data = request.get_json()
        print(data)
        access_token = create_access_token(identity=data['uid'])
        vendor = Vendor.find_by_uid(data['uid'])
        print(vendor)
        if vendor is None:
            print('New Vendor')
            vendor = Vendor(name=data['displayName'], uid=data['uid'],
                            page_access_token=data['pageAccessToken'], page_id=data['uid'])
            vendor.save()
            return jsonify({'data': data, 'jwt_token': access_token})

        return jsonify({'data': data, 'jwt_token': access_token})

    @jwt_required
    def put(self):
        identity = get_jwt_identity()
        data = request.get_json()
        print(data)

        vendor = Vendor.find_by_uid(identity)
        if vendor:
            if 'closing_hours' in data or 'opening_hours' in data:
                vendor.set_working_hours(
                    data['opening_hours'], data['closing_hours'])
            else:
                vendor.update(data)
            vendor.save()
            return 'Vendor Updated'
        return 'Vendor Not Found'

    def delete(self):
        pass


@api.route('/all')
class VendorAll(Resource):
    def get(self):
        vendors = Vendor.query.all()
        vendor_schema = VendorSchema(many=True)
        output = vendor_schema.dump(vendors)
        return jsonify(output)


@api.route('/fb_page')
class VendorFbPage(Resource):
    def get(self):
        pass

    def post(self):
        data = request.get_json()
        print(data)
        vendor = Vendor.find_by_uid(data['uid'])
        if vendor is None:
            return 'Vendor Not Found'

        request_endpoint = 'https://graph.facebook.com/v6.0/{}/subscribed_apps?access_token={}&subscribed_fields=messages,messaging_postbacks'.format(
            data['page']['id'], data['page']['access_token'])
        response = requests.post(request_endpoint)
        print(response.json())
        vendor.page_access_token = data['page']['access_token']
        vendor.page_id = data['page']['id']
        vendor.save()
        return 'Page Connected'

    def delete(self):
        data = request.get_json()
        print(data)
        request_endpoint = 'https://graph.facebook.com/v6.0/{}/subscribed_apps?access_token={}&subscribed_fields=messages,messaging_postbacks'.format(
            data['page']['id'], data['page']['access_token'])
        response = requests.delete(request_endpoint)
        print(response.json())
        return 'Page Disconected'
