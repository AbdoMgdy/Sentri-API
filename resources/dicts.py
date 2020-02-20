from resources.menu import *
# blocks = {
#     'get_started': welcome_message,
#     'main_menu': main_menu,
#     'family_menu': family_menu,
#     'sandwiches_menu': sandwiches_menu,
#     'trex_meals_menu': trex_meals_menu,
#     'special_menu': special_menu,
#     'kids_meals_menu': kids_menu,
#     'appetizers_menu': appetizers_menu,
#     'sauces_menu': sauces,
#     'info': info_menu,
#     'confirm_block': confirm_block,
# }


access_tokens = {
    '103750251156613': 'EAAF5Cd9fC3YBAD6cfpba6mDeKm5BYvovVZBciSRCzMfjJ9SMTKiQ2pQgxc9r68ZAyyPTICHs7qYcFov3SSZCrI9ImcvvnXqVZAKZAOlgUeW8oZAMP2DQZCA1xe8WSkq0a7ozUsZAIdZA1zX5wFLuNp57YzUhv1hedFZAN61Q8ajJxDqAZDZD',
    '2163571837030935': 'EAAF5Cd9fC3YBALSQ2BjRm5b2uovOkt8TwfJm2jSK4VPwZBLFFA8AA81NGJR8M6udWJhsejjZB9Gs4hYY8bjuxLbwUFXuqOMCjwq6GoL73KPkboq7f1YQEMRfbfxokasM2ZCkahXCAt82ZBHLBSif4XZCwz6BYtkvAKNOmu5N7iAZDZD',
    '2190651954374978': 'EAAF5Cd9fC3YBAE8JUS0LE4HiaZCzuUnPbZAvmeB30jEgNsxD9NWZBqOc4ULq3LEzlyyfWzZBFcoxhQllGscl1HZCkfZCYvxvw13BEZAZAPvn3IVhZAykNgjXbYVn6XZC6nCTAZCZASad4vkNAyxaoLoDPhuKZAXPkS4wf2ydU3Y90crBE2AZDZD'
}

orders = {}

prices = {
    '103750251156613': {
        # Family Meals
        '9-Chicken': 155,
        '12-Chicken': 196,
        '15-Chicken': 230,
        '18-Chicken': 270,
        # Sandwiches
        'Original-150': 32,
        'Original-300': 45,
        'Smoke-House-150': 45,
        'Smoke-House-300': 58,
        'Boom-Mozzarella-150': 65,
        'Boom-Mozzarella-300': 78,
        'Spicy-Houstn-150': 67,
        'Spicy-Houstn-300': 78,
        'Down-Bacon-300': 65,
        'Down-Bacon-450': 78,
        'Down-Turkey-300': 65,
        'Down-Turkey-450': 78,
        'Troodon': 80,
        'Chiken-Pizza': 42,
        'Heavy-Trex': 90,
        # Trex Special
        'Trex-Waffle-150': 60,
        'Trex-Waffle-300': 75,
        'Route-66': 45,
        'Quesadilla': 45,
        'Mexican-Wrap': 35,
        # Trex Meals
        'Trex': 55,
        'Dinner-Box': 55,
        'Snack-Box': 38,
        'Turkey-Box': 70,
        'Jumbo-Crispy-Strips': 50,
        'Crispy-Strips': 35,
        # Appetizers
        'Mozzarella-Sticks': 30,
        'Jalapeno-Sticks': 32,
        'Onion-Rings': 20,
        'Mexican-Fries': 30,
        'Rizo': 20,
        'Spicy-Rice': 10,
        # Kids Meals
        'Kids-Chicken-Piece': 29,
        'Kids-Chicken-Strips': 29,
        # Sauces
        'Cheddar-Sauce': 10,
        '1000-Island-Sauce': 10,
        'BBQ-Sauce': 10,
        'Trex-Sauce': 10,
        'Coleslaw-Small': 10,
        'Coleslaw-Large': 20,
        'Cola': 10,
        'Water': 7,
    },
    '2163571837030935': {
        # Family Meals
        '9-Chicken': 155,
        '12-Chicken': 196,
        '15-Chicken': 230,
        '18-Chicken': 270,
        # Sandwiches
        'Original-150': 32,
        'Original-300': 45,
        'Smoke-House-150': 45,
        'Smoke-House-300': 58,
        'Boom-Mozzarella-150': 65,
        'Boom-Mozzarella-300': 78,
        'Spicy-Houstn-150': 67,
        'Spicy-Houstn-300': 78,
        'Down-Bacon-300': 65,
        'Down-Bacon-450': 78,
        'Down-Turkey-300': 65,
        'Down-Turkey-450': 78,
        'Troodon': 80,
        'Chiken-Pizza': 42,
        'Heavy-Trex': 90,
        # Trex Special
        'Trex-Waffle-150': 60,
        'Trex-Waffle-300': 75,
        'Route-66': 45,
        'Quesadilla': 45,
        'Mexican-Wrap': 35,
        # Trex Meals
        'Trex': 55,
        'Dinner-Box': 55,
        'Snack-Box': 38,
        'Turkey-Box': 70,
        'Jumbo-Crispy-Strips': 50,
        'Crispy-Strips': 35,
        # Appetizers
        'Mozzarella-Sticks': 30,
        'Jalapeno-Sticks': 32,
        'Onion-Rings': 20,
        'Mexican-Fries': 30,
        'Rizo': 20,
        'Spicy-Rice': 10,
        # Kids Meals
        'Kids-Chicken-Piece': 29,
        'Kids-Chicken-Strips': 29,
        # Sauces
        'Cheddar-Sauce': 10,
        '1000-Island-Sauce': 10,
        'BBQ-Sauce': 10,
        'Trex-Sauce': 10,
        'Coleslaw-Small': 10,
        'Coleslaw-Large': 20,
        'Cola': 10,
        'Water': 7,
    },
}

