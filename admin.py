from flask_admin import Admin, expose, AdminIndexView
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user
from flask import redirect, url_for
from app import app, db
from models import User, TrashPost

class MyModelView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and getattr(current_user, 'is_admin', False)

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('login'))

class MyAdminIndexView(AdminIndexView):
    @expose('/')
    def index(self):
        total_users = User.query.count()
        total_posts = TrashPost.query.count()
        total_earnings = db.session.query(db.func.sum(TrashPost.price)).filter(TrashPost.status == 'completed').scalar() or 0.0

        return self.render(
            'admin/dashboard.html',
            total_users=total_users,
            total_posts=total_posts,
            total_earnings=f'{total_earnings:,.2f}'
        )

    def is_accessible(self):
        return current_user.is_authenticated and getattr(current_user, 'is_admin', False)

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('login'))

# আপডেট করা অংশ
admin = Admin(
    app,
    name='TrashToTreasure',
    template_mode='bootstrap4',
    index_view=MyAdminIndexView(
        name="Dashboard",
        template='admin/dashboard.html',
        url='/admin'
    )
)

admin.add_view(MyModelView(User, db.session))
admin.add_view(MyModelView(TrashPost, db.session))