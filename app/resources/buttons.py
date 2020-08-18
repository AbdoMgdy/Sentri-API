from app.models.button import ButtonTemplate

# Confirm Block
confirm_block = ButtonTemplate()
confirm_block.add_web_url(
    **{'تأكيد الأوردر': 'https://rest-bot-dev.herokuapp.com/confirm_order'})
confirm_block.add_postback(**{'اضافة للأوردر': 'main_menu'})
confirm_block.add_web_url(
    **{'تعديل الأوردر': 'https://rest-bot-dev.herokuapp.com/edit_order'})
