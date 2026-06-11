from flask import render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app import db
from app.blueprints.mentors import mentors_bp
from app.models import Mentor, MentorBooking

@mentors_bp.route('/')
def index():
    ai_mentors = Mentor.query.filter_by(is_ai=True).all()
    human_mentors = Mentor.query.filter_by(is_ai=False).all()
    return render_template('mentors/index.html', ai_mentors=ai_mentors, human_mentors=human_mentors)

@mentors_bp.route('/book/<int:mentor_id>', methods=['POST'])
@login_required
def book(mentor_id):
    mentor = Mentor.query.get_or_404(mentor_id)
    booking = MentorBooking(user_id=current_user.id, mentor_id=mentor.id, status='pending')
    db.session.add(booking)
    db.session.commit()
    flash(f'Booking request for {mentor.name} created. Please proceed to payment.')
    return redirect(url_for('mentors.index'))
