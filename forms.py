from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, EmailField
from wtforms.validators import DataRequired, Email
from flask_ckeditor import CKEditorField


class RegisterForm(FlaskForm):
    name = StringField("Username", validators=[DataRequired()])
    email = EmailField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Register")


class LoginForm(FlaskForm):
    name = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Login")


class ExpenseTypeForm(FlaskForm):
    expense_type = StringField("Expense Type", validators=[DataRequired()])
    submit = SubmitField("Add Expense Type")


class IncomeTypeForm(FlaskForm):
    income_type = StringField("Income Type", validators=[DataRequired()])
    submit = SubmitField("Add Income Type")