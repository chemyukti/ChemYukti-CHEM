from flask import render_template, redirect, url_for, flash, request, make_response
from flask_login import current_user, login_required
from app import db
from app.blueprints.main import main_bp
from app.models import Course, Testimonial, LearningBlueprint, LeadRequest
from app.forms import LearningBlueprintForm, LeadRequestForm
import json

@main_bp.route('/')
def index():
    testimonials = Testimonial.query.all()
    return render_template('main/index.html', testimonials=testimonials)

@main_bp.route('/courses')
def courses():
    courses = Course.query.all()
    return render_template('main/courses.html', courses=courses)

@main_bp.route('/chea')
def chea():
    return render_template('main/chea.html')

@main_bp.route('/chet')
def chet():
    return render_template('main/chet.html')

@main_bp.route('/loop90')
def loop90():
    return render_template('main/loop90.html')

@main_bp.route('/tools')
def tools():
    return render_template('main/tools.html')

@main_bp.route('/about')
def about():
    return render_template('main/about.html')

@main_bp.route('/learning-blueprint', methods=['GET', 'POST'])
def learning_blueprint():
    form = LearningBlueprintForm()
    if form.validate_on_submit():
        blueprint = LearningBlueprint(
            user_id=current_user.id if current_user.is_authenticated else None,
            student_class=form.student_class.data,
            board=form.board.data,
            exam_type=form.exam_type.data,
            learning_goal=form.learning_goal.data,
            subject_interests=form.subject_interests.data
        )
        # Mock logic for generating recommendations
        recommendations = {
            "assessment": "https://pratipariksha.in",
            "mentor": "AI Mentor",
            "resource": "Applied Cybernetics Module 1",
            "program": "CHEA Foundation"
        }
        blueprint.results = json.dumps(recommendations)
        db.session.add(blueprint)
        db.session.commit()
        return render_template('main/blueprint_result.html', blueprint=blueprint, recommendations=recommendations)
    return render_template('main/learning_blueprint.html', form=form)

@main_bp.route('/contact', methods=['GET', 'POST'])
def contact():
    form = LeadRequestForm()
    if form.validate_on_submit():
        lead = LeadRequest(
            name=form.name.data,
            email=form.email.data,
            phone=form.phone.data,
            service_type=form.service_type.data,
            message=form.message.data
        )
        db.session.add(lead)
        db.session.commit()
        flash('Your request has been sent. We will contact you soon.')
        return redirect(url_for('main.contact'))
    return render_template('main/contact.html', form=form)

@main_bp.route('/robots.txt')
def robots():
    response = make_response(render_template('robots.txt'))
    response.headers['Content-Type'] = 'text/plain'
    return response

@main_bp.route('/sitemap.xml')
def sitemap():
    response = make_response(render_template('sitemap.xml'))
    response.headers['Content-Type'] = 'application/xml'
    return response
