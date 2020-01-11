from templates.generic import GenericTemplate

test_buttons = [
    {
        "type": "web_url",
                "url": "https://petersfancybrownhats.com",
                "title": "View Website"
    }, {
        "type": "postback",
                "title": "Start Chatting",
                "payload": "DEVELOPER_DEFINED_PAYLOAD"
    }
]


test = GenericTemplate()

test.add_element(title="Big Test",image_url="https://petersfancybrownhats.com/company_image.png", subtitle="test", buttons=test_buttons)

