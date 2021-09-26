from multiprocessing import Process #For dance parallelism
from Utils import utils

choose_music.id = 1

def choose_music():
    choose_music.id = (1-choose_music.id)
    return

def play_dance_music(music_folder_path):
  print ('func1: starting')
  utils.load_play_tts_clip(os.path.join(music_folder_path, choose_music.id + ".mp3"))
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
