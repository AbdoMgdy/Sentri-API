from models.button import ButtonTemplate

family_btn = ButtonTemplate()
family_btn.add_postback(**{'Show Menu عرض المنيو': 'family_menu'})

burger_btn = ButtonTemplate()
# burger_btn.add_postback(**{'Back': 'family_menu'})
burger_btn.add_web_url(
    **{'Order Now!': 'https://trex-chat-bot.herokuapp.com/webview/order/burger'})
