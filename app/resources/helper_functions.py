from app.resources.dicts import menus, arabic, prices
from app.order import Order, OrderSchema
from app.customer import Customer
from app.vendor import Vendor
from app.catalog import Catalog
from app.models.bot import Bot
from firebase_admin import messaging
import firebase_admin
import ast
import json
from firebase_admin import credentials

from wit import Wit


def get_type_from_payload(data):
    if "changes" in data["entry"][0]:
        return "changes"
    elif "messaging" in data["entry"][0]:
        return "messaging"


def get_type_from_message(data):

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


def get_vendor_from_comment(data):
    return data["entry"][0]["id"]


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
    catalog = Catalog(page_id)
    catalog.save()
    new_vendor.arabic = arabic['103750251156613']
    new_vendor.prices = prices['103750251156613']
    # new_vendor.is_setup = True
    new_vendor.save()
    return new_vendor, catalog


def handle_current_vendor(page_id):
    current_vendor = Vendor.find_by_page_id(page_id)
    catalog = Catalog.find_by_page_id(page_id)
    if not catalog:
        catalog = Catalog(page_id)
        catalog.save()
        print(catalog)
    return current_vendor, catalog


def handle_vendor(page_id):
    vendor = Vendor.find_by_page_id(page_id)
    if vendor:
        vendor = handle_current_vendor(page_id)[0]
        catalog = handle_current_vendor(page_id)[1]
    else:
        vendor = handle_first_time_vendor(page_id)[0]
        catalog = handle_first_time_vendor(page_id)[1]
    return vendor, catalog


def get_order_from_customer(customer):
    orders = customer.orders
    if orders:
        for order in orders:
            if not order.is_confirmed:
                return order
    order = Order(customer.psid, customer.page_id)
    return order


def send_order_to_vendor(result, fcm_token):
    # orders_schema = OrderSchema()
    # order = orders_schema.dump(result)
    # print(order)
    # data = []
    # info = {}
    # info['customer'] = order['customer']
    # info['time'] = order['time']
    # info['number'] = order['number']
    # info['price'] = order['price']
    # info['status'] = order['status']
    # data.append(info)
    # print(data)
    try:
        app = firebase_admin.get_app()
    except ValueError as e:
        cred = credentials.Certificate("serviceAccountKey.json")
        firebase_admin.initialize_app(cred)
    msg = messaging.Message(data={'message': 'New Order'}, token=fcm_token)
    msg_id = messaging.send(msg)
    return msg_id


def get_comment_from_feed(data):
    return data["entry"][0]["changes"][0]["value"]["message"]


def ask_wit(msg, page_id):
    client = Wit('GQ4J2DTDIZSTOFHZ744JOP5MWXKWQCX2')
    response = client.message(msg)
    print(response)
    if response['intents'] == []:
        return False
    intent = response['intents'][0]
    knowledge = Catalog.find_by_page_id(
        page_id).knowledge['comments']['values']
    print(msg)
    print(knowledge)
    print(intent)
    if intent['confidence'] > 0.55:
        for q in knowledge:
            if q['key'] == intent:
                print(q)
                return q['value']
    return False
