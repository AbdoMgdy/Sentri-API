from models.button import ButtonTemplate

# Confirm Block
confirm_block = ButtonTemplate()
confirm_block.add_web_url(
    **{'تأكيد الأوردر': 'https://trex-chat-bot.herokuapp.com/confirm_order'})
confirm_block.add_postback(**{'اضافة للأوردر': 'main_menu'})
confirm_block.add_web_url(
    **{'تعديل الأوردر': 'https://trex-chat-bot.herokuapp.com/edit_order'})

# Main Menu
family = ButtonTemplate()
family.add_postback(**{'Show Menu عرض المنيو': 'family_menu'})

sandwiches = ButtonTemplate()
sandwiches.add_postback(**{'Show Menu عرض المنيو': 'sandwiches_menu'})

special = ButtonTemplate()
special.add_postback(**{'Show Menu عرض المنيو': 'special_menu'})

kids_meals = ButtonTemplate()
kids_meals.add_postback(**{'Show Menu عرض المنيو': 'kids_meals_menu'})

trex_meals = ButtonTemplate()
trex_meals.add_postback(**{'Show Menu عرض المنيو': 'trex_meals_menu'})

appetizers = ButtonTemplate()
appetizers.add_postback(**{'Show Menu عرض المنيو': 'appetizers_menu'})

sauces = ButtonTemplate()
sauces.add_postback(**{'Show Menu عرض المنيو': 'sauces_menu'})

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

# Sandwiches Menu

original = ButtonTemplate()
original.add_web_url(
    **{'اطلب 150جم بـ30': 'https://trex-chat-bot.herokuapp.com/webview/order/sandwich/Original-150'})
original.add_web_url(
    **{'اطلب 300جم بـ45': 'https://trex-chat-bot.herokuapp.com/webview/order/sandwich/Original-300'})

somke_house = ButtonTemplate()
somke_house.add_web_url(
    **{'اطلب 150جم بـ45': 'https://trex-chat-bot.herokuapp.com/webview/order/sandwich/Smoke-House-150'})
somke_house.add_web_url(
    **{'اطلب 300جم بـ58': 'https://trex-chat-bot.herokuapp.com/webview/order/sandwich/Smoke-House-300'})

boom_mozzarella = ButtonTemplate()
boom_mozzarella.add_web_url(
    **{'اطلب 150جم بـ65': 'https://trex-chat-bot.herokuapp.com/webview/order/sandwich/Boom-Mozzarella-150'})
boom_mozzarella.add_web_url(
    **{'اطلب 300جم بـ78': 'https://trex-chat-bot.herokuapp.com/webview/order/sandwich/Boom-Mozzarella-300'})

spicy_houston = ButtonTemplate()
spicy_houston.add_web_url(
    **{'اطلب 150جم بـ67': 'https://trex-chat-bot.herokuapp.com/webview/order/sandwich/Spicy-Houston-150'})
spicy_houston.add_web_url(
    **{'اطلب 300جم بـ78': 'https://trex-chat-bot.herokuapp.com/webview/order/sandwich/Spicy-Houston-300'})

down_bacon = ButtonTemplate()
down_bacon.add_web_url(
    **{'اطلب 300جم بـ65': 'https://trex-chat-bot.herokuapp.com/webview/order/sandwich/Down-Bacon-300'})
down_bacon.add_web_url(
    **{'اطلب 450جم بـ78': 'https://trex-chat-bot.herokuapp.com/webview/order/sandwich/Down-Bacon-450'})

down_turkey = ButtonTemplate()
down_turkey.add_web_url(
    **{'اطلب 300جم بـ65': 'https://trex-chat-bot.herokuapp.com/webview/order/sandwich/Down-Turkey-300'})
down_turkey.add_web_url(
    **{'اطلب 450جم بـ78': 'https://trex-chat-bot.herokuapp.com/webview/order/sandwich/Down-Turkey-450'})

chicken_pizza = ButtonTemplate()
chicken_pizza.add_web_url(
    **{'اطلب بـ42': 'https://trex-chat-bot.herokuapp.com/webview/order/sandwich/Chicken-Pizza'})

heavey_trex = ButtonTemplate()
heavey_trex.add_web_url(
    **{'اطلب بـ90': 'https://trex-chat-bot.herokuapp.com/webview/order/sandwich/Heavy-Trex'})

troodon = ButtonTemplate()
troodon.add_web_url(
    **{'اطلب بـ80': 'https://trex-chat-bot.herokuapp.com/webview/order/sandwich/Troodon'})


# Trex Special
trex_waffle = ButtonTemplate()
trex_waffle.add_web_url(
    **{'اطلب 150جم بـ60': 'https://trex-chat-bot.herokuapp.com/webview/order/sandwich/Trex-Waffle-150'})
trex_waffle.add_web_url(
    **{'اطلب 300جم بـ75': 'https://trex-chat-bot.herokuapp.com/webview/order/sandwich/Trex-Waffle-300'})

route66 = ButtonTemplate()
route66.add_web_url(
    **{'اطلب بـ45': 'https://trex-chat-bot.herokuapp.com/webview/order/sandwich/Route-66'})

