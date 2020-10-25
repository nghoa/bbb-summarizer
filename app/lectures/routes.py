from flask import render_template, jsonify, request, redirect, url_for, json
import time
from datetime import datetime, timedelta
# In App Modules
from app.apis.bigbluebutton import get_meetings
from app.apis.pb_connect import meeting_has_ended
from app.utils.mk_folder import mkdir_data_folder, mkdir_presentation_folder, mkdir_audio_folder
from app.utils.gcp_transcription import execute_transcription
from . import lectures_blueprint
from .get_stuff import get_config

# Querystring from confnum => get_meetings and so on...
## Getting Query String
# data?param=value&param2=value2
@lectures_blueprint.route('/lectures/data')
def get_meeting_info():
    # Get all current meetings via API Call
    meetings = get_meetings()
    conf_num = request.args.get('confnum')

    for meeting in meetings:
        # Voice Bridge used as identifier for "current meeting"
        if (meeting['voice_bridge'] == conf_num):
            internal_meeting_id = meeting['internal_meeting_id']
            meeting_name = meeting['meeting_name']
            current_presenter = meeting['current_presenter']

            # Dateformat transform: "1234567890" -> "dd-mm-YYYY hh:mm:ss" 
            start_time_str = meeting['start_time']
            f_start_number = float(start_time_str)
            start_time = datetime.fromtimestamp(f_start_number / 1e3)
            # original timezone was UTC -> +2 for Germany
            german_start_time = (start_time + timedelta(hours=2)).strftime('%d-%m-%Y %H:%M:%S')
            duration = int((datetime.now() - start_time).total_seconds() / 60)

            metadata_dict = {
                "conference_number": conf_num,
                "conference_name": meeting_name,            # request.args.get('confname') also possible
                "internal_meeting_id": internal_meeting_id,
                "start_time": german_start_time,
                "current_presenter": current_presenter,
                "current_duration": duration
            }
            metadata = json.dumps(metadata_dict)

            return redirect(url_for('.show_lecture_with_metadata', metadata=metadata))


@lectures_blueprint.route('/lectures')
def show_lecture_with_metadata():
    metadata = request.args['metadata']     # counterpart for url_for
    metadata_json = json.loads(metadata)

    # through ajax the /lectures/prepare_meeting_data route will be immediately triggered
    return render_template('lecture.html', metadata = metadata_json)


@lectures_blueprint.route('/lectures/prepare_meeting_data')
def prepare_meeting_summary():
    # meeting_has_ended function
    internal_meeting_id = request.args.get('internalMeetingId')
    meeting_end = meeting_has_ended(internal_meeting_id)
    if (meeting_end):

        # TODO:
        ###### after meeting has ended do following:
        # mkdir folders
        data_folder_constructed = mkdir_data_folder()
        if (data_folder_constructed):
            audio_folder_constructed = mkdir_audio_folder(internal_meeting_id)
            presentation_folder_constructed = mkdir_presentation_folder(internal_meeting_id)
            print('prepare_meeting_summary route: ')
            print(audio_folder_constructed)
            print(presentation_folder_constructed)
            if (audio_folder_constructed and presentation_folder_constructed):
                # TODO: transcribe meeting
                transcription_done = execute_transcription()
                # get presentation
                # align meeting
                # TODO:
                # redirect to summarization route
                # serve files there...
                return  ''' 
                            <div id="overlay" style="display: none;">
                                <div class="w-100 d-flex justify-content-center align-items-center">
                                    <div class="spinner"></div>
                                </div>
                            </div>
                        '''

@lectures_blueprint.route('/lectures/new_loading_script')
def replace_ajax():
    return ''


# TODO
#### ------- Working Space ------- #####

# TODO: Testing another ajax 
@lectures_blueprint.route('/lectures/ajax')
def lecture_ajax():
    return render_template('lecture_ajax.html')

# TODO:
####### ---------- Testspace -------------------
@lectures_blueprint.route('/lectures/stuff')
def stuff():
    test = get_config()
    print(test)
    return test

# TODO: instead of using submit as an Event Trigger -> I want to use a backend eventHandler -> meeting_has_ended to replace the specific svg
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



# TODO:
# Archive

# Testing out redirect from confnum -> lecture with metadata
@lectures_blueprint.route('/lectures/testplace/data')
def get_meeting_info_test():
    conf_num = request.args.get('confnum')
    start_number = "1603483882428"
    f_start_number = float(start_number)
    start_time = datetime.datetime.fromtimestamp(f_start_number / 1e3).strftime('%d-%m-%Y %H:%M:%S')

    metadata_dict = {
        "conference_number": conf_num,
        "conference_name": "Conference Name Test",
        "internal_meeting_id": "Internal Meeting ID test",
        "start_time": start_time,
        "current_presenter": "Lorem Ipsum"
    }
    metadata = json.dumps(metadata_dict)

    return redirect(url_for('.show_lecture_with_metadata', metadata=metadata))

# AJAX Loading screen
@lectures_blueprint.route('/lectures/ajax/prepare_meeting')
def prepare_meeting_summary_test():
    # meeting_has_ended function
    time.sleep(5)
    return  ''' 
                <div id="overlay" style="display: none;">
                    <div class="w-100 d-flex justify-content-center align-items-center">
                        <div class="spinner"></div>
                    </div>
                </div>
            '''

# TODO: dunno for what
@lectures_blueprint.route('/lectures/ajax/new_loading_script')
def replace_ajax_test():
    return ''

# Prototype for simple loading screen with parsing status_code param
@lectures_blueprint.route('/lectures/overview')
def overview():
    status_code = {"code": "loading"}
    return render_template('lecture_loading.html', status_code = status_code)

@lectures_blueprint.route('/lectures/overview/loaded')
def overview_loaded():
    time.sleep(5)
    status_code = {"code": "done"}
    return render_template('lecture_loading.html', status_code = status_code)