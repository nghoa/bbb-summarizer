'''
    After successfully converting opus -> wav 
    Wav.file is saved in same directory
'''

def serve_wav(internal_meeting_id):
    path = path = f'/var/bigbluebutton/recording/raw{internal_meeting_id}/audio/{internal_meeting_id}.wav'
    return 'file'

