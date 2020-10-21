#################
#### imports ####
#################
from flask import render_template, jsonify, request
import time

from app.apis.bigbluebutton import get_meetings
from . import lectures_blueprint
from .get_stuff import get_config

@lectures_blueprint.route('/lectures')
def index():
    return render_template('lectures.html')

@lectures_blueprint.route('/lectures/album')
def album():
    return render_template('album.html')

@lectures_blueprint.route('/lectures/stuff')
def stuff():
    test = get_config()
    print(test)
    return test

## Getting Query String
# data?param=value&param2=value2
@lectures_blueprint.route('/lectures/data')
def get_query_string():
    # request.query_string           ## Whole Request String
    meetings = get_meetings()
    conf_num = request.args.get('confnum')

    for meeting in meetings:
        if (meeting['voice_bridge'] == conf_num):
            internal_meeting_id = meeting['internal_meeting_id']

    filepath = serve_filepath(internal_meeting_id)

    metadata = {
        "conference_number": conf_num,
        "conference_name": request.args.get('confname'),
        "internal_meeting_id": internal_meeting_id,
        "filepath": filepath
    }

    return render_template('meta-data.html', metadata=metadata)

# AJAX Loading screen
@lectures_blueprint.route('/lectures/ajax/index')
def load():
    # Processing function
    time.sleep(5)
    return '<h1>Done Loading!</h1>'

# Test interactive ajax after submitting a form
@lectures_blueprint.route('/lectures/interactive')
def interactivate():
    return render_template('interactive.html')

@lectures_blueprint.route('/background_process')
def background_process():
    try:
        lang = request.args.get('proglang', 0, type=str)
        if lang.lower() == 'python':
            return jsonify(result='Your are wise')
        else:
            return jsonify(result='Try again.')
    except Exception as e:
        return str(e)