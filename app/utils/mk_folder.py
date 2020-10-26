import os
import shutil
import time
from flask import jsonify

# Getting dir for creation
# PROJECT_APP_DIR = os.path.expanduser("~/dev/bbb-summarizer")
PROJECT_APP_DIR = os.path.dirname(os.path.abspath(os.path.join(__file__ ,"..")))
TARGET_DATA_PATH = os.path.join(PROJECT_APP_DIR, 'data')

def mkdir_data_folder():
    access_rights = 0o755
    if not os.path.exists(TARGET_DATA_PATH):
        try:
            os.makedirs(TARGET_DATA_PATH)
            return True
        except OSError:
            print("Creation of directory %s failed" % TARGET_DATA_PATH)
        else:
            print("Sucessfully created directory %s " % TARGET_DATA_PATH)
    else:
        print("Data Directory already exists")
        return True

def mkdir_presentation_folder(internal_meeting_id):
    # TODO: Test internal_meeting_id where presentation was uploaded
    root_src_path = "/var/bigbluebutton/recording/raw/{}/presentation".format(internal_meeting_id)
    root_replacement_path = "/var/bigbluebutton/recording/raw"

    # BBB needs time to process the recording and create the files
    while not os.path.exists(root_src_path):
        time.sleep(2)

    # Get Move_Dir => Directory which contains files, where we want to move them out
    if os.path.exists(root_src_path):
        try:
            for o in os.listdir(root_src_path):
                # directory of default presentation starts with default_string
                # needs to be ignored
                default_string = 'd2d9a672040fbde2a47a10bf6c37b6a4b5ae187f'
                if not default_string in o:
                    root_src_dir = os.path.join(root_src_path, o)
                    print('Root Source Presentation Path: ' + root_src_dir)

                    # Get all files from presentation_dir 
                    for src_dir, dirs, files in os.walk(root_src_dir):
                        # Use root_replacement_path NOT root_src_dir because there might be multiple presentation 
                        dst_dir = src_dir.replace(root_replacement_path, TARGET_DATA_PATH)        # Test # root_src_dir
                        print("New Destination Dir: " + dst_dir)
                        if not os.path.exists(dst_dir):
                            os.makedirs(dst_dir)
                        # Simple Copy Paste into new folder
                        for file_ in files:
                            print('Files: ', file_)
                            src_file = os.path.join(src_dir, file_)
                            print('Source File: ', src_file)
                            dst_file = os.path.join(dst_dir, file_)
                            print('Destination file: ', dst_file)
                            if os.path.exists(dst_file):
                                os.remove(dst_file)
                            shutil.copy(src_file, dst_dir)
                    return True
        except OSError:
            print("OS Error for that path: " + root_src_path)
        else:
            print("Mkdir presentation, everything is done")
    else:
        print("Path for presentation does not exists: " + root_src_path)
    

# Check audio structure
def mkdir_audio_folder(internal_meeting_id):
    root_src_path = "/var/bigbluebutton/recording/raw/{}/audio".format(internal_meeting_id)
    root_replacement_path = "/var/bigbluebutton/recording/raw"

    # BBB needs time to process the recording and create the files
    while not os.path.exists(root_src_path):
        time.sleep(2)

    if os.path.exists(root_src_path):
        try:
            for src_dir, dirs, files in os.walk(root_src_path):
                dst_dir = src_dir.replace(root_replacement_path, TARGET_DATA_PATH)        # Test # root_src_dir
                # Make Audio folder if not existent
                if not os.path.exists(dst_dir):
                    os.makedirs(dst_dir)
                for file_ in files:
                    src_file = os.path.join(src_dir, file_)
                    dst_file = os.path.join(dst_dir, file_)
                    if os.path.exists(dst_file):
                        os.remove(dst_file)
                    shutil.copy(src_file, dst_dir)
            return True
        except OSError:
            print("OSError for that path: " + root_src_path)
        else:
            print("Mkdir audio folder, Everything is done!")
    else:
        print("Path for audio does not exists: " + root_src_path)

# TODO:
# Auslagern der Funktion in create_summary()
# Auslagern der Funktion in create_alignment()

def mkdir_summarization_folder(internal_meeting_id):
    alignment_dir = os.path.join(TARGET_DATA_PATH, internal_meeting_id, 'alignment')
    summarization_dir = os.path.join(TARGET_DATA_PATH, internal_meeting_id, 'summarization')
    if not os.path.exists(alignment_dir):
        os.makedirs(alignment_dir)
    if not os.path.exists(summarization_dir):
        os.makedirs(summarization_dir)

if __name__ == '__main__':
    # main()
    internal_meeting_id = '043a5a1430143ef9dd85be452e4e59901e944642-1603650621063'
    mkdir_summarization_folder(internal_meeting_id)