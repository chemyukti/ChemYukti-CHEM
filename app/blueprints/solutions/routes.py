from flask import render_template
from app.blueprints.solutions import solutions_bp

@solutions_bp.route('/')
def index():
    return render_template('solutions/index.html')