arabic = {
    '103750251156613': {
        'Spicy': 'سبايسي',
        'Normal': 'عادي',
        # Family Meals
        '9-Chicken': 'وجبة 9 قطع دجاج',
        '12-Chicken': 'وجبة 12 قطع دجاج',
        '15-Chicken': 'وجبة 15 قطع دجاج',
        '18-Chicken': 'وجبة 18 قطع دجاج',
        # Sandwiches
        'Original-150': 'أوريجينال 150جم',
        'Original-300': 'أوريجينال 300جم',
        'Smoke-House-150': 'سموك هاوس 150جم',
        'Smoke-House-300': 'سموك هاوس 300جم',
        'Boom-Mozzarella-150': 'بووم موتزاريلا 150جم',
        'Boom-Mozzarella-300': 'بووم موتزاريلا 300جم',
        'Spicy-Houstn-150': 'سبايسي هيوستن 150جم',
        'Spicy-Houstn-300': 'سبايسي هيوستن 300جم',
        'Down-Bacon-300': 'داون بيكون 300جم',
        'Down-Bacon-450': 'داون بيكون 450جم',
        'Down-Turkey-300': 'داون تركي 300جم',
        'Down-Turkey-450': 'داون تركي 450جم',
        'Troodon': 'تروودون',
        'Chiken-Pizza': 'تشيكن بيتزا',
        'Heavy-Trex': 'هيفي تركس',
        # Trex Special
        'Trex-Waffle-150': 'تركس وافل 150جم',
        'Trex-Waffle-300': 'تركس وافل 300جم',
        'Route-66': 'رووت 66',
        'Quesadilla': 'كاساديا',
        'Mexican-Wrap': 'ميكسيكان راب',
        # Trex Meals
        'Trex': 'تركس',
        'Dinner-Box': 'دينر بوكس',
        'Snack-Box': 'سناك بوكس',
        'Turkey-Box': 'تركي بوكس',
        'Jumbo-Crispy-Strips': 'جامبو كرسبي ستربس',
        'Crispy-Strips': 'كرسبي ستربس',
        # Appetizers
        'Mozzarella-Sticks': 'أصابع موتزاريلا',
        'Jalapeno-Sticks': 'أصابع هالبينو شيدر',
        'Onion-Rings': 'حلقات البصل',
        'Mexican-Fries': 'ميكسيكان فرايز',
        'Rizo': 'ريزو',
        'Spicy-Rice': 'أرز مبهر',
        # Kids Meals
        'Kids-Chicken-Piece': 'وجبة أطفال قطعة دجاج',
        'Kids-Chicken-Strips': 'وجبة أطفال ستربس',
        # Sauces
        'Cheddar-Sauce': 'صوص الشيدر',
        '1000-Island-Sauce': 'صوص 1000 Island',
        'BBQ-Sauce': 'صوص باربيكيو',
        'Trex-Sauce': 'صوص تركس',
        'Coleslaw-Small': 'كول سلو صغير',
        'Coleslaw-Large': 'كول سلو كبير',
        'Cola': 'كولا 350 ملل',
        'Water': 'مياه صغير',
    },
    '2163571837030935': {
        'Spicy': 'سبايسي',
        'Normal': 'عادي',
        # Family Meals
        '9-Chicken': 'وجبة 9 قطع دجاج',
        '12-Chicken': 'وجبة 12 قطع دجاج',
        '15-Chicken': 'وجبة 15 قطع دجاج',
        '18-Chicken': 'وجبة 18 قطع دجاج',
        # Sandwiches
        'Original-150': 'أوريجينال 150جم',
        'Original-300': 'أوريجينال 300جم',
        'Smoke-House-150': 'سموك هاوس 150جم',
        'Smoke-House-300': 'سموك هاوس 300جم',
        'Boom-Mozzarella-150': 'بووم موتزاريلا 150جم',
        'Boom-Mozzarella-300': 'بووم موتزاريلا 300جم',
        'Spicy-Houstn-150': 'سبايسي هيوستن 150جم',
        'Spicy-Houstn-300': 'سبايسي هيوستن 300جم',
        'Down-Bacon-300': 'داون بيكون 300جم',
        'Down-Bacon-450': 'داون بيكون 450جم',
        'Down-Turkey-300': 'داون تركي 300جم',
        'Down-Turkey-450': 'داون تركي 450جم',
        'Troodon': 'تروودون',
        'Chiken-Pizza': 'تشيكن بيتزا',
        'Heavy-Trex': 'هيفي تركس',
        # Trex Special
        'Trex-Waffle-150': 'تركس وافل 150جم',
        'Trex-Waffle-300': 'تركس وافل 300جم',
        'Route-66': 'رووت 66',
        'Quesadilla': 'كاساديا',
        'Mexican-Wrap': 'ميكسيكان راب',
        # Trex Meals
        'Trex': 'تركس',
        'Dinner-Box': 'دينر بوكس',
        'Snack-Box': 'سناك بوكس',
        'Turkey-Box': 'تركي بوكس',
        'Jumbo-Crispy-Strips': 'جامبو كرسبي ستربس',
        'Crispy-Strips': 'كرسبي ستربس',
        # Appetizers
        'Mozzarella-Sticks': 'أصابع موتزاريلا',
        'Jalapeno-Sticks': 'أصابع هالبينو شيدر',
        'Onion-Rings': 'حلقات البصل',
        'Mexican-Fries': 'ميكسيكان فرايز',
        'Rizo': 'ريزو',
        'Spicy-Rice': 'أرز مبهر',
        # Kids Meals
        'Kids-Chicken-Piece': 'وجبة أطفال قطعة دجاج',
        'Kids-Chicken-Strips': 'وجبة أطفال ستربس',
        # Sauces
        'Cheddar-Sauce': 'صوص الشيدر',
        '1000-Island-Sauce': 'صوص 1000 Island',
        'BBQ-Sauce': 'صوص باربيكيو',
        'Trex-Sauce': 'صوص تركس',
        'Coleslaw-Small': 'كول سلو صغير',
        'Coleslaw-Large': 'كول سلو كبير',
        'Cola': 'كولا 350 ملل',
        'Water': 'مياه صغير',
    }
}

