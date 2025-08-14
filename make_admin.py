import sys
from app import app, db
from models import User

def make_admin(email):
    with app.app_context():
        user = User.query.filter_by(email=email).first()
        if user:
            user.is_admin = True
            db.session.commit()
            print(f"User '{email}' has been successfully made an admin.")
        else:
            print(f"User with email '{email}' not found.")

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python make_admin.py <your_registered_email>")
    else:
        user_email = sys.argv[1]
        make_admin(user_email)