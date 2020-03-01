import requests
from flask import Blueprint, render_template, request, redirect
from flask_jwt_extended import (
    jwt_required, create_access_token,
    get_jwt_identity
)
from models.data_models import Order, OrderSchema, Customer, CustomerSchema, Vendor, VendorSchema
import json
from datetime import datetime
import ast
# Set up a Blueprint
vendor_bp = Blueprint('vendor_bp', __name__,
                      template_folder='templates',
                      static_folder='static')


@vendor_bp.route('/vendor/orders', methods=['POST'])
@jwt_required
def vendor_orders():
    identity = get_jwt_identity()
    print(identity)
    vendor = Vendor.find_by_uid(identity)
    orders = Order.query.filter_by(page_id=vendor.page_id).all()
    orders_schema = OrderSchema(many=True)
    output = orders_schema.dump(orders)
    data = []
    # print(output)
    for order in output:
        info = {}
        info['customer'] = order['customer']
        info['time'] = order['time']
        info['number'] = order['number']
        info['price'] = order['total']
        info['status'] = order['status']
        items = ast.literal_eval(order['items'])
        order_text = ''
        for item in items:
            if item['combo'] == 15:
                combo = 'Combo'
            else:
                combo = ''
            temp = '- {} * {} ({}) {} Notes({}) \n'.format(item['quantity'],
                                                           item['name'], item['type'], combo, item['notes'])
            order_text += temp
        info['items'] = order_text
        data.append(info)
    # print(data)
    # print(output)
    return json.dumps(data)


@vendor_bp.route('/vendor/customers', methods=['GET'])
def vendor_customers():
    identity = get_jwt_identity()
    print(identity)
    vendor = Vendor.find_by_uid(identity)
    customers = Customer.query.filter_by(page_id=vendor.page_id).all()
    customers_schema = CustomerSchema(many=True).dump(customers)
    return json.dumps({'customers': customers_schema})


@vendor_bp.route('/vendor/login', methods=['POST'])
def vendor_login():
    data = request.get_json()
    print(data)
    vendor = Vendor.find_by_username(data['username'])
    access_token = create_access_token(identity=data['username'])
    print(vendor)
    print(vendor is not None and vendor.password == data['password'])
    if vendor is not None and vendor.password == data['password']:
        print(vendor)
        return json.dumps({'userData': data, 'accessToken': access_token}), 200

    return json.dumps('Wrong Username or Pasword'), 200


@vendor_bp.route('/vendor/register', methods=['POST'])
@jwt_required
def vendor_register():
    data = request.get_json()
    print(data)
    access_token = create_access_token(identity=data['uid'])
    vendor = Vendor.find_by_uid(data['uid'])
    print(vendor)
    if vendor is None:
        print('New Vendor')
        vendor = Vendor(name=data['displayName'], uid=data['uid'],
                        access_token=data['accessToken'], user_name=data['displayName'], page_id=data['uid'])
        vendor.save()
        return json.dumps({'data': data, 'jwt_token': access_token}), 201

    return json.dumps({'data': data, 'jwt_token': access_token}), 200


@vendor_bp.route('/vendor/edit', methods=['POST'])
def vendor_edit():
    data = request.get_json()
    print(data)
    time_format = '%H:%M'
    vendor = Vendor.find_by_page_id(data['page_id'])
    if vendor is not None:
        if 'address_info' in data:
            vendor.address_info = data['address_info']
        if 'menu_info' in data:
            vendor.menu_info = data['menu_info']
        if 'password' in data:
            vendor.password = data['password']
        if 'closing_hours' in data:
            vendor.closing_hours = datetime.strptime(
                data['closing_hours'], time_format).time()
        if 'opening_hours' in data:
            vendor.opening_hours = datetime.strptime(
                data['opening_hours'], time_format).time()
        if 'menu' in data:
            vendor.menu = data['menu']
        if 'access_token' in data:
            vendor.access_token = data['access_token']
        if 'prices' in data:
            vendor.prices = data['prices']
        if 'arabic' in data:
            vendor.arabic = data['arabic']
        vendor.save()
        return 'Success', 200
    else:
        return 'Vendor Not Found', 404


@vendor_bp.route('/vendor/connect_page', methods=['GET', 'POST'])
def connect_page():
    data = request.get_json()
    print(data)
    vendor = Vendor.find_by_uid(data['uid'])
    if vendor is None:
        return 'Vendor Not Found', 404

    request_endpoint = 'https://graph.facebook.com/v6.0/{}/subscribed_apps?access_token={}&subscribed_fields=messages,messaging_postbacks'.format(
        data['page']['id'], data['page']['access_token'])
    response = requests.post(request_endpoint)
    print(response.json())
    vendor.access_token = data['page']['access_token']
    vendor.page_id = data['page']['id']
    vendor.save()
    return 'Page Connected', 200


@vendor_bp.route('/vendor/disconnect_page', methods=['GET', 'POST'])
def disconnect_page():
    data = request.get_json()
    print(data)
    request_endpoint = 'https://graph.facebook.com/v6.0/{}/subscribed_apps?access_token={}&subscribed_fields=messages,messaging_postbacks'.format(
        data['page']['id'], data['page']['access_token'])
    response = requests.delete(request_endpoint)
    print(response.json())
    return 'Page Disconnected', 200

# For Comments
@vendor_bp.route('/vendors', methods=['GET'])
def vendors():
    vendors = Vendor.query.all()
    vendor_schema = VendorSchema(many=True)
    output = vendor_schema.dump(vendors)
    return json.dumps(output)
