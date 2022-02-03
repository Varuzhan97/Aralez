#!/usr/bin/env python
import RPi.GPIO as GPIO
import time
import subprocess

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(3, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def press_checker(channel):
    global button_status
    start_time = time.time()
    #Wait for the button up
    while GPIO.input(channel) == 0:
        pass

    #How long was the button down?
    button_time = time.time() - start_time

    #Ignore noise
    #1 - brief push (shutdown)
    if .1 <= button_time < 2:
        button_status = 1
        subprocess.call(['shutdown', '-h', 'now'], shell=False)
    #2 - Long push (restart)
    elif 2 <= button_time:
        button_status = 2
        subprocess.call(['shutdown', '-r', 'now'], shell=False)

GPIO.add_event_detect(3, GPIO.FALLING, callback=press_checker, bouncetime=500)
try:
    while True : pass
except:
    GPIO.cleanup()
