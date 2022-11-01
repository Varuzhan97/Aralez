import yaml
import random
import os
from Utils import utils

def process_answer(vad_audio, correct_answer):
    while True:
        answer = vad_audio.listen_audio()
        print(answer)
        if answer == '':
            continue
        elif answer == 'stop' or answer == 'stop the game':
            return -2
        elif answer == 'i can not answer' or answer == 'i do not know':
            return -1
        elif answer == correct_answer:
            return 1
        else:
            return 0

def riddles(riddles_data_folder, riddles_tts_folder, vad_audio, correct_tts_folder, wrong_tts_folder):
    #Load YAML file that contains country-capital pairs
    data_file_yaml = None
    with open(os.path.join(riddles_data_folder, "data.yaml"), 'r') as file:
            data_file_yaml = yaml.full_load(file)


    number_of_riddles = len(data_file_yaml.items())

    #Configure TTS speech audio clips paths
    #riddles_tts_folder is a full path and contains language ID too
    prequestion_speech = os.path.join(riddles_tts_folder, "1")
    question_speech = os.path.join(riddles_tts_folder, "2")
    think_time_speech = os.path.join(riddles_tts_folder, "3")
    think_time_end_speech = os.path.join(riddles_tts_folder, "4")
    correct_speech = os.path.join(riddles_tts_folder, "5")
    wrong_speech = os.path.join(riddles_tts_folder, "6")
    stop_speech = os.path.join(riddles_tts_folder, "7")
    do_not_know_speech = os.path.join(riddles_tts_folder, "8")

    #Choose riddle
    riddle_speech = random.choice(os.listdir(question_speech))
    riddle_speech = os.path.join(question_speech, riddle_speech)

    #YAML file contains ID's of riddles and corresponding answers
    #Riddle ID is the name of audio file (without extension)
    correct_answer = data_file_yaml.get(os.path.basename(riddle_speech)[0:-4])

    utils.load_play_tts_clip(prequestion_speech)
    utils.play_tts_clip(riddle_speech)

    utils.load_play_tts_clip(think_time_speech)
    #Timer for a 5 seconds think time
    #After 5 seconds inform
    utils.load_play_tts_clip(tts_folder = think_time_end_speech, stop_time = 3)

    print("jjjjjjjjjjjj", correct_answer)

    result = process_answer(vad_audio, correct_answer)

    if result == -2:
        utils.load_play_tts_clip(stop_speech)
        return
    if result == -1:
        utils.load_play_tts_clip(do_not_know_speech)
        return
    if result == 0:
        utils.load_play_tts_clip(wrong_speech)
        utils.load_play_tts_clip(wrong_tts_folder)
        return
    if result == 1:
        utils.load_play_tts_clip(correct_speech)
        utils.load_play_tts_clip(correct_tts_folder)
        return
