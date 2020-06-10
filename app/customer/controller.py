from flask import jsonify, request
from flask_restx import Resource, Namespace, reqparse

from .model import Customer
from app.order.model import Order
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
        bot = Bot(access_token=vendor.page_access_token)
        order = helper.get_order_from_customer(customer)

        print(order)
        if not vendor.is_open():
            bot.send_text_message(psid,
                                  'الرجاء المحاولة مرة أخري خلال مواعيد العمل الرسمية')
            return 'Vendor is Closed', 200
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
            psid, 'يتم الآن تحضير الأوردر وسيصلك في خلال 45 - 60 دقيقة')
        order.confirm()  # imp
        msg_id = helper.send_order_to_vendor(order, vendor.fcm_token)
        print(msg_id)
        return 'Customer info was added', 200


@api.route('/car/<string:psid>')
class CarCustomer(Resource):
    def post(self, psid):
        data = (request.get_json())
        print(data)
        bot = Bot(access_token=ACCESS_TOKEN)
        bot.send_text_message(psid, 'تم تسجيل بياناتك')
        return 'ok', 200


ACCESS_TOKEN = 'EAAJMYpx9YFkBAHPGjj1FWtZAfiwGZAZAD7igxPIlYX5INZANePO3B7X4vKZBF4rZAqWPnMTyfSuMTtjZAxK2SfFrjNcPr7gxlba2cEvdtUU1BtpPULEpBkpAfoFeqL2aRitAqZBlJypP50ArG6ISZA5ISM5sVZCFQhhtpxZCIOJ0y8st93bopRx6n0smn0i9jpZByY8ZD'


"""
{
    'psid':[{},{},{}]
}
"""
