import os

def get_audio_file(internal_meeting_id):
    PROJECT_APP_DIR = os.path.dirname(os.path.abspath(os.path.join(__file__ ,"..")))
    DATA_DIR = os.path.join(PROJECT_APP_DIR, 'data')
    audio_dir = os.path.join(DATA_DIR, internal_meeting_id + '/audio')
    audio_files = []
    for src_dir, dirs, files in os.walk(audio_dir):
        for file_ in files:
            audio_file = file_
            audio_file_path = os.path.join(src_dir, audio_file)

            audio_files.append({'file_name': audio_file, 'file_path': audio_file_path, 'src_dir': src_dir})
        return audio_files

def get_transcription(internal_meeting_id):
    pass

def get_presentation_svgs(internal_meeting_id):
    pass

def get_presentation_txt(internal_meeting_id):
    pass

def get_alignment_file(internal_meeting_id):
    pass