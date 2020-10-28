from flask import render_template, send_file, send_from_directory, redirect, request, url_for, session, make_response
from app.utils.serve_meeting_files import get_pdf_file, get_wav_file, read_transcription, read_alignment, cp_presentation_svgs, get_all_presentation_txt
import json
import re
 
from . import summarization_blueprint

# Entrypoint to summarizationclear
# get internal_meeting_id
@summarization_blueprint.route('/summarization/data')
def get_internal_meeting_id():
    internal_meeting_id = request.args.get('internalMeetingId')
    # Copy svgs for html serving
    # TODO:
    # cp_presentation_svgs(internal_meeting_id)
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
                'end_time': end_time,
                'slide_index': None
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
            'end_time': end_time,
            'slide_index': None
        })

    firstSvgLink = url_for('static', filename='img/b43a5a9996343ef9dd85be452e4e59901e944642-123456311/slide1.svg')
    new_render_output = handle_alignment(render_output, internal_meeting_id)

    return render_template('summary.html', transcription=new_render_output, internalMeetingId=internal_meeting_id, svgLink=firstSvgLink)

'''
    function which gets alignment.json from hmm_alignment model
        > cleans up alignment
        > align the output of the model with slide
        > returns new dict with {slide_index, spoken_words, ...}
        > returned dict is used for mapping between slides and spoken words
'''
def serve_alignment(internal_meeting_id):
    data_dict = read_alignment(internal_meeting_id)

    # Clean Alignment dict:
    x = [i for i in data_dict if not (i['Sent Text']=="")]            # - clean from empty Sent Text
    y = [i for i in x if not (i['Sent Text']=="\n")]                  # - clean newLine Sent Text
    cleaned_alignment = [i for i in y if not (i['Sent Text']=="\t")]  # - clean tab empty Sent Text
    sorted_cleaned_alignment = sorted(cleaned_alignment, key = lambda i: i['Sent i'])           # Sort alignment
    
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

    # Alignment between spoken words and slides
    new_alignment_dict = []
    
    # take first occurent of alignment
    for align_dict in sorted_cleaned_alignment:
        sent_text = align_dict['Sent Text'].lower()
        sent_duration = align_dict['Duration']
        spoken_words = align_dict['Spoken words']
        sent_i = align_dict['Sent i']                 # used for relative measurement
        for slide in slide_text_dict:
            slide_index = slide['index']
            slide_content = slide['slide_content'].lower()
            slide_name = slide['file_name']
            if (sent_text in slide_content and not sent_text == ''):
                new_alignment_dict.append({ "slide_index": slide_index, "spoken_words": spoken_words })
                break

    return new_alignment_dict

def handle_alignment(transcript_dict, internal_meeting_id):
    alignment_dict = serve_alignment(internal_meeting_id)
    
    for alignment in alignment_dict:
        spoken_words = alignment['spoken_words']
        spoken_words_array = spoken_words.split(' ')
        for j in range(len(transcript_dict['sentences'])):
            sentence = transcript_dict['sentences'][j]['sentence']
            sentence_array = sentence.split(' ')
            count = 0
            for sentence_word in sentence_array:
                for spoken_word in spoken_words_array:
                    if (sentence_word == spoken_word):
                        count += 1
            if (len(sentence_array) > len(spoken_words_array)):
                threshold = len(spoken_words_array) / 2
            else:
                threshold = len(sentence_array) / 2
            # threshold currently by 50%
            if (count > threshold):
                slide_index = alignment['slide_index']
                transcript_dict['sentences'][j]['slide_index'] = slide_index
                break
    
    return transcript_dict


# TODO:
# Serve static pdf file
@summarization_blueprint.route('/summarization/show/static-pdf')
def show_static_pdf():
    internal_meeting_id = session['internal_meeting_id']
    pdf_json = json.loads(get_pdf_file(internal_meeting_id))
    file_path = pdf_json['file_path']
    static_file = open(file_path, 'rb')
    return send_file(static_file, attachment_filename='meeting.pdf')