import os
import json

PROJECT_APP_DIR = os.path.dirname(os.path.abspath(os.path.join(__file__ ,"..")))
DATA_DIR = os.path.join(PROJECT_APP_DIR, 'data')

def get_audio_file(internal_meeting_id):
    audio_dir = os.path.join(DATA_DIR, internal_meeting_id, 'audio')
    audio_files = []
    for src_dir, dirs, files in os.walk(audio_dir):
        for file_ in files:
            audio_file = file_
            audio_file_path = os.path.join(src_dir, audio_file)

            audio_files.append({'file_name': audio_file, 'file_path': audio_file_path, 'src_dir': src_dir})

        return audio_files

def get_transcription_path(internal_meeting_id):
    transcription_dir = os.path.join(DATA_DIR, internal_meeting_id, 'audio', 'transcription')
    # just one transcription file
    for src_dir, dirs, files in os.walk(transcription_dir):
        for file_ in files:
            transcription_file = file_
            transcription_file_path = os.path.join(src_dir, transcription_file)
            if (transcription_file.split('.')[1] == 'json'):
                return transcription_file_path

def get_full_text_transcription_path(internal_meeting_id):
    transcription_dir = os.path.join(DATA_DIR, internal_meeting_id, 'audio', 'transcription')
    # just one transcription file
    for src_dir, dirs, files in os.walk(transcription_dir):
        for file_ in files:
            transcription_file = file_
            transcription_file_path = os.path.join(src_dir, transcription_file)
            if (transcription_file.split('.')[1] == 'txt'):
                response = { 'file_name': transcription_file, 'file_path': transcription_file_path }

                return response

def read_transcription(internal_meeting_id):
    transcription_file_path = get_transcription_path(internal_meeting_id)
    with open(transcription_file_path) as json_file:
        data = json.load(json_file)
        return data

def get_pdf_file(internal_meeting_id):
    presentation_dir = os.path.join(DATA_DIR, internal_meeting_id, 'presentation')
    for src_dir, dirs, files in os.walk(presentation_dir):
        for file_ in files:
            file_name, extension = file_.split('.')
            # only serve the pdf_file
            if(extension == 'pdf'):
                pdf_file = file_
                pdf_file_path = os.path.join(src_dir, pdf_file)
                
                return json.dumps({'file_name': pdf_file, 'file_path': pdf_file_path})

def get_wav_file(internal_meeting_id):
    audio_dir = os.path.join(DATA_DIR, internal_meeting_id, 'audio')
    for src_dir, dirs, files in os.walk(audio_dir):
        for file_ in files:
            audio_file = file_
            audio_file_path = os.path.join(src_dir, audio_file)
            if (audio_file.split('.')[1] == 'wav'):
                response = { 'file_name': audio_file, 'file_path': audio_file_path, 'src_dir': src_dir}

                return response

def get_presentation_svgs(internal_meeting_id):
    pass

def get_all_presentation_txt(internal_meeting_id):
    presentation_dir = os.path.join(DATA_DIR, internal_meeting_id, 'presentation')
    # presentation folder structure has a unique dir in the above level
    for lower_dir in os.listdir(presentation_dir):
        txt_dir = os.path.join(presentation_dir, lower_dir, 'textfiles')
        all_txt_files = []
        for src_dir, dirs, files in os.walk(txt_dir):
            for file_ in files:
                txt_file = file_
                txt_file_path = os.path.join(src_dir, txt_file)

                all_txt_files.append({ 'file_name': txt_file, 'file_path': txt_file_path })

            return all_txt_files

def get_alignment_file(internal_meeting_id):
    hmm_dir = os.path.join(PROJECT_APP_DIR, 'hmm_alignment')
    hmm_alignment_dir = os.path.join(hmm_dir, 'data', 'results', 'output', 'alignment')
    for src_dir, dirs, files in os.walk(hmm_alignment_dir):
        for file_ in files:
            alignment_file = file_
            alignment_file_path = os.path.join(src_dir, alignment_file)
            if (alignment_file.split('.')[1] == 'json'):
                response = { 'file_name': alignment_file, 'file_path': alignment_file_path }

                print(response)
                return response

def get_alignment_from_meeting(internal_meeting_id):
    alignment_dir = os.path.join(DATA_DIR, internal_meeting_id, 'alignment')
    for src_dir, dirs, files in os.walk(alignment_dir):
        for file_ in files:
            alignment_file = file_
            alignment_file_path = os.path.join(src_dir, alignment_file)
            if (alignment_file.split('.')[1] == 'json'):
                response = { 'file_name': alignment_file, 'file_path': alignment_file_path }

                return response

def read_alignment(internal_meeting_id):
    alignment_dict = get_alignment_from_meeting(internal_meeting_id)
    alignment_path = alignment_dict['file_path']
    with open(alignment_path) as json_file:
        data = json.load(json_file)
        return data

def alignment_file_exists(internal_meeting_id):
    alignment_dir = os.path.join(DATA_DIR, internal_meeting_id, 'alignment')
    for file_ in os.listdir(alignment_dir):
        if (file_.split('.')[1] == 'json'):
            return True



if __name__ == '__main__':
    # internal_meeting_id = '043a5a1430143ef9dd85be452e4e59901e944642-1603650621063'
    internal_meeting_id = 'b43a5a9996343ef9dd85be452e4e59901e944642-123456311'
    alignment_file_exists(internal_meeting_id)
    # get_full_text_transcription_path(internal_meeting_id)
    # get_all_presentation_txt(internal_meeting_id)
    # get_alignment_file(internal_meeting_id)
    # get_wav_file(internal_meeting_id)
    # get_pdf_file(internal_meeting_id)
    # read_transcription(internal_meeting_id)
    # get_transcription(internal_meeting_id)