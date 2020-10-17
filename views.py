from flask import Flask, render_template, request
from apis.bigbluebutton import get_meetings
from utility.serve_audio import serve_wav

def hello():
    return render_template('hello.html')

def album():
	return render_template('album.html')

## Getting Query String
def get_query_string():
    # request.query_string           ## Whole Request String
    meetings = get_meetings()
    conf_num = request.args.get('confnum')

    # Check whether "Summarized Meeting" is same as an actual running meeting
    for meeting in meetings:
        if (meeting['voice_bridge'] == conf_num):
            internal_meeting_id = meeting['internal_meeting_id']

    metadata = {
        "conference_number": conf_num,
        "conference_name": request.args.get('confname'),
        "internal_meeting_id": internal_meeting_id
    }

    return render_template('meta-data.html', metadata=metadata)

## Getting direct value from url
def get_param(param):
    return render_template('meta-data.html', metadata=param)

def table():
    return render_template('table.html')