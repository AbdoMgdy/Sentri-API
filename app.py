# Standard library imports
import os
import ast
import json
import datetime
import logging


# Third party imports
import eventlet
from flask import Flask, request, render_template, url_for, redirect, flash, send_file, send_from_directory, current_app
from flask_restful import Resource, Api
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity
)
from flask_socketio import SocketIO, emit, join_room, leave_room, send
from flask_cors import CORS, cross_origin
from flask_migrate import Migrate


# Local application imports
# Models
from models.forms import OrderSandwich, OrderMeal, OrderSauce, CustomerInfo, RegistrationForm, LoginForm
from models.data_models import Order, OrderSchema, Customer, CustomerSchema, Vendor, VendorSchema
from models.receipt import ReceiptTemplate
from models.bot import Bot
# resources
from resources.helper_functions import *
from resources.dicts import orders, access_tokens
from resources.buttons import confirm_block
from resources.menu import main_menu, welcome_message, info_menu, m1, m2, m3, m4, m5
from db import db
from vendor import routes as vendor_routes

eventlet.monkey_patch()  # to enable message queue for Flask-SockeIO
app = Flask(__name__, static_folder='static', static_url_path='',
            template_folder='templates')
socketio = SocketIO(app, cors_allowed_origins="*",
                    message_queue=os.environ.get('REDIS_URL', None))

migrate = Migrate(app, db, compare_type=True)
jwt = JWTManager(app)
api = Api(app)
CORS(app)
SECRET_KEY = os.urandom(32)
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = False
app.config['JWT_SECRET_KEY'] = SECRET_KEY

app.config['SECRET_KEY'] = SECRET_KEY
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
    'DATABASE_URL', 'sqlite:///data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.register_blueprint(vendor_routes.vendor_bp)
VERIFICATION_TOKEN = "test"


# Webhook Routes
@app.route('/webhook', methods=['GET'])
def verify():
    if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.challenge"):
        if not request.args.get("hub.verify_token") == VERIFICATION_TOKEN:
            return "Verification token mismatch", 403
        return request.args["hub.challenge"], 200
    return "Hello world", 200


@app.route('/webhook', methods=['POST'])
def handle_incoming_messages():
    data = request.get_json()
    print(data)
    webhook_type = get_type_from_payload(data)
    page_id = get_vendor_from_message(data)
    vendor = handle_vendor(page_id, access_tokens[page_id])
    bot = Bot(access_token=vendor.access_token)
    sender_id = get_customer_from_message(data)
    customer = handle_customer(sender_id, page_id)
    print(sender_id)
    print(webhook_type)
    bot.send_before_message(sender_id)
    if not vendor.is_open():
        bot.send_text_message(
            sender_id, 'الرجاء المحاولة مرة أخرى خلال مواعيد العمل الرسمية من {} الى {}'.format(vendor.open_hours.strftime('%H:%M'), vendor.close_hours.strftime('%H:%M')))
        return 'Vendor is Closed', 200
    if webhook_type == "text":
        # HANDLE TEXT MESSAGES HERE
        # bot.send_before_message(sender_id)
        blocks = vendor.menu
        block = blocks['welcome_message']
        print(bot.send_template_message(sender_id, block))
        return "text", 200
    elif webhook_type == "quick_reply" and quick_replies_events(data) == "send_menu":
        m1.send(sender_id)
        m2.send(sender_id)
        m3.send(sender_id)
        m4.send(sender_id)
        m5.send(sender_id)
        return "Sent Menu", 200

    elif webhook_type == "quick_reply":
        # HANDLE QUICK REPLIES HERE
        # bot.send_before_message(sender_id)
        block_name = quick_replies_events(data)
        blocks = vendor.menu
        if block_name in blocks:
            block = blocks[block_name]
            # bot.send_template_message(sender_id, block)
            print(bot.send_template_message(sender_id, block))

        return "quick_reply", 200

    elif webhook_type == "postback":
        # HANDLE POSTBACK HERE
        # bot.send_before_message(sender_id)
        block_name = postback_events(data)
        print(block_name)
        blocks = vendor.menu
        if block_name in blocks:
            print('Found it')
            block = blocks[block_name]
            # bot.send_template_message(sender_id, block)
            print(bot.send_template_message(sender_id, block))

        return "postback", 200
    else:
        return "ok", 200
    return "ok", 200

# Dashboard Routes


@app.route('/webview/order/<string:food>/<string:item>', methods=['GET'])
def show_webview(food, item):
    if food == "sandwich":
        sandwich = OrderSandwich()
        return render_template('order sandwich.jinja', food="sandwich", item=item, form=sandwich)
    elif food == "meal":
        meal = OrderMeal()
        return render_template('order meal.jinja', food="meal", item=item, form=meal)
    elif food == "sauce":
        sauce = OrderSauce()
        return render_template('order sauce.jinja', food="sauce", item=item, form=sauce)


