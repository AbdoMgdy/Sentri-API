from copy import deepcopy as copy
from models.bot import Bot

template = {
    "template_type": "receipt",
    "value": {
        "attachment": {
            "type": "template",
            "payload": {
                "template_type": "receipt",
                "recipient_name": "",
                "order_number": "",
                "currency": "",
                "payment_method": ""
            }
        }
    }
}


class ReceiptTemplate(Bot):
    def __init__(self, recipient_name='', order_number='', timestamp='', order_url=''):
        super().__init__()
        self.template = copy(template['value'])
        self.template['attachment']['payload']['recipient_name'] = recipient_name
        self.template['attachment']['payload']['order_number'] = order_number
        self.template['attachment']['payload']['currency'] = 'EGP'
        self.template['attachment']['payload']['payment_method'] = 'Cash On Deleivery'
        if timestamp != '':
            self.template['attachment']['payload']['timestamp'] = timestamp
        if order_url != '':
            self.template['attachment']['payload']['order_url'] = order_url
        self.elements = []
        self.address = {}
        self.summary = {}
        self.adjustments = []

    def add_element(self, title='', subtitle='', quantity=-1, price=0, image_url=''):
        element = {}
        element['title'] = title
        if subtitle != '':
            element['subtitle'] = subtitle
        if quantity != -1:
            element['quantity'] = int(quantity)
        element['price'] = price
        element['currency'] = 'EGP'
        if image_url != '':
            element['image_url'] = image_url
        self.elements.append(element)
        self.template['attachment']['payload']['elements'] = self.elements

    def set_address(self, street_1='', street_2='', city='', postal_code='', state='', country=''):
        self.address['street_1'] = street_1
        if street_2 != '':
            self.address['street_2'] = street_2
        self.address['city'] = city
        self.address['postal_code'] = postal_code
        self.address['state'] = state
        self.address['country'] = country
        self.template['attachment']['payload']['address'] = self.address

    def set_summary(self, subtotal=-1, shipping_cost=-1, total_tax=-1, total_cost=0):
        if subtotal != -1:
            self.summary['subtotal'] = subtotal
        if shipping_cost != -1:
            self.summary['shipping_cost'] = shipping_cost
        if total_tax != -1:
            self.summary['total_tax'] = total_tax
        self.summary['total_cost'] = total_cost
        self.template['attachment']['payload']['summary'] = self.summary

    def add_adjustment(self, name='', amount=0):
        adjustment = {}
        adjustment['name'] = name
        adjustment['amount'] = amount
        self.adjustments.append(adjustment)
        self.template['attachment']['payload']['adjustments'] = self.adjustments

    def get_receipt(self):
        self.template['attachment']['payload']['elements'] = self.elements
        if self.address != {}:
            self.template['attachment']['payload']['address'] = self.address
        self.template['attachment']['payload']['summary'] = self.summary
        if self.adjustments != []:
            self.template['attachment']['payload']['adjustments'] = self.adjustments
        return self.template
