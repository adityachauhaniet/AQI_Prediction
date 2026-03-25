from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, PasswordField
from wtforms.validators import DataRequired, Length, Email

#---------------------------------------------------------Registration Form------------------------
class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=5, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    submit = SubmitField('Register')


    #----------------------------------------Login Form-----------------------
    #Using Email/Username
class LoginForm(FlaskForm):
    email_or_username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')


#----------------------------------------Prediction Form-----------------------
class PredictionForm(FlaskForm):
    co = StringField('CO Level', validators=[DataRequired()])
    ozone = StringField('Ozone Level', validators=[DataRequired()])
    no2 = StringField('NO2 Level', validators=[DataRequired()])
    pm25 = StringField('PM25 Level', validators=[DataRequired()])
    submit = SubmitField('Predict AQI')


#----------------------------------------Feedback Form-----------------------



#----------------------------------------City Search Form-----------------------


    




