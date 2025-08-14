from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, DecimalField, IntegerField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, Optional # Optional ইম্পোর্ট করা হয়েছে
from models import User

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    # --- নতুন: কনফার্ম পাসওয়ার্ড ফিল্ড যোগ করা হয়েছে ---
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    
    user_type = SelectField('Register as', choices=[
        ('user', 'User (I want to sell scrap)'),
        ('collector', 'Collector (I want to collect scrap)')
    ], validators=[DataRequired()])
    
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken. Please choose a different one.')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Login')

class PostForm(FlaskForm):
    trash_type = StringField('Trash Type', validators=[DataRequired(), Length(max=50)])
    quantity = IntegerField('Quantity (Kg or Pieces)', validators=[DataRequired()])
    price = DecimalField('Price (Per Unit)', validators=[DataRequired()], places=2)
    location = StringField('Location', validators=[DataRequired(), Length(max=255)])
    description = TextAreaField('Description', validators=[DataRequired()])
    
    # --- নতুন: ফোন নম্বর এবং গুগল ম্যাপ ফিল্ড যোগ করা হয়েছে ---
    phone_number = StringField('Contact Phone Number', validators=[DataRequired(), Length(min=11, max=15)])
    google_map_link = StringField('Google Maps Link (Optional)', validators=[Optional(), Length(max=500)])
    
    submit = SubmitField('Create Post')