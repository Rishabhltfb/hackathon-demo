import os
import secrets
from PIL import Image
from flask import render_template, url_for, flash, redirect, request, abort
from flaskapp import app, db, bcrypt
from flaskapp.forms import RegistrationForm, LoginForm, UpdateAccountForm, DetailForm
from flaskapp.models import User, Detail
from flask_login import login_user, current_user, logout_user, login_required


@app.route("/")
def cover():
    cover_img = url_for('static', filename='profile_pics/cover.jpg')
    return render_template('cover.html',cover_img=cover_img)

@app.route("/home")
def home():
    page = request.args.get('page', 1, type=int)
    return render_template('home.html')

@app.route("/choice")
@login_required
def choice():
    return render_template('choice.html')


@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        if current_user.is_registered == 'False':
            return redirect(url_for('detail'))
        elif current_user.is_registered == 'True':
            return redirect(url_for('choice'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        if current_user.is_registered == 'False':
            return redirect(url_for('detail'))
        elif current_user.is_registered == 'True':
            return redirect(url_for('choice'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data) and user.is_registered == 'True':
            login_user(user, remember=form.remember.data)
            return redirect('choice')
        elif user and bcrypt.check_password_hash(user.password, form.password.data) and user.is_registered == 'False':
            login_user(user, remember=form.remember.data)
            return redirect('detail')
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('login'))


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)

    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn

@app.route("/detail", methods=['GET', 'POST'])
@login_required
def detail():
    form = DetailForm()
    if form.validate_on_submit():
        detail = Detail(name=form.name.data, address=form.address.data, gender=form.gender.data,phone_no=form.phone_no.data)
        user= User.query.filter_by(username=current_user.username).first()
        user.is_registered = 'True'
        db.session.add(detail)
        db.session.add(user)
        db.session.commit()
        flash('Details received!', 'success')
        return redirect(url_for('choice'))
    return render_template('detail.html', form=form)


@app.route("/account/<string:choice>", methods=['GET', 'POST'])
@login_required
def account(choice):
    form = UpdateAccountForm()
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=current_user.username).first_or_404()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)

    if choice == "donate":
        return render_template('donate.html', title='Account',
                           image_file=image_file, form=form, user=user)
    elif choice == "ngo":
        return render_template('ngo.html', title='Account',
                           image_file=image_file, form=form, user=user)
    elif choice == "deliver":
        return render_template('deliver.html', title='Account',
                           image_file=image_file, form=form, user=user)         
    


