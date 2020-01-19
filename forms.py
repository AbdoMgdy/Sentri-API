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
    combo = SelectField('اضافة كومبو بـ15ج (بطاطس + كولا)', choices=[(15, 'لا No'),
                                                                     (0, 'نعم Yes')])


class SignUpForm(FlaskForm):
    name = StringField('الاسم', render_kw={
        'placeholder': 'من فضلك أدخل اسمك'})
    phone_number = StringField('رقم الموبيل', render_kw={'type': 'tel',
                                                         'pattern': '[0-9]{3}-[0-9]{4}-[0-9]{4}',
                                                         'placeholder': 'من فضلك أدخل رقم هاتف صحيح'})
    address = StringField('العنوان', render_kw={
        'placeholder': 'من فضلك أدخل عنوان صحيح'})
