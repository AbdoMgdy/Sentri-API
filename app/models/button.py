import json


QUICK_REPLIES_LIMIT = 11
TITLE_CHARACTER_LIMIT = 20
PAYLOAD_CHARACTER_LIMIT = 1000
TITLE_CHARACTER_LIMIT = 80
SUBTITLE_CHARACTER_LIMIT = 80
BUTTON_TITLE_CHARACTER_LIMIT = 20
BUTTON_LIMIT = 3


class ButtonTemplate():
    def __init__(self):

        self.template = {
            'template_type': 'button'
        }
        self.text = ''
        self.buttons = []
        self.quick_replies = []

    def set_text(self, text):
        self.text = text

    def set_vendor(self, page_id):
        self.template['buttons'][0]['url'] = 'https://rest-bot-dev.herokuapp.com/{}/confirm_order'.format(
            page_id)
        self.template['buttons'][2]['url'] = 'https://rest-bot-dev.herokuapp.com/{}/edit_url'.format(
            page_id)

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

    def add_quick_replies(self, **kwargs):
        for title, paylod in kwargs.items():
            if len(self.quick_replies) < QUICK_REPLIES_LIMIT:
                quick_reply = {}
                # TODO: location + image_url
                quick_reply['content_type'] = 'text'
                quick_reply['title'] = title[:TITLE_CHARACTER_LIMIT]
                quick_reply['payload'] = json.dumps(
                    paylod)[:PAYLOAD_CHARACTER_LIMIT]
                self.quick_replies.append(quick_reply)

    def get_template(self):
        self.template['text'] = self.text
        self.template['buttons'] = self.buttons
        return self.template
