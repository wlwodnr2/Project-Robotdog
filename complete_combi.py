#-*- coding: utf-8 -*-
from __future__ import division
from google.cloud import speech
from google.cloud.speech import enums
from google.cloud.speech import types
from six.moves import queue
from pygame import mixer
import time, re, os, math, sys, pyaudio, cv2
import tensorflow.keras as tf
import numpy as np
from subprocess import Popen

#캡쳐하고 yolo로 사람 판독하고 teachable로 낙상 판별, stt까지 합쳤음 

credential_path = "/home/pi/sttfile/1ukbs-d5b756b7353c.json"
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credential_path #자격증명 한거 
RATE = 44100 #마이크 주파수 맞춰주기 
CHUNK = 512  # 100ms


class MicrophoneStream(object):
    
    def __init__(self, rate, chunk):
        self._rate = rate
        self._chunk = chunk

        self._buff = queue.Queue()
        self.closed = True

    def __enter__(self):
        self._audio_interface = pyaudio.PyAudio() 
        self._audio_stream = self._audio_interface.open(   #오디오를 재생하기 위해 PyAudio.open
            format=pyaudio.paInt16, #paInt16 16비트 정수 
            channels=1, rate=self._rate,
            input=True, frames_per_buffer=self._chunk,
            stream_callback=self._fill_buffer,
        )

        self.closed = False

        return self

    def __exit__(self, type, value, traceback):
        self._audio_stream.stop_stream()
        self._audio_stream.close()
        self.closed = True
        self._buff.put(None)
        self._audio_interface.terminate()

    def _fill_buffer(self, in_data, frame_count, time_info, status_flags):
        
        self._buff.put(in_data)
        return None, pyaudio.paContinue

    def generator(self):
        while not self.closed:
            chunk = self._buff.get()
            if chunk is None:
                return
            data = [chunk]

            while True:
                try:
                    chunk = self._buff.get(block=False)
                    if chunk is None:
                        return
                    data.append(chunk)
                except queue.Empty:
                    break

            yield b''.join(data)

def listen_print_loop(responses):
    num_chars_printed = 0
    for response in responses:
        if not response.results:
            continue
        
        result = response.results[0]
        if not result.alternatives:
            continue

        transcript = result.alternatives[0].transcript

        overwrite_chars = ' ' * (num_chars_printed - len(transcript))

        if not result.is_final:
            sys.stdout.write(transcript + overwrite_chars + '\r')
            sys.stdout.flush()

            num_chars_printed = len(transcript)
            
            if "살려 줘" in transcript:   
                mixer.init()
                mixer.music.load('/home/pi/Desktop/complete_file/voice_folder/siren2.mp3')
                mixer.music.play()
                mixer.init()
                mixer.music.load('/home/pi/Desktop/complete_file/voice_folder/siren1.mp3')
                mixer.music.play()
                break
            elif ("응" in transcript) or ("잘게" in transcript):
                #continue 안녕히 주무십쇼 음성
                mixer.init()
                mixer.music.load('/home/pi/Desktop/complete_file/voice_folder/goodnight.mp3')
                mixer.music.play()
                break
          

        else:
            print(transcript + overwrite_chars)

            if re.search(r'\b(exit|quit)\b', transcript, re.I):
                print('Exiting..')
                break

            num_chars_printed = 0

def main():
    language_code = 'ko-KR'  

    client = speech.SpeechClient()
    config = types.RecognitionConfig(
        encoding=enums.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=RATE,
        language_code=language_code)
    streaming_config = types.StreamingRecognitionConfig(
        config=config,
        interim_results=True)

    with MicrophoneStream(RATE, CHUNK) as stream:
        audio_generator = stream.generator()
        requests = (types.StreamingRecognizeRequest(audio_content=content)
                    for content in audio_generator)

        responses = client.streaming_recognize(streaming_config, requests) #음성 데이터를 가능한 대체 텍스트로 변환

        listen_print_loop(responses)


