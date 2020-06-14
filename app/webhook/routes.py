from flask import Blueprint, render_template, request
import json
from datetime import datetime
import ast
from app.models.bot import Bot
import app.resources.helper_functions as helper
# Set up a Blueprint
webhook_bp = Blueprint('webhook_bp', __name__,
                       template_folder='templates',
                       static_folder='static')

VERIFICATION_TOKEN = 'test'


@webhook_bp.route('/webhook', methods=['GET'])
def verify():
    if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.challenge"):
        if not request.args.get("hub.verify_token") == VERIFICATION_TOKEN:
            return "Verification token mismatch", 403
        return request.args["hub.challenge"], 200
    return "Hello world", 200


@webhook_bp.route('/webhook', methods=['POST'])
def handle_incoming_messages():
    data = request.get_json()
    print(data)
    webhook_type = helper.get_type_from_payload(data)
    page_id = helper.get_vendor_from_message(data)
    vendor = helper.handle_vendor(page_id)[0]
    catalog = helper.handle_vendor(page_id)[1]
    blocks = catalog.blocks
    bot = Bot(access_token=vendor.page_access_token)
    sender_id = helper.get_customer_from_message(data)
    customer = helper.handle_customer(sender_id, page_id)
    print(sender_id)
    print(webhook_type)
    bot.send_before_message(sender_id)
    # if not vendor.is_open():
    #     bot.send_text_message(
    #         sender_id, 'المطعم مغلق حاليا \nالرجاء المحاولة مرة أخرى خلال مواعيد العمل الرسمية من {} الى {}'.format(vendor.opening_hours.strftime('%H:%M'), vendor.closing_hours.strftime('%H:%M')))
    #     return 'Vendor is Closed', 200
    if webhook_type == "text":
        # HANDLE TEXT MESSAGES HERE
        bot.send_before_message(sender_id)

        block = blocks['get_started']
        print(bot.send_template_message(sender_id, block))
        return "text", 200

    elif webhook_type == "quick_reply":
        # HANDLE QUICK REPLIES HERE
        bot.send_before_message(sender_id)
        block_name = helper.quick_replies_events(data)
        if block_name in blocks:
            block = blocks[block_name]
            print(block)
            # bot.send_template_message(sender_id, block)
            print(bot.send_template_message(sender_id, block))

        return "quick_reply", 200

    elif webhook_type == "postback":
        # HANDLE POSTBACK HERE
        bot.send_before_message(sender_id)
        block_name = helper.postback_events(data)
        if block_name in blocks:

            block = blocks[block_name]
            print(block)
            # bot.send_template_message(sender_id, block)
            print(bot.send_template_message(sender_id, block))

        return "postback", 200
    else:
        return "ok", 200
    return "ok", 200


ACCESS_TOKEN = 'EAAJMYpx9YFkBAHPGjj1FWtZAfiwGZAZAD7igxPIlYX5INZANePO3B7X4vKZBF4rZAqWPnMTyfSuMTtjZAxK2SfFrjNcPr7gxlba2cEvdtUU1BtpPULEpBkpAfoFeqL2aRitAqZBlJypP50ArG6ISZA5ISM5sVZCFQhhtpxZCIOJ0y8st93bopRx6n0smn0i9jpZByY8ZD'


@webhook_bp.route('/webhook/car', methods=['POST'])
def handle_incoming_messages_car():
    data = request.get_json()
    print(data)
    webhook_type = helper.get_type_from_payload(data)
    page_id = helper.get_vendor_from_message(data)
    bot = Bot(access_token=ACCESS_TOKEN)
    sender_id = helper.get_customer_from_message(data)
    blocks = car_blocks
    print(sender_id)
    print(webhook_type)
    bot.send_before_message(sender_id)
    if webhook_type == "text":
        # HANDLE TEXT MESSAGES HERE
        bot.send_before_message(sender_id)
        block = blocks['get_started']
        print(bot.send_template_message(sender_id, block))
        return "text", 200

    elif webhook_type == "quick_reply":
        # HANDLE QUICK REPLIES HERE
        bot.send_before_message(sender_id)
        block_name = helper.quick_replies_events(data)

        if block_name in blocks:
            block = blocks[block_name]
            print(bot.send_template_message(sender_id, block))

        return "quick_reply", 200

    elif webhook_type == "postback":
        # HANDLE POSTBACK HERE
        bot.send_before_message(sender_id)
        block_name = helper.postback_events(data)

        if block_name in blocks:
            block = blocks[block_name]
            print(bot.send_template_message(sender_id, block))

        return "postback", 200
    else:
        return "ok", 200
    return "ok", 200


