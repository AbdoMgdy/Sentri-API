from models.button import ButtonTemplate

family_btn = ButtonTemplate()
family_btn.add_postback(**{'Show Menu عرض المنيو': 'family_menu'})

burger_btn = ButtonTemplate()
burger_btn.add_postback(**{'Back': 'family_menu'})
burger_btn.add_web_url(
    **{'Order Now!': 'https://trex-chat-bot.herokuapp.com/webview/order/sandwich/burger/100.0'})

meal_btn = ButtonTemplate()
meal_btn.add_postback(**{'Back': 'family_menu'})
meal_btn.add_web_url(
    **{'Order Now!': 'https://trex-chat-bot.herokuapp.com/webview/order/meal/9-chicekn/100.0'})
sauce_btn = ButtonTemplate()
sauce_btn.add_postback(**{'Back': 'family_menu'})
sauce_btn.add_web_url(
    **{'Order Now!': 'https://trex-chat-bot.herokuapp.com/webview/order/sauce/hot-sauce/100.0'})


confirm_block = ButtonTemplate()
confirm_block.add_web_url(
    **{'Confirm': 'https://trex-chat-bot.herokuapp.com/confirm_order'})
confirm_block.add_postback(**{'Add to Order': 'main_menu'})
confirm_block.add_postback(
    **{'Cancel': 'cancel_order'})