quesadilla = ButtonTemplate()
quesadilla.add_web_url(
    **{'اطلب بـ45': 'https://trex-chat-bot.herokuapp.com/webview/order/sandwich/Quesadilla'})

mexican_wrap = ButtonTemplate()
mexican_wrap.add_web_url(
    **{'اطلب بـ35': 'https://trex-chat-bot.herokuapp.com/webview/order/sandwich/Mexican-Wrap'})

# Trex Meals
trex = ButtonTemplate()
trex.add_web_url(
    **{'اطلب بـ55': 'https://trex-chat-bot.herokuapp.com/webview/order/meal/Trex'})

dinner_box = ButtonTemplate()
dinner_box.add_web_url(
    **{'اطلب بـ55': 'https://trex-chat-bot.herokuapp.com/webview/order/meal/Dinner-Box'})

snack_box = ButtonTemplate()
snack_box.add_web_url(
    **{'اطلب بـ38': 'https://trex-chat-bot.herokuapp.com/webview/order/meal/Snack-Box'})

turkey_box = ButtonTemplate()
turkey_box.add_web_url(
    **{'اطلب بـ70': 'https://trex-chat-bot.herokuapp.com/webview/order/meal/Turkey-Box'})

crispy_strips = ButtonTemplate()
crispy_strips.add_web_url(
    **{'اطلب بـ35': 'https://trex-chat-bot.herokuapp.com/webview/order/meal/Crispy-Strips'})

jumbo_crispy_strips = ButtonTemplate()
jumbo_crispy_strips.add_web_url(
    **{'اطلب بـ50': 'https://trex-chat-bot.herokuapp.com/webview/order/meal/Jumpo-Crispy-Strips'})


# Appetizers
mozzarella_sticks = ButtonTemplate()
mozzarella_sticks.add_web_url(
    **{'اطلب بـ30': 'https://trex-chat-bot.herokuapp.com/webview/order/sauce/Mozzarella-Sticks'})

onion_rings = ButtonTemplate()
onion_rings.add_web_url(
    **{'اطلب بـ20': 'https://trex-chat-bot.herokuapp.com/webview/order/sauce/Onion-Rings'})

jalapeno_sticks = ButtonTemplate()
jalapeno_sticks.add_web_url(
    **{'اطلب بـ32': 'https://trex-chat-bot.herokuapp.com/webview/order/sauce/Jalapeno-Sticks'})

mexican_fries = ButtonTemplate()
mexican_fries.add_web_url(
    **{'اطلب بـ32': 'https://trex-chat-bot.herokuapp.com/webview/order/sauce/Mexican-Fries'})

rizo = ButtonTemplate()
rizo.add_web_url(
    **{'اطلب بـ20': 'https://trex-chat-bot.herokuapp.com/webview/order/sauce/Rizo'})

spicy_rice = ButtonTemplate()
spicy_rice.add_web_url(
    **{'اطلب بـ10': 'https://trex-chat-bot.herokuapp.com/webview/order/sauce/Spicy-Rice'})

# Kids Meals
kids_chicken_piece = ButtonTemplate()
kids_chicken_piece.add_web_url(
    **{'اطلب بـ29': 'https://trex-chat-bot.herokuapp.com/webview/order/sauce/Kids-Chicken-Piece'})

kids_chicken_strips = ButtonTemplate()
kids_chicken_piece.add_web_url(
    **{'اطلب بـ29': 'https://trex-chat-bot.herokuapp.com/webview/order/sauce/Kids-Chicken-Strips'})

# Sauces
cheddar_sauce = ButtonTemplate()
cheddar_sauce.add_web_url(
    **{'اطلب بـ10': 'https://trex-chat-bot.herokuapp.com/webview/order/sauce/Cheddar-Sauce'})

ranch_sauce = ButtonTemplate()
ranch_sauce.add_web_url(
    **{'اطلب بـ10': 'https://trex-chat-bot.herokuapp.com/webview/order/sauce/Ranch-Sauce'})

island1000 = ButtonTemplate()
island1000.add_web_url(
    **{'اطلب بـ10': 'https://trex-chat-bot.herokuapp.com/webview/order/sauce/1000-Island'})

bbq_sauce = ButtonTemplate()
bbq_sauce.add_web_url(
    **{'اطلب بـ10': 'https://trex-chat-bot.herokuapp.com/webview/order/sauce/BBQ-Sauce'})

trex_sauce = ButtonTemplate()
trex_sauce.add_web_url(
    **{'اطلب بـ10': 'https://trex-chat-bot.herokuapp.com/webview/order/sauce/Trex-Sauce'})

coleslaw = ButtonTemplate()
coleslaw.add_web_url(
    **{'اطلب بـ10': 'https://trex-chat-bot.herokuapp.com/webview/order/sauce/Coleslw-Small'})
coleslaw.add_web_url(
    **{'اطلب بـ20': 'https://trex-chat-bot.herokuapp.com/webview/order/sauce/Coleslw-Large'})

cola = ButtonTemplate()
cola.add_web_url(
    **{'اطلب بـ10': 'https://trex-chat-bot.herokuapp.com/webview/order/sauce/Cola'})

water = ButtonTemplate()
water.add_web_url(
    **{'اطلب بـ10': 'https://trex-chat-bot.herokuapp.com/webview/order/sauce/Water'})
