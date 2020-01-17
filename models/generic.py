from models.bot import Bot
import json


QUICK_REPLIES_LIMIT = 11
TITLE_CHARACTER_LIMIT = 20
PAYLOAD_CHARACTER_LIMIT = 1000
TITLE_CHARACTER_LIMIT = 80
SUBTITLE_CHARACTER_LIMIT = 80
BUTTON_TITLE_CHARACTER_LIMIT = 20
BUTTON_LIMIT = 3
ELEMENTS_LIMIT = 10


class GenericTemplate(Bot):
    def __init__(self):
        super().__init__()
        self.elements = []
        self.quick_replies = []

    def add_element(self, title="", image_url="", subtitle="", buttons=[]):
        element = {}
        element['title'] = title[:TITLE_CHARACTER_LIMIT]
        element['image_url'] = image_url
        if subtitle != '':
            element['subtitle'] = subtitle[:SUBTITLE_CHARACTER_LIMIT]
        # make sure button title is in limits
        for button in buttons:
            button['title'] = button['title'][:BUTTON_TITLE_CHARACTER_LIMIT]
        if len(buttons) > 0:
            element['buttons'] = buttons[:BUTTON_LIMIT]
        if len(self.elements) < ELEMENTS_LIMIT:
            self.elements.append(element)

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
        super().send_generic_message(reciepiant_id, self.elements, self.quick_replies)
