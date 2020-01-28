from models.bot import Bot
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


class MediaTemplate(Bot):
    def __init__(self, url=''):
        super().__init__()
        self.template = copy(template['value'])
        self.template['attachment']['payload']['elements'] = [{
            'media_type': 'image',
            'url': url
        }]

    def send(self, recipient_id):
        super().send_message(recipient_id, self.template)
