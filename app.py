
from flask import Flask, request
import json
import requests
from models.bot import Bot
from views.menu import *

app = Flask(__name__)		

VERIFICATION_TOKEN = "test"

bot = Bot()

@app.route('/', methods=['GET'])
def verify():
	if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.challenge"):
		if not request.args.get("hub.verify_token") == VERIFICATION_TOKEN:
			return "Verification token mismatch", 403
		return request.args["hub.challenge"], 200
	return "Hello world", 200


@app.route('/', methods=['POST'])
def handle_incoming_messages():
	print(request.data)
	data = request.get_json()

	if data['object'] == "page":
		entries = data['entry']

		for entry in entries:
			messaging = entry['messaging']

			for messaging_event in messaging:

				sender_id = messaging_event['sender']['id']
				#recipient_id = messaging_event['recipient']['id']

				if messaging_event.get('message'):
					# HANDLE NORMAL MESSAGES HERE
					if messaging_event['message'].get('text'):
						bot.send_before_message(sender_id)
						menu.send(sender_id)
						return "ok", 200
				if messaging_event.get('postback'):
					block_name = messaging_event['postback'].get('payload')
					print('it came here')
					print(block_name)
					block_obj = eval(block_name)
					print(block_obj)
					print(block_obj.children)
					menu.send(sender_id)
					block_obj.send(sender_id)
					return "ok", 200
	return "ok", 200

	


if __name__ == "__main__":
    app.run()
