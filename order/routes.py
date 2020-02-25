from flask import Blueprint, render_template, request, send_file
from flask_jwt_extended import (
    jwt_required, create_access_token,
    get_jwt_identity
)
from resources.buttons import confirm_block
from models.forms import OrderForm, OrderSandwich, OrderSauce, OrderMeal, CustomerInfo
from models.data_models import Order, OrderSchema, Customer, CustomerSchema, Vendor, VendorSchema
import json
from models.bot import Bot
from datetime import datetime
import resources.helper_functions as helper
import ast
# Set up a Blueprint
order_bp = Blueprint('order_bp', __name__,
                     template_folder='templates',
                     static_folder='static')


@order_bp.route('/webview/order/<string:food>/<string:item>', methods=['GET'])
def show_webview(food, item):
    if food == "type-1":
        order = OrderForm()
        return render_template('order.jinja', food="sandwich", item=item, form=order)
    if food == "sandwich":
        sandwich = OrderSandwich()
        return render_template('order sandwich.jinja', food="sandwich", item=item, form=sandwich)
    elif food == "meal":
        meal = OrderMeal()
        return render_template('order meal.jinja', food="meal", item=item, form=meal)
    elif food == "sauce":
        sauce = OrderSauce()
        return render_template('order sauce.jinja', food="sauce", item=item, form=sauce)


@order_bp.route('/user/<string:sender_id>/add_to_order/<string:food>/<string:item>/', methods=['GET', 'POST'])
def add_to_order(sender_id, food, item):
    customer = Customer.find_by_psid(sender_id)
    vendor = customer.vendor
    prices = vendor.prices
    arabic = vendor.arabic
    bot = Bot(access_token=vendor.access_token)
    # save unconfirmed orders in dict
    order_item = {}
    order_item['quantity'] = request.form.get('quantity')
    if request.form.get('spicy') is not None:
        order_item['type'] = request.form.get('spicy')
    if request.form.get('notes') is not None:
        order_item['notes'] = request.form.get('notes')
    if request.form.get('combo') is None:
        order_item['combo'] = 0
    elif request.form.get('combo') is not None:
        order_item['combo'] = request.form.get('combo')
    order_item['category'] = food
    order_item['name'] = item
    order_item['price'] = prices[item]

    helper.update_order(sender_id, order_item)

    if order_item['type'] in arabic:
        text = '{} * {} {} تمت اضافته للأوردو الخاص بك'.format(order_item['quantity'],
                                                               arabic[item], arabic[order_item['type']])
    else:
        text = '{} * {} {} تمت اضافته للأوردو الخاص بك'.format(order_item['quantity'],
                                                               arabic[item], order_item['type'])
    confirm_block.set_text(text)
    bot.send_template_message(
        sender_id, {'payload': confirm_block.get_template()})
    return 'Item added to Order', 200


@order_bp.route('/edit_order', methods=['GET'])
def edit_order():
    return send_file('edit_order.html')


@order_bp.route('/confirm_order', methods=['GET'])
def confirm_order():
    form = CustomerInfo()
    return render_template('user info.jinja', form=form)  # take user info


@order_bp.route('/edit_order_status', methods=['POST'])
def edit_order_status():
    print(request.form.get('order_status'))
    print(request.form.get('order_number'))
    order = Order.find_by_number(request.form.get('order_number'))
    if order:
        order.edit(request.form.get('order_status'))
        order.save()
    return 'Order Stauts was edited', 200
