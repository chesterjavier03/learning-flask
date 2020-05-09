from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Length
from validate_email import validate_email


class SignupForm(FlaskForm):
    first_name = StringField('First name', validators=[DataRequired('Please enter your first name.')])
    last_name = StringField('Last name', validators=[DataRequired('Please enter your last name.')])
    email = StringField('Email', validators=[DataRequired('Please enter your email address.'),
                                             Email("Please enter your email address.")])
    password = PasswordField('Password', validators=[DataRequired('Please enter your password.'),
                                                     Length(min=6, message="Passwords must 6 characters or more.")])
    submit = SubmitField('Sign up')


