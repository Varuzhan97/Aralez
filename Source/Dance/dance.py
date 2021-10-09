#For dance parallelism
from multiprocessing import Process
import os
from Utils import utils, lights

def play_dance_music(music_folder_path):
    choose_music_id = 1
    choose_music_id = (1-choose_music_id)
    utils.play_tts_clip(os.path.join(music_folder_path, str(choose_music_id) + ".mp3"))

def do_dance_steps():
    print("Hi.")

def start_dance(music_folder_path, lights):
    #Randomly choose music
    #Check music ID and choose dance
    music_proc = Process(target=play_dance_music(music_folder_path))
    dance_proc = Process(target=do_dance_steps)
    music_proc.start()
    dance_proc.start()
    music_proc.join()
    dance_proc.join()
    lights.light_show(music_proc)
