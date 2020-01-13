from copy import deepcopy as copy
from models.bot import Bot
import json
from templates.quick_replies import QuickReplies
from anytree import NodeMixin

TITLE_CHARACTER_LIMIT = 80
SUBTITLE_CHARACTER_LIMIT = 80
BUTTON_TITLE_CHARACTER_LIMIT = 20
BUTTON_LIMIT = 3
ELEMENTS_LIMIT = 10

# template = {
#     "template_type": "generic",
#     "value": {
#         "attachment": {
#             "type": "template",
#             "payload": {
#                 "template_type": "generic",
#                 "image_aspect_ratio": "horizontal",
#                 "elements": []
#             }
#         }
#     }
# }

class GenericTemplate(Bot, NodeMixin):
    def __init__(self, quick_replies=None, parent=None, children=None):
        super().__init__()
        self.elements = []
        
        self.parent = parent
        if children:
            self.children = children
        if quick_replies:
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
        