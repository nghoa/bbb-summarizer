import os
import shutil
from flask import jsonify

def mkdir_data_folder():
    access_rights = 0o755
    dev_dir = os.path.expanduser("~/dev")
    path = dev_dir + "/data"
    directory = os.path.dirname(path)
    if not os.path.exists(directory):
        try:
            os.mkdir(path)
        except OSError:
            print("Creation of directory %s failed" % path)
        else:
            print("Sucessfully created directory %s " % path)
    else:
        print("Directory already exists")

def mkdir_presentation_folder():
    # TODO: Test internal_meeting_id where presentation was uploaded
    internal_meeting_id = 'd3b050f3b31a8b967b4affec4a6a044b31fbf0dc-1601799973266'
    root_src_path = "/var/bigbluebutton/recording/raw/{}/presentation".format(internal_meeting_id)

    # Getting dir for creation
    dev_dir = os.path.expanduser("~/dev")
    dev_path = dev_dir + "/data/"
    root_target_dir = os.path.dirname(dev_path)
    print('Root Target Dir: ' + root_target_dir)

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
                # Use root_src_path NOT root_src_dir because there might be multiple presentation 
                # folder structure: 
                # <meeting_id_folder>
                # ---- <presentation_id_folder_1>
                # ---- <presentation_id_folder_2>
                # ---- ....
                dst_dir = src_dir.replace(root_src_path, root_target_dir)        
                print("New Destination Dir: " + dst_dir)
                if not os.path.exists(dst_dir):
                    os.mkdir(dst_dir)
                for file_ in files:
                    src_file = os.path.join(src_dir, file_)
                    dst_file = os.path.join(dst_dir, file_)
                    if os.path.exists(dst_file):
                        os.remove(dst_file)
                    shutil.copy(src_file, dst_dir)

    return jsonify(status='success')

if __name__ == '__main__':
    mkdir_presentation()