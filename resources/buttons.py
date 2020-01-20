from models.button import ButtonTemplate

family_btn = ButtonTemplate()
family_btn.add_postback(**{'Show Menu عرض المنيو': 'family_menu'})

burger_btn = ButtonTemplate()
burger_btn.add_postback(**{'Back': 'family_menu'})
burger_btn.add_web_url(
    **{'Order Now!': 'https://trex-chat-bot.herokuapp.com/webview/order/sandwich/burger/100.0'})


confirm_block = ButtonTemplate()
confirm_block.add_web_url(
    **{'Confirm': 'https://trex-chat-bot.herokuapp.com/confirm_order'})
confirm_block.add_postback(**{'Add to Order': 'main_menu'})
confirm_block.add_web_url(
    **{'Edit': 'https://trex-chat-bot.herokuapp.com/edit_order'})
