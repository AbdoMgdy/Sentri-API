import os
import ast
from flask import Flask, request, render_template
from models.data_models import Order, OrderSchema, User, UserSchema
from models.receipt import ReceiptTemplate
import json
from models.bot import Bot
from forms import OrderSandwich, OrderMeal, OrderSauce, SignUpForm
from tables import Results, Items
from resources.buttons import confirm_block
from resources.menu import main_menu, family_menu


app = Flask(__name__, template_folder='templates')
SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
    'DATABASE_URL', 'sqlite:///data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

VERIFICATION_TOKEN = "test"

bot = Bot()


blocks = {
    'get_started': main_menu,
    'main_menu': main_menu,
    'family_menu': family_menu,
    'confirm_block': confirm_block,
}


orders = {}

restaurant = ''


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
    user = User.find_by_psid(sender_id)

    if user is None:
        first = handle_first_time_user(sender_id)
        user = first
        print('new user {}'.format(user.psid))
    elif user and len(user.orders) > 0:
        current = handle_current_user(sender_id)
        user = current
        print('current user {}'.format(user.psid))

    if webhook_type == "text":
        # HANDLE TEXT MESSAGES HERE
        bot.send_before_message(sender_id)
        main_menu.send(sender_id)
        return "text", 200

    elif webhook_type == "quick_reply":
        # HANDLE QUICK REPLIES HERE
        bot.send_before_message(sender_id)
        block_name = quick_replies_events(data)
        block = blocks[block_name]
        block.send(sender_id)
        return "quick_reply", 200
    elif webhook_type == "postback" and postback_events(data) == "cancel_order":
        orders.pop(sender_id, None)
        bot.send_text_message(sender_id, 'Order Was Canceld')
    elif webhook_type == "postback":
        # HANDLE POSTBACK HERE
        bot.send_before_message(sender_id)
        block_name = postback_events(data)
        block = blocks[block_name]
        block.send(sender_id)
        return "postback", 200
    return "ok", 200


@app.route('/webview/order/<string:food>/<string:item>/<float:price>', methods=['GET'])
def show_webview(food, item, price):
    if food == "sandwich":
        sandwich = OrderSandwich()
        return render_template('order sandwich.jinja', food="sandwich", item=item, form=sandwich, price=price)
    elif food == "meal":
        meal = OrderMeal()
        return render_template('order meal.jinja', food="meal", item=item, form=meal, price=price)
    elif food == "sauce":
        sauce = OrderSauce()
        return render_template('order sauce.jinja', food="sauce", item=item, form=sauce, price=price)


@app.route('/user/<string:sender_id>/add_to_order/<string:food>/<string:item>/<float:price>', methods=['GET', 'POST'])
def add_to_order(sender_id, food, item, price):
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
    order_item['price'] = price
    order_item['combo'] = combo
    order_item['notes'] = notes

    update_order(sender_id, order_item)

    text = '{} * {} was added to your order'.format(qty,
                                                    item)
    confirm_block.set_text(text)
    confirm_block.send(sender_id)
    return 'Item added to Order', 200


@app.route('/edit_order/', methods=['GET', 'POST'])
def edit_order():
    order = Order.find_by_number(55)
    order_schema = OrderSchema()
    order_list = order_schema.dump(order)
    print(order_list)
    print(order.items)
    forms = []
    if order is not None:
        for item in order.items:
            if item['category'] == "sandwich":
                data = {}
                form_data = {'quantity': int(item['quantity']), 'spicy': item['type'],
                             'notes': item['notes'], 'combo': int(item['combo'])}
                data['name'] = item['name']
                data['form'] = OrderSandwich(
                    data=form_data, prefix=item['name'])
                forms.append(data)
            elif item['category'] == "meal":
                data = {}
                form_data = {'quantity': int(item['quantity']), 'spicy': item['type'],
                             'notes': item['notes']}
                data['name'] = item['name']
                data['form'] = OrderMeal(
                    data=form_data, prefix=item['name'])
                forms.append(data)
            elif item['category'] == "sauce":
                data = {}
                form_data = {'quantity': int(item['quantity'])}
                data['name'] = item['name']
                data['form'] = OrderSauce(
                    data=form_data, prefix=item['name'])
                forms.append(data)
    return render_template('edit order.jinja', forms=forms)


