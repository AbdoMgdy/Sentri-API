import os
from flask import Flask, request, render_template
import json
from models.user import User
from models.order import Order, OrderSchema
from models.bot import Bot
from forms import OrderForm
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
    'family_menu': family_menu
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

    print(webhook_type)

    if data['object'] == "page":
        entries = data['entry']

        for entry in entries:
            messaging = entry['messaging']

            global sender_id
            sender_id = messaging[0]['sender']['id']
            user = User.find_by_psid(sender_id)

            if user is None:
                first = handle_first_time(sender_id)
                user = first[0]
                new_order = first[1]
                global order_number
                order_number = new_order.number
                print(user.first_name)
            elif user and len(user.orders) > 0:
                last_order = user.orders[-1]
                print(user.first_name)
                if last_order.is_confirmed:
                    last_order = Order(sender_id)
                    last_order.add()
                order_number = last_order.number
            print(order_number)
            for messaging_event in messaging:

                if messaging_event.get('message'):
                    # HANDLE QUICK REPLIES HERE
                    if messaging_event['message'].get('quick_reply'):
                        bot.send_before_message(sender_id)
                        block_name_q = messaging_event['message']['quick_reply']['payload']
                        block_name = block_name_q.replace('"', '')
                        block = blocks[block_name]
                        block.send(sender_id)
                        return "ok", 200
                        print(sender_id)
                    # HANDLE TEXT MESSAGES HERE
                    if messaging_event['message'].get('text'):
                        bot.send_before_message(sender_id)
                        main_menu.send(sender_id)
                        return "text", 200
                elif messaging_event.get('postback'):
                    # HANDLE POSTBACK HERE
                    bot.send_before_message(sender_id)
                    block_name_q = messaging_event['postback']['payload']
                    block_name = block_name_q.replace('"', '')
                    block = blocks[block_name]

                    block.send(sender_id)
                    return "ok", 200
    return "ok", 200


@app.route('/webview/order/<string:item>/<float:price>', methods=['GET', 'POST'])
def show_webview(item, price):
    form = OrderForm()
    return render_template('order.jinja', item=item, form=form, price=price)


@app.route('/add_to_order/<string:item>/<float:price>', methods=['POST'])
def save(item, price):
    qty = request.form.get('quantity')
    spicy = request.form.get('spicy')
    notes = request.form.get('notes')
    print(item)
    print(price)
    print(spicy)
    print(qty)
    order = Order.find_by_number(order_number)
    print(order.number)

    text = '{} was added to your order Your toatl {}'.format(item, order.total)
    confirm_block.set_text(text)
    confirm_block.add_postback(**{'Confirm': 'Order_Confirmed'})

    if order is None:
        order = Order(sender_id)
        order.add_item(item, qty, spicy, notes, price)
        order.save()

    if not order.is_confirmed:
        order.add_item(item, qty, spicy, notes, price)
        order.save()
        print('added to DB')
        print(confirm_block.buttons)
    confirm_block.send(sender_id)
    # return 'Item added to Order', 200


@app.route('/confirm_order', methods=['POST'])
def confirm_order():
    order = Order.find_by_number(order_number)
    if not order.is_confirmed:
        order.confirm()
    return 'Order Confirmed', 200


@app.route('/show_orders', methods=['GET'])
def search_results():
    orders = Order.query.all()
    orders_schema = OrderSchema(many=True)
    output = orders_schema.dump(orders)
    print(output)
    return render_template('show orders.jinja', rows=output)


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


def handle_first_time(sender_id):
    new_user = User(sender_id)
    new_user.save()
    new_order = Order(sender_id)
    new_order.add_item('Pizza', 3, 'Spicy', '', 49.99)
    new_order.save()
    return new_user, new_order


if __name__ == "__main__":
    app.run()
