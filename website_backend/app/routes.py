from flask import render_template, flash, redirect, url_for, request
from werkzeug.urls import url_parse
from app import app, db
from app.forms import LoginForm, AddOrder, EditProfileForm, EditOrderForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User, Order
from datetime import datetime

@app.route('/')
@app.route('/index')
@login_required
def index():
    orders = Order.query.order_by(Order.finished_at.asc()).all()
    return render_template('index.html', title='Home', orders=orders)

#login worker
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)

#logout worker
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        db.session.add(current_user)
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('edit_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
    return render_template('edit_profile.html', title='Edit Profile',form=form)

@app.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    orders = Order.query.order_by(Order.finished_at.asc()).all()
    return render_template('user.html', user=user, orders=orders)

#under construction
@app.route('/edit_order/<id>', methods=["GET", "POST"])
@login_required
def edit_order(id):
    form = EditOrderForm()
    order = Order.query.filter_by(id=id).first_or_404()
    if form.validate_on_submit():
        order.amount = form.amount.data
        order.finished_at = form.time.data
        db.session.add(order)
        db.session.commit()
        flash('Your changes have been saved')
    elif request.method == "GET":
        form.amount.data = order.amount
        form.time.data = order.finished_at
    return render_template('edit_order.html', title="Edit order", form=form, order=order)
        


@app.route('/order', methods=['GET', 'POST'])
@login_required
def order():
    form = AddOrder()
    if form.validate_on_submit():
        order = Order(food = form.material.data, finished_at = form.time.data,amount = form.amount.data, user_id = current_user.username)
        db.session.add(order)
        db.session.commit()
        flash('your order has been added')
        return redirect(url_for('index'))
    return render_template('selectFood.html', title='Order the Food you want to...', form=form)