from multiprocessing import Process #For dance parallelism
import os
from Utils import utils

def play_dance_music(music_folder_path):
    choose_music_id = 1
    choose_music_id = (1-choose_music_id)
    print ('func1: starting')
    utils.play_tts_clip(os.path.join(music_folder_path, str(choose_music_id) + ".mp3"))
    print ('func1: finishing')

def do_dance_steps():
    print ('func2: starting')
    #os.system("mpg321 %s --stereo" % ('"' + "/home/varuzhan/Desktop/Aralez/Source/Actions/Dance/Music/MA_Бэтси__Симпл_димп-HQ(320k)-[AudioTrimmer.com].mp3" + '"'))
    print ('func2: finishing')

def dance(music_folder_path):
    #Randomly choose music
    #Check music ID and choose dance
    p1 = Process(target=play_dance_music(music_folder_path))
    p1.start()
    p2 = Process(target=do_dance_steps)
    p2.start()
    p1.join()
    p2.join()
