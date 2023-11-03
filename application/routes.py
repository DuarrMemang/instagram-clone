from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, login_required, logout_user,current_user

from application import app
from application.models import *
from application.forms import *
from application.utils import save_image

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('profile'))

    form = LoginForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = User.query.filter_by(username=username).first()
        if user and password == user.password:
            login_user(user)
            return redirect(url_for('profile'))
        else:
            flash('Invalid username or password', 'error')

    return render_template('login.html', title="Login", form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

# @app.route('/profile')
# @login_required
# def profile():
#     return render_template('profile.html', title=f'{current_user.fullname} Profile')

@app.route('/<string:username>')
@login_required
def profile(username):
    return render_template('profile.html', title=f'{current_user.username} Profile')

@app.route('/', methods=('GET', 'POST'))
@login_required
def index():
    form = CreatePostForm()

    if form.validate_on_submit():
        post = Post(
            author_id = current_user.id,
            caption =form.caption.data
        )
        post.photo = save_image(form.post_pic.data)
        db.session.add(post)
        db.session.commit()
        flash('Your image has been posted ❤!', "success")

    page = request.args.get('page', 1, type=int)
    posts = Post.query.filter_by(author_id = current_user.id).order_by(Post.post_date.desc()).paginate(page=page, per_page=3)
    
    return render_template('index.html', title='Home', form=form, posts=posts)

@app.route('/signup')
def signup():
    form = SignUpForm()
    return render_template('signup.html', title="SignUp", form=form)
    
@app.route('/about')
def about():
    return render_template('about.html', title='About')

@app.route('/forgotpassword')
def forgotpassword():
    form = ForgotPasswordForm()
    return render_template('forgot_password.html', title='ForgotPassword', form=form)

@app.route('/editprofile')
def editprofile():
    form = EditProfileForm()
    return render_template('profile_edit.html', title='Edit Profile', form=form)

@app.route('/resetpassword')
def resetpassword():
    form = ResetPasswordForm()
    return render_template('reset_password.html', title='Reset Password', form=form)

@app.route('/verif')
def verif():
    form = VerificationResetPasswordForm()
    return render_template('verif.html', title= 'Verification', form=form)

@app.route('/createpost')
def createpost():
    form = CreatePostForm()
    return render_template('create_post.html', title='Create Post', form=form)

@app.route('/editpost')
def editpost():
    form = EditPostForm()
    return render_template('edit_post.html', title='Edit post', form=form)
