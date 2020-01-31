# Standard library imports
import os
import ast
import json

# Third party imports
from flask import Flask, request, render_template, url_for, redirect, flash
from flask_restful import Resource, Api
from flask_login import current_user, login_user, logout_user, login_required

# Local application imports
from models.forms import OrderSandwich, OrderMeal, OrderSauce, CustomerInfo, LoginForm, RegistrationForm
from models.data_models import Order, OrderSchema, User, UserSchema, LoginUser, LoginUserSchema
from models.receipt import ReceiptTemplate
from models.bot import Bot

from resources.helper_functions import *
from resources.dicts import orders, blocks, prices, arabic
from resources.buttons import confirm_block
from resources.menu import main_menu, welcome_message, info_menu, m1, m2, m3, m4, m5


app = Flask(__name__, static_folder='', static_url_path='',
            template_folder='templates')

api = Api(app)
SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
    'DATABASE_URL', 'sqlite:///data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

VERIFICATION_TOKEN = "test"

bot = Bot()

restaurant = ''


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('show_orders'))
    form = RegistrationForm()
    if form.validate_on_submit():
        print('submit pressed')
        user = LoginUser(form.username.data, form.password.data)
        user.save()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('admin register.jinja', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('show_orders'))
    form = LoginForm()
    if form.validate_on_submit():
        print('submit pressed')
        user = LoginUser.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return 'wrong'
        print(user.username)
        login_user(user, remember=form.remember_me.data)
        return redirect('/show_orders')
    return render_template('admin login.jinja', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/', methods=['GET'])
def verify():
    if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.challenge"):
        if not request.args.get("hub.verify_token") == VERIFICATION_TOKEN:
            return "Verification token mismatch", 403
        return request.args["hub.challenge"], 200
    return "Hello world", 200


@app.route('/', methods=['POST'])
def handle_incoming_messages():
    print(request.data)
    data = request.get_json()

    webhook_type = get_type_from_payload(data)

    user = get_user_from_message(data)
    print(user)
    print(webhook_type)

    sender_id = get_user_from_message(data)
    user = handle_user(sender_id)

    if webhook_type == "text":
        # HANDLE TEXT MESSAGES HERE
        bot.send_before_message(sender_id)
        welcome_message.set_text(
            'مرحبا بك {} في تركس تشيكن كيف أستطيع مساعدتك؟'.format(user.name))
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
        bot.send_before_message(sender_id)
        block_name = quick_replies_events(data)
        block = blocks[block_name]
        block.send(sender_id)
        return "quick_reply", 200

    elif webhook_type == "postback":
        # HANDLE POSTBACK HERE
        bot.send_before_message(sender_id)
        block_name = postback_events(data)
        block = blocks[block_name]
        block.send(sender_id)
        return "postback", 200
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


@app.route('/show_orders', methods=['GET'])
@login_required
def show_orders():
    orders = Order.query.filter_by(is_confirmed=True).all()
    orders_schema = OrderSchema(many=True)
    output = orders_schema.dump(orders)
    data = []
    print(output)
    for order in output:
        info = {}
        user = order['user']
        info['user'] = user
        total = order['total']
        info['total'] = total
        items = ast.literal_eval(order['items'])
        order = ''
        for item in items:
            if item['combo'] == 15:
                combo = 'Combo'
            else:
                combo = ''
            temp = '- {} * {} ({}) {} Notes({}) \n'.format(item['quantity'],
                                                           item['name'], item['type'], combo, item['notes'])
            order += temp
        info['items'] = order
        data.append(info)
    print(data)
    print(output)
    return render_template('show orders.jinja', data=data)


@app.route('/omar_test', methods=['GET', 'POSt'])
def test_omar():
    orders = Order.query.filter_by(is_confirmed=True).all()
    orders_schema = OrderSchema(many=True)
    output = orders_schema.dump(orders)
    output.reverse()
    return json.dumps(output), 200


@app.route('/omar_test_items', methods=['GET', 'POSt'])
def test_omar_items():
    orders = Order.query.filter_by(is_confirmed=True).all()
    orders_schema = OrderSchema(many=True)
    output = orders_schema.dump(orders)
    output.reverse()
    new_items = []
    order_s = ''
    for order in output:
        obj = {}
        items = ast.literal_eval(order['items'])
        for item in items:
            if item['combo'] == 15:
                combo = 'Combo'
            else:
                combo = ''
            temp = '- {} * {} ({}) {} Notes({}) \n'.format(item['quantity'],
                                                           item['name'], item['type'], combo, item['notes'])
            order_s += temp
        obj['string'] = order
        new_items.append(obj)
    print(items)
    return json.dumps(new_items), 200


@app.route('/show_users', methods=['GET'])
def show_users():
    users = LoginUser.query.all()
    users_schema = LoginUserSchema(many=True)
    output = users_schema.dump(users)
    print(output)
    return render_template('show users.jinja', rows=output)


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
    result = orders.pop(sender_id, None)  # remove order from temp dict
    print(result)
    # look for user
    user = User.find_by_psid(sender_id)
    # update user info
    user.name = request.form.get('name')
    user.phone_number = request.form.get('phone_number')
    user.address = request.form.get('address')
    user.save()
    # get last order and confirm it
    order.confirm()
    # make a receipt
    receipt = ReceiptTemplate(
        recipient_name=user.name, order_number=order.number)

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
    print(receipt.get_receipt())
    bot.send_text_message(
        sender_id, 'يتم الآن تحضير الأوردر وسيصلك في خلال 45 - 60 دقيقة')
    # receipt.send(restaurant)
    return 'User info was added', 200


@app.route('/user/<string:sender_id>/order_info', methods=['GET'])
def post_order_info(sender_id):
    print(request.data)
    if sender_id in orders:
        return json.dumps(orders[sender_id]), 200
    else:
        return 'user not found', 404


@app.route('/user/<string:sender_id>/edit_order', methods=['POST'])
def get_order_info(sender_id):
    user = User.find_by_psid(sender_id)
    data = request.get_json()
    if not data['items']:
        bot.send_text_message(sender_id, 'انت لم تطلب شيء بعد!')
        result = orders.pop(sender_id, None)  # remove order from temp dict
        print(result)
        return 'order Empty', 200
    if sender_id in orders:
        orders[sender_id] = data['items']
    confirm_block.set_text('تم تعديل الأوردر الخاص بك')
    confirm_block.send(sender_id)
    return 'ok', 200


if __name__ == "__main__":
    app.run()
