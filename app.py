import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from sqlalchemy.orm import DeclarativeBase
from werkzeug.middleware.proxy_fix import ProxyFix
from flask_migrate import Migrate

# --- ডাটাবেস পাথের জন্য নতুন কোড ---
# প্রজেক্টের রুট ডিরেক্টরির পাথ খুঁজে বের করা হচ্ছে
basedir = os.path.abspath(os.path.dirname(__file__))
# instance ফোল্ডারের পাথ তৈরি করা হচ্ছে
instance_path = os.path.join(basedir, 'instance')
# যদি instance ফোল্ডার না থাকে, তবে তৈরি করা হচ্ছে
os.makedirs(instance_path, exist_ok=True)


class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)
login_manager = LoginManager()
migrate = Migrate()

app = Flask(__name__)
app.secret_key = "a-very-secret-key-for-development"
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

# --- ডাটাবেস URI-তে নতুন পাথ ব্যবহার করা হচ্ছে ---
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(instance_path, 'database.db')
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# --- নতুন: ছবি আপলোডের জন্য ফোল্ডার কনফিগারেশন ---
UPLOAD_FOLDER = os.path.join(basedir, 'static/post_pics')
os.makedirs(UPLOAD_FOLDER, exist_ok=True) 
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


db.init_app(app)
login_manager.init_app(app)
migrate.init_app(app, db)

login_manager.login_view = 'login'
login_manager.login_message = 'Please log in to access this page.'
login_manager.login_message_category = 'info'

@login_manager.user_loader
def load_user(user_id):
    from models import User
    return User.query.get(int(user_id))

from routes import *