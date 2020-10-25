## Reference:
# https://towardsdatascience.com/how-to-use-google-speech-to-text-api-to-transcribe-long-audio-files-1c886f4eb3e9

# Import libraries
from pydub import AudioSegment
import io
from io import BytesIO
import os
from google.cloud import speech
from google.cloud.speech import enums
from google.cloud.speech import types
import wave
from google.cloud import storage


'''
    GCloud Service on ngyshadi account
        0. Start Conda NlP environment
        1. Set creds in "env_festlegen.txt"
        2. modify file_name
        3. python big_transcription.py
'''

# file_name = "smolt_lecture_1_48k.wav"
# file_name = "smolt_1min.wav"
file_name = "test.opus"
filepath = "./data/"     #Input audio file path
output_filepath = "./transcription/" #Final transcript path
bucketname = "wilps-bucket" #Name of the bucket created in the step before

def mp3_to_wav(audio_file_name):
    if audio_file_name.split('.')[1] == 'mp3':    
        sound = AudioSegment.from_mp3(audio_file_name)
        audio_file_name = audio_file_name.split('.')[0] + '.wav'
        sound.export(filepath + audio_file_name, format="wav")

def opus_to_wav(audio_file_name):
    if audio_file_name.split('.')[1] == 'opus':
        print('------opus to wav file test--------')
        # f = open(filepath + audio_file_name, "rb")
        # opus_data = BytesIO(f)    
        # "C:\\Users\\Hoa\\workspace\\uhh\\wilps\\gcloud_speech\\test.opus"
        sound = AudioSegment.from_file("test.opus", codec="opus")
        audio_file_name = audio_file_name.split('.')[0] + '.wav'
        sound.export(filepath + audio_file_name, format="wav")

def stereo_to_mono(audio_file_name):
    sound = AudioSegment.from_wav(audio_file_name)
    sound = sound.set_channels(1)
    sound.export(audio_file_name, format="wav")

def frame_rate_channel(audio_file_name):
    with wave.open(audio_file_name, "rb") as wave_file:
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

def google_transcribe(audio_file_name):
    # Check for format and otherwise transform
    mp3_to_wav(audio_file_name)
    opus_to_wav(audio_file_name)
    if audio_file_name.split('.')[1] == 'opus':
        audio_file_name = audio_file_name.split('.')[0] + '.wav'
    file_name = filepath + audio_file_name

    # get frame & channels
    frame_rate, channels = frame_rate_channel(file_name)
    
    if channels > 1:
        stereo_to_mono(file_name)
    
    bucket_name = bucketname
    source_file_name = filepath + audio_file_name
    destination_blob_name = audio_file_name
    
    upload_blob(bucket_name, source_file_name, destination_blob_name)
    
    gcs_uri = 'gs://' + bucketname + '/' + audio_file_name
    transcript = ''
    
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

    for result in response.results:
        alternative = result.alternatives[0]
        print(u'Transcript: {}'.format(alternative.transcript))
        print('Confidence: {}'.format(alternative.confidence))
        transcript += alternative.transcript                            ## Whole transcript
        
        ### Get timestamp about speecific words
        for word_info in alternative.words:
            word = word_info.word
            start_time = word_info.start_time
            end_time = word_info.end_time
            print('Word: {}, start_time: {}, end_time: {}'.format(
                word,
                start_time.seconds + start_time.nanos * 1e-9,
                end_time.seconds + end_time.nanos * 1e-9
            ))


    
    delete_blob(bucket_name, destination_blob_name)
    return transcript

def write_transcripts(transcript_filename, transcript):
    f= open(output_filepath + transcript_filename,"w+")
    f.write(transcript)
    f.close()

def main():
    # for audio_file_name in os.listdir(filepath):
    audio_file_name = file_name
    transcript = google_transcribe(audio_file_name)
    transcript_filename = audio_file_name.split('.')[0] + '.txt'
    write_transcripts(transcript_filename, transcript)

if __name__ == '__main__':
    main()