from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField, IntegerField
from wtforms.fields.html5 import DateField
from wtforms.validators import DataRequired
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class AddOrder(FlaskForm):
    material = SelectField("What do you want to order?", choices = ['-','Hörnli'])
    amount = IntegerField("How much do you want in [g]?", validators=[DataRequired()])
    time = DateField("On what time do you want it?", validators=[DataRequired()])
    submit = SubmitField('Order Now')

class EditProfileForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    submit = SubmitField('Submit')