from models.generic import GenericTemplate
from resources.buttons import *

# Main Menu
main_menu = GenericTemplate()

main_menu.add_element(title="Family Meals الوجبات العائلية", image_url='https://i.ibb.co/N7Z2Y0Y/image.png',
                      buttons=family.buttons)
main_menu.add_element(title="Sandwiches الساندوتشات", image_url="https://ibb.co/KG3Q2CM",
                      buttons=sandwiches.buttons)
main_menu.add_element(title="Trex Meals وجبات تركس", image_url="https://ibb.co/9qWC959",
                      buttons=trex_meals.buttons)
main_menu.add_element(title="Trex Special", image_url="https://ibb.co/fXL4Kyb",
                      buttons=special.buttons)
main_menu.add_element(title="Kids Meals وجبات الأطفال",
                      image_url="https://ibb.co/9qWC959",
                      buttons=kids_meals.buttons)
main_menu.add_element(title="Appetizers المقبلات", image_url="https://ibb.co/ZmppQBC",
                      buttons=appetizers.buttons)
main_menu.add_element(title="Sauces الصوصات", image_url="https://ibb.co/s3vmvxB",
                      buttons=sauces.buttons)

# Family Menu
family_menu = GenericTemplate()

family_menu.add_element(
    title="وجبة 9 قطع دجاج", image_url='https://i.ibb.co/N7Z2Y0Y/image.png', buttons=chicken9.buttons)
family_menu.add_element(
    title="وجبة 12 قطع دجاج", image_url='https://i.ibb.co/N7Z2Y0Y/image.png', buttons=chicken12.buttons)
family_menu.add_element(
    title="وجبة 15 قطع دجاج", image_url='https://i.ibb.co/N7Z2Y0Y/image.png', buttons=chicken15.buttons)
family_menu.add_element(
    title="وجبة 18 قطع دجاج", image_url='https://i.ibb.co/N7Z2Y0Y/image.png', buttons=chicken18.buttons)
family_menu.add_quick_replies(**{'Back العودة للخلف': 'main_menu'})

# Sandwiches Menu
sandwiches_menu = GenericTemplate()

sandwiches_menu.add_element(
    title='Original أوريجينال', image_url='https://ibb.co/LkfX8Qm', buttons=original.buttons)
sandwiches_menu.add_element(
    title='Smoke House سموك هاوس', image_url='https://ibb.co/kQfNhtG', buttons=somke_house.buttons)
sandwiches_menu.add_element(
    title='Boom Mozzarella بوم موتزاريلا', image_url='https://ibb.co/X5Cjy7Z', buttons=boom_mozzarella.buttons)
sandwiches_menu.add_element(
    title='Spicy Houston سبايسي هيوستون', image_url='https://ibb.co/v3tpPZ1', buttons=spicy_houston.buttons)
sandwiches_menu.add_element(
    title='Down Bacon داون بيكون', image_url='https://ibb.co/ZXnzkcF', buttons=down_bacon.buttons)
sandwiches_menu.add_element(
    title='Down Turkey داون تركي', image_url='https://ibb.co/drvCR6T', buttons=down_turkey.buttons)
sandwiches_menu.add_element(
    title='Chicken Pizza تشيكن بيتزا', image_url='https://ibb.co/0mwTvfZ', buttons=chicken_pizza.buttons)
sandwiches_menu.add_element(
    title='Troodon تروودون', image_url='https://ibb.co/KG3Q2CM', buttons=troodon.buttons)
sandwiches_menu.add_element(
    title='Heavey Trex هيفي تركس', image_url='https://ibb.co/qxc2Gtf', buttons=heavey_trex.buttons)

# Trex Special

