from models.generic import GenericTemplate
from resources.buttons import family, sandwiches, trex_meals, special, appetizers, kids_meals

# Main Menu
main_menu = GenericTemplate()

main_menu.add_element(title="Family Meals الوجبات العائلية", image_url='https://i.ibb.co/N7Z2Y0Y/image.png',
                      buttons=family.buttons)
main_menu.add_element(title="Sandwiches الساندوتشات", image_url="https://petersfancybrownhats.com/company_image.png",
                      buttons=sandwiches.buttons)
main_menu.add_element(title="Trex Special", image_url="https://petersfancybrownhats.com/company_image.png",
                      buttons=special.buttons)
main_menu.add_element(title="Trex Meals وجبات تركس", image_url="https://petersfancybrownhats.com/company_image.png",
                      buttons=trex_meals.buttons)
main_menu.add_element(title="Kids Meals وجبات الأطفال",
                      image_url="https://petersfancybrownhats.com/company_image.png",
                      buttons=kids_meals.buttons)
main_menu.add_element(title="Appetizers المقبلات", image_url="https://petersfancybrownhats.com/company_image.png",
                      buttons=appetizers.buttons)


# Family Menu

family_menu = GenericTemplate()

family_menu.add_element(
    title="وجبة 9 قطع دجاج", image_url='https://i.ibb.co/N7Z2Y0Y/image.png', buttons=9-chicken.buttons)
family_menu.add_element(
    title="وجبة 12 قطع دجاج", image_url='https://i.ibb.co/N7Z2Y0Y/image.png', buttons=12-chicken.buttons)
family_menu.add_element(
    title="وجبة 15 قطع دجاج", image_url='https://i.ibb.co/N7Z2Y0Y/image.png', buttons=15-chicken.buttons)
family_menu.add_element(
    title="وجبة 18 قطع دجاج", image_url='https://i.ibb.co/N7Z2Y0Y/image.png', buttons=18-chicken.buttons)
family_menu.add_quick_replies(**{'Back العودة للخلف': 'main_menu'})
