import RPi.GPIO as GPIO
from time import sleep
 
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

Motor1 = {'input1': 18, 'input2': 16}
Motor2 = {'input1': 13, 'input2': 15}

class Motor():
    def __init__(self, motor):
        self.motor = motor
        for x in self.motor:
            GPIO.setup(self.motor[x], GPIO.OUT)

       # GPIO.output(self.motor['EN'], GPIO.HIGH)

    def spin_forward(self):
        GPIO.output(self.motor['input1'], GPIO.HIGH)
        GPIO.output(self.motor['input2'], GPIO.LOW)

    def spin_back(self):
        GPIO.output(self.motor['input1'], GPIO.LOW)
        GPIO.output(self.motor['input2'], GPIO.HIGH)
    
    def spin_stop(self):
        GPIO.output(self.motor['input1'], GPIO.LOW)
        GPIO.output(self.motor['input2'], GPIO.LOW)

class Vehicle():
    def __init__(self, motorR, motorL):
        self.motorR = Motor(motorR)
        self.motorL = Motor(motorL)

    def forward(self):
        self.motorR.spin_forward()
        self.motorL.spin_forward()

    def back(self):
        self.motorR.spin_back()
        self.motorL.spin_back()

    def right(self):
        self.motorR.spin_back()
        self.motorL.spin_fowrard()

    def left(self):
        self.motorR.spin_forward()
        self.motorL.spin_back()

    def stop(self):
        self.motorR.spin_stop()
        self.motorL.spin_stop()

"""

for x in Motor1:
    GPIO.setup(Motor1[x], GPIO.OUT)
    GPIO.setup(Motor2[x], GPIO.OUT)

#EN1 = GPIO.PWM(Motor1['EN'], 100)    
#EN2 = GPIO.PWM(Motor2['EN'], 100)    

#EN1.start(0)                    
#EN2.start(0)                    
GPIO.output(Motor1['EN'], GPIO.HIGH)

while True:
    for x in range(40, 100):
        print ("FORWARD MOTION")
       # EN1.ChangeDutyCycle(x)
       # EN2.ChangeDutyCycle(x)

        GPIO.output(Motor1['input1'], GPIO.HIGH)
        GPIO.output(Motor1['input2'], GPIO.LOW)
        
        GPIO.output(Motor2['input1'], GPIO.HIGH)
        GPIO.output(Motor2['input2'], GPIO.LOW)

        sleep(0.1)
   
    print ("STOP")
   # EN1.ChangeDutyCycle(0)
   # EN2.ChangeDutyCycle(0)

    sleep(5)
     
    for x in range(40, 100):
        print ("BACKWARD MOTION")
       # EN1.ChangeDutyCycle(x)
       # EN2.ChangeDutyCycle(x)
        
        GPIO.output(Motor1['input1'], GPIO.LOW)
        GPIO.output(Motor1['input2'], GPIO.HIGH)

        GPIO.output(Motor2['input1'], GPIO.LOW)
        GPIO.output(Motor2['input2'], GPIO.HIGH)

        sleep(0.1)
     
    print ("STOP")
   # EN1.ChangeDutyCycle(0)
   # EN2.ChangeDutyCycle(0)

    sleep(5)
"""
GPIO.cleanup()

