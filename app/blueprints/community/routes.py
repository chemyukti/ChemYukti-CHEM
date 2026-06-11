from flask import render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app import db
from app.blueprints.community import community_bp
from app.models import ForumPost, ForumReply, SupportTicket, Referral
from app.forms import ForumPostForm, ForumReplyForm

@community_bp.route('/')
def index():
    posts = ForumPost.query.order_by(ForumPost.created_at.desc()).all()
    return render_template('community/index.html', posts=posts)

@community_bp.route('/post/<int:post_id>', methods=['GET', 'POST'])
def post(post_id):
    post = ForumPost.query.get_or_404(post_id)
    form = ForumReplyForm()
    if form.validate_on_submit():
        if not current_user.is_authenticated:
            flash('Please login to reply.')
            return redirect(url_for('auth.login'))
        reply = ForumReply(content=form.content.data, user_id=current_user.id, post_id=post.id)
        db.session.add(reply)
        db.session.commit()
        return redirect(url_for('community.post', post_id=post.id))
    return render_template('community/post.html', post=post, form=form)

@community_bp.route('/new_post', methods=['GET', 'POST'])
@login_required
def new_post():
    form = ForumPostForm()
    if form.validate_on_submit():
        post = ForumPost(title=form.title.data, content=form.content.data, user_id=current_user.id)
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('community.index'))
    return render_template('community/new_post.html', form=form)

@community_bp.route('/referrals')
@login_required
def referrals():
    referrals = Referral.query.filter_by(referrer_id=current_user.id).all()
    return render_template('community/referrals.html', referrals=referrals)
