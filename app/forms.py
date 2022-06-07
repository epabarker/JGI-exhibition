from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerRangeField
from wtforms.validators import DataRequired, NumberRange

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class SmellForm(FlaskForm):
    va_rating = IntegerRangeField('Rating for Box 1')
    co_rating = IntegerRangeField('Rating for Box 2')
    vi_rating = IntegerRangeField('Rating for Box 3')
    submit = SubmitField('Submit rating')
