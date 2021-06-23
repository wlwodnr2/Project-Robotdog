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

def setPinConfig(EN, INA, INB):
    wiringpi.pinMode(EN, OUTPUT)
    wiringpi.pinMode(INA, OUTPUT)
    wiringpi.pinMode(INB, OUTPUT)
    wiringpi.softPwmCreate(EN, 0, 255)


def setMotorContorl(PWM, INA, INB, speed, stat):

    wiringpi.softPwmWrite(PWM, speed)


    if stat == FORWARD:
        wiringpi.digitalWrite(INA, HIGH)
        wiringpi.digitalWrite(INB, LOW)

    elif stat == BACKWORD:
        wiringpi.digitalWrite(INA, LOW)
        wiringpi.digitalWrite(INB, HIGH)
    elif stat == STOP:
        wiringpi.digitalWrite(INA, LOW)
        wiringpi.digitalWrite(INB, LOW)

def setMotor(ch, speed, stat):
    
    setMotorContorl(ENA, IN1, IN2, speed, stat)


def setPinConfig2(INA, INB):
    
    wiringpi.pinMode(INA, OUTPUT)

def setMotorContorl2(INA, INB, stat):
   
    if stat == FORWARD:
        wiringpi.digitalWrite(INA, HIGH)
        wiringpi.digitalWrite(INB, LOW)
    elif stat == BACKWORD:
        wiringpi.digitalWrite(INA, LOW)
        wiringpi.digitalWrite(INB, HIGH)
    elif stat == STOP:
        wiringpi.digitalWrite(INA, LOW)
        wiringpi.digitalWrite(INB, LOW)
wiringpi.wiringPiSetup()
setPinConfig(ENA, IN1, IN2)
setMotor(CH1, 350, BACKWORD)
wiringpi.delay(100)

setMotor(CH1, 250, STOP)
setMotor(CH1, 80, STOP)

