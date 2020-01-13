from templates.generic import GenericTemplate
from templates.button import ButtonTemplate
from templates.quick_replies import QuickReplies


family = ButtonTemplate()
family.add_postback(**{'Go to Menu':'menu.children[0]'})

specials = ButtonTemplate()
specials.add_postback(title='Specials', payload='specials')

sandwiches = ButtonTemplate()
sandwiches.add_postback(**{'Go Back':'none for now'})


family_buttons = ButtonTemplate()
family_buttons.add_postback(**{'Go Back':'family_menu.parent'})

qr = QuickReplies()
qr.add_quick_replies(**{'1st qr': 'family_menu.parent', 'go back': 'family_menu.parent'})


menu = GenericTemplate()

menu.add_element(title="Family",image_url="https://petersfancybrownhats.com/company_image.png", subtitle="Family Menu", buttons=family.buttons)
menu.add_element(title="Specials",image_url="https://petersfancybrownhats.com/company_image.png", subtitle="Specials Menu", buttons=specials.buttons)
menu.add_element(title="Sandwiches",image_url="https://petersfancybrownhats.com/company_image.png", subtitle="Sandwiches Menu", buttons=sandwiches.buttons)

family_menu = GenericTemplate(parent=menu, quick_replies=qr.quick_replies)
family_menu.add_element(title="1st Sandwich", image_url="https://petersfancybrownhats.com/company_image.png",subtitle="2nd Sandwich Sub Menu", buttons=family_buttons.buttons)

