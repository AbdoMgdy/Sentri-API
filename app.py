# Standard library imports
import os
import ast
import json

# Third party imports
from flask import Flask, request, render_template, url_for, redirect, flash, send_file
from flask_restful import Resource, Api
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity
)
from flask_login import current_user, login_user, logout_user, login_required
from flask_socketio import SocketIO, emit
from flask_cors import CORS, cross_origin


# Local application imports
# Models
from models.forms import OrderSandwich, OrderMeal, OrderSauce, CustomerInfo, RegistrationForm, LoginForm
from models.data_models import Order, OrderSchema, Customer, CustomerSchema, Vendor, VendorSchema
from models.receipt import ReceiptTemplate
from models.bot import Bot
# resources
from resources.helper_functions import *
from resources.dicts import orders, prices, arabic, access_tokens
from resources.buttons import confirm_block
from resources.menu import main_menu, welcome_message, info_menu, m1, m2, m3, m4, m5


app = Flask(__name__, static_folder='templates', static_url_path='',
            template_folder='templates')
socketio = SocketIO(app, cors_allowed_origins="*")

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

VERIFICATION_TOKEN = "test"


def send_order_to_vendor(result):
    print(result)
    orders_schema = OrderSchema()
    order = orders_schema.dump(result)
    print(order)
    print(type(order))
    print(order['customer'])
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
    print(info)
    print(data)
    socketio.emit('order', json.dumps(data))
    return info

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
@app.route('/vendor/orders', methods=['GET'])
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


@app.route('/vendor/customers', methods=['GET'])
@jwt_required
def vendor_customers():
    identity = get_jwt_identity()
    print(identity)
    vendor = Vendor.find_by_username(identity)
    subs = Customer.query.filter_by(page_id=vendor.page_id).count()
    return json.dumps({'customers': subs})


@app.route('/vendor/login', methods=['POST'])
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


@app.route('/vendor/register', methods=['POST'])
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


@app.route('/', defaults={'u_path': ''})
@app.route('/<path:u_path>')
def dashboard(u_path):
    # Start Vue SPA
    return app.send_static_file('index.html')


# Ordering Routes
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


@app.route('/edit_order/', methods=['GET'])
def edit_order():
    return app.send_static_file('index.html')


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
    order = Order(sender_id)
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
    customer.save()
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
    send_order_to_vendor(order)
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


# @app.route('/register', methods=['GET', 'POST'])
# def register():
#     if current_user.is_authenticated:
#         return redirect(url_for('dashboard'))
#     form = RegistrationForm()
#     if form.validate_on_submit():
#         vendor = Vendor(user_name=form.username.data,
#                         password=form.password.data,
#                         name=form.vendor_name.data,
#                         access_token=form.access_token.data,
#                         page_id=form.page_id.data)
#         vendor.save()
#         return redirect(url_for('login'))
#     return render_template('admin register.jinja', form=form)


# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     if current_user.is_authenticated:
#         return redirect(url_for('dashboard'))
#     form = LoginForm()
#     if form.validate_on_submit():
#         vendor = Vendor.query.filter_by(username=form.username.data).first()
#         if vendor is None or not vendor.check_password(form.password.data):
#             flash('Invalid username or password')
#             return 'Invalid username or password'
#         else:
#             login_user(vendor, remember=form.remember_me.data)
#             return redirect(url_for('dashboard'))
#     return render_template('admin login.jinja', form=form)


# @app.route('/logout')
# def logout():
#     logout_user()
#     return redirect(url_for('login'))

if __name__ == "__main__":
    socketio.run(app)
