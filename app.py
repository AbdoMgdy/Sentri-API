# Standard library imports
import os
import ast
import json

# Third party imports
from flask import Flask, request, render_template, url_for, redirect, flash
from flask_restful import Resource, Api
from flask_login import current_user, login_user, logout_user, login_required
from flask_socketio import SocketIO, emit
from flask_cors import CORS, cross_origin


# Local application imports
# Models
from models.forms import OrderSandwich, OrderMeal, OrderSauce, CustomerInfo
from models.data_models import Order, OrderSchema, Customer, CustomerSchema, Vendor, VendorSchema
from models.receipt import ReceiptTemplate
from models.bot import Bot
# resources
from resources.helper_functions import *
from resources.dicts import orders, blocks, prices, arabic
from resources.buttons import confirm_block
from resources.menu import main_menu, welcome_message, info_menu, m1, m2, m3, m4, m5


app = Flask(__name__, static_folder='', static_url_path='',
            template_folder='templates')
socketio = SocketIO(app, cors_allowed_origins="*")
api = Api(app)
CORS(app)
SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
    'DATABASE_URL', 'sqlite:///data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

VERIFICATION_TOKEN = "test"

bot = Bot(access_token='EAAF5Cd9fC3YBAJmuHxR8QDEZB07kkZBlY8lH6bk0RhLklxOAFaqIrylvgBOCQtaZADGG2gr34ePPzj4ScTy2fHsfxw1FlDJ9gxBn6i8cvwtEOzcPBxIH8xlVZAtGr65nZAQ6GEokrBqvZAGMlN7keMPHD68shwg8Mlt01ZA8pFzfAZDZD')


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
    vendor = handle_vendor(page_id)
    sender_id = get_customer_from_message(data)
    customer = handle_customer(sender_id, page_id)
    print(sender_id)
    print(webhook_type)

    if webhook_type == "text":
        # HANDLE TEXT MESSAGES HERE
        # bot.send_before_message(sender_id)
        welcome_message.set_text(
            'مرحبا بك {} كيف أستطيع مساعدتك؟'.format(user.name))
        welcome_message.send(sender_id)
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
        if block_name in blocks:
            block = blocks[block_name]
            block.send(sender_id)

        return "quick_reply", 200

    elif webhook_type == "postback":
        # HANDLE POSTBACK HERE
        # bot.send_before_message(sender_id)
        block_name = postback_events(data)
        print(block_name)
        if block_name in blocks:
            print('Found it')
            block = blocks[block_name]
            bot.send_template_message(sender_id, block)
            print(bot.send_template_message(sender_id, block))

        return "postback", 200
    else:
        return "ok", 200
    return "ok", 200


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
    confirm_block.send(sender_id)
    return 'Item added to Order', 200


@app.route('/edit_order/', methods=['GET'])
def edit_order():
    return app.send_static_file('index.html')


@app.route('/vuexy', methods=['GET'])
def vuexy():
    orders = Order.query.all()
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
    print(data)
    # print(output)
    return json.dumps(data)


# @app.route('/', methods=['GET'])
# @login_required
# def admin_panel():
#     orders = Order.query.all()
#     orders_schema = OrderSchema(many=True)
#     output = orders_schema.dump(orders)
#     data = []
#     # print(output)
#     for order in output:
#         info = {}
#         info['customer'] = order['user']
#         info['time'] = order['time']
#         info['number'] = order['number']
#         info['total'] = order['total']
#         info['status'] = order['status']
#         items = ast.literal_eval(order['items'])
#         order_text = ''
#         for item in items:
#             if item['combo'] == 15:
#                 combo = 'Combo'
#             else:
#                 combo = ''
#             temp = '- {} * {} ({}) {} Notes({}) \n'.format(item['quantity'],
#                                                            item['name'], item['type'], combo, item['notes'])
#             order_text += temp
#         info['items'] = order_text
#         data.append(info)
#     # print(data)
#     # print(output)
#     return render_template('admin-panel.jinja', data=data)


# @app.route('/admin_analytics', methods=['GET'])
# @login_required
# def admin_analytics():
#     subs = User.query.count()
#     orders_d = Order.query.filter_by(status="Delivered").count()
#     orders_c = Order.query.filter_by(status="Canceled").count()
#     orders_o = Order.query.filter_by(status="Out").count()
#     orders_p = Order.query.filter_by(status="Pending").count()
#     total = orders_d + orders_c + orders_o + orders_p
#     print(total)
#     return render_template('admin-analytics.jinja', total=total, subs=subs, pending=orders_p, out=orders_o, canceled=orders_c, delivered=orders_d)


@app.route('/vuexy_users', methods=['GET'])
def vuexy_users():
    subs = Customer.query.count()
    return json.dumps({'Customers': subs})


@app.route('/confirm_order', methods=['GET'])
def confirm_order():
    form = CustomerInfo()
    return render_template('user info.jinja', form=form)  # take user info


@app.route('/user/<string:sender_id>/add_user_info', methods=['GET', 'POST'])
def add_user_info(sender_id):
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

    # look for customer
    customer = Customer.find_by_psid(sender_id)
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
    receipt.send(sender_id)
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


@socketio.on('message')
def handle_my_custom_event(json, methods=['GET', 'POST']):
    print('received message: ' + str(json))
    socketio.emit('response', json)


# @app.route('/register', methods=['GET', 'POST'])
# def register():
#     if current_user.is_authenticated:
#         return redirect(url_for('admin_panel'))
#     form = RegistrationForm()
#     if form.validate_on_submit():
#         user = Vendor(form.username.data, form.password.data)
#         user.save()
#         flash('Congratulations, you are now a registered user!')
#         return redirect(url_for('login'))
#     return render_template('admin register.jinja', form=form)


# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     if current_user.is_authenticated:
#         return redirect(url_for('admin_panel'))
#     form = LoginForm()
#     if form.validate_on_submit():

#         user = Vendor.query.filter_by(username=form.username.data).first()
#         if user is None or not user.check_password(form.password.data):
#             flash('Invalid username or password')
#             return 'wrong'

#         login_user(user, remember=form.remember_me.data)
#         return redirect(url_for('admin_panel'))
#     return render_template('admin login.jinja', form=form)


# @app.route('/logout')
# def logout():
#     logout_user()
#     return redirect(url_for('login'))


if __name__ == "__main__":
    socketio.run(app)
