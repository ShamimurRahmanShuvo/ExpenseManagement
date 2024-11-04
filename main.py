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


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/register")
def register():
    form = RegisterForm()
    return render_template("register.html", form=form)


@app.route("/login")
def login():
    form = LoginForm()
    return render_template("login.html", form=form)


@app.route("/add-expense")
def add_expense():
    form = AddExpenseForm()
    form.expense_id.choices = [('1', 'Fixed'), ('2', 'Variable')]
    return render_template("expense.html", form=form)


@app.route("/add-expense-type")
def add_expense_type():
    form = ExpenseTypeForm()
    return render_template("expense_type.html", form=form)


@app.route("/add-income-type")
def add_income_type():
    form = IncomeTypeForm()
    return render_template("income_type.html", form=form)


@app.route("/add-income")
def add_income():
    form = AddIncomeForm()
    form.income_id.choices = [('1', 'Salary'), ('2', 'Others')]
    return render_template("income.html", form=form)


@app.route("/view-report")
def view_report():
    return render_template("report.html")


if __name__ == "__main__":
    app.run(debug=True, port=5008)
