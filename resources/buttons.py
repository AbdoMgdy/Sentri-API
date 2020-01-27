from models.button import ButtonTemplate

# Confirm Block
confirm_block = ButtonTemplate()
confirm_block.add_web_url(
    **{'Confirm': 'https://trex-chat-bot.herokuapp.com/confirm_order'})
confirm_block.add_postback(**{'Add to Order': 'main_menu'})
confirm_block.add_web_url(
    **{'Edit': 'https://trex-chat-bot.herokuapp.com/edit_order'})

# Main Menu
family = ButtonTemplate()
family.add_postback(**{'Show Menu عرض المنيو': 'family'})

sandwiches = ButtonTemplate()
sandwiches.add_postback(**{'Show Menu عرض المنيو': 'sandwiches'})

special = ButtonTemplate()
special.add_postback(**{'Show Menu عرض المنيو': 'special'})

kids_meals = ButtonTemplate()
kids_meals.add_postback(**{'Show Menu عرض المنيو': 'kids_meals'})

trex_meals = ButtonTemplate()
trex_meals.add_postback(**{'Show Menu عرض المنيو': 'trex_meals'})

appetizers = ButtonTemplate()
appetizers.add_postback(**{'Show Menu عرض المنيو': 'appetizers'})

sauces = ButtonTemplate()
sauces.add_postback(**{'Show Menu عرض المنيو': 'sauces'})

# Family Menu
chicken9 = ButtonTemplate()
chicken9.add_web_url(
    **{'اطلب بـ155': 'https://trex-chat-bot.herokuapp.com/webview/order/meal/9-Chicken'})
chicken12 = ButtonTemplate()
chicken12.add_web_url(
    **{'اطلب بـ196': 'https://trex-chat-bot.herokuapp.com/webview/order/meal/12-Chicken'})
chicken15 = ButtonTemplate()
chicken15.add_web_url(
    **{'اطلب بـ230': 'https://trex-chat-bot.herokuapp.com/webview/order/meal/15-Chicken'})
chicken18 = ButtonTemplate()
chicken18.add_web_url(
    **{'اطلب بـ270': 'https://trex-chat-bot.herokuapp.com/webview/order/meal/18-Chicken'})
