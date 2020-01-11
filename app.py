from flask import Flask, request
import json
import requests
from pymessenger.bot import Bot

app = Flask(__name__)

FB_ACCESS_TOKEN = "EAAF5Cd9fC3YBAD1ZB6zZCkeTlw4iqz3aXQaXCZC8DrjPAIvcOT6sm9ptCSWeCHmKB9D33q1zNG5HgDezOhByXjTlFwoLgtgXkXbSl4hPJYrwNcInQ7bb2FVZBOGWp6pkLWdd8Wf34ZA6jWvLGl827E8jqDmX4DIZB2zhUyxz4c0QZDZD"

bot = Bot(FB_ACCESS_TOKEN)

#"https://ibb.co/mvmrRr5"

VERIFICATION_TOKEN = "test"


@app.route('/', methods= ['GET'])
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
				recipient_id = messaging_event['recipient']['id']

				if messaging_event.get('message'):
					# HANDLE NORMAL MESSAGES HERE
					if messaging_event['message'].get('text'):
						# HANDLE TEXT MESSAGES
						query = messaging_event['message']['text']
						# ECHO THE RECEIVED MESSAGE
						bot.send_text_message(sender_id, query)
	return "ok", 200


if __name__ == "__main__":
	app.run(port=8000, use_reloader=True)
