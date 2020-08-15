from flask import Blueprint, render_template, request
import json
from datetime import datetime
import ast
from app.models.bot import Bot
import app.resources.helper_functions as helper
from facebook import GraphAPI

# Set up a Blueprint
webhook_bp = Blueprint('webhook_bp', __name__,
                       template_folder='templates',
                       static_folder='static')

VERIFICATION_TOKEN = 'test'


@webhook_bp.route('/webhook', methods=['GET'])
def verify():
    if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.challenge"):
        if not request.args.get("hub.verify_token") == VERIFICATION_TOKEN:
            return "Verification token mismatch", 403
        return request.args["hub.challenge"], 200
    return "Hello world", 200


@webhook_bp.route('/webhook', methods=['POST'])
def handle_incoming_messages():
    data = request.get_json()
    print(data)
    request_type = helper.get_type_from_payload(data)
    if request_type == "messaging":
        return handle_messaging(data)
    elif request_type == "changes":
        return handle_page_feed(data)


def handle_page_feed(data):
    page_id = helper.get_vendor_from_comment(data)
    vendor = helper.handle_vendor(page_id)[0]
    graph = GraphAPI(access_token=vendor['access_token'])
    comment = helper.get_comment_from_feed(data)
    reply = helper.ask_wit(comment, page_id)
    if reply:
        graph.put_comment(object_id=comment['id'],
                          message=reply)
        print('Replied to Comment')
    return 'Replied to Comment', 200


def handle_messaging(data):
    message_type = helper.get_type_from_message(data)
    page_id = helper.get_vendor_from_message(data)
    vendor = helper.handle_vendor(page_id)[0]
    catalog = helper.handle_vendor(page_id)[1]
    blocks = catalog.blocks
    bot = Bot(access_token=vendor.page_access_token)
    sender_id = helper.get_customer_from_message(data)
    customer = helper.handle_customer(sender_id, page_id)
    print(sender_id)
    print(message_type)
    if not vendor.check_customer_limit:
        bot.send_text_message(
            sender_id, 'You have reached the Maximum Customer limit for you tier.')
        return 'Customer Limit', 200
    # if not vendor.is_open():
    #     bot.send_text_message(
    #         sender_id, 'المطعم مغلق حاليا \nالرجاء المحاولة مرة أخرى خلال مواعيد العمل الرسمية من {} الى {}'.format(vendor.opening_hours.strftime('%H:%M'), vendor.closing_hours.strftime('%H:%M')))
    #     return 'Vendor is Closed', 200
    if message_type == "text":
        # HANDLE TEXT MESSAGES HERE
        bot.send_before_message(sender_id)

        block = blocks['get_started']
        print(bot.send_template_message(sender_id, block))
        return "text", 200

    elif message_type == "quick_reply":
        # HANDLE QUICK REPLIES HERE
        bot.send_before_message(sender_id)
        block_name = helper.quick_replies_events(data)
        if block_name in blocks:
            block = blocks[block_name]
            print(block)
            # bot.send_template_message(sender_id, block)
            print(bot.send_template_message(sender_id, block))

        return "quick_reply", 200

    elif message_type == "postback":
        # HANDLE POSTBACK HERE
        bot.send_before_message(sender_id)
        block_name = helper.postback_events(data)
        if block_name in blocks:

            block = blocks[block_name]
            print(block)
            # bot.send_template_message(sender_id, block)
            print(bot.send_template_message(sender_id, block))

        return "postback", 200
    else:
        return "ok", 200
    return "ok", 200
