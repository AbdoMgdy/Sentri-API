from resources.menu import *
from resources.buttons import confirm_block
blocks = {
    'get_started': main_menu,
    'main_menu': main_menu,
    'family_menu': family_menu,
    'sandwiches_menu': sandwiches_menu,
    'confirm_block': confirm_block,
}


orders = {}

prices = {
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
}
