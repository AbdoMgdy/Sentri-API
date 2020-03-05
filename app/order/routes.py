from flask import Blueprint, render_template, request, send_file
from flask_jwt_extended import (
    jwt_required, create_access_token,
    get_jwt_identity
)
from app.resources.buttons import confirm_block
from app.models.forms import OrderForm, OrderSandwich, OrderSauce, OrderMeal, CustomerInfo
from app.models.data_models import Order, OrderSchema, Customer, CustomerSchema, Vendor, VendorSchema
import json
from app.models.bot import Bot
from datetime import datetime
import app.resources.helper_functions as helper
import ast
# Set up a Blueprint
order_bp = Blueprint('order_bp', __name__,
                     template_folder='templates',)
