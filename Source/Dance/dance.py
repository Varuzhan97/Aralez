#For dance parallelism
import multiprocessing
import os
import RPi.GPIO as GPIO
import random
from Utils import utils, lights

class Dance:
    def __init__(self, move):
        self.move = move

    def play_madagascar(self, shared_num):
        self.move.set_medium_speed()
        while shared_num.value == 0:
            self.move.turnaround()
            self.move.forward()
            self.move.backward()
            self.move.stop()

    def play_dance_music(self, music_folder_path, shared_num):
        choose_music_id = random.randint(0, 1)
        utils.play_tts_clip(os.path.join(music_folder_path, str(choose_music_id) + ".mp3"))
        shared_num.value = 1

    def start_dance(self, music_folder_path, lights):
        shared_num = multiprocessing.Value('d', 0)
        #Randomly choose music
        #Check music ID and choose dance
        proc = []

        music_proc = multiprocessing.Process(target=self.play_dance_music,args=(self, music_folder_path, shared_num))
        music_proc.start()
        proc.append(music_proc)

        dance_proc = multiprocessing.Process(target=self.play_madagascar,args=(self, shared_num))
        dance_proc.start()
        proc.append(dance_proc)

        lights_proc = multiprocessing.Process(target=lights.light_show, args=(self, shared_num))
        lights_proc.start()
        proc.append(lights_proc)

        for p in proc:
            p.join()
