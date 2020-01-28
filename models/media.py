from models.bot import Bot

template = {
    "template_type": "receipt",
    "value": {
        "attachment": {
            "type": "template",
            "payload": {
                "template_type": "receipt",
                "recipient_name": "",
                "order_number": "",
                "currency": "",
                "payment_method": ""
            }
        }
    }
}
