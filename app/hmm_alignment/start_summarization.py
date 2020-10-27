import os
import shutil
import re

from app.hmm_alignment.summarize import main
from app.utils.serve_meeting_files import get_full_text_transcription_path, get_alignment_file, get_all_presentation_txt

CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))
PROJECT_APP_DIR = os.path.dirname(os.path.abspath(os.path.join(__file__ ,"..")))

def start_alignment(internal_meeting_id):
    transcript_done = get_transcription(internal_meeting_id)
    presentation_done = get_presentation_text(internal_meeting_id)
    if (transcript_done and presentation_done):
        summarization_done = start_summarization()
        if (summarization_done):
            copy_done = cp_alignment_file(internal_meeting_id)
            if (copy_done):
                deleted_m_files = rm_meeting_files()
                deleted_r_folder = rm_results_folder()
                if (deleted_m_files and deleted_r_folder):
                    print('start_alignment completely finished')
                    return True

# Copy <full-text-transcription>.txt into data/transcript for hmm_alignment 
def get_transcription(internal_meeting_id):
    transcription_dict = get_full_text_transcription_path(internal_meeting_id)
    src_file_path = transcription_dict['file_path']
    dst_dir = os.path.join(CURRENT_DIR, 'data', 'transcript')
    shutil.copy(src_file_path, dst_dir)
    return True
    

# get_all_presentation files
def get_presentation_text(internal_meeting_id):
    txt_dict = get_all_presentation_txt(internal_meeting_id)
    # sort dict by file_name <slide-1.txt, slide-2.txt, ...>
    new_dict = []
    for dict_ in txt_dict:
        index = int(re.split('\-|\.', dict_['file_name'])[1])
        new_dict.append({'index': index, 'file_name': dict_['file_name'], 'file_path': dict_['file_path']})
    
    sorted_dict = sorted(new_dict, key = lambda i: i['index'])
    # Start getting full_text of pdf by concat all txt_files in sorted_manner <slide-1 + slide-2.txt + ...>
    full_pdf_txt = ''
    # iterate through all files
    for dict_ in sorted_dict:
        with open(dict_['file_path'], 'r+') as f:
            txt_content = f.read()
            full_pdf_txt += txt_content + '\n'

    file_name = internal_meeting_id + '.txt'
    dst_dir = os.path.join(CURRENT_DIR, 'data', 'presentation_text', file_name)
    with open(dst_dir, 'w+') as p:
        p.write(full_pdf_txt)

    return True

# Start summarization
def start_summarization():
    summarization_done = main()
    if (summarization_done):
        return True
    else:
        return False

# Copy alignment file into corresponding folder
def cp_alignment_file(internal_meeting_id):
    alignment_dir = os.path.join(CURRENT_DIR, 'data', 'results', 'output', 'alignment')
    dst_dir = os.path.join(PROJECT_APP_DIR, 'data', internal_meeting_id, 'alignment')
    for src_dir, dirs, files in os.walk(alignment_dir):
        for file_ in files:
            alignment_file = file_
            alignment_file_path = os.path.join(src_dir, alignment_file)
            if (alignment_file.split('.')[1] == 'json'):
                shutil.copy(alignment_file_path, dst_dir)
                return True

# Remove meeting files after alignment
def rm_meeting_files():
    transcript_dir = os.path.join(CURRENT_DIR, 'data', 'transcript')
    presentation_dir = os.path.join(CURRENT_DIR, 'data', 'presentation_text')
    # delete transcription
    for file_name in os.listdir(transcript_dir):
        file_path = os.path.join(transcript_dir, file_name)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))
    # delete presentation
    for file_name in os.listdir(presentation_dir):
        file_path = os.path.join(presentation_dir, file_name)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))
    return True

# rm results folder
def rm_results_folder():
    results_dir = os.path.join(CURRENT_DIR, 'data', 'results')
    shutil.rmtree(results_dir)
    return True

if __name__ == '__main__':
    internal_meeting_id = '043a5a1430143ef9dd85be452e4e59901e944642-1603650621063'
    main(internal_meeting_id)






