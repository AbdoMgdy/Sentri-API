from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, FormField, FieldList, PasswordField, BooleanField, SubmitField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from wtforms.fields.html5 import TelField
from app.vendor import Vendor


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()], render_kw={
        'placeholder': 'Username'})
    password = PasswordField('Password', validators=[DataRequired()], render_kw={
        'placeholder': 'Password'})
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Login')


class RegistrationForm(FlaskForm):
    name = StringField('الاسم', validators=[DataRequired()], render_kw={
        'placeholder': 'الاسم'})
    phone = TelField('التليفون', validators=[DataRequired()], _prefix='20', render_kw={
        'placeholder': 'التليفون'})
    address = StringField('العنوان', validators=[DataRequired()], render_kw={
        'placeholder': 'العنوان'})
    job = StringField('الوظيفة', validators=[DataRequired()], render_kw={
        'placeholder': 'الوظيفة'})
    manufactoror = StringField('الماركة', validators=[DataRequired()], render_kw={
        'placeholder': 'الماركة'})
    model = StringField('الموديل', validators=[DataRequired()], render_kw={
        'placeholder': 'الموديل'})
    submit = SubmitField('Register')


class OrderForm(FlaskForm):
    quantity = SelectField('الكمية', choices=[
        (1, 1), (2, 2), (3, 3), (4, 4), (5, 5)])
    spicy = SelectField('عادي أم سبايسي؟', choices=[('Normal', 'عادي'),
                                                    ('Spicy', 'سبايسي')])
    notes = StringField('اضافة ملحوظة؟', render_kw={
        'placeholder': 'اضافة ملحوظة'})
    combo = SelectField('اضافة كومبو (بطاطس + كولا)', choices=[(0, 'بدون كومبو'),
                                                               (15, 'اضف كومبو (بطاطس + كولا)')])


class OrderSandwich(FlaskForm):
    quantity = SelectField('الكمية', choices=[
        (1, 1), (2, 2), (3, 3), (4, 4)])
    spicy = SelectField('عادي أم سبايسي؟', choices=[('Normal', 'عادي'),
                                                    ('Spicy', 'سبايسي')])
    notes = StringField('اضافة ملحوظة؟', render_kw={
        'placeholder': 'اضافة ملحوظة'})
    combo = SelectField('اضافة كومبو (بطاطس + كولا)', choices=[(0, 'بدون كومبو'),
                                                               (15, 'اضف كومبو (بطاطس + كولا)')])


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


class CustomerInfo(FlaskForm):
    name = StringField('الاسم', render_kw={
        'placeholder': 'من فضلك أدخل اسمك'})
    phone_number = TelField('رقم الموبيل', _prefix='20', render_kw={
        'placeholder': 'من فضلك أدخل رقم هاتف صحيح'})
    address = StringField('العنوان', render_kw={
        'placeholder': 'من فضلك أدخل عنوان صحيح'})
