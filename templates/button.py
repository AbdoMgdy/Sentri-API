import json
from copy import deepcopy as copy


TEXT_CHARACTER_LIMIT = 640

template = {
    'template_type': 'button',
    'value': {
        'attachment': {
            'type': 'template',
            'payload': {
                'template_type': 'button',
                'text': '',
                'buttons': []
            }
        }
    }
}


class ButtonTemplate:
    def __init__(self):
        self.buttons = []

    def add_web_url(self, title='', url=''):
        web_url_button = {}
        web_url_button['type'] = 'web_url'
        web_url_button['title'] = title
        web_url_button['url'] = url
        self.buttons.append(web_url_button)

    def add_postback(self, title='', payload=''):
        postback_button = {}
        postback_button['type'] = 'postback'
        postback_button['title'] = title
        postback_button['payload'] = json.dumps(payload)
        self.buttons.append(postback_button)

