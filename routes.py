from flask import render_template, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from app import app, db
from models import User, TrashPost
from forms import LoginForm, RegistrationForm, PostForm # নতুন ফর্ম ইম্পোর্ট করা হলো

#  (ল্যান্ডিং পেজ)
@app.route('/')
def home():
    return render_template('home.html')


@app.route('/posts')
def all_posts():
    posts = TrashPost.query.order_by(TrashPost.created_at.desc()).all()
    return render_template('index.html', posts=posts, title='Available Posts')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            flash(f'Welcome back, {user.username}!', 'success')
            
            if user.user_type == 'collector':
                return redirect(url_for('collector_dashboard'))
            return redirect(url_for('user_dashboard'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Sign In', form=form)

# লগআউট
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))

# রেজিস্ট্রেশন পেজ
@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(
    username=form.username.data, 
    email=form.email.data,
    user_type=form.user_type.data
)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route('/post/new', methods=['GET', 'POST'])
@login_required
def create_post():
    form = PostForm()
    if form.validate_on_submit():
        post = TrashPost(
            user_id=current_user.id,
            trash_type=form.trash_type.data,
            quantity=form.quantity.data,
            price=form.price.data,
            location=form.location.data,
            description=form.description.data
        )
        db.session.add(post)
        db.session.commit()
        flash('Your post has been created!', 'success')
        return redirect(url_for('all_posts'))
    return render_template('create_post.html', title='New Post', form=form)

@app.route('/post/<int:post_id>')
def view_post(post_id):
    post = TrashPost.query.get_or_404(post_id)
    return render_template('view_post.html', title=post.trash_type, post=post)

@app.route('/dashboard')
@login_required
def user_dashboard():
    if current_user.user_type == 'collector':
        return redirect(url_for('collector_dashboard'))
    
    user_posts = TrashPost.query.filter_by(user_id=current_user.id).order_by(TrashPost.created_at.desc()).all()
    return render_template('user_dashboard.html', title='My Dashboard', user_posts=user_posts)

@app.route('/collector/dashboard')
@login_required
def collector_dashboard():
    if current_user.user_type != 'collector':
        return redirect(url_for('user_dashboard'))
    
    available_posts = TrashPost.query.filter_by(status='pending').all()
    return render_template('collector_dashboard.html', title='Collector Dashboard', posts=available_posts)