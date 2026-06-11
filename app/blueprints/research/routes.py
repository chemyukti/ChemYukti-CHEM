from flask import render_template
from app.blueprints.research import research_bp
from app.models import ResearchPaper, Publication

@research_bp.route('/')
def index():
    papers = ResearchPaper.query.all()
    return render_template('research/index.html', papers=papers)

@research_bp.route('/publications')
def publications():
    pubs = Publication.query.all()
    return render_template('research/publications.html', publications=pubs)
