from flask_login import UserMixin
from datetime import datetime
from affiliate_store import login_manager, db


@login_manager.user_loader
def load_user(ide):
    return Admin.query.get(int(ide))


class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    first_par = db.Column(db.String)
    content = db.Column(db.Text)
    image_file = db.Column(db.String(20), nullable=False, default="test_img.jpg")
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    clicks = db.Column(db.Integer, default=0)
    tags = db.Column(db.String)

    def __repr__(self):
        return f'Blog <{self.title}> <{self.first_par}>'


class Topic(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    topic_tags = db.Column(db.String)


class Admin(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False)
    password1 = db.Column(db.String(30), nullable=False)
    password2 = db.Column(db.String(30), nullable=False)


class AdminLogs(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    admin_name = db.Column(db.String)
    log_info = db.Column(db.String)
    log_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
