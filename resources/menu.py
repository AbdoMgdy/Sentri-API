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

family_menu.add_element(title="Burger", image_url='https://doc-0s-ak-docs.googleusercontent.com/docs/securesc/3qkntbp784gih25oroho3r47me1jgmch/jlphga688uc6jes8ulatpn61h1hgeg64/1579572000000/13568283427112821664/09937701626796241172/1kCvZ1JOQvlCGI5iAdXqoIyBGPyBA44dQ?e=view&authuser=0&nonce=9dq5r4moebq3k&user=09937701626796241172&hash=o066diajn9fht9gcisod7gdb80hkr8cd', buttons=burger_btn.buttons)
family_menu.add_element(title="9 Chicken", image_url='https://doc-00-ak-docs.googleusercontent.com/docs/securesc/3qkntbp784gih25oroho3r47me1jgmch/pbr33fracf5t7ao9t794jtv5v80006vl/1579572000000/13568283427112821664/09937701626796241172/185HZ6ei1bUL-bbzjM05Wo_UOnbalU_Ur?e=view&authuser=0' buttons=meal_btn.buttons)
family_menu.add_element(title="Sauce", image_url='https://doc-0s-ak-docs.googleusercontent.com/docs/securesc/3qkntbp784gih25oroho3r47me1jgmch/fojum5edfgeuhafqfo1l9ib0v07js3jq/1579572000000/13568283427112821664/09937701626796241172/1xmGNqrIHzhYbYsvVdTWTsZ9eIjbp8uDm?e=view&authuser=0' buttons=sauce_btn.buttons)
# family_menu.add_quick_replies(**{'Back العودة للخلف': 'main_menu'})