car_blocks = {
    'info': {
        'payload': {'teplate_type': 'button',
                    'text': """ العنوان:50 حسن المأمون - مدينة نصر
        التليفون لخدمات الدليفيري والتوصيل: 16920  """,
                    'buttons': [{
                            'type': 'postback',
                            'title': 'المنيو',
                            'payload': 'main_menu'
                    }],
                    }
    },
    'get_started': {
        'payload': {
            'template_type': 'generic',
            'elements': [
                {
                    'title': """مرحبا بك
                     انا مساعدك الافتراضي كيف أستطيع مساعدتك؟""",
                    'buttons': [{
                        'type': 'postback',
                        'title': 'الخدمات المتاحة',
                        'payload': 'main_menu'
                    },
                        {
                        'type': 'postback',
                            'title': 'العنوان/التليفون',
                            'payload': 'info'
                    }]

                }
            ]
        },
        'qucik_replies': [
            {
                'content_type': 'text',
                'title': 'الخدمات المتاحة',
                'payload': 'sub-menu-1',
            }
        ]
    },
    'main_menu': {
        'payload': {
            'template_type': 'generic',
            'elements': [
                {
                    'title': 'خدمة التقسيط',
                    'image_url': 'https://www.unoragetours.com/wp-content/uploads/2019/10/911-road-3629a.jpg',
                    'subtitle': '',
                    'buttons': [{
                        'type': 'postback',
                        'title': 'عرض الخدمة',
                        'payload': 'sub-menu-1'
                    }]
                },
            ]
        }
    },
    'sub-menu-1': {
        'payload': {
            'template_type': 'generic',
            'elements': [
                {
                    'title': 'التقديم على قسط سيارة',

                    'buttons': [{
                        'type': 'web_url',
                        'title': 'اختار',
                        'url': 'https://rest-bot-dev.herokuapp.com/webview/car',
                        'webview_height_ratio': 'tall',
                        'messenger_extensions': 'true'
                    }]
                },
            ]
        }
    },
    'sub-menu-2': {
        'payload': {
            'template_type': 'generic',
            'elements': [
                {
                    'title': 'اضافة شطة',
                    'image_url': 'https://scontent-hbe1-1.xx.fbcdn.net/v/t1.0-9/p960x960/80390516_2962955900382554_7936731969642037248_o.jpg?_nc_cat=108&_nc_ohc=68iQXp-Lxn0AX9pBDCk&_nc_ht=scontent-hbe1-1.xx&_nc_tp=6&oh=f886d8238a13919294e79f9bfb70fa0b&oe=5EFDAE46',
                    'subtitle': '',
                    'buttons': [{
                        'type': 'web_url',
                        'title': 'اطلب بـ5ج',
                        'url': 'https://rest-bot-dev.herokuapp.com/webview/order/type-1/Hot-Sauce',
                        'webview_height_ratio': 'tall',
                        'messenger_extensions': 'true'
                    }]
                },
                {
                    'title': 'اضافة تقلية',
                    'image_url': 'https://scontent-hbe1-1.xx.fbcdn.net/v/t1.0-9/p960x960/80390516_2962955900382554_7936731969642037248_o.jpg?_nc_cat=108&_nc_ohc=68iQXp-Lxn0AX9pBDCk&_nc_ht=scontent-hbe1-1.xx&_nc_tp=6&oh=f886d8238a13919294e79f9bfb70fa0b&oe=5EFDAE46',
                    'subtitle': '',
                    'buttons': [{
                        'type': 'web_url',
                        'title': 'اطلب بـ5ج',
                        'url': 'https://rest-bot-dev.herokuapp.com/webview/order/type-1/Fired-Onions',
                        'webview_height_ratio': 'tall',
                        'messenger_extensions': 'true'
                    }]
                },
                {
                    'title': 'أرز باللبن',
                    'image_url': 'https://scontent-hbe1-1.xx.fbcdn.net/v/t1.0-9/p960x960/80390516_2962955900382554_7936731969642037248_o.jpg?_nc_cat=108&_nc_ohc=68iQXp-Lxn0AX9pBDCk&_nc_ht=scontent-hbe1-1.xx&_nc_tp=6&oh=f886d8238a13919294e79f9bfb70fa0b&oe=5EFDAE46',
                    'subtitle': '',
                    'buttons': [{
                        'type': 'web_url',
                        'title': 'اطلب بـ10ج',
                        'url': 'https://rest-bot-dev.herokuapp.com/webview/order/type-1/Milk-Rice',
                        'webview_height_ratio': 'tall',
                        'messenger_extensions': 'true'
                    }]
                },
            ]
        },

        'quick_replies': [
            {
                'content_type': 'text',
                'title': 'العودة للخلف',
                'payload': 'main_menu',
            }
        ],
    },
}
