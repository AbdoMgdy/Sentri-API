import os
from flask import Flask, request, render_template, redirect
from models.user import User
from models.order import Order
from models.bot import Bot
from forms import OrderForm
from resources.menu import *


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
order_number = ''


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
            elif user and len(user.orders) > 0:
                last_order = user.orders[-1]
                if last_order.is_confirmed:
                    new_order = Order(sender_id)
                    new_order.add()
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
                    print(block.elements)
                    block.send(sender_id)
                    return "ok", 200
    return "ok", 200


@app.route('/webview/order/<string:item>', methods=['GET', 'POST'])
def show_webview(item):
    form = OrderForm()
    if form.validate_on_submit():
        redirect('/add_to_order/{}'.format(item))
    return render_template('order.jinja', item=item, form=form)


@app.route('/add_to_order/<string:item>', methods=['POST'])
def save(item):
    qty = request.form.get('quantity')
    spicy = request.form.get('spicy')
    notes = request.form.get('notes')
    print(item, qty, spicy, notes, 250)
    order = Order.find_by_number(order_number)
    print(order.number)
    if not order.is_confirmed:
        order.add_item(item, qty, spicy, notes)
        print('added to DB')
    return '{} was added to order'.format(item), 200


@app.route('/confirm_order', methods=['POST'])
def confirm_order():
    order = Order.find_by_number(order_number)
    if not order.is_confirmed:
        order.confirm()
    return 'Order Confirmed', 200


def handle_first_time(sender_id):
    new_user = User(sender_id)
    new_user.add()
    new_order = Order(sender_id)
    new_order.add()
    return new_user, new_order


if __name__ == "__main__":
    app.run()
