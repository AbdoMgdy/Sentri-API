from models.generic import GenericTemplate
from models.text import TextTemplate
from models.media import MediaTemplate
from resources.buttons import *


# Welcome Message
welcome_message = TextTemplate()
welcome_message.set_text('مرحبا بك في تركس تشيكن كيف أستطيع مساعدتك؟')
welcome_message.add_quick_replies(
    **{'ابدأ أوردر': 'main_menu', 'المنيو': 'send_menu', 'العنوان والتليفون': 'info'})

# Info Message
info_menu = TextTemplate()
info_menu.set_text(
    'رقم التليفون للدليفري وطلبات التوصيل:01206444463\nالعنوان: شيراتون المطار - شارع البحر \nمواعيد العمل: من 10 ص حتي 3 ص')
info_menu.add_quick_replies(
    **{'Back العودة للخلف': 'get_started'})

"""
{
    'sandwiches_menu': {
        {
            'title': 'smoke',
            'subtitle': 'ss',
            'image_url': '',
            'buttons': {
                'title': 'btn_ttl'
                'type': 'web_url',
                'url': '.com',
            }
        }
    }
}
"""

# Menu Media
m1 = MediaTemplate(
    url='https://www.facebook.com/trexchick/photos/482039192561576/')
m2 = MediaTemplate(
    url='https://www.facebook.com/trexchick/photos/482039212561574/')
m3 = MediaTemplate(
    url='https://www.facebook.com/trexchick/photos/482039115894917/')
m4 = MediaTemplate(
    url='https://www.facebook.com/trexchick/photos/482039079228254/')
m5 = MediaTemplate(
    url='https://www.facebook.com/trexchick/photos/482039319228230/')

# Main Menu
main_menu = GenericTemplate()

main_menu.add_element(title="Family Meals الوجبات العائلية", image_url='https://i.ibb.co/N7Z2Y0Y/image.png',
                      buttons=family.buttons)
main_menu.add_element(title="Sandwiches الساندوتشات", image_url="https://i.ibb.co/Tv5xkK6/image.png",
                      buttons=sandwiches.buttons)
main_menu.add_element(title="Trex Meals وجبات تركس", image_url="https://i.ibb.co/p3d9vFv/image.png",
                      buttons=trex_meals.buttons)
main_menu.add_element(title="Trex Special", image_url="https://i.ibb.co/VL52hzd/image.png",
                      buttons=special.buttons)
main_menu.add_element(title="Kids Meals وجبات الأطفال",
                      image_url="https://i.ibb.co/p3d9vFv/image.png",
                      buttons=kids_meals.buttons)
main_menu.add_element(title="Appetizers المقبلات", image_url="https://i.ibb.co/Qd33WPG/image.png",
                      buttons=appetizers.buttons)
main_menu.add_element(title="Sauces الصوصات", image_url="https://i.ibb.co/C0515Cr/image.png",
                      buttons=sauces.buttons)

# Family Menu
family_menu = GenericTemplate()

family_menu.add_element(
    title="وجبة 9 قطع دجاج", subtitle='عدد 9 قطع دجاج + بطاطس كبير + كول سلو + خبز + لتر كولا ', image_url='https://i.ibb.co/N7Z2Y0Y/image.png', buttons=chicken9.buttons)
family_menu.add_element(
    title="وجبة 12 قطع دجاج", subtitle='عدد 12 قطعة دجاج + بطاطس كبير + كول سلو + خبز + لتر كولا ', image_url='https://i.ibb.co/N7Z2Y0Y/image.png', buttons=chicken12.buttons)
family_menu.add_element(
    title="وجبة 15 قطع دجاج", subtitle='عدد 15 قطعة دجاج + بطاطس كبير + كول سلو + خبز + لتر كولا ', image_url='https://i.ibb.co/N7Z2Y0Y/image.png', buttons=chicken15.buttons)
family_menu.add_element(
    title="وجبة 18 قطع دجاج", subtitle='عدد 18 قطعة دجاج + بطاطس كبير + كول سلو + خبز + لتر كولا ', image_url='https://i.ibb.co/N7Z2Y0Y/image.png', buttons=chicken18.buttons)
family_menu.add_quick_replies(**{'Back العودة للخلف': 'main_menu'})

# Sandwiches Menu
sandwiches_menu = GenericTemplate()

sandwiches_menu.add_element(
    title='Original أوريجينال', subtitle='قطعة من الدجاج الكرسبي + المايونيز + جبنة الشيدر + صوص تركس الشهير', image_url='https://i.ibb.co/Tv5xkK6/image.png', buttons=original.buttons)