def yolo(count1):
    #if count1 == 4:
    #    return
    net = cv2.dnn.readNet("yolov3.weights", "yolov3.cfg")
    classes = []
    
    filename1 = "/home/pi/Desktop/complete_file/yolo/motor_control.py" #"motor_control.py"
     #"motor_rotate.py"
    
    with open("coco.names", "r") as f:
        classes = [line.strip() for line in f.readlines()]
    layer_names = net.getLayerNames() #ok
    output_layers = [layer_names[i[0] - 1] for i in net.getUnconnectedOutLayers()] #ok
    colors = np.random.uniform(0, 255, size=(80, 3))

    cap = cv2.VideoCapture(0)

    ret,frame = cap.read()
    cv2.imwrite("test.jpg", frame)
    cap.release()

    img = cv2.imread("test.jpg")
    height, width = img.shape[:2] #o   
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             
    blob = cv2.dnn.blobFromImage(img, 0.00392, (320,320), (0, 0, 0), True, crop=False) #ok
    net.setInput(blob) #ok
    outs = net.forward(output_layers)  #ok

    class_ids = []
    confidences = []
    boxes = []
    for out in outs:
        for detection in out:
            scores = detection[5:]
            class_id = np.argmax(scores)
            max_conf = scores[class_id]
            
            if max_conf > 0.5:
           
                center_x = int(detection[0] * width)
                center_y = int(detection[1] * height)
                w = int(detection[2] * width)
                h = int(detection[3] * height)
            
                x = int(center_x - w / 2)
                y = int(center_y - h / 2)
                boxes.append([x, y, w, h])
                confidences.append(float(max_conf))
                class_ids.append(class_id)

    indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)
    number = 0
    font = cv2.FONT_HERSHEY_PLAIN
    for i in range(len(boxes)):
        if i in indexes:
            x, y, w, h = boxes[i]
            label = str(classes[class_ids[i]])
            color = colors[i]
            cv2.rectangle(img, (x, y), (x+w, y+h), color, 2)
            cv2.putText(img, label, (x, y + 30), font, 3, color, 3)
            label += ' ' + str(format(confidences[i] * 100, '.2f')) + '%'
            cv2.putText(img, label, (boxes[i][0],boxes[i][1]-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
            
        try:
            if 'person' in label:
                if number == 0:
                    if  (h < 350):
                        start = Popen("python3 " + filename1, shell = True) #stt 파일에서 시작이라고 말 하면 밑에 프로그램 시작 
                        start.wait()
                        number = number + 1
                        count1 = 0
                        return count1
                    
                    else:
                        print ("가깝습니다.")
                        count1 = 0
                        return count1
            else:
                print ("사람이 없습니다")
                #rotate = Popen("python3 " + filename2, shell = True) #stt 파일에서 시작이라고 말 하면 밑에 프로그램 시작 
                #rotate.wait()
                #count1 = count1 + 1
                #if count1 == 4:
                    #time.sleep(600)
                count1 = 100
                return count1
                
        except Exception:
            pass
    if not boxes:
        print ("사람이 없습니다")
        #rotate = Popen("python3 " + filename2, shell = True) #stt 파일에서 시작이라고 말 하면 밑에 프로그램 시작 
        #rotate.wait()
        #count1 = count1 + 1
        #if count1 == 4:
        #    time.sleep(600)
        count1 = 100
        return count1
        
if __name__ == '__main__':

    labels_path = "/home/pi/Desktop/complete_file/yolo/labels.txt"
    
    labelsfile = open(labels_path, 'r')
    
    classes = []
    line = labelsfile.readline()
    while line:
        
        classes.append(line.split(' ', 1)[1].rstrip())
        line = labelsfile.readline()
    
    labelsfile.close()
    
    model_path = '/home/pi/Desktop/complete_file/yolo/keras_model.h5'
    model = tf.models.load_model(model_path, compile=False)

    frameWidth = 1280
    frameHeight = 720

    classify = 'others'
    
    count1 = 0
    count2 = 0
    x = 0
    filename2 = "/home/pi/Desktop/complete_file/yolo/motor_rotate.py"
    while True:
        
        cap = cv2.VideoCapture(0)

        ret,frame = cap.read()
        cv2.imwrite("test.jpg", frame)
        cap.release()
      
        np.set_printoptions(suppress=True)

        data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)

        frame = cv2.imread("test.jpg")

        margin = int(((frameWidth-frameHeight)/2))
        square_frame = frame[0:frameHeight, margin:margin + frameHeight]
        
        resized_img = cv2.resize(square_frame, (224, 224))

        model_img = cv2.cvtColor(resized_img, cv2.COLOR_BGR2RGB)

        image_array = np.asarray(model_img)
        
        normalized_image_array = (image_array.astype(np.float32) / 127.0) - 1
        
        data[0] = normalized_image_array
        
        predictions = model.predict(data)

        confidence = []
        
        for i in range(0, len(classes)):
            
            confidence.append(int(predictions[0][i]*100))
        filename1 = "/home/pi/Desktop/complete_file/re/stt_help.py"     
        if int(confidence[0]) > int(confidence[1]):    #몇 퍼센트 이상일때 말할건지 
            if classify == 'others':
                mixer.init()
                mixer.music.load('/home/pi/Desktop/complete_file/voice_folder/sleep.mp3') #제 이름을 불러주세요 
                mixer.music.play()
                print('굿')
                #print("\nStarting " + filename1)
                #start = Popen("python3 " + filename1, shell = True) #stt 파일에서 시작이라고 말 하면 밑에 프로그램 시작 
                #start.wait()
                main()
                classify = classify.replace('others','sleep')
                count1 = 0
            elif classify == 'sleep':
                print ("계속 누워계세요")
                count1 = 0
        elif int(confidence[1]) > int(confidence[0]):
            if classify == 'sleep':
                classify = classify.replace('sleep','others')
                print ("서")
        
            x = yolo(count1)
        
        
        
        if x == 100:
            rotate = Popen("python3 " + filename2, shell = True) #stt 파일에서 시작이라고 말 하면 밑에 프로그램 시작 
            rotate.wait()
            count2 = count2 + 1
            if count2 == 4:
                count2 = 0
                time.sleep(600)
            
        
        time.sleep(5)
    
