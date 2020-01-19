import os
from flask import Flask, request, render_template
from models.user import User, UserSchema
from models.order import Order, OrderSchema
import json
from models.bot import Bot
from forms import OrderForm, SignUpForm
from tables import Results
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
    'confirm_order': 'order_confirmed'
}


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

    elif webhook_type == "postback" and postback_events(data) == 'confirm_order':
        confirm_order(order_number, sender_id)

    elif webhook_type == "postback":
        # HANDLE POSTBACK HERE
        bot.send_before_message(sender_id)
        block_name = postback_events(data)
        block = blocks[block_name]
        block.send(sender_id)
        return "postback", 200
    return "ok", 200


@app.route('/webview/order/<string:item>/<float:price>', methods=['GET', 'POST'])
def show_webview(item, price):
    form = OrderForm()
    return render_template('order.jinja', item=item, form=form, price=price)


@app.route('/add_to_order/<string:item>/<float:price>', methods=['POST'])
def add_to_order(item, price):
    qty = request.form.get('quantity')
    spicy = request.form.get('spicy')
    notes = request.form.get('notes')
    print(item)
    print(price)
    print(spicy)
    print(qty)
    order = Order.find_by_number(order_number)
    print(order.number)

    if order is None:
        order = Order(sender_id)
        order.add_item(item, qty, spicy, notes, price)
        order.save()
        text = '{} was added to your order Your toatl {}'.format(
            item, order.total)
        confirm_block.set_text(text)

    if not order.is_confirmed:
        order.add_item(item, qty, spicy, notes, price)
        order.save()
        text = '{} was added to your order Your toatl {}'.format(
            item, order.total)
        confirm_block.set_text(text)
    confirm_block.send(sender_id)
    return 'Item added to Order', 200


@app.route('/show_orders', methods=['GET'])
def show_orders_t():
    orders = Order.query.all()
    orders_schema = OrderSchema(many=True)
    output = orders_schema.dump(orders)
    print(output)
    return render_template('show orders.jinja', rows=output)


@app.route('/show_orders', methods=['GET'])
def search_users():
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
    table = Results(output)
    print(output)
    return render_template('show table.jinja', table=table)


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


@app.route('/signup', methods=['GET', 'POST'])
def confirm_order():
    order = Order.find_by_number(order_number)
    user = User.find_by_psid(sender_id)
    print(user)
    form = SignUpForm(obj=user)
    if form.validate_on_submit():
        user.name = request.form.get('name')
        user.phone = request.form.get('phone')
        user.address = request.form.get('address')

    if order is not None:
        order.confirm()
        return render_template('signup.jinja', form=form)
    return 'ok', 200


if __name__ == "__main__":
    app.run()
