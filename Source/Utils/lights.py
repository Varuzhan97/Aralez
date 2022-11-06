import RPi.GPIO as GPIO
import time
from multiprocessing import Process

class Lights:
    def __init__(self, default_color = 1):
        self.red = 12
        self.blue = 13

        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(self.red, GPIO.OUT)
        GPIO.setup(self.blue, GPIO.OUT)
        self.reset_led()
        self.set_led_color(default_color)

    def reset_led(self):
        GPIO.output(self.red, GPIO.HIGH)
        GPIO.output(self.blue, GPIO.HIGH)

    def light_show(self, shared_num):
        self.reset_led()
        while shared_num.value == 0:
            GPIO.output(self.red, GPIO.LOW)
            GPIO.output(self.blue, GPIO.HIGH)
            time.sleep(1)
            GPIO.output(self.red, GPIO.HIGH)
            GPIO.output(self.blue, GPIO.LOW)
            time.sleep(1)
            GPIO.output(self.red, GPIO.LOW)
            GPIO.output(self.blue, GPIO.LOW)
            time.sleep(1)

        #Reset colors
        self.set_led_color(1)

    #Function to change LED lights
    #Color ID's
    #0 ---> red
    #1 ---> bright green / yellow
    #2 ---> dark green / yellow
    def set_led_color(self, color_id: int):
        self.reset_led()
        if color_id == 0:
            GPIO.output(self.red, GPIO.LOW)
        elif color_id == 1:
            GPIO.output(self.blue, GPIO.LOW)
        elif color_id == 2:
            GPIO.output(self.red, GPIO.LOW)
            GPIO.output(self.blue, GPIO.LOW)
