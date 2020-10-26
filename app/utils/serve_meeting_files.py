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

def get_transcription(internal_meeting_id):
    transcription_dir = os.path.join(DATA_DIR, internal_meeting_id, 'audio', 'transcription')
    # just one transcription file
    for src_dir, dirs, files in os.walk(transcription_dir):
        for file_ in files:
            transcription_file = file_
            transcription_file_path = os.path.join(src_dir, transcription_file)

            return transcription_file_path

def read_transcription(internal_meeting_id):
    transcription_file_path = get_transcription(internal_meeting_id)
    with open(transcription_file_path) as json_file:
        data = json.load(json_file)
        for t_words in data['transcribed_words']:
            word = t_words['word']
            start_time = t_words['start_time']
            end_time = t_words['end_time']
            print('Word: {}, start_time: {}, end_time: {}'.format(
                word,
                start_time,
                end_time
            ))

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
    pass

def get_alignment_file(internal_meeting_id):
    pass

if __name__ == '__main__':
    internal_meeting_id = '043a5a1430143ef9dd85be452e4e59901e944642-1603650621063'
    get_wav_file(internal_meeting_id)
    # get_pdf_file(internal_meeting_id)
    # read_transcription(internal_meeting_id)
    # get_transcription(internal_meeting_id)