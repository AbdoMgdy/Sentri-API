from models.button import ButtonTemplate

family_btn = ButtonTemplate()
family_btn.add_postback(**{'Show Menu عرض المنيو': 'family_menu'})

burger_btn = ButtonTemplate()
burger_btn.add_postback(**{'Back': 'family_menu'})
burger_btn.add_web_url(
    **{'Order Now!': 'https://trex-chat-bot.herokuapp.com/webview/order/burger/100.0'})


confirm_block = ButtonTemplate()
confirm_block.add_web_url(
    **{'Confirm': 'https://trex-chat-bot.herokuapp.com/signup'})
confirm_block.add_postback(**{'Details': 'confirm_order'})
confirm_block.add_postback(**{'Edit': 'confirm_order'})
