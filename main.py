import os
from datetime import date
from flask import Flask, abort, render_template, redirect, url_for, flash
from flask_bootstrap import Bootstrap5
from flask_ckeditor import CKEditor
from flask_gravatar import Gravatar
from flask_login import UserMixin, login_user, LoginManager, current_user, logout_user
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship, DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Float
from functools import wraps
from werkzeug.security import generate_password_hash, check_password_hash
from forms import RegisterForm, LoginForm, AddTransactionTypeForm, AddTransactionForm, ViewReportForm


app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('FLASK_KEY', '8BYkEfBA6O6donzWlSihBXox7C0sKR6b')
ckeditor = CKEditor(app)
Bootstrap5(app)

login_manager = LoginManager()
login_manager.init_app(app)


# Create Database
class Base(DeclarativeBase):
    pass


app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DB_URI", "sqlite:///expense-sheet.db")
db = SQLAlchemy(model_class=Base)
db.init_app(app)


# Configure Tables
class User(UserMixin, db.Model):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String)
    email: Mapped[str] = mapped_column(String, unique=True)
    password: Mapped[str] = mapped_column(String)
    balances = relationship("Transactions", back_populates="user")


class TransactionType(db.Model):
    __tablename__ = "trans_type"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    type_name: Mapped[str] = mapped_column(String, nullable=False)
    cat_rel = relationship("Transactions", back_populates="type_relation")


class Transactions(db.Model):
    __tablename__ = "transaction"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    transaction_type_id: Mapped[int] = mapped_column(Integer, db.ForeignKey("trans_type.id"))
    type_relation = relationship("TransactionType", back_populates="cat_rel")
    user_id: Mapped[int] = mapped_column(Integer, db.ForeignKey("users.id"))
    user = relationship("User", back_populates="balances")
    transaction_date: Mapped[str] = mapped_column(String(250), nullable=False)
    transaction_name: Mapped[str] = mapped_column(String(250), nullable=False)
    transaction_amount: Mapped[float] = mapped_column(Float, nullable=False)


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


@app.route("/add-type", methods=["GET", "POST"])
def add_transaction_type():
    form = AddTransactionTypeForm()
    if form.validate_on_submit():
        transaction_type_name = form.transaction_type.data.capitalize()
        result = db.session.execute(db.select(TransactionType).where(
            TransactionType.type_name == transaction_type_name
        )).scalar()

        if result:
            flash("Transaction type already exists, add new transaction type")
            return redirect(url_for("add_transaction_type"))

        new_transaction_type = TransactionType(
            type_name=transaction_type_name
        )
        db.session.add(new_transaction_type)
        db.session.commit()
        flash("Transaction type added successfully!")
        return redirect(url_for("add_transaction_type"))

    return render_template("transaction_type.html", form=form, current_user=current_user)


@app.route("/add-transaction", methods=["GET", "POST"])
def add_transaction():
    form = AddTransactionForm()
    form.transaction_type_id.choices = [(choice.id, choice.type_name) for choice in TransactionType.query.all()]

    if form.validate_on_submit():
        if not current_user.is_authenticated:
            flash("You need to login to add your transactions")
            return redirect(url_for("login"))

        new_transaction = Transactions(
            transaction_type_id=form.transaction_type_id.data,
            user_id=current_user.id,
            transaction_date=form.transaction_date.data,
            transaction_name=form.transaction_name.data,
            transaction_amount=form.transaction_amount.data
        )
        db.session.add(new_transaction)
        db.session.commit()

        flash("Transaction added successfully")
        return redirect(url_for("add_transaction"))

    return render_template("transaction.html", form=form, current_user=current_user)

"""
@app.route("/report", methods=["GET", "POST"])
def report():
    form = ViewReportForm()

    if form.validate_on_submit():
        if not current_user.is_authenticated:
            flash("You need to login to see your report")
            return redirect(url_for("login"))

        user = current_user.id
        table = form.category.data
        from_date = form.from_date.data
        to_date = form.to_date.data
        print(user, table, from_date, to_date)

        if table == "Income":
            results = Income.query.filter(Income.transaction_date.between(from_date, to_date)).where(
                Income.user_id == user).all()
            return render_template("view_report.html",
                                   results=results,
                                   table=table,
                                   from_date=from_date,
                                   to_date=to_date,
                                   user=current_user.username)
        elif table == "Expense":
            results = Expense.query.filter(Expense.transaction_date.between(from_date, to_date)).where(
                Expense.user_id == user).all()
            return render_template("view_report.html",
                                   results=results,
                                   table=table,
                                   from_date=from_date,
                                   to_date=to_date,
                                   user=current_user.username)
        else:
            flash("Select report category")
            return redirect(url_for("report"))

    return render_template("report.html", current_user=current_user, form=form)


@app.route("/view-report")
def view_report():
    return render_template("view_report.html", current_user=current_user)
"""

if __name__ == "__main__":
    app.run(debug=True, port=5002)
