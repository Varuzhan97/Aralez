#For dance parallelism
import multiprocessing
import os
import random
from Utils import utils, lights

def play_dance_music(music_folder_path, shared_num):
    choose_music_id = random.randint(0, 1)
    utils.play_tts_clip(os.path.join(music_folder_path, str(choose_music_id) + ".mp3"))
    shared_num.value = 1

def do_dance_steps(shared_num):
    while shared_num.value == 0:
        print("**************")

def start_dance(music_folder_path, lights):
    shared_num = multiprocessing.Value('d', 0)
    #Randomly choose music
    #Check music ID and choose dance
    music_proc = multiprocessing.Process(target=play_dance_music,args=(music_folder_path, shared_num, ))
    dance_proc = multiprocessing.Process(target=do_dance_steps,args=(shared_num, ))

    music_proc.start()
    dance_proc.start()

    music_proc.join()
    dance_proc.join()

    #lights.light_show(music_proc)
