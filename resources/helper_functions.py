from resources.dicts import blocks, orders
from models.data_models import Customer, Vendor
from models.bot import Bot


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
    orders[sender_id] = []
    return new_customer


def handle_current_customer(sender_id):
    current_customer = Customer.find_by_psid(sender_id)
    if sender_id in orders:
        pass
    else:
        orders[sender_id] = []
    return current_customer


def handle_customer(sender_id, vendor):
    customer = Customer.find_by_psid(sender_id)
    if customer is None:
        customer = handle_first_time_customer(sender_id, vendor)
    elif customer and len(customer.orders) > 0:
        customer = handle_current_customer(sender_id)
    return customer


def handle_first_time_vendor(page_id, access_token):
    new_vendor = Vendor(page_id=page_id, access_token=access_token)
    new_vendor.menu = blocks
    bot = Bot(access_token)
    bot.
    new_vendor.save()
    return new_vendor


def handle_current_vendor(page_id, access_token):
    current_vendor = Vendor.find_by_page_id(page_id)
    current_vendor.access_token = access_token
    return current_vendor


def handle_vendor(page_id, access_token):
    vendor = Vendor.find_by_page_id(page_id)
    if vendor is None:
        vendor = handle_first_time_vendor(page_id, access_token)
    else:
        vendor = handle_current_vendor(page_id, access_token)
    return vendor


def update_order(sender_id, item):
    if sender_id in orders:
        orders[sender_id].append(item)
    else:
        orders[sender_id] = []
        orders[sender_id].append(item)
