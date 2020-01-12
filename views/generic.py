from templates.generic import GenericTemplate
from templates.button import ButtonTemplate


family = ButtonTemplate()
family.add_postback(title='Family', payload=1)

specials = ButtonTemplate()
specials.add_postback(title='Specials', payload=2)

sandwiches = ButtonTemplate()
sandwiches.add_postback(title='Sandwiches', payload=3)

menu = GenericTemplate()

menu.add_element(title="Family",image_url="https://petersfancybrownhats.com/company_image.png", subtitle="test", buttons=family.buttons)
menu.add_element(title="Specials",image_url="https://petersfancybrownhats.com/company_image.png", subtitle="test", buttons=specials.buttons)
menu.add_element(title="Sandwiches",image_url="https://petersfancybrownhats.com/company_image.png", subtitle="test", buttons=sandwiches.buttons)

