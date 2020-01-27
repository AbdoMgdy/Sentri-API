from models.bot import Bot
import json

TEXT_CHARACTER_LIMIT = 640
QUICK_REPLIES_LIMIT = 11
TITLE_CHARACTER_LIMIT = 20
PAYLOAD_CHARACTER_LIMIT = 1000
TITLE_CHARACTER_LIMIT = 80
SUBTITLE_CHARACTER_LIMIT = 80
BUTTON_TITLE_CHARACTER_LIMIT = 20
BUTTON_LIMIT = 3
ELEMENTS_LIMIT = 10

template = {
    'template_type': 'text',
    'value': {
        'text': ''
    }
}


class TextTemplate(Bot):
    def __init__(self, text='', post_text='', limit=TEXT_CHARACTER_LIMIT):
        super().__init__()
        self.template = template['value']
        self.text = text
        self.post_text = post_text
        self.limit = limit
        self.quick_replies = []

    def set_text(self, text=''):
        self.text = text

    def set_post_text(self, post_text=''):
        self.post_text = post_text

    def set_limit(self, limit=TEXT_CHARACTER_LIMIT):
        self.limit = limit

    def get_message(self):
        n = self.limit - len(self.post_text)
        if n > len(self.text):
            self.template['text'] = self.text + self.post_text
        else:
            # append ellipsis (length = 3)
            self.template['text'] = self.text[:n -
                                              3].rsplit(' ', 1)[0] + '...' + self.post_text
        return self.template

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

    def send(self, reciepiant_id):
        super().send_text_message(reciepiant_id,
                                  self.text, quick_replies=self.quick_replies)
