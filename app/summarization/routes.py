from flask import render_template, send_file, send_from_directory, redirect, request, url_for, session
from app.utils.serve_meeting_files import get_pdf_file, get_wav_file, read_transcription, read_alignment
import json
 
from . import summarization_blueprint

# TODO: redirect from lecture.html
# Entrypoint to summarization
# get internal_meeting_id
@summarization_blueprint.route('/summarization/data')
def get_internal_meeting_id():
    internal_meeting_id = request.args.get('internalMeetingId')
    session['internal_meeting_id'] = internal_meeting_id
    return redirect(url_for('.serve_transcription', internalMeetingId=internal_meeting_id))

# Serve static pdf file
@summarization_blueprint.route('/summarization/show/static-pdf')
def show_static_pdf():
    internal_meeting_id = session['internal_meeting_id']
    pdf_json = json.loads(get_pdf_file(internal_meeting_id))
    file_path = pdf_json['file_path']
    print(file_path)
    static_file = open(file_path, 'rb')
    return send_file(static_file, attachment_filename='meeting.pdf')


@summarization_blueprint.route('/summarization/wav')
def serve_wav_file():
    internal_meeting_id = session['internal_meeting_id']
    file_dict = get_wav_file(internal_meeting_id)
    src_dir = file_dict['src_dir']
    file_name = file_dict['file_name']
    file_path = file_dict['file_path']
    # static_file = open(file_path, 'rb')
    # return send_file(static_file, attachment_filename='meeting.wav')
    return send_from_directory(src_dir, file_name)

@summarization_blueprint.route('/summarization/serve_transcription')
def serve_transcription():
    internal_meeting_id = session['internal_meeting_id']
    transcription_dict = read_transcription(internal_meeting_id)

    render_output = {}
    render_output['sentences'] = []
    sentence = ''
    words_in_sentence = 10
    word_count = 0
    sentence_index = 0
    for t_words in transcription_dict['transcribed_words']:
        # start_time = t_words['start_time']
        # end_time = t_words['end_time']
        # print('Word: {}, start_time: {}, end_time: {}'.format(
        #     word,
        #     start_time,
        #     end_time
        # ))
        
        # formulate a sentence which consists of the number of the defined words_in_sentence
        word = t_words['word']
        if (word_count < words_in_sentence):
            if (word_count == 0):
                start_time = t_words['start_time']
            sentence += word + ' '
            word_count += 1
        else:
            sentence += word + ' '
            end_time = t_words['end_time']
            render_output['sentences'].append({
                'index': sentence_index,
                'sentence': sentence,
                'start_time': start_time,
                'end_time': end_time
            })
            sentence_index += 1
            # Reset sentence
            word_count = 0
            sentence = ''
    # There are "rest-words", which were not appended to the string
    if (word_count > 0 and word_count < words_in_sentence):
        end_time = t_words['end_time']
        render_output['sentences'].append({
            'index': sentence_index,
            'sentence': sentence,
            'start_time': start_time,
            'end_time': end_time
        })

    return render_template('summary.html', transcription=render_output)

@summarization_blueprint.route('/summarization/alignment')
def serve_alignment():
    # internal_meeting_id = session['internal_meeting_id']
    internal_meeting_id = request.args.get('internalMeetingId')     # prototype
    data = read_alignment(internal_meeting_id)
    print(data)

    return 'hello world'