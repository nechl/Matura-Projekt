from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField, IntegerField
from wtforms.fields.html5 import DateField, TimeField
from wtforms.validators import DataRequired
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class AddOrder(FlaskForm):
    material = SelectField("What do you want to order?", choices = ['-','Hoernli'])
    amount = IntegerField("How much do you want in [g]?", validators=[DataRequired()])
    date = DateField("Time? ", validators=[DataRequired()])
    time = TimeField("Date?", validators=[DataRequired()])
    submit = SubmitField('Order Now')

class EditProfileForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    submit = SubmitField('Submit')

class EditOrderForm(FlaskForm):
    amount = IntegerField("How much do you want in [g]?", validators=[DataRequired()])
    date = DateField("On what date do you want it?", validators=[DataRequired()])
    time = TimeField("On what time do you want it?", validators=[DataRequired()])
    cooking = BooleanField("Is it already cooked? ")
    submit = SubmitField('Save Order')

class DeleteForm(FlaskForm):
    submit = SubmitField("Do you want to delete that order?")