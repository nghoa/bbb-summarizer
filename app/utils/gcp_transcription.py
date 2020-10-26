## Reference:
# https://towardsdatascience.com/how-to-use-google-speech-to-text-api-to-transcribe-long-audio-files-1c886f4eb3e9

# Import libraries
from pydub import AudioSegment
import os
import json
from google.cloud import speech
from google.cloud.speech import enums
from google.cloud.speech import types
from app.utils.serve_meeting_files import get_audio_file
# from serve_meeting_files import get_audio_file            # Use it for local development
import wave
from google.cloud import storage

def mp3_to_wav(audio_dict):
    audio_file_name = audio_dict['file_name']   
    sound = AudioSegment.from_mp3(audio_dict['file_path'])
    new_audio_file_name = audio_file_name.split('.')[0] + '.wav'
    new_audio_path = os.path.join(audio_dict['src_dir'], new_audio_file_name)
    sound.export(new_audio_path, format="wav")

def opus_to_wav(audio_dict):
    audio_file_name = audio_dict['file_name']
    sound = AudioSegment.from_file(audio_dict['file_path'], codec="opus")
    new_audio_file_name = audio_file_name.split('.')[0] + '.wav'
    new_audio_path = os.path.join(audio_dict['src_dir'], new_audio_file_name)
    sound.export(new_audio_path, format="wav")

def stereo_to_mono(audio_dict):
    sound = AudioSegment.from_wav(audio_dict['file_path'])
    sound = sound.set_channels(1)
    sound.export(audio_dict['file_path'], format="wav")

def frame_rate_channel(audio_dict):
    with wave.open(audio_dict['file_path'], "rb") as wave_file:
        frame_rate = wave_file.getframerate()
        channels = wave_file.getnchannels()
        return frame_rate,channels

## Upload files to Google storage
def upload_blob(bucket_name, source_file_name, destination_blob_name):
    """Uploads a file to the bucket."""
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    blob.upload_from_filename(source_file_name)

## Delete File after usage
def delete_blob(bucket_name, blob_name):
    """Deletes a blob from the bucket."""
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)
    blob = bucket.blob(blob_name)

    blob.delete()

def google_transcribe(audio_dict):
    BUCKETNAME = "wilps-bucket" 
    # get frame & channels
    audio_file_name = audio_dict['file_name']
    frame_rate, channels = frame_rate_channel(audio_dict)
    
    if channels > 1:
        stereo_to_mono(audio_dict)
    
    bucket_name = BUCKETNAME
    source_file_name = audio_dict['file_path']
    destination_blob_name = audio_file_name
    
    upload_blob(bucket_name, source_file_name, destination_blob_name)
    
    gcs_uri = 'gs://' + bucket_name + '/' + audio_file_name
    
    client = speech.SpeechClient()
    audio = types.RecognitionAudio(uri=gcs_uri)

    config = types.RecognitionConfig(
        encoding=enums.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=frame_rate,
        language_code='en-US',
        enable_word_time_offsets=True)

    # Detects speech in the audio file
    operation = client.long_running_recognize(config, audio)
    print('Waiting for operation to be completed....')

    response = operation.result(timeout=10000)

    transcript = {}
    transcript['transcribed_words'] = []

    for result in response.results:
        alternative = result.alternatives[0]
        print('Confidence: {}'.format(alternative.confidence))
        
        ### Get timestamp about speecific words
        for word_info in alternative.words:
            word = word_info.word
            start_time = word_info.start_time
            end_time = word_info.end_time

            transcript['transcribed_words'].append({
                'word': word,
                'start_time': start_time.seconds + start_time.nanos * 1e-9,
                'end_time': end_time.seconds + end_time.nanos * 1e-9
            })

            print('Word: {}, start_time: {}, end_time: {}'.format(
                word,
                start_time.seconds + start_time.nanos * 1e-9,
                end_time.seconds + end_time.nanos * 1e-9
            ))
    
    delete_blob(bucket_name, destination_blob_name)
    return transcript

def write_transcripts(audio_dict, transcript):
    output_dir = 'transcription'
    output_filepath = os.path.join(audio_dict['src_dir'], output_dir)
    if not os.path.exists(output_filepath):
        os.makedirs(output_filepath)
    transcript_filename = audio_dict['file_name'].split('.')[0] + '.txt'
    output_file = os.path.join(output_filepath, transcript_filename)
    with open(output_file, 'w+') as outfile:
        json.dump(transcript, outfile, indent=4)

def execute_transcription(internal_meeting_id):
    # input internal_meeting_id
    audio_files = get_audio_file(internal_meeting_id)
    # Transform mp3 -> wav || opus -> wav
    for audio_dict in audio_files:
        audio_file_name = audio_dict['file_name']
        # Check for format and otherwise transform
        if audio_file_name.split('.')[1] == 'mp3':
            mp3_to_wav(audio_dict)
        if audio_file_name.split('.')[1] == 'opus':
            opus_to_wav(audio_dict)
    # After file transformation -> Transcribe 
    audio_files = get_audio_file(internal_meeting_id)
    for audio_dict in audio_files:
        audio_file_name = audio_dict['file_name']
        if audio_file_name.split('.')[1] == 'wav':
            transcript = google_transcribe(audio_dict)
            write_transcripts(audio_dict, transcript)
            return True

# TODO: Prototyping
if __name__ == '__main__':
    internal_meeting_id = '043a5a1430143ef9dd85be452e4e59901e944642-1603650621063'
    execute_transcription(internal_meeting_id)