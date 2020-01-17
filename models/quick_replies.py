import json
from copy import deepcopy as copy

QUICK_REPLIES_LIMIT = 11
TITLE_CHARACTER_LIMIT = 20
PAYLOAD_CHARACTER_LIMIT = 1000


class QuickReplies:
    def __init__(self):
        self.quick_replies = []
    #Pass Quick Replies as a **dict    
    def add_quick_replies(self, **kwargs):
        for title, paylod in kwargs.items():
            if len(self.quick_replies) < QUICK_REPLIES_LIMIT:
                quick_reply = {}
                # TODO: location + image_url
                quick_reply['content_type'] = 'text'
                quick_reply['title'] = title[:TITLE_CHARACTER_LIMIT]
                quick_reply['payload'] = json.dumps(paylod)[:PAYLOAD_CHARACTER_LIMIT]
                self.quick_replies.append(quick_reply)


