from flask_wtf import FlaskForm
# নতুন দুটি ক্লাস ইম্পোর্ট করা হয়েছে
from flask_wtf.file import FileField, FileAllowed 
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, DecimalField, IntegerField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, Optional
from models import User

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
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
    price_per_kg = DecimalField('Price (Per Kg)', validators=[DataRequired()], places=2)
    location = StringField('Location', validators=[DataRequired(), Length(max=255)])
    description = TextAreaField('Description', validators=[DataRequired()])
    
    phone_number = StringField('Contact Phone Number', validators=[DataRequired(), Length(min=11, max=15)])
    google_map_link = StringField('Google Maps Link (Optional)', validators=[Optional(), Length(max=500)])
    
    is_negotiable = BooleanField('Price is Negotiable')
    
    # --- নতুন: ছবি আপলোডের ফিল্ড যোগ করা হয়েছে ---
    picture = FileField('Upload a Picture of the Scrap (Optional)', validators=[FileAllowed(['jpg', 'png', 'jpeg'])])
    
    submit = SubmitField('Create Post')