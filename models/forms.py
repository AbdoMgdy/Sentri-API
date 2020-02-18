from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, FormField, FieldList, PasswordField, BooleanField, SubmitField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from wtforms.fields.html5 import TelField
from models.data_models import Vendor


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()], render_kw={
        'placeholder': 'Username'})
    password = PasswordField('Password', validators=[DataRequired()], render_kw={
        'placeholder': 'Password'})
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Login')


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()], render_kw={
        'placeholder': 'Username'})
    vendor_name = StringField('Vendor Name', validators=[DataRequired()], render_kw={
        'placeholder': 'Vendor Name'})
    password = PasswordField('Password', validators=[DataRequired()], render_kw={
        'placeholder': 'Password'})
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')], render_kw={
            'placeholder': 'Repeat Password'})
    access_token = StringField('Access Token', validators=[DataRequired()], render_kw={
        'placeholder': 'Access Token'})
    admin_code = StringField('Admin Security Code', validators=[
                             DataRequired()], render_kw={'placeholder': 'Admin Security Code'})
    submit = SubmitField('Register')

    def validate_username(self, username):
        vendor = Vendor.query.filter_by(username=username.data).first()
        if vendor is not None:
            raise ValidationError('Please use a different username.')

    def validate_vendo_name(self, vendor_name):
        vendor = Vendor.query.filter_by(name=vendor_name.data).first()
        if vendor is not None:
            raise ValidationError('Please use a different vendor name.')

    def validate_admin_code(self, admin_code):
        if admin_code.data != 'Sentri101':
            raise ValidationError('Wrong Security Code')


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


class CustomerInfo(FlaskForm):
    name = StringField('الاسم', render_kw={
        'placeholder': 'من فضلك أدخل اسمك'})
    phone_number = TelField('رقم الموبيل', _prefix='20', render_kw={
        'placeholder': 'من فضلك أدخل رقم هاتف صحيح'})
    address = StringField('العنوان', render_kw={
        'placeholder': 'من فضلك أدخل عنوان صحيح'})
