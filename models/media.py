
from copy import deepcopy as copy

template = {
    "template_type": "receipt",
    "value": {
        "attachment": {
            "type": "template",
            "payload": {
                "template_type": "media",
                "elements": [],

            }
        }
    }
}


class MediaTemplate():
    def __init__(self, url=''):
        super().__init__()
        self.template = copy(template['value'])
        self.template['attachment']['payload']['elements'] = [{
            'media_type': 'image',
            'url': url
        }]

    def get_template(self):
        return self.template
