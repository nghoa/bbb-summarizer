from flask import Flask, render_template, request
from apis.bigbluebutton import get_meetings
from utility.serve_audio import serve_wav

def hello():
    return render_template('hello.html')

def album():
	return render_template('album.html')

## Getting Query String
# data?param=value&param2=value2
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

def serve_filepath(internal_meeting_id):
    path = path = f'/var/bigbluebutton/recording/raw{internal_meeting_id}/audio/{internal_meeting_id}.wav'
    return 'file'


## Getting direct value from url
def get_param(param):
    return render_template('meta-data.html', metadata=param)

def table():
    return render_template('table.html')