from flask import jsonify, request
from flask_restx import Resource, Namespace, reqparse
# from flask_jwt_extended import (
#     jwt_required, create_access_token,
#     get_jwt_identity
# )
from .model import Order
from .schema import OrderSchema
from app.customer.model import Customer
from app.vendor.model import Vendor
from app.models.bot import Bot
from app.resources.buttons import confirm_block
api = Namespace('Order')


@api.route('/<string:order_number>')
class OrderResourceByNumber(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('order_status')

    def get(self):
        pass

    def post(self):
        pass

    def put(self, order_number):
        args = self.parser.parse_args()
        print(args)
        print(order_number)
        order = Order.find_by_number(order_number)
        if order:
            try:
                order.update({'status': request.form.get('order_status')})
                order.save()
                return 'Order Status was edited', 200
            except Exception as e:
                raise e
        return 'Order Not Found', 404

    def delete(self, order_number):
        order = Order.find_by_number(order_number)
        if order:
            try:
                order.delete()
                return 'Oder was Deleted', 200
            except Exception as e:
                raise e
        return 'Order Not Found', 404


@api.route('/<string:psid>')
class OrderResourceByPsid(Resource):
    def get(self, psid):
        order = Order.query.filter_by(psid=psid, is_confirmed=False)
        if order:
            output = OrderSchema.dump(order)
            return jsonify(output)
        else:
            return 'Customer not found', 404


@api.route('/item/<string:sender_id>/<string:category>/<string:item>/')
class OrderItem(Resource):
    def get(self):
        pass

    def post(self, sender_id, category, item):
        customer = Customer.find_by_psid(sender_id)
        vendor = customer.vendor
        prices = vendor.prices
        arabic = vendor.arabic
        order = Order.query.filter_by(
            psid=sender_id, is_confirmed=False).first()
        if order is None:
            order = Order(sender_id, vendor.page_id)
        bot = Bot(access_token=vendor.access_token)
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
        order_item['category'] = category
        order_item['name'] = item
        order_item['price'] = prices[item]

        order.add_item(order_item)

        if 'type' in order_item:
            text = '{} * {} {} تمت اضافته للأوردو الخاص بك'.format(order_item['quantity'],
                                                                   arabic[item], arabic[order_item['type']])
        else:
            text = '{} * {} تمت اضافته للأوردو الخاص بك'.format(order_item['quantity'],
                                                                arabic[item])
        confirm_block.set_text(text)
        bot.send_template_message(
            sender_id, {'payload': confirm_block.get_template()})
        return 'Item added to Order', 200

        def put(self, sender_id):
            customer = Customer.find_by_psid(sender_id)
            vendor = Vendor.find_by_page_id(customer.page_id)
            bot = Bot(access_token=vendor.access_token)
            order = Order.query.filter_by(psid=sender_id, is_confirmed=False)
            data = request.get_json()
            print(data)
            if not data['items']:
                bot.send_text_message(sender_id, 'انت لم تطلب شيء بعد!')
                order.update({'items', []})
                return 'Order is empty', 200
            order.update({'items': data['items']})
            confirm_block.set_text('تم تعديل الأوردر الخاص بك')
            bot.send_template_message(
                sender_id, {'payload': confirm_block.get_template()})
            return 'Order Updated', 200
