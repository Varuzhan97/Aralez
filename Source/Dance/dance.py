#For dance parallelism
import multiprocessing
import os
import random
from Utils import utils, lights

class Dance:
    def __init__(self):
        self.expected_distance = 30
        # Motor 1
        self.in1 = 17
        self.in2 = 27
        self.en1 = 22
        # Motor 2
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
        self.p1.start(50)
        self.p2.start(50)

    def play_madagascar(self):
        self.set_medium_speed()
        while shared_num.value == 0:
            self.turnaround()
            self.forward()
            self.backward()
            self.stop()

    def stop(self):
        GPIO.output(self.in1, GPIO.LOW)
        GPIO.output(self.in2, GPIO.LOW)
        GPIO.output(self.in3, GPIO.LOW)
        GPIO.output(self.in4, GPIO.LOW)

    def forward(self):
        if detect_distance(self.expected_distance):
            GPIO.output(self.in1, GPIO.HIGH)
            GPIO.output(self.in2, GPIO.LOW)
            GPIO.output(self.in3, GPIO.HIGH)
            GPIO.output(self.in4, GPIO.LOW)
            time.sleep(2)
            self.stop()

    def backward(self):
        if detect_distance(self.expected_distance):
            GPIO.output(self.in1, GPIO.LOW)
            GPIO.output(self.in2, GPIO.HIGH)
            GPIO.output(self.in3, GPIO.LOW)
            GPIO.output(self.in4, GPIO.HIGH)
            logging.info("backward")

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

    def turnaround(self):
        self.low()
        GPIO.output(self.in1, GPIO.HIGH)
        GPIO.output(self.in2, GPIO.LOW)
        GPIO.output(self.in3, GPIO.LOW)
        GPIO.output(self.in4, GPIO.HIGH)
        time.sleep(4)
        self.stop()

    def set_high_speed(self):
        self.p1.ChangeDutyCycle(75)
        self.p2.ChangeDutyCycle(75)

    def set_medium_speed(self):
        self.p1.ChangeDutyCycle(50)
        self.p2.ChangeDutyCycle(50)

    def play_dance_music(self, music_folder_path, shared_num):
        choose_music_id = random.randint(0, 1)
        utils.play_tts_clip(os.path.join(music_folder_path, str(choose_music_id) + ".mp3"))
        shared_num.value = 1

    def start_dance(self, music_folder_path, lights):
        shared_num = multiprocessing.Value('d', 0)
        #Randomly choose music
        #Check music ID and choose dance
        music_proc = multiprocessing.Process(target=play_dance_music,args=(music_folder_path, shared_num, ))
        dance_proc = multiprocessing.Process(target=play_madagasca,args=(shared_num, ))
        lights_proc = multiprocessing.Process(target=lights.light_show(music_proc, shared_num, ))

        music_proc.start()
        dance_proc.start()
        lights_proc.start()

        music_proc.join()
        dance_proc.join()
        lights_proc.start()
