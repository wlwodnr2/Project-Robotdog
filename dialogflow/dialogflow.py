
"""Dialogflow API streams user input through the microphone and
speaks voice responses through the speaker.
Examples:
  python mic_stream_audio_response.py
  python mic_stream_audio_response.py--project-id PROJECT_ID
"""
import dialogflow
import pyaudio
import simpleaudio as sa
import os
import argparse
import uuid
import time
import sys


# Audio recording parameters

credential_path = "/home/pi/Desktop/complete_file/first-henu-tvclhj-7ebb92ce3259.json"
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credential_path
SAMPLE_RATE = 44100
CHUNK_SIZE = 512


def grab_intent(projectId, sessionId, languageCode):
    session_client = dialogflow.SessionsClient()
    
    final_request_received = False

    def __request_generator():
        input_stream = pyaudio.PyAudio().open(channels=1,
                rate=SAMPLE_RATE, format=pyaudio.paInt16, input=True)
        audio_encoding = dialogflow.enums.AudioEncoding.AUDIO_ENCODING_LINEAR_16
        session_path = session_client.session_path(projectId, sessionId)
        print('Session path: {}\n'.format(session_path))
        
        input_audio_config = dialogflow.types.InputAudioConfig(audio_encoding=audio_encoding, 
            language_code=languageCode,
            sample_rate_hertz=SAMPLE_RATE)
        speech_config = dialogflow.types.SynthesizeSpeechConfig(
            voice=dialogflow.types.VoiceSelectionParams(ssml_gender=dialogflow.enums.SsmlVoiceGender.SSML_VOICE_GENDER_FEMALE))
        output_audio_config = dialogflow.types.OutputAudioConfig(
            audio_encoding=dialogflow.enums.OutputAudioEncoding.OUTPUT_AUDIO_ENCODING_LINEAR_16,
            sample_rate_hertz=SAMPLE_RATE,
            synthesize_speech_config=speech_config)
        query_input = dialogflow.types.QueryInput(audio_config=input_audio_config)

        # The first request contains the configuration.
        yield dialogflow.types.StreamingDetectIntentRequest(
            session=session_path, query_input=query_input, output_audio_config=output_audio_config)

        while True:
            if final_request_received:
                print("received final request")
                input_stream.close()
                print("closed stream")
                return
            if input_stream.is_active():
                content = input_stream.read(CHUNK_SIZE, exception_on_overflow = False)
                yield dialogflow.types.StreamingDetectIntentRequest(input_audio=content)
        

    while True:
        print('=' * 20)
        requests = __request_generator()
        responses = session_client.streaming_detect_intent(requests)

        for response in responses:
            print(f'I said : {response.recognition_result.transcript}')
            if response.recognition_result.is_final:
                final_request_received = True
            if response.query_result.query_text:
                print(f'Fullfilment Text: {response.query_result.fulfillment_text}')
                print(f'Intent: {response.query_result.intent}')
            if response.output_audio:
                return response


def play_audio(audio):
    audio_obj = sa.play_buffer(audio, 1, 2, SAMPLE_RATE)
    audio_obj.wait_done()

def main():
    while(True):
        response = grab_intent('first-henu-tvclhj', args.session_id, args.language_code)
        play_audio(response.output_audio)
        

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter) #ArgumentParser 객체는 명령행을 파이썬 데이터형으로 파싱하는데 필요한 모든 정보를 담고 있습니다.
    #ArgumentParser 에 프로그램 인자에 대한 정보를 채우려면 add_argument() 메서드를 호출하면 됩니다. 
    parser.add_argument(
        '--session-id',
        help='Identifier of the DetectIntent session. '
             'Defaults to a random UUID.', #랜덤 아이디 생성임 
        default=str(uuid.uuid4()))
    parser.add_argument(
        '--language-code',
        help='Language code of the query. Defaults to "ko-KR".',
        default='ko-KR')
    args = parser.parse_args()
    main()
    
