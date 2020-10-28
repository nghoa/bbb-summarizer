from flask import render_template, jsonify, request, redirect, url_for, json
import time
from datetime import datetime, timedelta
# In App Modules
from app.apis.bigbluebutton import get_meetings
from app.apis.pb_connect import meeting_has_ended
from app.utils.mk_folder import mkdir_data_folder, mkdir_presentation_folder, mkdir_audio_folder
from app.utils.gcp_transcription import execute_transcription
from app.utils.serve_meeting_files import alignment_file_exists
from app.hmm_alignment.start_summarization import start_alignment
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
    alignment_file_exists = alignment_file_exists(internal_meeting_id)
    if (meeting_end and not alignment_file_exists):
        ###### after meeting has ended do following:
        # mkdir folders
        data_folder_constructed = mkdir_data_folder()
        if (data_folder_constructed):
            audio_folder_constructed = mkdir_audio_folder(internal_meeting_id)
            presentation_folder_constructed = mkdir_presentation_folder(internal_meeting_id)
            if (audio_folder_constructed and presentation_folder_constructed):
                transcription_done = execute_transcription(internal_meeting_id)
                if (transcription_done):
                    # align meeting
                    alignment_done = start_alignment(internal_meeting_id)
                    if (alignment_done):
                        # redirect to summarization route
                        # TODO: return #loading -> with button 
                        return  ''' 
                                    <div id="overlay" style="display: none;">
                                        <div class="w-100 d-flex justify-content-center align-items-center">
                                            <div class="spinner"></div>
                                        </div>
                                    </div>
                                    <div class="btn-group">
									    <a href="">
                                            <button type="button" class="btn btn-sm btn-outline-secondary">Go to Alignment</button>
                                        </a>
								    </div>
                                '''
    else:
        return  ''' 
                <div id="overlay" style="display: none;">
                    <div class="w-100 d-flex justify-content-center align-items-center">
                        <div class="spinner"></div>
                    </div>
                </div>
                <div class="btn-group">
                    <a href="">
                        <button type="button" class="btn btn-sm btn-outline-secondary">Go to Alignment</button>
                    </a>
                </div>
                '''

### Test setup
@lectures_blueprint.route('/lectures/workplace')
def test_workplace():
    # internal_meeting_id = '043a5a1430143ef9dd85be452e4e59901e944642-1603650621063'
    internal_meeting_id = 'b43a5a9996343ef9dd85be452e4e59901e944642-123456311'
    ## TODO: test
    transcription_done = execute_transcription(internal_meeting_id)
    if (transcription_done):
        # align meeting
        alignment_done = start_alignment(internal_meeting_id)
        return 'Everything done'