@app.route('/user/<string:sender_id>/add_to_order/<string:food>/<string:item>/', methods=['GET', 'POST'])
def add_to_order(sender_id, food, item):
    customer = Customer.find_by_psid(sender_id)
    vendor = customer.vendor
    prices = vendor.prices
    arabic = vendor.arabic
    bot = Bot(access_token=vendor.access_token)
    # save unconfirmed orders in dict
    order_item = {}
    qty = request.form.get('quantity')
    if request.form.get('spicy') is None:
        spicy = ''
    elif request.form.get('spicy') is not None:
        spicy = request.form.get('spicy')
    if request.form.get('notes') is None:
        notes = ''
    elif request.form.get('notes') is not None:
        notes = request.form.get('notes')
    if request.form.get('combo') is None:
        combo = 0
    elif request.form.get('combo') is not None:
        combo = request.form.get('combo')
    order_item['category'] = food
    order_item['name'] = item
    order_item['quantity'] = qty
    order_item['type'] = spicy
    order_item['price'] = prices[item]
    order_item['combo'] = combo
    order_item['notes'] = notes

    update_order(sender_id, order_item)

    if spicy in arabic:
        text = '{} * {} {} تمت اضافته للأوردو الخاص بك'.format(qty,
                                                               arabic[item], arabic[spicy])
    else:
        text = '{} * {} {} تمت اضافته للأوردو الخاص بك'.format(qty,
                                                               arabic[item], spicy)
    confirm_block.set_text(text)
    bot.send_template_message(
        sender_id, {'payload': confirm_block.get_template()})
    return 'Item added to Order', 200


@app.route('/edit_order', methods=['GET'])
def edit_order():
    return app.send_static_file('edit_order.html')


@app.route('/confirm_order', methods=['GET'])
def confirm_order():
    form = CustomerInfo()
    return render_template('user info.jinja', form=form)  # take user info


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
                           _type=item['type'],
                           price=item['price'],
                           combo=item['combo'],
                           notes=item['notes'])

    else:
        bot.send_text_message(
            sender_id, 'انتهت صلاحة الأوردر من فضلك ابدأ أوردر جديد')
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
    send_order_to_vendor(order, vendor.username)
    return 'Customer info was added', 200


@app.route('/user/<string:sender_id>/order_info', methods=['GET'])
def post_order_info(sender_id):
    if sender_id in orders:
        return json.dumps(orders[sender_id]), 200
    else:
        return 'Customer not found', 404


@app.route('/user/<string:sender_id>/edit_order', methods=['POST'])
def get_order_info(sender_id):
    customer = Customer.find_by_psid(sender_id)
    vendor = Vendor.find_by_page_id(customer.page_id)
    bot = Bot(access_token=vendor.access_token)
    data = request.get_json()
    if not data['items']:
        bot.send_text_message(sender_id, 'انت لم تطلب شيء بعد!')
        result = orders.pop(sender_id, None)  # remove order from temp dict
        return 'order Empty', 200
    if sender_id in orders:
        orders[sender_id] = data['items']
    confirm_block.set_text('تم تعديل الأوردر الخاص بك')
    confirm_block.send(sender_id)
    return 'ok', 200


@app.route('/edit_order_status', methods=['POST'])
def edit_order_status():
    print(request.form.get('order_status'))
    print(request.form.get('order_number'))
    order = Order.find_by_number(request.form.get('order_number'))
    if order:
        order.edit(request.form.get('order_status'))
        order.save()
    return 'Order Stauts was edited', 200

# For Comments
@app.route('/vendors', methods=['GET'])
def vendors():
    vendors = Vendor.query.all()
    vendor_schema = VendorSchema(many=True)
    output = vendor_schema.dump(vendors)
    return json.dumps(output)

# Load Test
@app.route('/load_test/2525', methods=['POST'])
def load_test():
    data = {'object': 'page', 'entry': [{'id': '103750251156613', 'time': 1582133174018, 'messaging': [{'sender': {'id': '1826620787462649'}, 'recipient': {
        'id': '103750251156613'}, 'timestamp': 1582133173655, 'postback': {'title': 'Show Menu', 'payload': 'family_menu'}}]}]}

    webhook_type = get_type_from_payload(data)
    page_id = get_vendor_from_message(data)
    vendor = handle_vendor(page_id, access_tokens[page_id])
    bot = Bot(access_token=vendor.access_token)
    sender_id = get_customer_from_message(data)
    customer = handle_customer(sender_id, page_id)

    if webhook_type == "text":
        # HANDLE TEXT MESSAGES HERE
        # bot.send_before_message(sender_id)
        blocks = vendor.menu
        block = blocks['welcome_message']

        return "text", 200
    elif webhook_type == "quick_reply" and quick_replies_events(data) == "send_menu":
        m1.send(sender_id)
        m2.send(sender_id)
        m3.send(sender_id)
        m4.send(sender_id)
        m5.send(sender_id)
        return "Sent Menu", 200

    elif webhook_type == "quick_reply":
        # HANDLE QUICK REPLIES HERE
        # bot.send_before_message(sender_id)
        block_name = quick_replies_events(data)
        blocks = vendor.menu
        if block_name in blocks:
            block = blocks[block_name]
            # bot.send_template_message(sender_id, block)

        return "quick_reply", 200

    elif webhook_type == "postback":
        # HANDLE POSTBACK HERE
        # bot.send_before_message(sender_id)
        block_name = postback_events(data)

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
    room = data['username']
    join_room(room)
    send('connected to room: {}'.format(room), room=room)


def send_order_to_vendor(result, vendor_username):
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
    socketio.emit('order', json.dumps(data), room=vendor_username)
    return info


if __name__ == "__main__":
    socketio.run(app)
