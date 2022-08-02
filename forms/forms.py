from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField
from wtforms.validators import DataRequired


# Also used for password updates
class SignupForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    verify = PasswordField('Verify Password', validators=[DataRequired()])
    submit = SubmitField('Signup')

# User Login
class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')


class BlabForm(FlaskForm):
    content = TextAreaField('Content', validators=[DataRequired()])
    submit = SubmitField('Save Script')

class UpdatePwForm(FlaskForm):
    password = PasswordField('New Password', validators=[DataRequired()])
    verify = PasswordField('Verify Password', validators=[DataRequired()])
    submit = SubmitField('Submit')