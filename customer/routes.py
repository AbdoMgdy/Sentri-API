import requests
from flask import Blueprint, render_template, request, redirect
from flask_jwt_extended import (
    jwt_required, create_access_token,
    get_jwt_identity
)
from models.bot import Bot
from models.receipt import ReceiptTemplate
from models.data_models import Order, OrderSchema, Customer, CustomerSchema, Vendor, VendorSchema
import json
from datetime import datetime
import ast
from resources.dicts import orders
from resources.buttons import confirm_block
# Set up a Blueprint
customer_bp = Blueprint('customer_bp', __name__,
                        template_folder='templates',
                        static_folder='static')


@customer_bp.route('/user/<string:sender_id>/order_info', methods=['GET'])
def post_order_info(sender_id):
    if sender_id in orders:
        return json.dumps(orders[sender_id]), 200
    else:
        return 'Customer not found', 404


@customer_bp.route('/user/<string:sender_id>/edit_order', methods=['POST'])
def get_order_info(sender_id):
    customer = Customer.find_by_psid(sender_id)
    vendor = Vendor.find_by_page_id(customer.page_id)
    bot = Bot(access_token=vendor.access_token)
    data = request.get_json()
    print(data)
    if not data['items']:
        bot.send_text_message(sender_id, 'انت لم تطلب شيء بعد!')
        result = orders.pop(sender_id, None)  # remove order from temp dict
        return 'Order is empty', 200
    if sender_id in orders:
        orders[sender_id] = data['items']
    confirm_block.set_text('تم تعديل الأوردر الخاص بك')
    bot.send_template_message(
        sender_id, {'payload': confirm_block.get_template()})
    return 'ok', 200
