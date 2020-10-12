# import bigbluebutton api -> for internal_meeting_id

'''
    !!! Only start the conversion of wav -> opus when meeting is finished!!!
'''


'''
    Needs to get "internalMeetingId" from /apis/bigbluebutton.py
'''
def get_opus():
    internal_meeting_id = get_meeting_id()
    path = f'/var/bigbluebutton/recording/raw{internal_meeting_id}/audio/{internal_meeting_id}.opus'
    return path

'''
    Opus -> Wav Converter
    Save Wav.file in BBB Filesystem
'''
def opus_to_wav():
    path = get_opus()
    # Save Wav.file in BBB filesystem

def main():
    pass




