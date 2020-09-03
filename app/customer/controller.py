from flask import jsonify, request
from flask_restx import Resource, Namespace, reqparse

from .model import Customer
from app.order.model import Order
from app.order.schema import OrderSchema
from app.vendor.model import Vendor
from app.models.bot import Bot
import app.resources.helper_functions as helper
from app.models.receipt import ReceiptTemplate
from app.resources.buttons import confirm_block
api = Namespace('Customer')


@api.route('/<string:psid>')
class CustomerResource(Resource):
    def get(self, psid):
        pass

    def post(self, psid):
        # look for customer
        customer = Customer.find_by_psid(psid)
        vendor = customer.vendor
        catalog = vendor.catalog
        knowledge = catalog.knowledge
        bot = Bot(access_token=vendor.page_access_token)
        order = helper.get_order_from_customer(customer)
        print(order)
        if order.is_confirmed:
            print('Order is Confirmed')
            return 'Order is Confirmed', 200
        # update customer info
        customer.name = request.form.get('name')
        customer.phone_number = request.form.get('phone_number')
        customer.address = request.form.get('address')
        customer.save()  # imp
        # make a receipt
        receipt = ReceiptTemplate(
            recipient_name=customer.name, order_number=order.number)

        for item in order.items:
            # fill receipt with order from database
            receipt.add_element(
                title=item['name'], quantity=item['quantity'], price=item['price'])
        receipt.set_summary(total_cost=order.price)
        print(receipt.get_receipt())
        print(bot.send_template_message(
            psid, {'payload': receipt.get_receipt()}))
        bot.send_text_message(
            psid, knowledge['browse']['values']['Order_Confirmation_Message'])
        order.confirm()  # imp
        msg_id = helper.send_order_to_vendor(order, vendor.fcm_token)
        print(msg_id)
        return 'Customer info was added', 200


@api.route('/order/<string:psid>')
class CustomerOrderInfoResource(Resource):

    def get(self, psid):
        customer = Customer.find_by_psid(psid)
        vendor = customer.vendor
        bot = Bot(access_token=vendor.page_access_token)
        order = helper.get_order_from_customer(customer)
        output = OrderSchema.dump(order)
        return jsonify(output), 200
