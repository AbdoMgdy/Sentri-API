from copy import deepcopy as copy
import json


TITLE_CHARACTER_LIMIT = 80
SUBTITLE_CHARACTER_LIMIT = 80
BUTTON_TITLE_CHARACTER_LIMIT = 20
BUTTON_LIMIT = 3
ELEMENTS_LIMIT = 10

template = {
    "template_type": "generic",
    "value": {
        "attachment": {
            "type": "template",
            "payload": {
                "template_type": "generic",
                "image_aspect_ratio": "horizontal",
                "elements": []
            }
        }
    }
}

class GenericTemplate:
    def __init__(self):
        self.elements = []

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