menus = {
    '103750251156613': {
        'welcome_message': {
            'payload': {
                'template_type': 'generic',
                'elements': [
                    {
                        'title': 'مرحبا بك كيف أستطيع مساعدتك؟',
                        'image_url': '',
                        'subtitle': '',
                        'buttons': [{
                            'type': 'postback',
                            'title': 'ابدأ أوردر',
                            'payload': 'main_menu'
                        }]

                    }
                ]
            },
            'qucik_replies': [
                {
                    'content_type': 'text',
                    'title': 'ابدأ أوردر',
                    'payload': 'main_menu',
                }
            ]
        },
        'main_menu': {
            'payload': {
                'template_type': 'generic',
                'elements': [
                    {
                        'title': 'Family Menu',
                        'image_url': 'https://i.ibb.co/N7Z2Y0Y/image.png',
                        'subtitle': '',
                        'buttons': [{
                            'type': 'postback',
                            'title': 'Show Menu',
                            'payload': 'family_menu'
                        }]
                    }
                ]
            },
            'quick_replies': [
                {
                    'content_type': 'text',
                    'title': 'back',
                    'payload': 'main_menu',
                }
            ]
        },
        'family_menu': {
            'payload': {
                'template_type': 'generic',
                'elements': [
                    {
                        'title': '9 Chicken',
                        'image_url': 'https://i.ibb.co/N7Z2Y0Y/image.png',
                        'subtitle': '',
                        'buttons': [{
                            'type': 'web_url',
                            'title': 'Buy',
                            'url': 'https://rest-bot-dev.herokuapp.com/webview/order/meal/9-Chicken',
                            'webview_height_ratio': 'tall',
                            'messenger_extensions': 'true'
                        }]
                    },
                    {
                        'title': '12 Chicken',
                        'image_url': 'https://i.ibb.co/N7Z2Y0Y/image.png',
                        'subtitle': '',
                        'buttons': [{
                            'type': 'web_url',
                            'title': 'Buy',
                            'url': 'https://rest-bot-dev.herokuapp.com/webview/order/meal/12-Chicken',
                            'webview_height_ratio': 'tall',
                            'messenger_extensions': 'true'
                        }]
                    },
                    {
                        'title': '15 Chicken',
                        'image_url': 'https://i.ibb.co/N7Z2Y0Y/image.png',
                        'subtitle': '',
                        'buttons': [{
                            'type': 'web_url',
                            'title': 'Buy',
                            'url': 'https://rest-bot-dev.herokuapp.com/webview/order/meal/15-Chicken',
                            'webview_height_ratio': 'tall',
                            'messenger_extensions': 'true'
                        }]
                    },
                    {
                        'title': '18 Chicken',
                        'image_url': 'https://i.ibb.co/N7Z2Y0Y/image.png',
                        'subtitle': '',
                        'buttons': [{
                            'type': 'web_url',
                            'title': 'Buy',
                            'url': 'https://rest-bot-dev.herokuapp.com/webview/order/meal/18-Chicken',
                            'webview_height_ratio': 'tall',
                            'messenger_extensions': 'true'

                        }]
                    }

                ]
            },

            'quick_replies': [
                {
                    'content_type': 'text',
                    'title': 'back',
                    'payload': 'main_menu',
                }
            ],
        },
        'sandwiches_menu': {},
        'trex_meals_menu': {},
        'special_menu': {},
        'kids_meals_menu': {},
        'appetizers_menu': {},
        'sauces_menu': {},
        'info': {},
        'confirm_block': {},
    },
    '2163571837030935': {
        'welcome_message': {
            'payload': {
                'template_type': 'generic',
                'elements': [
                    {
                        'title': 'مرحبا بك كيف أستطيع مساعدتك؟',
                        'image_url': '',
                        'subtitle': '',
                        'buttons': [{
                            'type': 'postback',
                            'title': 'ابدأ أوردر',
                            'payload': 'main_menu'
                        }]

                    }
                ]
            },
            'qucik_replies': [
                {
                    'content_type': 'text',
                    'title': 'ابدأ أوردر',
                    'payload': 'main_menu',
                }
            ]
        },
        'main_menu': {
            'payload': {
                'template_type': 'generic',
                'elements': [
                    {
                        'title': 'Family Menu of HO',
                        'image_url': 'https://i.ibb.co/N7Z2Y0Y/image.png',
                        'subtitle': '',
                        'buttons': [{
                            'type': 'postback',
                            'title': 'Show Menu',
                            'payload': 'family_menu'
                        }]
                    }
                ]
            },
            'quick_replies': [
                {
                    'content_type': 'text',
                    'title': 'back',
                    'payload': 'main_menu',
                }
            ]
        },
        'family_menu': {
            'payload': {
                'template_type': 'generic',
                'elements': [
                    {
                        'title': 'Burger',
                        'image_url': 'https://i.ibb.co/N7Z2Y0Y/image.png',
                        'subtitle': '',
                        'buttons': [{
                            'type': 'web_url',
                            'title': 'Buy',
                            'url': 'https://rest-bot-dev.herokuapp.com/webview/order/meal/burger',
                            'webview_height_ratio': 'tall',
                            'messenger_extensions': 'true'
                        }]
                    },
                    {
                        'title': 'big burger',
                        'image_url': 'https://i.ibb.co/N7Z2Y0Y/image.png',
                        'subtitle': '',
                        'buttons': [{
                            'type': 'web_url',
                            'title': 'Buy',
                            'url': 'https://rest-bot-dev.herokuapp.com/webview/order/meal/big-burger',
                            'webview_height_ratio': 'tall',
                            'messenger_extensions': 'true'
                        }]
                    },
                    {
                        'title': '15 Chicken',
                        'image_url': 'https://i.ibb.co/N7Z2Y0Y/image.png',
                        'subtitle': '',
                        'buttons': [{
                            'type': 'web_url',
                            'title': 'Buy',
                            'url': 'https://rest-bot-dev.herokuapp.com/webview/order/meal/15-Chicken',
                            'webview_height_ratio': 'tall',
                            'messenger_extensions': 'true'
                        }]
                    },
                    {
                        'title': '18 Chicken',
                        'image_url': 'https://i.ibb.co/N7Z2Y0Y/image.png',
                        'subtitle': '',
                        'buttons': [{
                            'type': 'web_url',
                            'title': 'Buy',
                            'url': 'https://rest-bot-dev.herokuapp.com/webview/order/meal/18-Chicken',
                            'webview_height_ratio': 'tall',
                            'messenger_extensions': 'true'

                        }]
                    }

                ]
            },

            'quick_replies': [
                {
                    'content_type': 'text',
                    'title': 'back',
                    'payload': 'main_menu',
                }
            ],
        },
        'sandwiches_menu': {},
        'trex_meals_menu': {},
        'special_menu': {},
        'kids_meals_menu': {},
        'appetizers_menu': {},
        'sauces_menu': {},
        'info': {},
        'confirm_block': {},
    },
}
