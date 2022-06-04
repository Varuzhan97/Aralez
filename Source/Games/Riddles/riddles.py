import yaml
import random
import os
from Utils import utils

def process_answer(vad_audio, wrong_answer, correct_answer):
    while True:
        answer = vad_audio.listen_audio()
        print(answer)
        if answer == '':
            continue
        if answer == 'stop' or answer == 'stop the game':
            return -2
        if answer == 'i can not answer' or answer == 'i do not know':
            return -1
        if answer == correct_answer:
            return 1
        if answer == wrong_answer:
            return 0

def riddles(riddles_data_folder, riddles_tts_folder, vad_audio):
    #Load YAML file that contains country-capital pairs
    data_file_yaml = None
    with open(os.path.join(capitals_data_folder, "data.yaml"), 'r') as file:
            data_file_yaml = yaml.full_load(file)


    number_of_riddles = len(data_file_yaml.items())
    print("jjjjjjjjjjjj", number_of_riddles)

    #Configure TTS speech audio clips paths
    #riddles_tts_folder is a full path and contains language ID too
    prequestion_speech = os.path.join(riddles_tts_folder, "1")
    question_speech = os.path.join(riddles_tts_folder, "2")
    options_speech = os.path.join(riddles_tts_folder, "3")
    options_or_speech = os.path.join(riddles_tts_folder, "4")
    correct_speech = os.path.join(riddles_tts_folder, "5")
    wrong_speech = os.path.join(riddles_tts_folder, 6")
    do_not_know_speech = os.path.join(riddles_tts_folder, "7")
    stop_speech = os.path.join(riddles_tts_folder, "8")

    #Choose riddle
    riddle_speech = random.choice(os.listdir(question_speech))
    riddle_speech = os.path.join(question_speech, riddle_speech)

    #YAML file contains ID's of riddles and corresponding answers
    #Riddle ID is the name of audio file (without extension)
    correct_answer = data_file_yaml.get(os.path.basename(riddle_speech)[0:-4])

    wrong_answer = str()
    #Riddles are 20 (indexes from 0 to 19)
    while True:
        #Get riddle random ID's answer from YAML
        #stugel id-n
        #Get random answer word
        wrong_answer = data_file_yaml.get(random.randint(0, number_of_riddles))
        if wrong_answer != correct_answer:
            break



    correct_answer_speech = os.path.join(options_speech, correct_answer, ".wav")
    wrong_answer_speech = os.path.join(options_speech, wrong_answer, ".wav")

    variants = list()
    variants.append(correct_answer_speech)
    variants.append(wrong_answer_speech)
    random.shuffle(variants)

    utils.load_play_tts_clip(prequestion_speech)
    utils.play_tts_clip(riddle_speech)
    utils.play_tts_clip(variants[0])
    utils.load_play_tts_clip(options_or_speech)
    utils.play_tts_clip(variants[1])

    result = process_answer(vad_audio, wrong_answer, correct_answer)
    if result == -2:
        utils.load_play_tts_clip(stop_speech)
        return
    if result == -1:
        utils.load_play_tts_clip(do_not_know_speech)
        continue
    if result == 0:
        utils.load_play_tts_clip(wrong_speech)
        continue
    if result == 1:
        utils.load_play_tts_clip(correct_speech)
    return
