from templates.generic import GenericTemplate
from templates.button import ButtonTemplate
from templates.quick_replies import QuickReplies



#Main Menu Buttons
family_buttons = ButtonTemplate()
family_buttons.add_postback(**{'Show Menu عرض المنيو':'family_menu'})

sandwiches_buttons = ButtonTemplate()
sandwiches_buttons.add_postback(**{'Show Menu عرض المنيو': 'sandwiches_menu'})

trex_special_buttons = ButtonTemplate()
trex_special_buttons.add_postback(**{'Show Menu عرض المنيو': 'trex_special_menu'})

trex_meals_buttons = ButtonTemplate()
trex_meals_buttons.add_postback(**{'Show Menu عرض المنيو': 'trex_meals_menu'})

kids_meals_buttons = ButtonTemplate()
kids_meals_buttons.add_postback(**{'Show Menu عرض المنيو': 'kids_meals_menu'})

appetizers_buttons = ButtonTemplate()
appetizers_buttons.add_postback(**{'Show Menu عرض المنيو': 'apppetizers_menu'})


main_menu = GenericTemplate()

#Main Menu Elements
main_menu.add_element(title="Family Meals الوجبات العائلية", image_url="https://petersfancybrownhats.com/company_image.png", buttons=family_buttons.buttons)
main_menu.add_element(title="Sandwiches الساندوتشات", image_url="https://petersfancybrownhats.com/company_image.png", buttons=sandwiches_buttons.buttons)
main_menu.add_element(title="Trex Special", image_url="https://petersfancybrownhats.com/company_image.png", buttons=trex_special_buttons.buttons)
main_menu.add_element(title="Trex Meals وجبات تركس", image_url="https://petersfancybrownhats.com/company_image.png", buttons=trex_meals_buttons.buttons)
main_menu.add_element(title="Kids Meals وجبات الأطفال", image_url="https://petersfancybrownhats.com/company_image.png", buttons=kids_meals_buttons.buttons)
main_menu.add_element(title="Appetizers المقبلات", image_url="https://petersfancybrownhats.com/company_image.png", buttons=appetizers_buttons.buttons)


#Family Menu Buttons

chicken_9 = ButtonTemplate()
chicken_9.add_postback(**{'اطلب الآن بـ155ج':'paylod'})

chicken_12 = ButtonTemplate()
chicken_12.add_postback(**{'اطلب الآن بـ155ج':'paylod'})

chicken_15 = ButtonTemplate()
chicken_15.add_postback(**{'اطلب الآن بـ155ج':'payload'})

chicken_18 = ButtonTemplate()
chicken_18.add_postback(**{'اطلب الآن بـ155ج':'paylod'})





family_quick_replies = QuickReplies()
family_quick_replies.add_quick_replies(**{'العودة للخلف':'family_menu.parent'})

family_menu = GenericTemplate(parent=main_menu, quick_replies=family_quick_replies.quick_replies)
family_menu.add_element(title="1st Sandwich", image_url="https://petersfancybrownhats.com/company_image.png",subtitle="2nd Sandwich Sub Menu", buttons=family_buttons.buttons)

