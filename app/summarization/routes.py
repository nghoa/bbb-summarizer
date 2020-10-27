from flask import render_template, send_file, send_from_directory, redirect, request, url_for, session, make_response
from app.utils.serve_meeting_files import get_pdf_file, get_wav_file, read_transcription, read_alignment, cp_presentation_svgs, get_all_presentation_txt
import json
import re
 
from . import summarization_blueprint


# TODO: redirect from lecture.html
# Entrypoint to summarizationclear
# get internal_meeting_id
@summarization_blueprint.route('/summarization/data')
def get_internal_meeting_id():
    internal_meeting_id = request.args.get('internalMeetingId')
    # Copy svgs for html serving
    cp_presentation_svgs(internal_meeting_id)
    session['internal_meeting_id'] = internal_meeting_id
    return redirect(url_for('.serve_transcription', internalMeetingId=internal_meeting_id))

@summarization_blueprint.route('/summarization/wav')
def serve_wav_file():
    internal_meeting_id = session['internal_meeting_id']
    file_dict = get_wav_file(internal_meeting_id)
    src_dir = file_dict['src_dir']
    file_name = file_dict['file_name']
    file_path = file_dict['file_path']
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

    firstSvgLink = url_for('static', filename='img/b43a5a9996343ef9dd85be452e4e59901e944642-123456311/slide1.svg')

    return render_template('summary.html', transcription=render_output, internalMeetingId=internal_meeting_id, svgLink=firstSvgLink)


@summarization_blueprint.route('/summarization/testplace')
def serve_test():
    internal_meeting_id = 'b43a5a9996343ef9dd85be452e4e59901e944642-123456311'
    test = serve_alignment(internal_meeting_id)
    return 'hello world'


'''
    function which gets alignment.json from hmm_alignment model
        > cleans up alignment
        > align the output of the model with slide
        > returns new dict with {slide_index, spoken_words, ...}
        > returned dict is used for mapping between slides and spoken words
'''
def serve_alignment(internal_meeting_id):
    data_dict = read_alignment(internal_meeting_id)
    # Clean Alignment dict a bit:
    print('Length before cleaning: ', len(data_dict))
    x = [i for i in data_dict if not (i['Sent Text']=="")]  # - clean from empty Sent Text
    y = [i for i in x if not (i['Sent Text']=="\n")]  # - clean from empty Sent Text
    cleaned_alignment = [i for i in y if not (i['Sent Text']=="\t")]  # - clean from empty Sent Text
    print('Length after cleaning: ', len(cleaned_alignment))
    
    txt_dict = get_all_presentation_txt(internal_meeting_id)
    # sort dict by file_name <slide-1.txt, slide-2.txt, ...>
    new_dict = []
    for dict_ in txt_dict:
        index = int(re.split('\-|\.', dict_['file_name'])[1])
        new_dict.append({'index': index, 'file_name': dict_['file_name'], 'file_path': dict_['file_path']})
    
    sorted_dict = sorted(new_dict, key = lambda i: i['index'])
    slide_text_dict = []
    for dict_ in sorted_dict:
        with open(dict_['file_path'], 'r+') as f:
            txt_content = f.read().lower()      # standardize txt_content
            slide_text_dict.append( { 'index': dict_['index'], 'slide_content': txt_content, 'file_name': dict_['file_name']} )

    new_alignment_dict = []
    for alignment_dict in cleaned_alignment:
        sent_text = alignment_dict['Sent Text'].lower()
        sent_duration = alignment_dict['Duration']
        spoken_words = alignment_dict['Spoken words']
        sent_i = alignment_dict['Sent i']       # used for relative measurement
        for slide_dict in slide_text_dict:
            slide_content = slide_dict['slide_content'].lower()
            slide_name = slide_dict['file_name']
            if (sent_text in slide_content and not sent_text == ''):
                print('Sent Text: ' + sent_text)
                print('Sent Duration: ', sent_duration, '---Sent i: ', sent_i)
                print('Slide Name: ' + slide_name)

    return True


# TODO:
# Serve static pdf file
@summarization_blueprint.route('/summarization/show/static-pdf')
def show_static_pdf():
    internal_meeting_id = session['internal_meeting_id']
    pdf_json = json.loads(get_pdf_file(internal_meeting_id))
    file_path = pdf_json['file_path']
    static_file = open(file_path, 'rb')
    return send_file(static_file, attachment_filename='meeting.pdf')