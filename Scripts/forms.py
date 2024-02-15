from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, BooleanField
from wtforms.validators import DataRequired

class ExpenseForm(FlaskForm):
    item = StringField('Pozycja', validators=[DataRequired()])
    description = TextAreaField('Opis')
    bought = BooleanField('Kupione')