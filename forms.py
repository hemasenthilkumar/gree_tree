from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, FileField,SubmitField, TextAreaField,validators,SelectField
from wtforms.widgets import TextArea
from wtforms.fields.html5 import DateField
from wtforms.validators import DataRequired, Length


class LoginForm(FlaskForm):
    username=StringField('Username',validators=[DataRequired(),Length(min=8,max=20)])
    password = PasswordField('Password',validators=[DataRequired()])
    submit = SubmitField('Login')
class SignupForm(FlaskForm):
    c=[(1,'Home Based seller'),(2,'Whole saler'),(3,'Just Gonna purchase')]
    username=StringField('Username',validators=[DataRequired()])
    email = StringField('Email Id',validators=[DataRequired()])
    updates = SelectField(u'User Type', choices =c, validators = [DataRequired()])
    password = PasswordField('Password',validators=[DataRequired()])
    cpassword = PasswordField(' Confirm password',validators=[DataRequired()])
    bday=DateField('Birth Date',validators=[DataRequired()])
    submit = SubmitField('Sign up')

class Post(FlaskForm):
    files=FileField()
    submit = SubmitField('Post')
    
class PostText(FlaskForm):
    post_text=StringField('Post',validators=[DataRequired()])
    submit = SubmitField('Post')

class EditUser(FlaskForm):
     username=StringField('Username',validators=[DataRequired(),Length(min=8,max=20)])
     submit = SubmitField('Confirm')
    
