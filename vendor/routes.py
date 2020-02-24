from flask import Blueprint, render_template, request
from flask import current_app as app
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


@vendor_bp.route('/vendor/orders', methods=['GET'])
@jwt_required
def vendor_orders():
    identity = get_jwt_identity()
    print(identity)
    vendor = Vendor.find_by_username(identity)
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
@jwt_required
def vendor_customers():
    identity = get_jwt_identity()
    print(identity)
    vendor = Vendor.find_by_username(identity)
    subs = Customer.query.filter_by(page_id=vendor.page_id).count()
    return json.dumps({'customers': subs})


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
def vendor_register():
    data = request.get_json()
    print(data)
    vendor = Vendor.find_by_username(data['username'])
    if vendor is None:
        print('new Vendor')
        access_token = create_access_token(identity=data['username'])
        vendor = Vendor(name=data['username'], user_name=data['username'],
                        password=data['password'], access_token=data['access_token'], page_id=data['page_id'])
        vendor.save()
        return json.dumps({'userData': data, 'accessToken': access_token}), 200

    return 'Username is Taken Please Choose another one!', 200


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