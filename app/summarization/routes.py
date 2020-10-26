from flask import render_template, send_file
from app.utils.serve_meeting_files import get_pdf_file
import json
 
from . import summarization_blueprint

@summarization_blueprint.route('/summarization')
def index():
    return render_template('summarization.html')

# Serve static pdf file
@summarization_blueprint.route('/summarization/show/static-pdf')
def show_static_pdf():
    internal_meeting_id = '043a5a1430143ef9dd85be452e4e59901e944642-1603650621063'
    pdf_json = json.loads(get_pdf_file(internal_meeting_id))
    file_path = pdf_json['file_path']
    print(file_path)
    static_file = open(file_path, 'rb')
    return send_file(static_file, attachment_filename='meeting.pdf')

# TODO:
# Another pdf prototype
@summarization_blueprint.route('/summarization/pdftest')
def render_pdf():
    internal_meeting_id = '043a5a1430143ef9dd85be452e4e59901e944642-1603650621063'
    pdf_json = json.loads(get_pdf_file(internal_meeting_id))
    file_path = pdf_json['file_path']
    return render_template('summary.html', filepath=file_path)