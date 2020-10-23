from flask import render_template, jsonify, request, redirect, url_for
import time
# In App Modules
from app.apis.bigbluebutton import get_meetings
from . import lectures_blueprint
from .get_stuff import get_config

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



# TODO:
# Testing out redirect from confnum -> lecture with metadata
@lectures_blueprint.route('/lectures/testplace/data')
def get_confnum():
    conf_num = request.args.get('confnum')
    metadata = {
        "conference_number": conf_num,
        "conference_name": "Conference Name Test",
        "internal_meeting_id": "Internal Meeting ID test",
        "starttime": "1603483882428",
        "current_presenter": "Lorem Ipsum"
    }

    return redirect(url_for('.show_lecture_with_metadata', metadata=metadata, _external=True))

@lectures_blueprint.route('/lectures/testplace')
def show_lecture_with_metadata():
    metadata = request.args.get('metadata')     # counterpart for url_for
    # metadata = {
    #     "conference_number": conf_num,
    #     "conference_name": "Conference Name Test",
    #     "internal_meeting_id": "Internal Meeting ID test",
    #     "starttime": "1603483882428",
    #     "current_presenter": "Lorem Ipsum"
    # }

    return render_template('lecture_test.html', metadata=metadata)


# TODO:
# - adding loading screen, while meeting has not ended
# - adding some basic information (metadata from bbb-api)
# - [internal_meeting_id, meeting_name, conf_num, current_presenter]
@lectures_blueprint.route('/lectures/overview')
def overview():
    status_code = {"code": "loading"}
    return render_template('lectures.html', status_code = status_code)

@lectures_blueprint.route('/lectures/overview/loaded')
def overview_loaded():
    time.sleep(5)
    status_code = {"code": "done"}
    return render_template('lectures.html', status_code = status_code)


@lectures_blueprint.route('/lectures/ajax')
def index():
    return render_template('ajaxindex.html')

# AJAX Loading screen
@lectures_blueprint.route('/lectures/ajax/loaded')
def load():
    # Processing function
    time.sleep(5)
    return '<h1>Done Loading!</h1>'



# TODO:
####### ---------- Testspace -------------------
@lectures_blueprint.route('/lectures/stuff')
def stuff():
    test = get_config()
    print(test)
    return test


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