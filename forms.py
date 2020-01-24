from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, FormField, FieldList
from wtforms.validators import DataRequired
from wtforms.fields.html5 import TelField


class OrderSandwich(FlaskForm):
    quantity = SelectField('Quantity الكمية', choices=[
                           (1, 1), (2, 2), (3, 3), (4, 4)])
    spicy = SelectField('عادي أم سبايسي؟', choices=[('Normal', 'عادي'),
                                                    ('Spicy', 'سبايسي')])
    notes = StringField('اضافة ملحوظة؟', render_kw={
        'placeholder': 'اضافة ملحوظة'})
    combo = SelectField('اضافة كومبو بـ15ج (بطاطس + كولا)', choices=[(0, 'بدون كومبو'),
                                                                     (15, 'اضف كومبو (بطاطس + كولا) بـ15ج')])


class OrderMeal(FlaskForm):
    quantity = SelectField('Quantity الكمية', choices=[
                           (1, 1), (2, 2), (3, 3), (4, 4)])
    spicy = SelectField('عادي أم سبايسي؟', choices=[('Normal', 'عادي'),
                                                    ('Spicy', 'سبايسي')])
    notes = StringField('اضافة ملحوظة؟', render_kw={
        'placeholder': 'اضافة ملحوظة؟'})


class OrderSauce(FlaskForm):
    quantity = SelectField('Quantity الكمية', choices=[
                           (1, 1), (2, 2), (3, 3), (4, 4)])


class SignUpForm(FlaskForm):
    name = StringField('الاسم', [DataRequired()], render_kw={
        'placeholder': 'من فضلك أدخل اسمك'})
    phone_number = TelField('رقم الموبيل', [DataRequired()], _prefix='20', render_kw={
        'placeholder': 'من فضلك أدخل رقم هاتف صحيح'})
    address = StringField('العنوان', [DataRequired()], render_kw={
        'placeholder': 'من فضلك أدخل عنوان صحيح'})


class EditOrderForm(FlaskForm):
    items = FieldList(FormField(OrderSandwich))
