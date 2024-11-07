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
    email = EmailField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Login")


class AddTransactionTypeForm(FlaskForm):
    transaction_type = StringField("Transaction Type", validators=[DataRequired()])
    submit = SubmitField("Add Transaction Type")


class AddTransactionForm(FlaskForm):
    transaction_type_id = SelectField("Transaction Type", choices=[], coerce=int, validators=[DataRequired()])
    transaction_date = DateField("Transaction Date", validators=[DataRequired()])
    transaction_name = StringField("Transaction Name", validators=[DataRequired()])
    transaction_amount = DecimalField("Transaction Amount", places=2, validators=[DataRequired()])
    submit = SubmitField("Add Transaction")


class ViewReportForm(FlaskForm):
    category = SelectField("Report Category",
                           choices=[('1', 'Income'), ('2', 'Expense'), ('3', 'Both')],
                           validators=[DataRequired()])
    from_date = DateField("From", validators=[DataRequired()])
    to_date = DateField("To", validators=[DataRequired()])
    submit = SubmitField("Show Report")
