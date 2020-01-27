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
    title='Original أوريجينال', image_url='https://i.ibb.co/Tv5xkK6/image.png', buttons=original.buttons)
sandwiches_menu.add_element(
    title='Smoke House سموك هاوس', image_url='https://i.ibb.co/wMX5Kfd/image.png', buttons=somke_house.buttons)
sandwiches_menu.add_element(
    title='Boom Mozzarella بوم موتزاريلا', image_url='https://i.ibb.co/3FC4fpy/image.png', buttons=boom_mozzarella.buttons)
sandwiches_menu.add_element(
    title='Spicy Houston سبايسي هيوستون', image_url='https://i.ibb.co/5r7m8BT/image.png', buttons=spicy_houston.buttons)
sandwiches_menu.add_element(
    title='Down Bacon داون بيكون', image_url='https://i.ibb.co/MSYk3Pt/image.png', buttons=down_bacon.buttons)
sandwiches_menu.add_element(
    title='Down Turkey داون تركي', image_url='https://i.ibb.co/80wvH2C/image.png', buttons=down_turkey.buttons)
sandwiches_menu.add_element(
    title='Chicken Pizza تشيكن بيتزا', image_url='https://i.ibb.co/9cM6Sq2/image.png', buttons=chicken_pizza.buttons)
sandwiches_menu.add_element(
    title='Troodon تروودون', image_url='https://i.ibb.co/59fzrqN/image.png', buttons=troodon.buttons)
sandwiches_menu.add_element(
    title='Heavey Trex هيفي تركس', image_url='https://i.ibb.co/JCGSLf4/image.png', buttons=heavey_trex.buttons)

# Trex Special
special_menu = GenericTemplate()

special_menu.add_element(
    title='Trex Waffle تركس وافل', image_url='https://i.ibb.co/VL52hzd/image.png', buttons=trex_waffle.buttons)

special_menu.add_element(
    title='Route 66 روت 66', image_url='https://i.ibb.co/BZwbF3H/66.png', buttons=route66.buttons)

special_menu.add_element(
    title='َQuesadilla كاساديا', image_url='https://i.ibb.co/cxcN6pn/image.png', buttons=quesadilla.buttons)

special_menu.add_element(
    title='َMexican Wrap ميكسيكان راب', image_url='https://i.ibb.co/LJxBy2H/image.png', buttons=mexican_wrap.buttons)


# Trex Meals

special_menu = GenericTemplate()

special_menu.add_element(
    title='Trex تركس', image_url='https://i.ibb.co/p3d9vFv/image.png', buttons=trex.buttons)
special_menu.add_element(
    title='Dinner Box دينر بوكس', image_url='https://i.ibb.co/p3d9vFv/image.png', buttons=dinner_box.buttons)
special_menu.add_element(
    title='Snack Box سناك بوكس', image_url='https://i.ibb.co/p3d9vFv/image.png', buttons=snack_box.buttons)
special_menu.add_element(
    title='Turkey Box تركي بوكس', image_url='https://i.ibb.co/p3d9vFv/image.png', buttons=turkey_box.buttons)
special_menu.add_element(
    title='Crispy Strips كرسبي ستربس', image_url='https://i.ibb.co/p3d9vFv/image.png', buttons=crispy_strips.buttons)
special_menu.add_element(
    title='Jumbo Crispy Strips', image_url='https://i.ibb.co/p3d9vFv/image.png', buttons=jumbo_crispy_strips.buttons)

# Kids Meals
kids_menu = GenericTemplate()
kids_menu.add_element(
    title='َوجبة أطفال قطعة دجاج', image_url='https://i.ibb.co/p3d9vFv/image.png', buttons=kids_chicken_piece.buttons)
kids_menu.add_element(
    title='َوجبة أطفال 2 استربس', image_url='https://i.ibb.co/p3d9vFv/image.png', buttons=kids_chicken_strips.buttons)

# Appetizers

appetizers_menu = GenericTemplate()
appetizers_menu.add_element(
    title='َأصابع موتزاريلا 3 قطع', image_url='https://i.ibb.co/p3d9vFv/image.png', buttons=mozzarella_sticks.buttons)
appetizers_menu.add_element(
    title='َحلقات البصل 5 قطع', image_url='https://i.ibb.co/p3d9vFv/image.png', buttons=onion_rings.buttons)
appetizers_menu.add_element(
    title='َأصابع هالبينو شيدر 3 قطع', image_url='https://i.ibb.co/p3d9vFv/image.png', buttons=onion_rings.buttons)
appetizers_menu.add_element(
    title='ميكسيكان فرايز', image_url='https://i.ibb.co/p3d9vFv/image.png', buttons=mexican_fries.buttons)
appetizers_menu.add_element(
    title='ريزو', image_url='https://i.ibb.co/p3d9vFv/image.png', buttons=rizo.buttons)
appetizers_menu.add_element(
    title='ارز مبهر', image_url='https://i.ibb.co/p3d9vFv/image.png', buttons=spicy_rice.buttons)

# Sauces
sauces = GenericTemplate()
sauces.add_element(
    title='Cheddar Sauce', image_url='https://i.ibb.co/C0515Cr/image.png', buttons=cheddar_sauce.buttons)
sauces.add_element(
    title='Ranch Sauce', image_url='https://i.ibb.co/C0515Cr/image.png', buttons=ranch_sauce.buttons)
sauces.add_element(
    title='1000 Island Sauce', image_url='https://i.ibb.co/C0515Cr/image.png', buttons=island1000.buttons)
sauces.add_element(
    title='BBQ Sauce', image_url='https://i.ibb.co/C0515Cr/image.png', buttons=bbq_sauce.buttons)
sauces.add_element(
    title='Trex Sauce', image_url='https://i.ibb.co/C0515Cr/image.png', buttons=trex_sauce.buttons)
sauces.add_element(
    title='Cola (350ml)', image_url='https://i.ibb.co/C0515Cr/image.png', buttons=cola.buttons)
sauces.add_element(
    title='Small Water', image_url='https://i.ibb.co/C0515Cr/image.png', buttons=water.buttons)
