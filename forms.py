from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField


class OrderForm(FlaskForm):
    quantity = SelectField('Quantity الكمية', choices=[
                           (1, 1), (2, 2), (3, 3), (4, 4)])
    spicy = SelectField('عادي أم سبايسي؟', choices=[
                        ('Spicy', 'سبايسي'), ('Normal', 'عادي')])
    notes = StringField('اضافة ملحوظة؟', render_kw={
                        'placeholder': 'مثال: 3 قطع فقط سبايسي أو بدون بصل'})
    submit = SubmitField('Add To Order')
