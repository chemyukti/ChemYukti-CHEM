from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import db, login_manager

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    role = db.Column(db.String(20), default='student') # student, institute, admin
    is_force_password_change = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    mentor_bookings = db.relationship('MentorBooking', backref='student', lazy='dynamic')
    blueprints = db.relationship('LearningBlueprint', backref='user', lazy='dynamic')
    referrals = db.relationship('Referral', backref='referrer', lazy='dynamic', foreign_keys='Referral.referrer_id')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))

class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128))
    description = db.Column(db.Text)
    price = db.Column(db.Float)
    type = db.Column(db.String(50)) # CHEA, Loop90, etc.

class Mentor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))
    subject = db.Column(db.String(128))
    bio = db.Column(db.Text)
    image_url = db.Column(db.String(256))
    is_ai = db.Column(db.Boolean, default=False)

class MentorBooking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    mentor_id = db.Column(db.Integer, db.ForeignKey('mentor.id'))
    status = db.Column(db.String(20), default='pending') # pending, confirmed, completed
    payment_id = db.Column(db.String(128))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Payment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    razorpay_order_id = db.Column(db.String(128))
    razorpay_payment_id = db.Column(db.String(128))
    amount = db.Column(db.Float)
    currency = db.Column(db.String(10), default='INR')
    status = db.Column(db.String(20))
    product_type = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class LearningBlueprint(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    student_class = db.Column(db.String(50))
    board = db.Column(db.String(100))
    exam_type = db.Column(db.String(100))
    learning_goal = db.Column(db.Text)
    subject_interests = db.Column(db.Text)
    results = db.Column(db.Text) # JSON or descriptive text
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class ResearchPaper(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(256))
    authors = db.Column(db.String(256))
    abstract = db.Column(db.Text)
    publication_date = db.Column(db.Date)
    link = db.Column(db.String(256))
    is_featured = db.Column(db.Boolean, default=False)

class Publication(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(256))
    description = db.Column(db.Text)
    price = db.Column(db.Float, default=150.0)
    file_url = db.Column(db.String(256))
    type = db.Column(db.String(50)) # Book, Module, Resource

class Testimonial(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))
    content = db.Column(db.Text)
    role = db.Column(db.String(128))
    image_url = db.Column(db.String(256))
    video_url = db.Column(db.String(256))

class ForumPost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(256))
    content = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    author = db.relationship('User', backref=db.backref('posts', lazy='dynamic'))
    replies = db.relationship('ForumReply', backref='post', lazy='dynamic')

class ForumReply(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    post_id = db.Column(db.Integer, db.ForeignKey('forum_post.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    author = db.relationship('User', backref=db.backref('forum_replies', lazy='dynamic'))

class SupportTicket(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    subject = db.Column(db.String(256))
    description = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    status = db.Column(db.String(20), default='open')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    user = db.relationship('User', backref=db.backref('support_tickets', lazy='dynamic'))

class Referral(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    referrer_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    referred_email = db.Column(db.String(120))
    status = db.Column(db.String(20), default='pending')

class SiteContent(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(64), unique=True)
    content = db.Column(db.Text)

class LeadRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))
    email = db.Column(db.String(120))
    phone = db.Column(db.String(20))
    service_type = db.Column(db.String(100)) # Website, App, Solution
    message = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
