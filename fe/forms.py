# coding=utf-8
import re

from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    TextField,
    TextAreaField,
    PasswordField,
    BooleanField,
    ValidationError
)
from wtforms.validators import DataRequired, Length, EqualTo, URL

from fe.database.sqlalchemy.models import User


class CommentForm(FlaskForm):
    """Comment Form"""

    # Set some field(InputBox) for enter the data.
    # patam validators: setup list of validators
    name = StringField(
        'Name',
        validators=[DataRequired(), Length(max=255)])

    text = TextField(u'Comment', validators=[DataRequired()])


class LoginForm(FlaskForm):
    """Login Form"""

    username = StringField('Usermame', [DataRequired(), Length(max=255)])
    password = PasswordField('Password', [DataRequired()])
    remember = BooleanField("Remember Me")

    def validate(self):
        """Validator for check the account information."""
        check_validata = super(LoginForm, self).validate()

        # If validator no pass
        if not check_validata:
            return False

        # Check the user whether exist.
        user = User.query.filter_by(username=self.username.data).first()
        if not user:
            self.username.errors.append('Invalid username or password.')
            return False

        # Check the password whether right.
        if not user.check_password(self.password.data):
            self.password.errors.append('Invalid username or password.')
            return False

        return True


class RegisterForm(FlaskForm):
    """Register Form."""

    username = StringField('Username', [DataRequired(), Length(max=255)])
    password = PasswordField('Password', [DataRequired(), Length(min=8)])
    comfirm = PasswordField('Confirm Password',
                            [DataRequired(), EqualTo('password')])

    # recaptcha = RecaptchaField()

    def validate(self):
        check_validate = super(RegisterForm, self).validate()

        # If validator no pass
        if not check_validate:
            return False

        # Check the user whether exist.
        user = User.query.filter_by(username=self.username.data).first()
        if user:
            self.username.errors.append('User with that name already exists.')
            return False
        return True


class PostForm(FlaskForm):
    """Post Form."""

    title = StringField('Title', [DataRequired(), Length(max=255)])
    text = TextAreaField('Blog Content', [DataRequired()])


class OpenIDForm(FlaskForm):
    """OpenID Form."""

    openid_url = StringField('OpenID URL', [DataRequired(), URL()])


def custom_email(form_object, field_object):
    """Define a vaildator"""
    if not re.match(r"[^@+@[^@]+\.[^@]]+", field_object.data):
        raise ValidationError('Field must be a valid email address.')
