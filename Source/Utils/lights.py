#import RPi.GPIO as GPIO
import time
from multiprocessing import Process

class Lights:
    def __init__(self):
        self.red = 4
        self.blue = 2
        self.green = 3
        '''
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.red, GPIO.OUT)
        GPIO.setup(self.blue, GPIO.OUT)
        GPIO.setup(self.green, GPIO.OUT)

        GPIO.output(self.red, GPIO.LOW)
        GPIO.output(self.blue, GPIO.LOW)
        GPIO.output(self.green, GPIO.LOW)
        '''
    '''
    def sleep(self):
        GPIO.output(self.red, GPIO.LOW)
        GPIO.output(self.blue, GPIO.LOW)
        GPIO.output(self.green, GPIO.LOW)

    def light_show(self, music_proc: Process):
        while music_proc.is_alive():
            GPIO.output(self.red, GPIO.HIGH)
            time.sleep(1)
            GPIO.output(self.blue, GPIO.LOW)
            time.sleep(1)
            GPIO.output(self.green, GPIO.LOW)
            time.sleep(1)

    #Function to change LED lights
    #Color ID's
    #0 ---> red
    #1 ---> bright green / yellow
    #2 ---> dark green / yellow
    def change_color(self, color_id: int):
        if color_id == 0:
            GPIO.output(self.blue, GPIO.HIGH)
        elif color_id == 1:
            GPIO.output(self.green, GPIO.HIGH)
        elif color_id == 2:
            GPIO.output(self.red, GPIO.HIGH)
    '''
