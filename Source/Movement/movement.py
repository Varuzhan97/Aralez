import RPi.GPIO as GPIO
import logging
import time
from Utils import utils

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
        self.p1 = GPIO.PWM(self.en1, 1000)
        self.p2 = GPIO.PWM(self.en2, 1000)
        self.p1.start(50)
        self.p2.start(50)

    def forward(self):
        if utils.detect_distance(self.expected_distance):
            GPIO.output(self.in1, GPIO.HIGH)
            GPIO.output(self.in2, GPIO.LOW)
            GPIO.output(self.in3, GPIO.HIGH)
            GPIO.output(self.in4, GPIO.LOW)
            time.sleep(3)
            self.stop()

    def backward(self):
        self.turn_back()
        self.forward()

    def stop(self):
        GPIO.output(self.in1, GPIO.LOW)
        GPIO.output(self.in2, GPIO.LOW)
        GPIO.output(self.in3, GPIO.LOW)
        GPIO.output(self.in4, GPIO.LOW)

    def left(self):
        GPIO.output(self.in1, GPIO.LOW)
        GPIO.output(self.in2, GPIO.LOW)
        GPIO.output(self.in3, GPIO.HIGH)
        GPIO.output(self.in4, GPIO.LOW)
        time.sleep(1.5)
        self.forward()

    def right(self):
        GPIO.output(self.in1, GPIO.HIGH)
        GPIO.output(self.in2, GPIO.LOW)
        GPIO.output(self.in3, GPIO.LOW)
        GPIO.output(self.in4, GPIO.LOW)
        time.sleep(1.5)
        self.forward()

    def turn_back(self):
        GPIO.output(self.in1, GPIO.HIGH)
        GPIO.output(self.in2, GPIO.LOW)
        GPIO.output(self.in3, GPIO.LOW)
        GPIO.output(self.in4, GPIO.HIGH)
        time.sleep(3)
        self.stop()

    def high_speed(self):
        self.p1.ChangeDutyCycle(75)
        self.p2.ChangeDutyCycle(75)

    def medium_speed(self):
        self.p1.ChangeDutyCycle(50)
        self.p2.ChangeDutyCycle(50)
