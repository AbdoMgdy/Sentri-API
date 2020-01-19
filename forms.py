from flask_wtf import FlaskForm
from wtforms import StringField, SelectField
from wtforms.validators import data_required


class OrderForm(FlaskForm):
    quantity = SelectField('Quantity الكمية', choices=[
                           (1, 1), (2, 2), (3, 3), (4, 4)])
    spicy = SelectField('عادي أم سبايسي؟', choices=[
                        ('Spicy', 'سبايسي'), ('Normal', 'عادي')])
    notes = StringField('اضافة ملحوظة؟', render_kw={
                        'placeholder': 'مثال: 3 قطع فقط سبايسي أو بدون بصل'})


class SignUpForm(FlaskForm):
    name = StringField('الاسم', render_kw={
        'placeholder': 'من فضلك أدخل اسمك'})
    phone_number = StringField('رقم الموبيل', render_kw={
        'placeholder': 'من فضلك أدخل رقم هاتف صحيح'})
    address = StringField('العنوان', render_kw={
        'placeholder': 'من فضلك أدخل عنوان صحيح'})