@app.route('/accept_edit', methods=['POST'])
def accept_edit():
    data = request.form.to_dict(flat=False)
    print(data)
    order = Order.query.filter_by(number=55).first()
    order_schema = OrderSchema()
    output = order_schema.dump(order)
    items = ast.literal_eval(output['items'])
    return 'Order was edited', 200


@app.route('/show_orders', methods=['GET'])
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
    return render_template('show orders.jinja', data=data)


@app.route('/show_users', methods=['GET'])
def show_users():
    users = User.query.all()
    users_schema = UserSchema(many=True)
    output = users_schema.dump(users)
    print(output)
    return render_template('show users.jinja', rows=output)


@app.route('/show_table', methods=['GET'])
def show_table():
    orders = Order.query.all()
    orders_schema = OrderSchema(many=True)
    output = orders_schema.dump(orders)
    items = output[0]['items']
    table = Items(items)
    print(items)
    return render_template('table.jinja', table=table)


@app.route('/confirm_order', methods=['GET'])
def confirm_order():
    form = SignUpForm()
    return render_template('signup.jinja', form=form)  # take user info


@app.route('/user/<string:sender_id>/add_user_info', methods=['GET', 'POST'])
def sign_up(sender_id):
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
        bot.send_text_message(sender_id, 'Order Expired Please Order Again!')
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
    last_order = order
    last_order.confirm()
    # make a receipt
    receipt = ReceiptTemplate(
        recipient_name=user.name, order_number=last_order.number)

    for item in last_order.items:
        # fill receipt with order from database
        if item['combo'] == 15:
            details = '{} + Combo'.format(item['type'])
        else:
            details = '{}'.format(item['type'])
        receipt.add_element(
            title=item['name'], subtitle=details, quantity=item['quantity'], price=item['price'])
    receipt.set_summary(total_cost=last_order.total)

    receipt.send(sender_id)
    print(receipt.get_receipt())
    bot.send_text_message(sender_id, 'Order on The Way.')
    # receipt.send(restaurant)
    return 'User info was added', 200


# ============================================== HELPER FUNCTIONS ============================================== #


def get_type_from_payload(data):

    if "postback" in data["entry"][0]["messaging"][0]:
        return "postback"

    elif "message" in data["entry"][0]["messaging"][0]:
        if "quick_reply" in data["entry"][0]["messaging"][0]['message']:
            return "quick_reply"
        elif "text" in data["entry"][0]["messaging"][0]['message']:
            return "text"


def get_user_from_message(data):
    messaging_events = data["entry"][0]["messaging"][-1]
    return messaging_events["sender"]["id"]


def postback_events(data):

    postbacks = data["entry"][0]["messaging"]

    for event in postbacks:
        postback_payload = event["postback"]["payload"]
        postback = postback_payload.replace('"', '')
        return postback


def quick_replies_events(data):
    quick_replies = data["entry"][0]["messaging"]

    for event in quick_replies:
        quick_reply_payload = event["message"]["quick_reply"]["payload"]
        quick_reply = quick_reply_payload.replace('"', '')
        return quick_reply


def handle_first_time_user(sender_id):
    new_user = User(sender_id)
    new_user.get_info()
    new_user.save()
    orders[sender_id] = []
    return new_user


def handle_current_user(sender_id):
    current_user = User.find_by_psid(sender_id)
    if sender_id in orders:
        pass
    else:
        orders[sender_id] = []
    return current_user


def update_order(sender_id, item):
    if sender_id in orders:
        orders[sender_id].append(item)
    else:
        orders[sender_id] = []
        orders[sender_id].append(item)


if __name__ == "__main__":
    app.run()
