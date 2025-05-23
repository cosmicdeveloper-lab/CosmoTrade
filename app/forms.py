from flask_wtf import FlaskForm
from wtforms import SubmitField, FloatField, DateField, IntegerField, SelectField
from wtforms.validators import DataRequired


class PositionsForm(FlaskForm):
    amount = IntegerField('Amount', validators=[DataRequired()])
    entry = FloatField('Entry price', validators=[DataRequired()])
    close = FloatField('Close price', validators=[DataRequired()])
    strategy = SelectField('Strategy', choices=[('BUY', 'buy'), ('SELL', 'sell')], validators=[DataRequired()])
    submit = SubmitField('Submit')
