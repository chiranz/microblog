from app import app
from flask import render_template, flash, redirect
from app.forms import LoginForm

@app.route('/')
@app.route('/index')
def index():
    user = {'username': 'Chiranz'}
    posts = [
    {'author': {'username': 'Chiranz'}, 'body': 'Beautiful day in kolkatta!'},
    {'author': {'username': 'Chiranz'}, 'body': 'What a wonderful world!'}]
    return render_template('index.html', user=user, title='Home', posts=posts)

@app.route('/login', methods=['GET', 'POST'])
def login():
	form = LoginForm()
	if form.validate_on_submit():
		flash(f'Login requested for {form.username.data}, remember_me= {form.remember_me.data}')
		return redirect('/index')
	return render_template('login.html', title='Sign In', form=form)
