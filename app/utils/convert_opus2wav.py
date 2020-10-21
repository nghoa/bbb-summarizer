import os
import shutil
from flask import jsonify

'''
    !!! Only start the conversion of wav -> opus when meeting is finished!!!
'''

'''
    Needs to get "internalMeetingId" from /apis/bigbluebutton.py
'''
def get_opus(internal_meeting_id, path):
    for paths, dirs, files in os.walk(path):
        for file_ in files:
            base, extension = file_.split('.')
            if (extension == 'opus'):
                # start conversion
                audio_file = os.path.join(paths, file_)
                test = opus_to_wav(audio_file)
                print (base)
                print (extension)
                

'''
    Opus -> Wav Converter
    Save Wav.file in BBB Filesystem
'''
def opus_to_wav():
    path = get_opus()
    # Save Wav.file in BBB filesystem

def main():
    internal_meeting_id = 'd3b050f3b31a8b967b4affec4a6a044b31fbf0dc-1601799973266'
    dev_dir = os.path.expanduser("~/dev")
    dev_path = dev_dir + "/data/" + internal_meeting_id + "/audio/"
    root_target_dir = os.path.dirname(dev_path)
    opus = get_opus(internal_meeting_id, root_target_dir)

if __name__ == '__main__':
    main()




