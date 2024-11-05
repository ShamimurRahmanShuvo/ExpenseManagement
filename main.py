import os
from datetime import date
from flask import Flask, abort, render_template, redirect, url_for, flash
from flask_bootstrap import Bootstrap5
from flask_ckeditor import CKEditor
from flask_gravatar import Gravatar
from flask_login import UserMixin, login_user, LoginManager, current_user, logout_user
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship, DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Text
from functools import wraps
from werkzeug.security import generate_password_hash, check_password_hash
from forms import RegisterForm, LoginForm, AddExpenseForm, ExpenseTypeForm, IncomeTypeForm, AddIncomeForm


app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
ckeditor = CKEditor(app)
Bootstrap5(app)

login_manager = LoginManager()
login_manager.init_app(app)


# Create Database
class Base(DeclarativeBase):
    pass


app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///expense-sheet.db"
db = SQLAlchemy(model_class=Base)
db.init_app(app)


# Configure Tables
class User(UserMixin, db.Model):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String)
    email: Mapped[str] = mapped_column(String, unique=True)
    password: Mapped[str] = mapped_column(String)


class ExpenseType(db.Model):
    __tablename__ = "expense_type"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    expense_type: Mapped[str] = mapped_column(String)


class IncomeType(db.Model):
    __table_name__ = "income_type"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    income_type: Mapped[str] = mapped_column(String)


with app.app_context():
    db.create_all()


@app.route("/")
def home():
    return render_template("index.html", current_user=current_user)


@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        result = db.session.execute(db.select(User).where(User.email == form.email.data))
        user = result.scalar()
        if user:
            flash("You've already signed up with this email or username, login instead!")
            return redirect(url_for("login"))
        hash_and_salted_password = generate_password_hash(
            form.password.data,
            method='pbkdf2:sha256',
            salt_length=8
        )
        new_user = User(
            username=form.name.data,
            email=form.email.data,
            password=hash_and_salted_password
        )
        db.session.add(new_user)
        db.session.commit()
        login_user(new_user)
        return redirect(url_for("home"))

    return render_template("register.html", form=form, current_user=current_user)


@login_manager.user_loader
def load_user(user_id):
    return db.get_or_404(User, user_id)


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        result = db.session.execute(db.select(User).where(User.email == email))
        user = result.scalar()

        if not user:
            flash("Email doesn't exist, please try again")
            return redirect(url_for("login"))
        elif not check_password_hash(user.password, password):
            flash("Incorrect password, please try again")
            return redirect(url_for("login"))
        else:
            login_user(user)
            return redirect(url_for("home"))

    return render_template("login.html", form=form, current_user=current_user)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("home"))


@app.route("/add-expense-type", methods=["GET", "POST"])
def add_expense_type():
    form = ExpenseTypeForm()
    if form.validate_on_submit():
        expense_name = form.expense_type.data
        expense_name_capitalize = expense_name.capitalize()
        result = db.session.execute(db.select(ExpenseType).where(
            ExpenseType.expense_type == expense_name_capitalize)).scalar()

        if result:
            flash("Expense type already exists, add new expense type")
            return redirect(url_for("add_expense_type"))

        new_expense_type = ExpenseType(
            expense_type=expense_name_capitalize
        )
        db.session.add(new_expense_type)
        db.session.commit()
        flash("Expense type successfully added")
        return redirect(url_for("add_expense_type"))

    return render_template("expense_type.html", form=form, current_user=current_user)


@app.route("/add-income-type", methods=["GET", "POST"])
def add_income_type():
    form = IncomeTypeForm()
    if form.validate_on_submit():
        income_name = form.income_type.data
        income_name_capitalize = income_name.capitalize()
        result = db.session.execute(db.select(IncomeType).where(
            IncomeType.income_type == income_name_capitalize)).scalar()
        if result:
            flash("Income type already exists, add new income type")
            return redirect(url_for("add_income_type"))

        new_income_type = IncomeType(
            income_type = income_name_capitalize
        )
        db.session.add(new_income_type)
        db.session.commit()
        flash("Income type successfully added")
        return redirect(url_for("add_income_type"))

    return render_template("income_type.html", form=form, current_user=current_user)


@app.route("/add-income")
def add_income():
    form = AddIncomeForm()
    results = db.session.execute(db.select(IncomeType)).scalars().all()

    choices = []
    for result in results:
        choice_id = result.id
        choice_name = result.income_type
        choices.append((choice_id, choice_name))

    form.income_id.choices = choices
    return render_template("income.html", form=form, current_user=current_user)


@app.route("/add-expense")
def add_expense():
    form = AddExpenseForm()
    results = db.session.execute(db.select(ExpenseType)).scalars().all()

    choices = []
    for result in results:
        choice_id = result.id
        choice_name = result.expense_type
        choices.append((choice_id, choice_name))
    # print(choices)
    form.expense_id.choices = choices
    return render_template("expense.html", form=form, current_user=current_user)


@app.route("/view-report")
def view_report():
    return render_template("report.html", current_user=current_user)


if __name__ == "__main__":
    app.run(debug=True, port=5008)
