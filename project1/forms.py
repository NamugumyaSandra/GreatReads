from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,BooleanField,SubmitField,TextAreaField,IntegerField
from wtforms.validators import DataRequired, Email,NumberRange,Length,EqualTo,ValidationError
from flask_login import current_user


class RegistrationForm(FlaskForm):
   username = StringField('Username', validators=[DataRequired(), Length(min=2, max=50)],render_kw={"placeholder": "Username"})
   email = StringField('Email', validators=[DataRequired(), Email()],render_kw={"placeholder": "Email"})
   password = PasswordField('Password', validators=[DataRequired()],render_kw={"placeholder": "Password"})
   confirm_password = PasswordField('Confirm Password', validators=[DataRequired(),EqualTo('password')],render_kw={"placeholder": "Confirm_Password"})
   submit = SubmitField('Sign Up')
    
   def validate_username(self, username):
      user = f"SELECT * FROM users WHERE username='{username.data}'".fetchone()
      if user:
         raise ValidationError('Username already exists.')
      
   def validate_email(self, email):
      user = f"SELECT * FROM users WHERE email='{email.data}'".fetchone()
      if user:
         raise ValidationError('Email already in use.')

class LoginForm(FlaskForm):
   email = StringField( validators=[DataRequired('Please enter your email address.'), Email('Please enter a valid email address')],render_kw={"placeholder": "Email"})
   password = PasswordField('Password', validators=[DataRequired('Please enter the password.')],render_kw={"placeholder": "Password"})
   remember = BooleanField('Remember Me')
   submit = SubmitField('Login')

class ReviewForm(FlaskForm):
   review = TextAreaField(validators=[DataRequired()])
   rating = IntegerField(validators=[DataRequired(),NumberRange(1,5)])
   send = SubmitField('send')

class SearchForm(FlaskForm):
   search = StringField('Search')
   submit = SubmitField('Search')