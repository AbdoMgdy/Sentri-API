from flask import Blueprint, render_template, request, send_file
import json
from datetime import datetime
import ast
from app.models.bot import Bot
from app.models.forms import CustomerInfo, OrderForm, OrderSandwich, OrderMeal, OrderSauce, RegistrationForm
import app.resources.helper_functions as helper
# Set up a Blueprint
webview_bp = Blueprint('webview_bp', __name__,
                       template_folder='templates',
                       static_folder='static')


@webview_bp.route('/edit_order', methods=['GET'])
def edit_order():
    return send_file('edit_order.html')


@webview_bp.route('/confirm_order', methods=['GET'])
def confirm_order():
    form = CustomerInfo()
    return render_template('user info.jinja', form=form)  # take user info


@webview_bp.route('/webview/order/<string:item_id>', methods=['GET'])
def show_webview(item_id):
    order = OrderForm()
    return render_template('order.jinja', food="sandwich", item_id=item_id, form=order)
