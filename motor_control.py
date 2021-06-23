import wiringpi
import wiringpi as gpio
import time
from random import *

i = randint(1,2)

# 모터 상태
STOP  = 0
FORWARD  = 1
BACKWORD = 2
                                 
# 모터 채널
CH1 = 0
CH2 = 1

# PIN 입출력 설정
OUTPUT = 1
INPUT = 0

# PIN 설정
HIGH = 1
LOW = 0

TRIG = 4
ECHO = 5
# 실제 핀 정의
#PWM PIN
ENA = 25
ENB = 30
#ENA2 = 25
#ENB2 = 30

#GPIO PIN
IN1 = 24
IN2 = 23
IN3 = 22
IN4 = 21
IN5 = 24
IN6 = 23
IN7 = 22
IN8 = 21

# 핀 설정 함수
def setPinConfig(EN, INA, INB):
    wiringpi.pinMode(EN, OUTPUT)
    wiringpi.pinMode(INA, OUTPUT)
    wiringpi.pinMode(INB, OUTPUT)
    wiringpi.softPwmCreate(EN, 0, 255)

# 모터 제어 함수
def setMotorContorl(PWM, INA, INB, speed, stat):
    #모터 속도 제어 PWM
    wiringpi.softPwmWrite(PWM, speed)

    #앞으로
    if stat == FORWARD:
        wiringpi.digitalWrite(INA, HIGH)
        wiringpi.digitalWrite(INB, LOW)
    #뒤로
    elif stat == BACKWORD:
        wiringpi.digitalWrite(INA, LOW)
        wiringpi.digitalWrite(INB, HIGH)
    #정지
    elif stat == STOP:
        wiringpi.digitalWrite(INA, LOW)
        wiringpi.digitalWrite(INB, LOW)

# 모터 제어함수 간단하게 사용하기 위해 한번더 래핑(감쌈)
def setMotor(ch, speed, stat):
    if ch == CH1:
        setMotorContorl(ENA, IN1, IN2, speed, stat)
    else:
        setMotorContorl(ENB, IN3, IN4, speed, stat)

########################################################

def setPinConfig2(EN, INA, INB):
    wiringpi.pinMode(EN, OUTPUT)
    wiringpi.pinMode(INA, OUTPUT)
    wiringpi.pinMode(INB, OUTPUT)
    wiringpi.softPwmCreate(EN, 0, 255)

# 모터 제어 함수
def setMotorContorl2(PWM, INA, INB, speed, stat):
    #모터 속도 제어 PWM
    wiringpi.softPwmWrite(PWM, speed)

    #앞으로
    if stat == FORWARD:
        wiringpi.digitalWrite(INA, HIGH)
        wiringpi.digitalWrite(INB, LOW)
    #뒤로
    elif stat == BACKWORD:
        wiringpi.digitalWrite(INA, LOW)
        wiringpi.digitalWrite(INB, HIGH)
    #정지
    elif stat == STOP:
        wiringpi.digitalWrite(INA, LOW)
        wiringpi.digitalWrite(INB, LOW)

# 모터 제어함수 간단하게 사용하기 위해 한번더 래핑(감쌈)
def setMotor2(ch, speed, stat):
    if ch == CH1:
        setMotorContorl(ENA, IN5, IN6, speed, stat)
    else:
        setMotorContorl(ENB, IN7, IN8, speed, stat)
        
#GPIO 라이브러리 설정
wiringpi.wiringPiSetup()

#모터 핀 설정
setPinConfig(ENA, IN1, IN2)
setPinConfig(ENB, IN3, IN4)
setPinConfig2(ENA2, IN5, IN6)
setPinConfig2(ENB2, IN7, IN8)

#제어 시작
# 앞으로 150속도로
setMotor(CH1, 3000, FORWARD)
setMotor(CH2, 3000, FORWARD)
setMotor2(CH1, 3000, FORWARD)
setMotor2(CH2, 3000, FORWARD)

#5초 대기
wiringpi.delay(3000)
setMotor(CH1, 1000, STOP)
setMotor(CH2, 1000, STOP)
setMotor2(CH1, 1000, STOP)
setMotor2(CH2, 1000, STOP)

gpio.wiringPiSetup()
gpio.pinMode(TRIG, OUTPUT)
gpio.pinMode(ECHO, INPUT)

t_end = time.time() + 5

while time.time() < t_end:
    gpio.digitalWrite(TRIG,LOW)
    gpio.delayMicroseconds(2)
    gpio.digitalWrite(TRIG, HIGH)
    gpio.delayMicroseconds(10)
    gpio.digitalWrite(TRIG, LOW)
    
    while gpio.digitalRead(ECHO) == LOW:
        startTime = gpio.micros()
        
    while gpio.digitalRead(ECHO) == HIGH:
        endTime = gpio.micros()
        
    travelTime = endTime - startTime
    distance = travelTime / 58.0
    
    if distance < 20:
        print('Distance :', round(distance, 2), 'cm')
        setMotor(CH1, 1000, STOP)
        setMotor(CH2, 1000, STOP)
        setMotor2(CH1, 1000, STOP)
        setMotor2(CH2, 1000, STOP)
        break
        
    gpio.delay(100);


if distance < 20:
    wiringpi.delay(500)
    print('Distance :', round(distance, 2), 'cm')

    if i == 1:
        setMotor(CH1, 3000,STOP)
        setMotor(CH2, 3000,BACKWORD)
        setMotor2(CH1, 3000, STOP)
        setMotor2(CH2, 3000, BACKWORD)
        wiringpi.delay(1500)
        setMotor(CH1, 1000, STOP)
        setMotor(CH2, 1000, STOP)
        setMotor2(CH1, 1000, STOP)
        setMotor2(CH2, 1000, STOP)
    elif i == 2:
        setMotor(CH1, 3000,BACKWORD)
        setMotor(CH2, 3000,STOP)
        setMotor2(CH1, 3000, BACKWORD)
        setMotor2(CH2, 3000, STOP)
        wiringpi.delay(1500)
        setMotor(CH1, 1000, STOP)
        setMotor(CH2, 1000, STOP)
        setMotor2(CH1, 1000, STOP)
        setMotor2(CH2, 1000, STOP)
#정지
setMotor(CH1, 1000, STOP)
setMotor(CH2, 1000, STOP)
setMotor2(CH1, 1000, STOP)
setMotor2(CH2, 1000, STOP)'''

