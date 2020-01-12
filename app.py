
from flask import Flask, request
import json
import requests
from models.bot import Bot
from views.generic import test

app = Flask(__name__)

FB_ACCESS_TOKEN = "EAAF5Cd9fC3YBAD1ZB6zZCkeTlw4iqz3aXQaXCZC8DrjPAIvcOT6sm9ptCSWeCHmKB9D33q1zNG5HgDezOhByXjTlFwoLgtgXkXbSl4hPJYrwNcInQ7bb2FVZBOGWp6pkLWdd8Wf34ZA6jWvLGl827E8jqDmX4DIZB2zhUyxz4c0QZDZD"

bot = Bot(FB_ACCESS_TOKEN)


VERIFICATION_TOKEN = "test"


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
						bot.send_generic_message(sender_id, test.elements)
					
	return "ok", 200

if __name__ == "__main__":
    app.run()
