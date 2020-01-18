import json
from models.bot import Bot


TEXT_CHARACTER_LIMIT = 640


class ButtonTemplate(Bot):
    def __init__(self):
        self.text = ''
        self.buttons = []
        self.quick_replies = []

    def set_text(self, text):
        self.text = text

    def add_web_url(self, **kwargs):
        for title, url in kwargs.items():
            web_url_button = {}
            web_url_button['type'] = 'web_url'
            web_url_button['url'] = url
            web_url_button['title'] = title
            web_url_button['webview_height_ratio'] = 'tall'
            web_url_button['messenger_extensions'] = 'true'
            self.buttons.append(web_url_button)

    def add_postback(self, **kwargs):
        # pass post back buttons as **dict
        for title, payload in kwargs.items():
            postback_button = {}
            postback_button['type'] = 'postback'
            postback_button['title'] = title
            postback_button['payload'] = json.dumps(payload)
            self.buttons.append(postback_button)

    def send(self, reciepiant_id):
        super().send_button_message(reciepiant_id,
                                    self.text, self.buttons, self.quick_replies)
