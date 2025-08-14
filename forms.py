from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, DecimalField, IntegerField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from models import User

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Sign Up')

    user_type = SelectField('Register as', choices=[
    ('user', 'User (I want to sell scrap)'),
    ('collector', 'Collector (I want to collect scrap)')
], validators=[DataRequired()])
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
    quantity = IntegerField('Quantity', validators=[DataRequired()])
    price = DecimalField('Price', validators=[DataRequired()], places=2)
    location = StringField('Location', validators=[DataRequired(), Length(max=255)])
    description = TextAreaField('Description')
    submit = SubmitField('Create Post')