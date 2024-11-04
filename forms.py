from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, EmailField, SelectField, DateField, DecimalField
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


class AddExpenseForm(FlaskForm):
    expense_id = SelectField("Expense Type", coerce=int, choices=[], validators=[DataRequired()])
    date = DateField("Date", validators=[DataRequired()])
    details = StringField("Expense Name", validators=[DataRequired()])
    amount = DecimalField("Expense Amount", places=2, validators=[DataRequired()])
    submit = SubmitField("Add Expense")


class IncomeTypeForm(FlaskForm):
    income_type = StringField("Income Type", validators=[DataRequired()])
    submit = SubmitField("Add Income Type")


class AddIncomeForm(FlaskForm):
    income_id = SelectField("Income Type", coerce=int, choices=[], validators=[DataRequired()])
    date = DateField("Date", validators=[DataRequired()])
    source = StringField("Income Source", validators=[DataRequired()])
    amount = DecimalField("Income Amount", places=2, validators=[DataRequired()])
    submit = SubmitField("Add Expense")
