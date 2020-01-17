from models.bot import Bot
from models.quick_replies import QuickReplies


TITLE_CHARACTER_LIMIT = 80
SUBTITLE_CHARACTER_LIMIT = 80
BUTTON_TITLE_CHARACTER_LIMIT = 20
BUTTON_LIMIT = 3
ELEMENTS_LIMIT = 10


class GenericTemplate(Bot):
    def __init__(self, quick_replies=None, parent=None, children=None):
        super().__init__()
        self.elements = []
        self.parent = parent
        if children:
            self.children = children
        self.quick_replies = quick_replies

    def add_element(self, title="", image_url="", subtitle="", buttons=[]):
        element = {}
        element['title'] = title[:TITLE_CHARACTER_LIMIT]
        element['image_url'] = image_url
        if subtitle != '':
            element['subtitle'] = subtitle[:SUBTITLE_CHARACTER_LIMIT]
        for button in buttons:
            button['title'] = button['title'][:BUTTON_TITLE_CHARACTER_LIMIT]
        if len(buttons) > 0:
            element['buttons'] = buttons[:BUTTON_LIMIT]
        if len(self.elements) < ELEMENTS_LIMIT:
            self.elements.append(element)

    def send(self, reciepiant_id):
        super().send_generic_message(reciepiant_id, self.elements, self.quick_replies)
