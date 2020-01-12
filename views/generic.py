from templates.generic import GenericTemplate
from templates.button import ButtonTemplate


family_buttons = ButtonTemplate()
family_buttons.add_postback(title='Family', payload='familyMenu')

specials_buttons = ButtonTemplate()
specials_buttons.add_postback(title='Specials', payload='specialsMenu')

sandwiches_buttons = ButtonTemplate()
sandwiches_buttons.add_postback(title='Sandwiches', payload='sandwichesMenu')

menu = GenericTemplate()

menu.add_element(title="Family",image_url="https://petersfancybrownhats.com/company_image.png", subtitle="test", buttons=family_buttons)
menu.add_element(title="Specials",image_url="https://petersfancybrownhats.com/company_image.png", subtitle="test", buttons=specials_buttons)
menu.add_element(title="Sandwiches",image_url="https://petersfancybrownhats.com/company_image.png", subtitle="test", buttons=sandwiches_buttons)

