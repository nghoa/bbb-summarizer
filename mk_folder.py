import os
import shutil
from flask import jsonify

# Getting dir for creation
dev_dir = os.path.expanduser("~/dev")
dev_path = dev_dir + "/data/"
root_target_dir = os.path.dirname(dev_path)
print('Root Target Dir: ' + root_target_dir)

def main():
    # TODO
    internal_meeting_id = 'd3b050f3b31a8b967b4affec4a6a044b31fbf0dc-1601799973266'
    # mkdir_data_folder()
    # Check if meeting has ended!!!
    # mkdir_presentation_folder(internal_meeting_id)
    mkdir_audio_folder(internal_meeting_id)

def mkdir_data_folder():
    access_rights = 0o755
    dev_dir = os.path.expanduser("~/dev")
    path = dev_dir + "/data"
    directory = os.path.dirname(path)
    if not os.path.exists(directory):
        try:
            os.makedirs(path)
        except OSError:
            print("Creation of directory %s failed" % path)
        else:
            print("Sucessfully created directory %s " % path)
    else:
        print("Directory already exists")

def mkdir_presentation_folder(internal_meeting_id):
    # TODO: Test internal_meeting_id where presentation was uploaded
    root_src_path = "/var/bigbluebutton/recording/raw/{}/presentation".format(internal_meeting_id)
    root_replacement_path = "/var/bigbluebutton/recording/raw"

    # Get Move_Dir => Directory which contains files, where we want to move them out
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
                dst_dir = src_dir.replace(root_replacement_path, root_target_dir)        # Test # root_src_dir
                print("New Destination Dir: " + dst_dir)
                if not os.path.exists(dst_dir):
                    os.makedirs(dst_dir)
                # Simple Copy Paste into new folder
                for file_ in files:
                    src_file = os.path.join(src_dir, file_)
                    dst_file = os.path.join(dst_dir, file_)
                    if os.path.exists(dst_file):
                        os.remove(dst_file)
                    shutil.copy(src_file, dst_dir)

    # TODO: Later for application 
    # return jsonify({'status': 200})

# Check audio structure
def mkdir_audio_folder(internal_meeting_id):
    root_src_path = "/var/bigbluebutton/recording/raw/{}/audio".format(internal_meeting_id)
    root_replacement_path = "/var/bigbluebutton/recording/raw"
    for src_dir, dirs, files in os.walk(root_src_path):
        dst_dir = src_dir.replace(root_replacement_path, root_target_dir)        # Test # root_src_dir
        # Make Audio folder if not existent
        if not os.path.exists(dst_dir):
            os.makedirs(dst_dir)
        for file_ in files:
            src_file = os.path.join(src_dir, file_)
            dst_file = os.path.join(dst_dir, file_)
            if os.path.exists(dst_file):
                os.remove(dst_file)
            shutil.copy(src_file, dst_dir)

    # TODO: Later for application 
    # return jsonify({'status': 200})

def mkdir_summarization_folder():
    # TODO
    # mkdir ~dev/<internal meeting id>/transcription
    # mkdir ~dev/<internal meeting id>/alignment
    # mkdir ~dev/<internal meeting id>/metadata.txt ???
    pass

if __name__ == '__main__':
    main()
