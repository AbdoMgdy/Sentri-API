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


restaurant = ''

sender_id = ''
order_number = 0


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

    global sender_id
    sender_id = get_user_from_message(data)
    user = User.find_by_psid(sender_id)

    if user is None:
        first = handle_first_time(sender_id)
        user = first[0]
        new_order = first[1]
        global order_number
        order_number = new_order.number
        print('new user {}'.format(user.psid))
    elif user and len(user.orders) > 0:
        last_order = user.orders[-1]
        print('current user {}'.format(user.psid))
        if last_order.is_confirmed:
            last_order = Order(sender_id)
            last_order.save()
        order_number = last_order.number
    print('Current Order Number {}'.format(order_number))

    if webhook_type == "text":
        # HANDLE TEXT MESSAGES HERE
        bot.send_before_message(sender_id)
        main_menu.send(sender_id)
        return "text", 200

    elif webhook_type == "quick_reply":
        # HANDLE QUICK REPLIES HERE
        bot.send_before_message(sender_id)
        block_name = postback_events(data)
        block = blocks[block_name]
        block.send(sender_id)
        return "quick_reply", 200

    elif webhook_type == "postback":
        # HANDLE POSTBACK HERE
        bot.send_before_message(sender_id)
        block_name = postback_events(data)
        block = blocks[block_name]
        print(block.send(sender_id))
        return "postback", 200
    return "ok", 200


@app.route('/webview/order/<string:food>/<string:item>/<float:price>', methods=['GET', 'POST'])
def show_webview(food, item, price):
    if food == "sandwich":
        sandwich = OrderSandwich()
        return render_template('order sandwich.jinja', item=item, form=sandwich, price=price)
    elif food == "meal":
        meal = OrderMeal()
        return render_template('order meal.jinja', item=item, form=meal, price=price)
    elif food == "sauce":
        sauce = OrderSauce()
        return render_template('order sauce.jinja', item=item, form=sauce, price=price)


@app.route('/add_to_order/<string:food>/<string:item>/<float:price>', methods=['POST'])
def add_to_order(food, item, price):
    qty = request.form.get('quantity')
    if request.form.get('spicy') is None:
        spicy = ''
    elif request.form.get('spicy') is not None:
        spicy = request.form.get('spicy')
    if request.form.get('notes') is None:
        notes = ''
    elif request.form.get('notes') is not None:
        notes = request.form.get('notes')
    if request.form.get('notes') is None:
        combo = 0
    elif request.form.get('notes') is not None:
        combo = request.form.get('combo')

    order = Order.find_by_number(order_number)
    print(food)
    if order is None:
        order = Order(sender_id)
        order.add_item(name=item, quantity=qty, _type=spicy,
                       notes=notes, price=price, combo=combo)
        order.save()
        text = '{} was added to your order Your toatl {}'.format(
            item, order.total)
        confirm_block.set_text(text)

    if not order.is_confirmed:
        order.add_item(item, qty, spicy, notes, price, combo)
        order.save()
        text = '{} was added to your order Your toatl {}'.format(
            item, order.total)
        confirm_block.set_text(text)
    print('Test')
    confirm_block.send(sender_id)

    return 'Item added to Order', 200


@app.route('/edit_order/', methods=['GET', 'POST'])
def edit_order():
    order = Order.find_by_number(order_number)
    forms = []
    if order is not None:
        for item in order.items:
            form = OrderSandwich(formdata=item, prefix=item['name'])
            forms.append(form)
    return render_template('edit order.jinja', forms=forms)


@app.route('/show_orders', methods=['GET'])
def show_orders_t():
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
            temp = '- {} * {} ({}) Combo({}) Notes({}) /'.format(
                item['name'], item['quantity'], item['type'], item['combo'], item['notes'])
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


@app.route('/confirm_order', methods=['GET', 'POST'])
def confirm_order():
    order = Order.find_by_number(order_number)
    user = User.find_by_psid(sender_id)
    form = SignUpForm(obj=user)

    if order is not None:
        order.confirm()
        return render_template('signup.jinja', form=form)
    return 'ok', 200


@app.route('/add_user_info', methods=['GET', 'POST'])
def sign_up():
    user = User.find_by_psid(sender_id)
    user.name = request.form.get('name')
    user.phone_number = request.form.get('phone_number')
    user.address = request.form.get('address')
    user.save()
    last_order = user.orders[-1]
    receipt = ReceiptTemplate(
        recipient_name=user.name, order_number=last_order.number)

    for item in last_order.items:
        receipt.add_element(
            title=item['name'], quantity=item['quantity'], price=item['price'])
    receipt.set_summary(total_cost=last_order.total)

    receipt.send(sender_id)
    bot.send_text_message(sender_id, 'Order on The Way.')
    receipt.send(restaurant)
    return 'User info was added', 200


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
    pass


def handle_first_time(sender_id):
    new_user = User(sender_id)
    new_user.get_info()
    new_user.save()
    new_order = Order(sender_id)
    new_order.add_item('Pizza', 3, 'Spicy', '', 49.99)
    new_order.save()
    return new_user, new_order


if __name__ == "__main__":
    app.run()
