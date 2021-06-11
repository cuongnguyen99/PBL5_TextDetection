import RPi.GPIO as GPIO  

import time
import board
import pwmio
from adafruit_motor import servo
import TextScanner
import read_vie

pwm1 = pwmio.PWMOut(board.D23, duty_cycle=2 ** 15, frequency=50)
pwm2 = pwmio.PWMOut(board.D24, duty_cycle=2 ** 15, frequency=50)
pwm3 = pwmio.PWMOut(board.D25, duty_cycle=2 ** 15, frequency=50)


def VatCan():
 #   GPIO.setmode(GPIO.BCM)
    inp=GPIO.input(26)
#    GPIO.cleanup()
    return inp

def Servo_1( ):
    my_servo = servo.Servo(pwm1)
    my_servo.angle = 70
    time.sleep(0.5)
    my_servo.angle = 0
    time.sleep(2)
    my_servo.angle = 70
def Servo_2():  
    my_servo = servo.Servo(pwm2)
    my_servo.angle = 70
    time.sleep(0.5)
    my_servo.angle = 0
    time.sleep(4)
    my_servo.angle = 70
    
def Servo_3():
    my_servo = servo.Servo(pwm3)
    my_servo.angle = 70
    time.sleep(0.5)
    my_servo.angle = 0
    time.sleep(13)
    my_servo.angle = 70

GPIO.setmode(GPIO.BCM)
GPIO.setup(26, GPIO.IN) #Read output from PIR motion sensor



# thread1 = TextScanner.camThread("Camera", 0)
# thread1.start()


while True:
    if VatCan()==0:
        khuVuc=read_vie.khuVucHang()
        if khuVuc==1:
            Servo_1()
        elif khuVuc==2:
            Servo_2()
GPIO.cleanup()


print(read_vie.khuVucHang())
