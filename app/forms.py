from app.models import User, Product
from flask import flash, redirect, url_for
import hashlib

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, ValidationError, DataRequired, Email, EqualTo


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Sign In')


class RegistrationForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    fname = StringField('First Name', validators=[DataRequired()])
    lname = StringField('Last Name', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')


class ProductAddingForm(FlaskForm):
    sku = StringField('SKU', validators=[DataRequired()])
    product_name = StringField('Book Name', validators=[DataRequired()])
    description = StringField('Desccription', validators=[DataRequired()])
    quantity = StringField('Quantity', validators=[DataRequired()])
    regular_price = StringField('Price', validators=[DataRequired()])
    category = StringField('Category', validators=[DataRequired()])
    submit = SubmitField('Add Item')

    def validate_product_name(self, product_name):
        product = Product.query.filter_by(product_name=product_name.data).first()
        if product is not None:
            raise ValidationError('{} already exist!, you might want to add the quantity').format(product_name.data)
