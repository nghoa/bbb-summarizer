import os
import shutil
import time
from flask import jsonify

# Getting dir for creation
# PROJECT_APP_DIR = os.path.expanduser("~/dev/bbb-summarizer")
PROJECT_APP_DIR = os.path.dirname(os.path.abspath(os.path.join(__file__ ,"..")))
print(PROJECT_APP_DIR)
DEV_PATH = PROJECT_APP_DIR + "/data/"
ROOT_TARGET_DIR = os.path.dirname(DEV_PATH)
print("Root Target Dir: " + ROOT_TARGET_DIR)

def main():
    # TODO
    internal_meeting_id = 'd3b050f3b31a8b967b4affec4a6a044b31fbf0dc-1601799973266'
    # mkdir_data_folder()
    # Check if meeting has ended!!!
    # mkdir_presentation_folder(internal_meeting_id)
    mkdir_audio_folder(internal_meeting_id)

def mkdir_data_folder():
    access_rights = 0o755
    directory = os.path.dirname(DEV_PATH)
    print('Data Directory: ' + directory)
    if not os.path.exists(directory):
        try:
            os.makedirs(ROOT_TARGET_DIR)
            return True
        except OSError:
            print("Creation of directory %s failed" % ROOT_TARGET_DIR)
        else:
            print("Sucessfully created directory %s " % ROOT_TARGET_DIR)
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
                        dst_dir = src_dir.replace(root_replacement_path, ROOT_TARGET_DIR)        # Test # root_src_dir
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
                dst_dir = src_dir.replace(root_replacement_path, ROOT_TARGET_DIR)        # Test # root_src_dir
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

def mkdir_summarization_folder():
    # TODO
    # mkdir ~dev/<internal meeting id>/transcription
    # mkdir ~dev/<internal meeting id>/alignment
    # mkdir ~dev/<internal meeting id>/metadata.txt ???
    pass


if __name__ == '__main__':
    # main()
    mkdir_summarization_folder()