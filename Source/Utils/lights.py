import RPi.GPIO as GPIO
import time
from multiprocessing import Process

class Lights:
    def __init__(self):
        self.red = 11
        self.blue = 9
        self.green = 10

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.red, GPIO.OUT)
        GPIO.setup(self.blue, GPIO.OUT)
        GPIO.setup(self.green, GPIO.OUT)
        self.reset_led()

    def reset_led(self):
        GPIO.output(self.red, GPIO.LOW)
        GPIO.output(self.blue, GPIO.LOW)
        GPIO.output(self.green, GPIO.LOW)

    def light_show(self, music_proc: Process, shared_num):
        self.reset_led()
        while shared_num.value == 0:
            GPIO.output(self.blue, GPIO.LOW)
            GPIO.output(self.red, GPIO.HIGH)
            time.sleep(1)
            GPIO.output(self.red, GPIO.LOW)
            GPIO.output(self.green, GPIO.HIGH)
            time.sleep(1)
            GPIO.output(self.green, GPIO.LOW)
            GPIO.output(self.blue, GPIO.HIGH)
            time.sleep(1)


    #Function to change LED lights
    #Color ID's
    #0 ---> red
    #1 ---> bright green / yellow
    #2 ---> dark green / yellow
    def set_led_color(self, color_id: int):
        self.reset_led()
        if color_id == 0:
            GPIO.output(self.blue, GPIO.HIGH)
        elif color_id == 1:
            GPIO.output(self.green, GPIO.HIGH)
        elif color_id == 2:
            GPIO.output(self.red, GPIO.HIGH)
