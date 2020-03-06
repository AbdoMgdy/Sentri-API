from app.resources.dicts import menus, arabic, prices
from app.order import Order, OrderSchema
from app.customer import Customer
from app.vendor import Vendor
from app.models.bot import Bot
from firebase_admin import messaging
import ast


def get_type_from_payload(data):

    if "postback" in data["entry"][0]["messaging"][0]:
        return "postback"

    elif "message" in data["entry"][0]["messaging"][0]:
        if "quick_reply" in data["entry"][0]["messaging"][0]['message']:
            return "quick_reply"
        elif "text" in data["entry"][0]["messaging"][0]['message']:
            return "text"


def get_customer_from_message(data):
    messaging_events = data["entry"][0]["messaging"][-1]
    return messaging_events["sender"]["id"]


def get_vendor_from_message(data):
    messaging_events = data["entry"][0]["messaging"][-1]
    return messaging_events["recipient"]["id"]


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


def handle_first_time_customer(sender_id, page_id):
    new_customer = Customer(sender_id, page_id)
    new_customer.save()
    return new_customer


# def handle_current_customer(sender_id):
#     current_customer = Customer.find_by_psid(sender_id)
#     if current_customer:
#         return current_customer
#     else:
#         return 'Customer Not Found'


def handle_customer(sender_id, vendor):
    customer = Customer.find_by_psid(sender_id)
    if customer is None:
        customer = handle_first_time_customer(sender_id, vendor)
    return customer


def handle_first_time_vendor(page_id):
    new_vendor = Vendor.find_by_page_id(page_id)
    bot = Bot(new_vendor.page_access_token)
    bot.set_get_started({
        'get_started': {
            'payload': 'get_started'
        }
    })
    bot.set_persistent_menu({
        'persistent_menu': [
            {
                'locale': 'default',
                'composer_input_disabled': False,
                'call_to_actions': [
                    {
                        'type': 'web_url',
                        'title': 'Powered By Sentri',
                        'url': 'https://www.sentri.io/',
                    }
                ]
            }
        ]
    })
    new_vendor.blocks = menus['103750251156613']
    new_vendor.arabic = arabic['103750251156613']
    new_vendor.prices = prices['103750251156613']
    # new_vendor.is_setup = True
    new_vendor.save()
    return new_vendor


def handle_current_vendor(page_id, ):
    current_vendor = Vendor.find_by_page_id(page_id)
    return current_vendor


def handle_vendor(page_id):
    vendor = Vendor.find_by_page_id(page_id)
    if vendor is not None and vendor.is_setup:
        vendor = handle_current_vendor(page_id)
    else:
        vendor = handle_first_time_vendor(page_id)
    return vendor


def get_order_from_customer(customer):
    orders = customer.orders
    if orders:
        for order in orders:
            if not order.is_confirmed:
                return order
    order = Order(customer.psid, customer.page_id)
    return order


def send_order_to_vendor(result, fcm_token):
    orders_schema = OrderSchema()
    order = orders_schema.dump(result)
    print(order)
    data = []
    info = {}
    info['customer'] = order['customer']
    info['time'] = order['time']
    info['number'] = order['number']
    info['price'] = order['price']
    info['status'] = order['status']
    # items = ast.literal_eval(order['items'])
    # order_text = ''
    # for item in items:
    #     if item['combo'] == 15:
    #         combo = 'Combo'
    #     else:
    #         combo = ''
    #     temp = '- {} * {} ({}) {} Notes({}) \n'.format(item['quantity'],
    #                                                    item['name'], item['type'], combo, item['notes'])
    #     order_text += temp
    # info['items'] = order_text
    data.append(info)
    print(data)
    msg = messaging.Message(data=order, token=fcm_token)
    msg_id = messaging.send(msg)
    return msg_id
