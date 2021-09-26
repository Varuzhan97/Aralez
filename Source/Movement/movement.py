import RPi.GPIO as GPIO
import logging
import time

from Utils.distance_detector import detect_distance


class Move:
    def __init__(self):
        self.expected_distance = 30
        # Motor/wheel 1
        self.in1 = 17
        self.in2 = 27
        self.en1 = 22
        # Motor/wheel 2
        self.in3 = 23
        self.in4 = 24
        self.en2 = 25

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.in1, GPIO.OUT)
        GPIO.setup(self.in2, GPIO.OUT)
        GPIO.setup(self.in3, GPIO.OUT)
        GPIO.setup(self.in4, GPIO.OUT)
        GPIO.setup(self.en1, GPIO.OUT)
        GPIO.setup(self.en2, GPIO.OUT)
        GPIO.output(self.in1, GPIO.LOW)
        GPIO.output(self.in2, GPIO.LOW)
        GPIO.output(self.in3, GPIO.LOW)
        GPIO.output(self.in4, GPIO.LOW)
        self.p1 = GPIO.PWM(en1, 1000)
        self.p2 = GPIO.PWM(en2, 1000)
        self.p1.start(25)
        self.p2.start(25)

    def forward(self):
        if detect_distance(self.expected_distance):
            GPIO.output(self.in1, GPIO.HIGH)
            GPIO.output(self.in2, GPIO.LOW)
            GPIO.output(self.in3, GPIO.HIGH)
            GPIO.output(self.in4, GPIO.LOW)
            logging.info("forward")

    def backward(self):
        if detect_distance(self.expected_distance):
            GPIO.output(self.in1, GPIO.LOW)
            GPIO.output(self.in2, GPIO.HIGH)
            GPIO.output(self.in3, GPIO.LOW)
            GPIO.output(self.in4, GPIO.HIGH)
            logging.info("backward")

    def stop(self):
        GPIO.output(self.in1, GPIO.LOW)
        GPIO.output(self.in2, GPIO.LOW)
        GPIO.output(self.in3, GPIO.LOW)
        GPIO.output(self.in4, GPIO.LOW)
        logging.info("stop")

    def left(self):
        GPIO.output(self.in1, GPIO.HIGH)
        GPIO.output(self.in2, GPIO.LOW)
        GPIO.output(self.in3, GPIO.LOW)
        GPIO.output(self.in4, GPIO.LOW)
        time.sleep(2)
        GPIO.output(self.in1, GPIO.LOW)

    def right(self):
        GPIO.output(self.in1, GPIO.LOW)
        GPIO.output(self.in2, GPIO.LOW)
        GPIO.output(self.in3, GPIO.HIGH)
        GPIO.output(self.in4, GPIO.LOW)
        time.sleep(2)
        GPIO.output(self.in3, GPIO.LOW)


    def turn_back(self):
        self.low()
        GPIO.output(self.in1, GPIO.HIGH)
        GPIO.output(self.in2, GPIO.LOW)
        GPIO.output(self.in3, GPIO.LOW)
        GPIO.output(self.in4, GPIO.HIGH)
        time.sleep(4)
        self.stop()

    def high(self):
        self.p1.ChangeDutyCycle(75)
        self.p2.ChangeDutyCycle(75)

    def low(self):
        self.p1.ChangeDutyCycle(25)
        self.p2.ChangeDutyCycle(25)

    def medium(self):
        self.p1.ChangeDutyCycle(50)
        self.p2.ChangeDutyCycle(50)
