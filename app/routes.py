import os
import secrets
from datetime import datetime
from app import app, db
from PIL import Image
from flask import render_template, flash, redirect, url_for, request
from werkzeug.urls import url_parse
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User
from app.forms import LoginForm, RegistrationForm, EditProfileForm



@app.before_request
def before_request():
	if current_user.is_authenticated:
		current_user.last_seen = datetime.utcnow()
		db.session.commit()


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


@app.route('/user/<username>')
@login_required
def user(username):
	user = User.query.filter_by(username=username).first_or_404()
	posts = [{'author': user, 'body': '#Test post 1'},
	 {'author': user, 'body': '#Test post 2'}]
	image_file=None
	if current_user.picture_file:
		image_file = url_for('static', filename='profile_pics/' + current_user.picture_file)
	return render_template('user.html', posts=posts, user=user, image_file=image_file)


def save_picture(form_picture):
	random_hex = secrets.token_hex(8)
	_, f_ext = os.path.splitext(form_picture.filename)
	picture_fn = random_hex + f_ext
	picture_path = os.path.join(app.root_path,'static/profile_pics',picture_fn)
	output_size = (384,126)
	i = Image.open(form_picture)
	i.thumbnail(output_size)
	print('saving picture')
	i.save(picture_path)
	return picture_fn
	
@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
	form = EditProfileForm()
	if form.validate_on_submit():
		if form.picture_file.data:
			picture_file = save_picture(form.picture_file.data)
			current_user.picture_file = picture_file
		current_user.username = form.username.data
		current_user.about_me = form.about_me.data
		db.session.commit()
		flash('Your changes have been saved', 'success')
		return redirect(url_for('edit_profile'))
	elif request.method == 'GET':
		form.username.data = current_user.username
		form.about_me.data = current_user.about_me
	return render_template('edit_profile.html', title="Edit Profile", form=form)


@app.route('/logout')
def logout():
	logout_user()
	return redirect(url_for('index'))
