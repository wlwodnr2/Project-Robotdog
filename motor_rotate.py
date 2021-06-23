import wiringpi

#초음파 센서 넣어야됨 
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

# 실제 핀 정의
#PWM PIN
ENA = 25
ENB = 30

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
setPinConfig2(ENA, IN5, IN6)
setPinConfig2(ENB, IN7, IN8)

#제어 시작
# 앞으로 150속도로
setMotor(CH1, 1000, FORWARD)
setMotor(CH2, 1000, STOP)
setMotor2(CH1, 1000, FORWARD)
setMotor2(CH2, 1000, STOP)
#5초 대기
wiringpi.delay(1500)

setMotor(CH1, 1000, STOP)
setMotor(CH2, 1000, STOP)
setMotor2(CH1, 1000, STOP)
setMotor2(CH2, 1000, STOP)

