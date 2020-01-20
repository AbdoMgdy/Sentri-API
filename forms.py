from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, FormField, FieldList
from wtforms.fields.html5 import TelField


class OrderSandwich(FlaskForm):
    quantity = SelectField('Quantity الكمية', choices=[
                           (1, 1), (2, 2), (3, 3), (4, 4)])
    spicy = SelectField('عادي أم سبايسي؟', choices=[
                        ('Spicy', 'سبايسي'), ('Normal', 'عادي')])
    notes = StringField('اضافة ملحوظة؟', render_kw={
        'placeholder': 'مثال: 3 قطع فقط سبايسي أو بدون بصل'})
    combo = SelectField('اضافة كومبو بـ15ج (بطاطس + كولا)', choices=[(0, 'لا No'),
                                                                     (15, 'نعم Yes')])


class OrderMeal(FlaskForm):
    quantity = SelectField('Quantity الكمية', choices=[
                           (1, 1), (2, 2), (3, 3), (4, 4)])
    spicy = SelectField('عادي أم سبايسي؟', choices=[
                        ('Spicy', 'سبايسي'), ('Normal', 'عادي')])
    notes = StringField('اضافة ملحوظة؟', render_kw={
        'placeholder': 'مثال: 3 قطع فقط سبايسي أو بدون بصل'})


class OrderSauce(FlaskForm):
    quantity = SelectField('Quantity الكمية', choices=[
                           (1, 1), (2, 2), (3, 3), (4, 4)])


class SignUpForm(FlaskForm):
    name = StringField('الاسم', render_kw={
        'placeholder': 'من فضلك أدخل اسمك'})
    phone_number = TelField('رقم الموبيل', _prefix='20', render_kw={
        'placeholder': 'من فضلك أدخل رقم هاتف صحيح'})
    address = StringField('العنوان', render_kw={
        'placeholder': 'من فضلك أدخل عنوان صحيح'})


class EditOrderForm(FlaskForm):
    items = FieldList(FormField(OrderSandwich))
