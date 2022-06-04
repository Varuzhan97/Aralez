#For dance parallelism
import multiprocessing
import os
import random
from Utils import utils, lights

class Music:
    #def __init__(self, move):

    def play_song(self, song_folder_path, shared_num):
        #Randomly choose music
        #Check music ID and choose dance
        choose_music_id = random.randint(0, 1)
        utils.play_tts_clip(os.path.join(song_folder_path, str(choose_music_id) + ".mp3"))
        shared_num.value = 1

    def play_lullaby(self, lullaby_folder_path, shared_num):
        utils.load_play_tts_clip(lullaby_folder)
        shared_num.value = 1

    #choice is the trigger for lullaby or song (0 ---> song, 1 ---> lullaby)
    def play_music(self, music_folder_path, lights, choice):
        shared_num = multiprocessing.Value('d', 0)

        music_proc = None

        if choice == 0:
            music_proc = multiprocessing.Process(target=self.play_music,args=(music_folder_path, shared_num,))
            music_proc.start()
        if choice == 1:
            music_proc = multiprocessing.Process(target=self.play_music,args=(play_lullaby, shared_num,))
            music_proc.start()

        lights_proc = multiprocessing.Process(target=lights.light_show, args=(shared_num,))
        lights_proc.start()

        music_proc.join()
        lights_proc.join()
