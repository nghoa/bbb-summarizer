import os
import shutil

from app.hmm_alignment.summarize import main
from app.utils.serve_meeting_files import get_full_text_transcription_path, get_alignment_file, get_all_presentation_txt

def start_alignment(internal_meeting_id):
    get_transcription(internal_meeting_id)
    get_presentation_text(internal_meeting_id)
    start_summarization()
    cp_alignment_file(internal_meeting_id)
    rm_meeting_files()
    rm_results_folder()

# get_transcription from transcription folder
def get_transcription(internal_meeting_id):
    transcription_dict = get_full_text_transcription_path(internal_meeting_id)
    print(transcription_dict)
    

# get_all_presentation files
def get_presentation_text(internal_meeting_id):
    pass

# Start summarization
def start_summarization():
    pass

# Copy alignment file into corresponding folder
def cp_alignment_file(internal_meeting_id):
    pass

# Remove meeting files after alignment
def rm_meeting_files():
    pass

# rm results folder
def rm_results_folder():
    pass


if __name__ == '__main__':
    internal_meeting_id = '043a5a1430143ef9dd85be452e4e59901e944642-1603650621063'
    main(internal_meeting_id)






