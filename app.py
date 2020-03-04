# Standard library imports
import os
import json
import datetime
import logging
import ast

# Third party imports
from flask_migrate import Migrate
from flask_cors import CORS, cross_origin
from flask_socketio import SocketIO, emit, join_room, leave_room, send
import eventlet
from flask import Flask, request, render_template, url_for, redirect, current_app

from flask_jwt_extended import JWTManager

# Local application imports
# BluePrints
from webhook import routes as webhook_routes
from vendor import routes as vendor_routes
from customer import routes as customer_routes
from order import routes as order_routes
from db import db

# resources
from resources.buttons import confirm_block
from resources.dicts import orders
import resources.helper_functions as helper
# Models
from models.bot import Bot
from models.receipt import ReceiptTemplate
from models.data_models import Order, Customer, Vendor, OrderSchema
from models.forms import OrderSandwich, OrderMeal, OrderSauce, CustomerInfo, OrderForm


# eventlet.monkey_patch()  # to enable message queue for Flask-SocketIO
app = Flask(__name__, static_folder='static',
            static_url_path='', template_folder='templates')
# message_queue=os.environ.get('REDIS_URL', None)
socketio = SocketIO(app, cors_allowed_origins="*")

migrate = Migrate(app, db, compare_type=True)
jwt = JWTManager(app)
CORS(app)
# SECRET_KEY = os.urandom(32)
# app.config['JWT_ACCESS_TOKEN_EXPIRES'] = False
# app.config['JWT_SECRET_KEY'] = SECRET_KEY
# app.config['SECRET_KEY'] = SECRET_KEY
# app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
#     'DATABASE_URL', 'sqlite:///data.db')
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.register_blueprint(vendor_routes.vendor_bp)
app.register_blueprint(webhook_routes.webhook_bp)
app.register_blueprint(order_routes.order_bp)
app.register_blueprint(customer_routes.customer_bp)


# Load Test
@app.route('/load_test/2525', methods=['POST'])
def load_test():
    data = {'object': 'page', 'entry': [{'id': '103750251156613', 'time': 1582133174018, 'messaging': [{'sender': {'id': '1826620787462649'}, 'recipient': {
        'id': '103750251156613'}, 'timestamp': 1582133173655, 'postback': {'title': 'Show Menu', 'payload': 'family_menu'}}]}]}

    webhook_type = helper.get_type_from_payload(data)
    page_id = helper.get_vendor_from_message(data)
    vendor = helper.handle_vendor(page_id)
    bot = Bot(access_token=vendor.access_token)
    sender_id = helper.get_customer_from_message(data)
    customer = helper.handle_customer(sender_id, page_id)

    if webhook_type == "text":
        # HANDLE TEXT MESSAGES HERE
        # bot.send_before_message(sender_id)
        blocks = vendor.menu
        block = blocks['welcome_message']

        return "text", 200
    elif webhook_type == "quick_reply":
        # HANDLE QUICK REPLIES HERE
        # bot.send_before_message(sender_id)
        block_name = helper.quick_replies_events(data)
        blocks = vendor.menu
        if block_name in blocks:
            block = blocks[block_name]
            # bot.send_template_message(sender_id, block)

        return "quick_reply", 200

    elif webhook_type == "postback":
        # HANDLE POSTBACK HERE
        # bot.send_before_message(sender_id)
        block_name = helper.postback_events(data)

        blocks = vendor.menu
        if block_name in blocks:

            block = blocks[block_name]
            # bot.send_template_message(sender_id, block)

        return "postback", 200
    else:
        return "ok", 200
    return "ok", 200


@socketio.on('join')
def join(data):
    print(data)
    room = data['uid']
    join_room(room)
    send('connected to room: {}'.format(room), room=room)


@app.route('/user/<string:sender_id>/add_user_info', methods=['GET', 'POST'])
def add_user_info(sender_id):
    # look for customer
    customer = Customer.find_by_psid(sender_id)
    vendor = customer.vendor
    bot = Bot(access_token=vendor.access_token)

    # creat order object and fill it from temp dict
    order = Order(sender_id, vendor.page_id)
    if sender_id in orders:
        items = orders[sender_id]
        for item in items:
            order.add_item(category=item['category'],
                           name=item['name'],
                           quantity=item['quantity'],
                           price=item['price'],
                           combo=item['combo'],
                           notes=item['notes'])

    else:
        bot.send_text_message(
            sender_id, 'انتهت صلاحية الأوردر من فضلك ابدأ أوردر جديد')
        return 'Order Expired', 200

    # update customer info
    customer.name = request.form.get('name')
    customer.phone_number = request.form.get('phone_number')
    customer.address = request.form.get('address')
    customer.save()  # imp
    # make a receipt
    receipt = ReceiptTemplate(
        recipient_name=customer.name, order_number=order.number)

    for item in order.items:
        # fill receipt with order from database
        if item['combo'] == 15:
            details = '{} + Combo'.format(item['type'])
        else:
            details = '{}'.format(item['type'])
        receipt.add_element(
            title=item['name'], subtitle=details, quantity=item['quantity'], price=item['price'])
    receipt.set_summary(total_cost=order.total)
    bot.send_template_message(sender_id, {'payload': receipt.get_receipt()})
    bot.send_text_message(
        sender_id, 'يتم الآن تحضير الأوردر وسيصلك في خلال 45 - 60 دقيقة')
    result = orders.pop(sender_id, None)  # remove order from temp dict
    # receipt.send(restaurant)
    order.save()  # imp
    send_order_to_vendor(order, vendor.uid)
    return 'Customer info was added', 200


def send_order_to_vendor(result, vendor_uid):
    orders_schema = OrderSchema()
    order = orders_schema.dump(result)
    print(order)
    data = []
    info = {}
    info['customer'] = order['customer']
    info['time'] = order['time']
    info['number'] = order['number']
    info['total'] = order['total']
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
    print(data)
    socketio.emit('order', json.dumps(data), room=vendor_uid)
    return info


if __name__ == "__main__":
    socketio.run(app)
