from flask import render_template
from app.utils.serve_meeting_files import get_audio_file
 
from . import summarization_blueprint

@summarization_blueprint.route('/summarization')
def index():
    return render_template('summarization.html')