from resources.dicts import blocks, orders
from models.data_models import User


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


def handle_user(sender_id):
    user = User.find_by_psid(sender_id)
    if user is None:
        user = handle_first_time_user(sender_id)
        print('new user {}'.format(user.psid))
    elif user and len(user.orders) > 0:
        user = handle_current_user(sender_id)
        print('current user {}'.format(user.psid))
    return user


def update_order(sender_id, item):
    if sender_id in orders:
        orders[sender_id].append(item)
    else:
        orders[sender_id] = []
        orders[sender_id].append(item)