sandwiches_menu.add_element(
    title='Smoke House سموك هاوس', subtitle='صدور الدجاج الكرسبي مع حلقات البصل + بيف بيكون + صوصات تركس الشهيرة', image_url='https://i.ibb.co/wMX5Kfd/image.png', buttons=somke_house.buttons)
sandwiches_menu.add_element(
    title='Boom Mozzarella بوم موتزاريلا', subtitle='صدور الدجاج الكرسبي + اصابع مزاريلا + صوص الجبنة الشيدر + صوص تركس الشهير', image_url='https://i.ibb.co/3FC4fpy/image.png', buttons=boom_mozzarella.buttons)
sandwiches_menu.add_element(
    title='Spicy Houston سبايسي هيوستون', subtitle='صدور الدجاج الكرسبي + مايونيز + فلفل هالبينو الحار + اصابع شيدر +صوص تركس الشهير', image_url='https://i.ibb.co/5r7m8BT/image.png', buttons=spicy_houston.buttons)
sandwiches_menu.add_element(
    title='Down Bacon داون بيكون', subtitle='قعطتين من الدجاج الكرسبي + مايونيز + بيكون + جبنة شيدر + صوص تركس الشهير', image_url='https://i.ibb.co/MSYk3Pt/image.png', buttons=down_bacon.buttons)
sandwiches_menu.add_element(
    title='Down Turkey داون تركي', subtitle='قطعتين دجاج كرسبي + جبنة شيدر + تركي مدخن + صوص تركس الشهير', image_url='https://i.ibb.co/80wvH2C/image.png', buttons=down_turkey.buttons)
sandwiches_menu.add_element(
    title='Chicken Pizza تشيكن بيتزا', subtitle='قطعتين دجاج كرسبي 300جم + صوص جبنة شيدر + جبنة موتزاريلا + فلفل ألوان + زيتون', image_url='https://i.ibb.co/9cM6Sq2/image.png', buttons=chicken_pizza.buttons)
sandwiches_menu.add_element(
    title='Troodon تروودون', subtitle='فطعتين دجاج كرسبي 300جم+بيف بيكون+ صوص الجبنة الشيدر+تركي مدخن+صوص تركس الشهير', image_url='https://i.ibb.co/59fzrqN/image.png', buttons=troodon.buttons)
sandwiches_menu.add_element(
    title='Heavey Trex هيفي تركس', subtitle='3 قطع دجاج كرسبي + جبنة شيدر + تركي مدخن + بيف بيكون + صوصات تركس المشهورة', image_url='https://i.ibb.co/JCGSLf4/image.png', buttons=heavey_trex.buttons)
sandwiches_menu.add_quick_replies(**{'Back العودة للخلف': 'main_menu'})

# Trex Special
special_menu = GenericTemplate()

special_menu.add_element(
    title='Trex Waffle تركس وافل', subtitle='قطع الوافل المقرمشة مع الدجاج الكرسبي وبيف بيكون وصوصات تركس الشهيرة', image_url='https://i.ibb.co/VL52hzd/image.png', buttons=trex_waffle.buttons)

special_menu.add_element(
    title='Route 66 روت 66', subtitle='شرائح التوست المحمصة بالزبدة ودجاج الكرسبي + مشروم + بصل + صوص تركس الشهير', image_url='https://i.ibb.co/BZwbF3H/66.png', buttons=route66.buttons)

special_menu.add_element(
    title='َQuesadilla كاساديا', subtitle='خبز التورتيلا مع الدجاج المقرمش بصوص جبنة الشيدر  والجبنة الموتزاريلا والفلفل', image_url='https://i.ibb.co/cxcN6pn/image.png', buttons=quesadilla.buttons)

special_menu.add_element(
    title='َMexican Wrap ميكسيكان راب', subtitle='خبز التورتيلا الشهير و جبنة شيدر وقطعة الدجاج الكرسبي + جبنة موتزاريلا وصوص تركس', image_url='https://i.ibb.co/LJxBy2H/image.png', buttons=mexican_wrap.buttons)
special_menu.add_quick_replies(**{'Back العودة للخلف': 'main_menu'})

# Trex Meals

trex_meals_menu = GenericTemplate()

trex_meals_menu.add_element(
    title='Trex تركس', subtitle='عدد 2 قطع دجاج + 2 استربس + خبز + بطاطس + كول سلو', image_url='https://i.ibb.co/p3d9vFv/image.png', buttons=trex.buttons)
