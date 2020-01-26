import os
import ast
from flask import Flask, request, render_template
from flask_restful import Resource, Api
from models.data_models import Order, OrderSchema, User, UserSchema
from models.receipt import ReceiptTemplate
import json
from models.bot import Bot
from forms import OrderSandwich, OrderMeal, OrderSauce, SignUpForm
from tables import Results, Items
from resources.buttons import confirm_block
from resources.menu import main_menu, family_menu
from resources.helper_functions import get_type_from_payload, get_user_from_message, handle_current_user, handle_first_time_user, quick_replies_events, postback_events
from resources.dicts import blocks, orders


bot = Bot

VERIFICATION_TOKEN = "test"


class MessageHandler(Resource):
    def get(self):
        if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.challenge"):
            if not request.args.get("hub.verify_token") == VERIFICATION_TOKEN:
                return "Verification token mismatch", 403
            return request.args["hub.challenge"], 200
        return "Hello world", 200

    def post(self):
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
            canceld_order = orders.pop(sender_id, None)
            print(canceld_order)
            if canceld_order is None:
                bot.send_text_message(sender_id, 'cant cancel confirmed order')
            else:
                bot.send_text_message(sender_id, 'cant cancel confirmed order')
        elif webhook_type == "postback":
            # HANDLE POSTBACK HERE
            bot.send_before_message(sender_id)
            block_name = postback_events(data)
            block = blocks[block_name]
            block.send(sender_id)
            return "postback", 200
        return "ok", 200
