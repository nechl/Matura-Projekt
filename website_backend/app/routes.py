from flask import render_template, flash, redirect, url_for, request
from werkzeug.urls import url_parse
from app import app, db
from app.forms import LoginForm, AddOrder, EditProfileForm, EditOrderForm, DeleteForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User, Order
import datetime
from datetime import timedelta, datetime
#from physical.cookBot import CookBot
import json
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore

jobstores = {
    'default': SQLAlchemyJobStore(url='sqlite:///jobs.sqlite')
}
scheduler = BackgroundScheduler(jobstores = jobstores)
scheduler.start()
#cookbot = CookBot("Ratatouile")
    
def my_test(order):
    print(order)
    order_to_edit = Order.query.filter_by(id=order.id).first_or_404()
    order_to_edit.cooking = True
    db.session.add(order_to_edit)
    db.session.commit()

#Welcome Page
@app.route('/')
@app.route('/index')
@login_required
def index():
    orders = Order.query.filter_by(cooking = False).order_by(Order.finished_at.asc()).all()
    orders_cooked = Order.query.filter_by(cooking = True).order_by(Order.finished_at.asc()).all()
    return render_template('index.html', title='Home', orders=orders, orders_cooked = orders_cooked)

#Login Page/Worker
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

#Logout Page/ Worker
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

#User Page
@app.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    orders = Order.query.order_by(Order.finished_at.asc()).all()
    return render_template('user.html', user=user, orders=orders)

#Edit User Page
@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        db.session.add(current_user)
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('index'))
    elif request.method == 'GET':
        form.username.data = current_user.username
    return render_template('edit_profile.html', title='Edit Profile',form=form)

@app.route('/order', methods=['GET', 'POST'])
@login_required
def order():
    form = AddOrder()
    if form.validate_on_submit():

        #calculate when the robot has to start cooking, in order to finish the meal on time. Goes following:
        #
        # start_at = finished at - TimeFor2LitersOfWater(boiling) + TimeToCookPasta
        
        # Opening JSON file
        f = open('data_recipe.json',)
        
        # returns JSON object as 
        # a dictionary
        data = json.load(f)
        
        # Iterating through the json
        # list
        for recipe in data['recipes']:
            if recipe["compound"] == form.material.data:
                TimeToCook = (recipe["time_in_water"])
        
        # Closing file
        f.close()
        # Calculate the time to start at
        delta = timedelta(minutes=TimeToCook)
        start_at = datetime.combine(form.date.data, form.time.data) - delta #work on converting int to datetime

        # Calculate the time to finish at
        finished_at = datetime.combine(form.date.data, form.time.data)
        order = Order(food = form.material.data, finished_at = finished_at, start_at = start_at, amount = form.amount.data, user_id = current_user.username, cooking = False)
        #commit the new order to the database
        if order.start_at > datetime.now():
            db.session.add(order)
            #db.session.flush()
            db.session.commit()
            
            scheduler.add_job(my_test, 'date', run_date=order.start_at, args=[order], id=str(order.id))
            #scheduler.add_job(cookbot.cook, 'date', run_date=order.start_at, args=[order], id=str(order.id))
        else:
            return redirect(url_for('order'))
            
        for job in scheduler.get_jobs():
            print(job.id, end = ': ')
            print(job)
        
        flash('your order has been added')
        return redirect(url_for('index'))

    return render_template('selectFood.html', title='Order the Food you want to...', form=form)

@app.route('/edit_order/<id>', methods=["GET", "POST"])
@login_required
def edit_order(id):
    form = EditOrderForm()
    order = Order.query.filter_by(id=id).first_or_404()
    if form.validate_on_submit():
        order.amount = form.amount.data
        order.finished_at = datetime.combine(form.date.data, form.time.data)
        order.start_at = order.finished_at - timedelta(minutes=10)
        order.cooking = form.cooking.data

        if form.cooking.data == 1:
            scheduler.remove_job(order.id)

        if datetime.now() >= order.start_at:
            flash("Not possible to change that order.\nPossible Errors:\n\t-Already cooked\n\t-No free slot")

        else:
            db.session.add(order)
            db.session.commit()

            
            if form.cooking.data != 1:
                print("[Old Job]", end=": ")
                print(scheduler.get_job(order.id))
                scheduler.get_job(order.id).reschedule('date', run_date=order.start_at) 
                print("[New Job]", end=": ")
                print(scheduler.get_job(order.id))
            else:
                pass


            flash('Your changes have been saved')
            return redirect( url_for('index'))
    
    elif request.method == "GET":
        form.amount.data = order.amount
        form.date.data = order.finished_at
        form.time.data = order.finished_at
        form.cooking.data = order.cooking

    return render_template('edit_order.html', title="Edit order", form=form, order=order)
        
@app.route('/delete_order/<id>', methods=["GET", "POST"])
@login_required
def delete_order(id):
    form = DeleteForm()
    order = Order.query.filter_by(id=id).first_or_404()
    if form.validate_on_submit():
        if datetime.now() >= order.start_at:
            pass
        else:
            try:
                scheduler.remove_job(order.id)
            except BaseException as e:
                print(e)

        Order.query.filter_by(id=id).delete()
        db.session.commit()
        
        for job in scheduler.get_jobs():
            print(job)        
        return redirect(url_for('index'))

    return render_template('delete_order.html', title="Delete Order", form=form, order=order)

# Next to do: add start_at for changing the time/date of order so that correct, then APScheduler