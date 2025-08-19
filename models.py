from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import db
from datetime import datetime
import statistics

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    user_type = db.Column(db.String(20), default='user', nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    total_earnings = db.Column(db.Numeric(10, 2), default=0.00)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    posts = db.relationship('TrashPost', foreign_keys='TrashPost.user_id', backref='owner', lazy='dynamic', cascade="all, delete-orphan")
    collections = db.relationship('TrashPost', foreign_keys='TrashPost.collector_id', backref='collector', lazy='dynamic')
    reviews_given = db.relationship('Review', foreign_keys='Review.reviewer_id', backref='reviewer', lazy='dynamic', cascade="all, delete-orphan")
    reviews_received = db.relationship('Review', foreign_keys='Review.reviewee_id', backref='reviewee', lazy='dynamic', cascade="all, delete-orphan")
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        
    def average_rating(self):
        reviews = self.reviews_received.all()
        if not reviews:
            return 0
        return round(statistics.mean([review.rating for review in reviews]), 1)
    
    @staticmethod
    def create(username, email, password, user_type='user'):
        user = User(username=username, email=email, user_type=user_type)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        return user

class TrashPost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    trash_type = db.Column(db.String(50), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    location = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    status = db.Column(db.String(20), default='available', nullable=False)
    collector_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    price_per_kg = db.Column(db.Numeric(10, 2), nullable=False)
    is_negotiable = db.Column(db.Boolean, default=False, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    completed_at = db.Column(db.DateTime)
    
    final_weight_kg = db.Column(db.Float, nullable=True)
    final_price_per_kg = db.Column(db.Numeric(10, 2), nullable=True)
    total_transaction_value = db.Column(db.Numeric(10, 2), nullable=True)
    platform_profit = db.Column(db.Numeric(10, 2), nullable=True)
    
    phone_number = db.Column(db.String(20), nullable=True)
    google_map_link = db.Column(db.String(500), nullable=True)
    image_file = db.Column(db.String(30), nullable=False, default='default.jpg')
    
    reviews = db.relationship('Review', backref='post', lazy='dynamic', cascade="all, delete-orphan")

    def __init__(self, user_id, trash_type, quantity, location, description, price_per_kg, is_negotiable, phone_number, google_map_link, image_file='default.jpg'):
        self.user_id = user_id
        self.trash_type = trash_type
        self.quantity = quantity
        self.location = location
        self.description = description
        self.price_per_kg = price_per_kg
        self.is_negotiable = is_negotiable
        self.phone_number = phone_number
        self.google_map_link = google_map_link
        self.image_file = image_file
    
    @staticmethod
    def get_available():
        return TrashPost.query.filter_by(status='available').order_by(TrashPost.created_at.desc()).all()
    

    @staticmethod
    def create(user_id, trash_type, quantity, location, description, price_per_kg, is_negotiable, phone_number, google_map_link, image_file='default.jpg'):
        post = TrashPost(user_id=user_id, trash_type=trash_type, quantity=quantity, location=location, description=description, price_per_kg=price_per_kg, is_negotiable=is_negotiable, phone_number=phone_number, google_map_link=google_map_link, image_file=image_file)
        db.session.add(post)
        db.session.commit()
        return post

class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    rating = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    post_id = db.Column(db.Integer, db.ForeignKey('trash_post.id'), nullable=False)
    reviewer_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    reviewee_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Review(rating={self.rating})"