trex_meals_menu.add_element(
    title='Dinner Box دينر بوكس', subtitle='عدد 3 قطع دجاج + بطاطس + خبز + كول سلو', image_url='https://i.ibb.co/p3d9vFv/image.png', buttons=dinner_box.buttons)
trex_meals_menu.add_element(
    title='Snack Box سناك بوكس', subtitle='عدد 2 قطع دجاج + بطاطس ', image_url='https://i.ibb.co/p3d9vFv/image.png', buttons=snack_box.buttons)
trex_meals_menu.add_element(
    title='Turkey Box تركي بوكس', subtitle='عدد 3 قطع فيليه تركي + بطاطس + خبز + كول سلو', image_url='https://i.ibb.co/p3d9vFv/image.png', buttons=turkey_box.buttons)
trex_meals_menu.add_element(
    title='Crispy Strips كرسبي ستربس', subtitle='عدد 3 قطع استربس + بطاطس', image_url='https://i.ibb.co/p3d9vFv/image.png', buttons=crispy_strips.buttons)
trex_meals_menu.add_element(
    title='Jumbo Crispy Strips', subtitle='عدد 5 قطع استربس + خبز + بطاطس', image_url='https://i.ibb.co/p3d9vFv/image.png', buttons=jumbo_crispy_strips.buttons)
trex_meals_menu.add_quick_replies(**{'Back العودة للخلف': 'main_menu'})


# Kids Meals
kids_menu = GenericTemplate()
kids_menu.add_element(
    title='َوجبة أطفال قطعة دجاج', subtitle='قطعة دجاج + فرايز + عصير', image_url='https://i.ibb.co/p3d9vFv/image.png', buttons=kids_chicken_piece.buttons)
kids_menu.add_element(
    title='َوجبة أطفال 2 استربس', subtitle='عدد 2 استربس + فرايز + عصير', image_url='https://i.ibb.co/p3d9vFv/image.png', buttons=kids_chicken_strips.buttons)
kids_menu.add_quick_replies(**{'Back العودة للخلف': 'main_menu'})


# Appetizers

appetizers_menu = GenericTemplate()
appetizers_menu.add_element(
    title='َأصابع موتزاريلا 3 قطع', image_url='https://i.ibb.co/5kKv6cj/4.jpg', buttons=mozzarella_sticks.buttons)
appetizers_menu.add_element(
    title='َحلقات البصل 5 قطع', image_url='https://i.ibb.co/6ww7L1t/3.jpg', buttons=onion_rings.buttons)
appetizers_menu.add_element(
    title='َأصابع هالبينو شيدر 3 قطع', image_url='https://i.ibb.co/Gk7hsWp/2.jpg', buttons=onion_rings.buttons)
appetizers_menu.add_element(
    title='ميكسيكان فرايز', image_url='https://i.ibb.co/PtW4C61/1.jpg', buttons=mexican_fries.buttons)
appetizers_menu.add_element(
    title='ريزو', image_url='https://i.ibb.co/PtW4C61/1.jpg', buttons=rizo.buttons)
appetizers_menu.add_element(
    title='ارز مبهر', image_url='https://i.ibb.co/PtW4C61/1.jpg', buttons=spicy_rice.buttons)
appetizers_menu.add_quick_replies(**{'Back العودة للخلف': 'main_menu'})

# Sauces
sauces = GenericTemplate()
sauces.add_element(
    title='Cheddar Sauce', image_url='https://i.ibb.co/Rz4nXYF/5.jpg', buttons=cheddar_sauce.buttons)
sauces.add_element(
    title='Ranch Sauce', image_url='https://i.ibb.co/fH7r0Y1/4.jpg', buttons=ranch_sauce.buttons)
sauces.add_element(
    title='1000 Island Sauce', image_url='https://i.ibb.co/pJMjz9h/3.jpg', buttons=island1000.buttons)
sauces.add_element(
    title='BBQ Sauce', image_url='https://i.ibb.co/H7mgSQh/2.jpg', buttons=bbq_sauce.buttons)
sauces.add_element(
    title='Trex Sauce', image_url='https://i.ibb.co/yqp4S0n/1.jpg', buttons=trex_sauce.buttons)
sauces.add_element(
    title='Cola (350ml)', image_url='', buttons=cola.buttons)
sauces.add_element(
    title='Small Water', image_url='', buttons=water.buttons)
sauces.add_quick_replies(**{'Back العودة للخلف': 'main_menu'})
