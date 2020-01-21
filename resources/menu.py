from models.generic import GenericTemplate
from resources.buttons import family_btn, burger_btn, meal_btn, sauce_btn

# Main Menu
main_menu = GenericTemplate()

main_menu.add_element(title="Family Meals الوجبات العائلية", image_url='https://i.ibb.co/N7Z2Y0Y/image.png',
                      buttons=family_btn.buttons)
# main_menu.add_element(title="Sandwiches الساندوتشات", image_url="https://petersfancybrownhats.com/company_image.png", **{'Show Menu عرض المنيو': 'sandwiches_menu'})
# main_menu.add_element(title="Trex Special", image_url="https://petersfancybrownhats.com/company_image.png", **{'Show Menu عرض المنيو': 'trex_meals_menu'})
# main_menu.add_element(title="Trex Meals وجبات تركس", image_url="https://petersfancybrownhats.com/company_image.png", **{'Show Menu عرض المنيو': 'kids_meals_menu'})
# main_menu.add_element(title="Kids Meals وجبات الأطفال", image_url="https://petersfancybrownhats.com/company_image.png", **{'Show Menu عرض المنيو': 'kids_meals_menu'})
# main_menu.add_element(title="Appetizers المقبلات", image_url="https://petersfancybrownhats.com/company_image.png",**{'Show Menu عرض المنيو': 'apppetizers_menu'})


# Family Menu

family_menu = GenericTemplate()

family_menu.add_element(
    title="Burger", image_url='https://i.ibb.co/N7Z2Y0Y/image.png', buttons=burger_btn.buttons)
family_menu.add_element(
    title="9 Chicken", image_url='https://i.ibb.co/N7Z2Y0Y/image.png', buttons=meal_btn.buttons)
family_menu.add_element(
    title="Sauce", image_url='https://i.ibb.co/N7Z2Y0Y/image.png', buttons=sauce_btn.buttons)
family_menu.add_quick_replies(**{'Back العودة للخلف': 'main_menu'})
