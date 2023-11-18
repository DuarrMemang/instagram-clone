from flask import render_template, redirect, url_for, flash, request, make_response, jsonify
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.utils import secure_filename
import os

from application import app
from application.models import *
from application.forms import *
from application.utils import save_image

app.config['UPLOAD_FOLDER'] = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static/images')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('profile',username=current_user.username))

    form = LoginForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = User.query.filter_by(username=username).first()
        if user and password == user.password:
            login_user(user)
            return redirect(url_for('profile', username=current_user.username))
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
    posts = current_user.posts
    reverse_posts = posts[::-1]
    return render_template('profile.html', title=f'{current_user.fullname} Profile', posts=reverse_posts)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower()

@app.route('/', methods=('GET', 'POST'))
@login_required
def index():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.filter_by(author_id = current_user.id).order_by(Post.post_date.desc()).paginate(page=page, per_page=5)

    return render_template('index.html', title='Home', posts=posts)
@app.route('/signup',methods=('GET', 'POST'))
def signup():
    if current_user.is_authenticated: 
        return redirect(url_for('profile', username=current_user.username))

    form = SignUpForm()

    if form.validate_on_submit():

        user = User(
            username = form.username.data,
            fullname = form.fullname.data,
            email = form.email.data,
            profile_pic = save_image(form.profile_pic.data, pfp=True),
            password = form.password.data
        )
        db.session.add(user)
        db.session.commit()
        flash('Account has been made', 'success')
        return redirect(url_for('login'))

    return render_template('signup.html', title='SignUp', form=form)
@app.route('/about')
def about():
    return render_template('about.html', title='About')

@app.route('/forgotpassword')
def forgotpassword():
    if current_user.is_authenticated: 
        return redirect(url_for('profile', username=current_user.username))
    form = ForgotPasswordForm()
    if form.validate_on_submit:
        flash('Password reset link has been sent to your email', 'success')
        return redirect(url_for('login'))
    return render_template('forgot_password.html', title='ForgotPassword', form=form)

@app.route('/editprofile',methods=['GET', 'POST'])
def editprofile():
    form = EditProfileForm()

    if form.validate_on_submit():
        user = User.query.get(current_user.id)
        if form.username.data != user.username:
            user.username = form.username.data
        user.fullname = form.fullname.data
        user.bio = form.bio.data

        if form.profile_pic.data:
            file = form.profile_pic.data
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                user.profile_pic = filename

        db.session.commit()
        flash('Profile updated', 'success')
        return redirect(url_for('profile', username=current_user.username))
    
    form.username.data = current_user.username
    form.fullname.data = current_user.fullname
    form.bio.data = current_user.bio
    
    return render_template('profile_edit.html', title=f'Edit {current_user.username} Profile', form=form)

@app.route('/resetpassword', methods=['GET', 'POST'])
def resetpassword():
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user = User.query.filter_by(password=form.old_password.data).first()

        if user:
            user.password = form.new_password.data
            db.session.commit()
            flash('password reset successfully!', 'success')
            return redirect(url_for('verif'))
        else:
            flash('old password is incorrect!', 'danger')
    return render_template('reset_password.html', title='Reset Password', form=form)

@app.route('/verif', methods=['GET', 'POST'])
@login_required
def verif():
    form = VerificationResetPasswordForm()
    if form.validate_on_submit():
        if form.password.data == form.confirm_password.data:
            flash('Password matched!', 'success')
            return redirect(url_for('resetpassword'))
        else:
            flash('Password does not match!', 'danger')
    return render_template('verif.html', title= 'Verification', form=form)

@app.route('/createpost', methods=["GET", "POST"])
@login_required
def createpost():
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
        posts = Post.query.filter_by(author_id = current_user.id).order_by(Post.post_date.desc()).paginate(page=page, per_page=5)

        return redirect(url_for('index'))

    return render_template('create_post.html', title='Create Post', form=form)
@app.route('/editpost')
@login_required
def editpost():
    form = EditPostForm()
    return render_template('edit_post.html', title='Edit post', form=form)

@app.route('/like', methods=['GET', 'POST'])
@login_required
def like():
    data = request.json
    post_id = int(data['postId'])
    like = Like.query.filter_by(user_id=current_user.id,post_id=post_id).first()
    if not like:
        like = Like(user_id=current_user.id, post_id=post_id)
        db.session.add(like)
        db.session.commit()
        return make_response(jsonify({"status" : True}), 200)
    
    db.session.delete(like)
    db.session.commit()
    return make_response(jsonify({"status" : False}), 200)