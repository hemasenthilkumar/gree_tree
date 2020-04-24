from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, IntegerField,FileField,SubmitField, TextAreaField,validators,SelectField,SelectMultipleField
from wtforms.widgets import TextArea, html5
from wtforms.fields.html5 import DateField
from flask_wtf.file import FileField
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
class ProductForm(FlaskForm):
    c=[(1,'Indoor'),(2,'Outdoor'),(3,'Decorative')]
    l=[(1,'Vellore'),(2,'Chennai'),(3,'Bangalore'),(4,'Hyderabad')]
    name=StringField('Product Name',validators=[DataRequired()])
    price = IntegerField('Price',widget=html5.NumberInput(),validators=[DataRequired()])
    location = SelectMultipleField(u'Available locations', choices =l, validators = [DataRequired()])
    category = SelectField(u'Plant Categories', choices =c, validators = [DataRequired()])
    file=FileField()
    submit = SubmitField('Add product')

class SearchByP(FlaskForm):
     l=[(1,'Vellore'),(2,'Chennai'),(3,'Bangalore'),(4,'Hyderabad')]
     location = SelectField(u'Available locations', choices =l, validators = [DataRequired()])
     submit = SubmitField('Search by location')

class SearchbyC(FlaskForm):
    c=[(1,'Indoor'),(2,'Outdoor'),(3,'Decorative')]
    category = SelectField(u'Plant Categories', choices =c, validators = [DataRequired()])
    submit = SubmitField('Search by Category')

    
    
    
    
