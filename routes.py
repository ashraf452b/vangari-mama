from flask import render_template, redirect, url_for, flash, request # request ইম্পোর্ট করা হয়েছে
from flask_login import login_user, logout_user, login_required, current_user
from app import app, db
from models import User, TrashPost
from forms import LoginForm, RegistrationForm, PostForm
from decimal import Decimal # Decimal ব্যবহারের জন্য ইম্পোর্ট করা হয়েছে
from datetime import datetime # datetime ব্যবহারের জন্য ইম্পোর্ট করা হয়েছে

# (ল্যান্ডিং পেজ)
@app.route('/')
def home():
    return render_template('home.html')

@app.route('/how-it-works')
def how_it_works():
    return render_template('how_it_works.html', title='How It Works')

@app.route('/posts')
def all_posts():
    # --- পরিবর্তন: এখন 'available' স্ট্যাটাসের পোস্টগুলো দেখানো হবে ---
    posts = TrashPost.query.filter_by(status='available').order_by(TrashPost.created_at.desc()).all()
    return render_template('index.html', posts=posts, title='Available Posts')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        if current_user.is_admin:
            return redirect(url_for('admin_dashboard'))
        return redirect(url_for('home'))
        
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user) 
            flash(f'Welcome back, {user.username}!', 'success')
            
            if user.is_admin:
                return redirect(url_for('admin_dashboard'))
            elif user.user_type == 'collector':
                return redirect(url_for('collector_dashboard'))
            else:
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
            price_per_kg=form.price_per_kg.data, # 'price' এখন 'price_per_kg'
            location=form.location.data,
            description=form.description.data,
            phone_number=form.phone_number.data,
            google_map_link=form.google_map_link.data,
            is_negotiable=form.is_negotiable.data
        )
        db.session.add(post)
        db.session.commit()
        flash('Your post has been created!', 'success')
        return redirect(url_for('user_dashboard'))
    return render_template('create_post.html', title='New Post', form=form)

@app.route('/post/<int:post_id>')
def view_post(post_id):
    post = TrashPost.query.get_or_404(post_id)
    return render_template('view_post.html', title=post.trash_type, post=post)

