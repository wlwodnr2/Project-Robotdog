#-*- coding: utf-8 -*-
from subprocess import Popen
from pygame import mixer
import time

#filename1 = "/home/pi/Desktop/complete_file/re/stt_copy.py" #"stt_copy.py"
filename2 = "/home/pi/Desktop/complete_file/re/henu.py" #"restart_base.py"

while True:
    #print("\nStarting " + filename1)
    #start = Popen("python3 " + filename1, shell = True) #stt 파일에서 시작이라고 말 하면 밑에 프로그램 시작 
    #start.wait()
    print("\nStarting " + filename2)
    p = Popen("python3 " + filename2, shell = True) #restart_base 프로그램 시작 
    p.wait()
    mixer.init()
    mixer.music.load('/home/pi/Desktop/complete_file/voice_folder/callme.mp3') #제 이름을 불러주세요 
    mixer.music.play()
    #mixer.init()
    #mixer.music.load('/home/pi/Desktop/complete_file/re/bbangbbong.mp3') #제 이름을 불러주세요 
    #mixer.music.play()
    time.sleep(2.5) #출력 음성까지 stt로 받아버려서 에러날 수 있으니 시간 간격 두기 
    

