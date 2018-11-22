from app import app, db
from flask import render_template, flash, redirect, url_for, request
from werkzeug.urls import url_parse
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User
from app.forms import LoginForm, RegistrationForm



@app.route('/')
@app.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    user = current_user
    posts = [
    {'author': {'username': 'Chiranz'}, 'body': 'Beautiful day in kolkatta!'},
    {'author': {'username': 'Chiranz'}, 'body': 'What a wonderful world!'}]
    return render_template('index.html', user=user, title='Home', posts=posts)

@app.route('/login', methods=['GET', 'POST'])
def login():
	if current_user.is_authenticated:
		return redirect(url_for('index'))
	form = LoginForm()
	if form.validate_on_submit():
		user = User.query.filter_by(email=form.email.data).first()
		if not user or not user.check_password(form.password.data):
			flash('Invalid email or password!', 'danger')
			return redirect(url_for('login'))
		login_user(user, remember=form.remember_me.data)

		# check if next page args is in address bar
		# url_parse check netloc makes the application more secure
		next_page = request.args.get('next')
		if not next_page or url_parse(next_page).netloc!='':
			next_page = url_for('index')
		flash('Successful login!',"success")
		return redirect(next_page)
	return render_template('login.html', title='Sign In', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
	if current_user.is_authenticated:
		return redirect(url_for('index'))
	form = RegistrationForm()
	if form.validate_on_submit():
		user = User(username=form.username.data, email=form.email.data)
		user.set_password(form.password.data)
		db.session.add(user)
		db.session.commit()
		flash('Congratulations you are now registered!','success')
		return redirect(url_for('login'))
	return render_template('register.html', form=form, title="Register")
@app.route('/logout')
def logout():
	logout_user()
	return redirect(url_for('index'))
