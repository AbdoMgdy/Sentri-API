import requests
from flask import Blueprint, render_template, request, redirect
from flask_jwt_extended import (
    jwt_required, create_access_token,
    get_jwt_identity
)
from app.models.data_models import Order, OrderSchema, Customer, CustomerSchema, Vendor, VendorSchema
import json
from datetime import datetime
import ast
# Set up a Blueprint
vendor_bp = Blueprint('vendor_bp', __name__,
                      template_folder='templates',
                      static_folder='static')

# For Comments
# @vendor_bp.route('/vendors', methods=['GET'])
# def vendors():
#     vendors = Vendor.query.all()
#     vendor_schema = VendorSchema(many=True)
#     output = vendor_schema.dump(vendors)
#     return json.dumps(output)