# --- পোস্ট এডিট করার রুট ---
@app.route('/post/<int:post_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_post(post_id):
    post = TrashPost.query.get_or_404(post_id)
    if post.owner != current_user or post.status != 'available':
        flash('You cannot edit this post at the moment.', 'danger')
        return redirect(url_for('user_dashboard'))
    
    form = PostForm(obj=post)
    if form.validate_on_submit():
        post.trash_type = form.trash_type.data
        post.quantity = form.quantity.data
        post.price_per_kg = form.price_per_kg.data # 'price' এখন 'price_per_kg'
        post.location = form.location.data
        post.description = form.description.data
        post.phone_number = form.phone_number.data
        post.google_map_link = form.google_map_link.data
        post.is_negotiable = form.is_negotiable.data
        db.session.commit()
        flash('Your post has been updated!', 'success')
        return redirect(url_for('user_dashboard'))
        
    return render_template('edit_post.html', title='Edit Post', form=form, post_id=post.id)

# --- পোস্ট ডিলিট করার রুট ---
@app.route('/post/<int:post_id>/delete', methods=['POST'])
@login_required
def delete_post(post_id):
    post = TrashPost.query.get_or_404(post_id)
    if post.owner != current_user or post.status != 'available':
        flash('You cannot delete this post at the moment.', 'danger')
        return redirect(url_for('user_dashboard'))
    
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted.', 'success')
    return redirect(url_for('user_dashboard'))

@app.route('/dashboard')
@login_required
def user_dashboard():
    if current_user.user_type == 'collector':
        return redirect(url_for('collector_dashboard'))
    
    user_posts = TrashPost.query.filter_by(user_id=current_user.id).order_by(TrashPost.created_at.desc()).all()
    
    total_kg_sold = db.session.query(db.func.sum(TrashPost.final_weight_kg)).filter_by(user_id=current_user.id, status='completed').scalar() or 0.0
    total_earnings = current_user.total_earnings or 0.0

    return render_template('user_dashboard.html', 
                           title='My Dashboard', 
                           user_posts=user_posts,
                           total_kg_sold=total_kg_sold,
                           total_earnings=total_earnings)

@app.route('/collector/dashboard')
@login_required
def collector_dashboard():
    if current_user.user_type != 'collector':
        return redirect(url_for('user_dashboard'))
    
    available_posts = TrashPost.query.filter_by(status='available').all()
    # --- নতুন: কালেক্টরের কেনা পোস্টগুলো যোগ করা হয়েছে ---
    recent_purchases = TrashPost.query.filter_by(collector_id=current_user.id, status='completed').order_by(TrashPost.completed_at.desc()).limit(10).all()
    
    return render_template('collector_dashboard.html', 
                           title='Collector Dashboard', 
                           available_posts=available_posts, 
                           recent_purchases=recent_purchases)

# --- অফার করার রুট ---
@app.route('/post/<int:post_id>/offer', methods=['POST'])
@login_required
def make_offer(post_id):
    if current_user.user_type != 'collector':
        flash('Only collectors can make offers.', 'danger')
        return redirect(url_for('home'))

    post = TrashPost.query.get_or_404(post_id)
    
    if post.user_id == current_user.id:
        flash("You cannot make an offer on your own post.", 'warning')
        return redirect(url_for('collector_dashboard'))
        
    try:
        final_weight = float(request.form.get('final_weight'))
        final_price_per_kg = Decimal(request.form.get('final_price_per_kg')) # এখন প্রতি কেজির দাম নেওয়া হচ্ছে
    except (TypeError, ValueError):
        flash('Invalid input for weight or price.', 'danger')
        return redirect(url_for('view_post', post_id=post.id))

    if final_weight > 0 and final_price_per_kg > 0:
        post.status = 'negotiating'
        post.collector_id = current_user.id
        post.final_weight_kg = final_weight
        post.final_price_per_kg = final_price_per_kg
        post.total_transaction_value = Decimal(final_weight) * final_price_per_kg # মোট মূল্য হিসাব করা হচ্ছে
        db.session.commit()
        flash('Your offer has been sent to the seller!', 'success')
        return redirect(url_for('collector_dashboard'))
    else:
        flash('Weight and Price must be greater than zero.', 'danger')
        return redirect(url_for('view_post', post_id=post.id))

# --- অফার গ্রহণ করার রুট ---
@app.route('/offer/<int:post_id>/accept', methods=['POST'])
@login_required
def accept_offer(post_id):
    post = TrashPost.query.get_or_404(post_id)
    if post.owner != current_user:
        flash('You are not authorized to perform this action.', 'danger')
        return redirect(url_for('user_dashboard'))

    # --- নতুন হিসাব: মোট মূল্যের উপর ২% লাভ ---
    profit = post.total_transaction_value * Decimal('0.02')
    seller_earning = post.total_transaction_value - profit

    post.status = 'completed'
    post.platform_profit = profit
    post.completed_at = datetime.utcnow()
    
    seller = post.owner
    if seller.total_earnings is None:
        seller.total_earnings = Decimal('0.0')
    seller.total_earnings += seller_earning
    
    db.session.commit()
    flash('Offer accepted and transaction is complete!', 'success')
    return redirect(url_for('user_dashboard'))

# --- অফার বাতিল করার রুট ---
@app.route('/offer/<int:post_id>/reject', methods=['POST'])
@login_required
def reject_offer(post_id):
    post = TrashPost.query.get_or_404(post_id)
    if post.owner != current_user:
        flash('You are not authorized to perform this action.', 'danger')
        return redirect(url_for('user_dashboard'))

    post.status = 'available'
    post.collector_id = None
    post.final_weight_kg = None
    post.final_price_per_kg = None
    post.total_transaction_value = None
    db.session.commit()
    flash('Offer has been rejected and your post is available again.', 'info')
    return redirect(url_for('user_dashboard'))

# --- অ্যাডমিন ড্যাশবোর্ড রুট ---
@app.route('/admin/dashboard')
@login_required
def admin_dashboard():
    if not current_user.is_admin:
        flash('You do not have permission to access this page.', 'danger')
        return redirect(url_for('home'))

    total_users = User.query.count()
    total_posts = TrashPost.query.count()
    # --- নতুন হিসাব: মোট বিক্রির পরিমাণ ---
    total_sales = db.session.query(db.func.sum(TrashPost.total_transaction_value)).filter(TrashPost.status == 'completed').scalar() or 0.0
    total_profit = db.session.query(db.func.sum(TrashPost.platform_profit)).filter(TrashPost.status == 'completed').scalar() or 0.0
    
    recent_users = User.query.order_by(User.created_at.desc()).limit(5).all()
    recent_transactions = TrashPost.query.filter(TrashPost.status == 'completed').order_by(TrashPost.completed_at.desc()).limit(5).all()

    return render_template('admin_dashboard.html', 
                           title='Admin Panel',
                           total_users=total_users,
                           total_posts=total_posts,
                           total_sales=total_sales,
                           total_profit=total_profit,
                           recent_users=recent_users,
                           recent_transactions=recent_transactions)

# --- অ্যাডমিন ফিচার: ইউজার ম্যানেজমেন্ট ---
@app.route('/admin/users')
@login_required
def manage_users():
    if not current_user.is_admin:
        flash('You do not have permission to access this page.', 'danger')
        return redirect(url_for('home'))
    
    users = User.query.all()
    return render_template('manage_users.html', title='Manage Users', users=users)

@app.route('/admin/user/<int:user_id>/delete', methods=['POST'])
@login_required
def delete_user(user_id):
    if not current_user.is_admin:
        flash('Unauthorized access.', 'danger')
        return redirect(url_for('home'))

    user_to_delete = User.query.get_or_404(user_id)
    if user_to_delete.is_admin:
        flash('Admin users cannot be deleted.', 'warning')
        return redirect(url_for('manage_users'))

    TrashPost.query.filter_by(user_id=user_id).delete()

    db.session.delete(user_to_delete)
    db.session.commit()
    flash('User and their posts have been deleted.', 'success')
    return redirect(url_for('manage_users'))