from flask import render_template, redirect, url_for, flash, request
from flask_login import login_required
from app import db
from app.blueprints.admin import admin_bp
from app.models import User, LeadRequest, Mentor, Publication, ResearchPaper, Testimonial
from app.decorators import admin_required
from app.forms import PublicationForm

@admin_bp.route('/dashboard')
@login_required
@admin_required
def dashboard():
    user_count = User.query.count()
    lead_count = LeadRequest.query.count()
    leads = LeadRequest.query.order_by(LeadRequest.created_at.desc()).limit(10).all()
    return render_template('admin/dashboard.html', user_count=user_count, lead_count=lead_count, leads=leads)

@admin_bp.route('/leads')
@login_required
@admin_required
def leads():
    all_leads = LeadRequest.query.order_by(LeadRequest.created_at.desc()).all()
    return render_template('admin/leads.html', leads=all_leads)

@admin_bp.route('/users')
@login_required
@admin_required
def users():
    all_users = User.query.all()
    return render_template('admin/users.html', users=all_users)

@admin_bp.route('/publications', methods=['GET', 'POST'])
@login_required
@admin_required
def publications():
    form = PublicationForm()
    if form.validate_on_submit():
        pub = Publication(
            title=form.title.data,
            description=form.description.data,
            price=form.price.data,
            type=form.type.data
        )
        db.session.add(pub)
        db.session.commit()
        flash('Publication added successfully.')
        return redirect(url_for('admin.publications'))
    pubs = Publication.query.all()
    return render_template('admin/publications.html', form=form, publications=pubs)

@admin_bp.route('/research/add', methods=['POST'])
@login_required
@admin_required
def add_research():
    title = request.form.get('title')
    authors = request.form.get('authors')
    abstract = request.form.get('abstract')
    paper = ResearchPaper(title=title, authors=authors, abstract=abstract)
    db.session.add(paper)
    db.session.commit()
    flash('Research paper added.')
    return redirect(url_for('research.index'))
