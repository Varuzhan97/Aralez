import yaml
import random
import os
from Utils import utils

#Function to choose (N = speech_number) options from samples_path directory
def choose_options(samples_path, speech_number):
    temp_result_speech = random.sample(os.listdir(samples_path), speech_number)
    result_speech = []
    for speech in temp_result_speech:
        result_speech.append(os.path.join(samples_path, speech))
    return result_speech

def process_answer(think_time_speech, think_time_end_speech, stt, vad_audio, three_variants_speech, correct_answer):
    #Think time and ending speeches
    utils.load_play_tts_clip(think_time_speech)
    #Timer for a 5 seconds think time
    #After 5 seconds inform
    utils.load_play_tts_clip(tts_folder = think_time_end_speech, stop_time = 5)

    while True:
        answer = stt.listen_audio(vad_audio)
        print(answer)
        if answer == '':
            continue
        if answer == 'stop' or answer == 'stop the game':
            return -2
        if answer == 'i can not answer' or answer == 'i do not know':
            return -1
        if answer == 'one' or answer == 'two' or answer == 'three':
            answer_number = utils.strings_to_numbers(answer)
            if(correct_answer[0] == os.path.basename(three_variants_speech[answer_number-1])[0:-4]):
                return 1
            else:
                return 0
            break

def capitals(capitals_questions_number, capitals_data_folder, capitals_tts_folder, stt, vad_audio):
    #Load YAML file that contains country-capital pairs
    data_file =  open(os.path.join(capitals_data_folder, "data.yaml"), 'r')
    data_file_yaml = yaml.full_load(data_file)

    #Configure TTS speech audio clips paths
    #capitals_tts_folder is a full path and contains language ID too
    prequestion_speech = os.path.join(capitals_tts_folder, "1")
    capitals_variants_speech = os.path.join(capitals_tts_folder, "3")
    question_speech = os.path.join(capitals_tts_folder, "2")
    correct_speech = os.path.join(capitals_tts_folder, "4")
    wrong_speech = os.path.join(capitals_tts_folder, "5")
    score_speech = os.path.join(capitals_tts_folder, "6")
    low_result_speech = os.path.join(capitals_tts_folder, "7")
    middle_result_speech = os.path.join(capitals_tts_folder, "8")
    high_result_speech = os.path.join(capitals_tts_folder, "9")
    perfect_result_speech = os.path.join(capitals_tts_folder, "10")
    options_speech = os.path.join(capitals_tts_folder, "11")
    options_number_speech = os.path.join(capitals_tts_folder, "12")
    #Load 1, 2, 3 options speech
    options_number_speech = choose_options(options_number_speech, 3)
    options_number_speech.sort()
    think_time_speech = os.path.join(capitals_tts_folder, "13")
    think_time_end_speech = os.path.join(capitals_tts_folder, "14")
    do_not_know_speech = os.path.join(capitals_tts_folder, "15")
    stop_speech = os.path.join(capitals_tts_folder, "16")

    score = 0

    #Choose countries to ask
    #Number of countries is equal to capitals_questions_number
    question_speech = choose_options(question_speech, capitals_questions_number)

    for question in question_speech:
        utils.load_play_tts_clip(prequestion_speech)
        utils.play_tts_clip(question)
        correct_answer = list()
        #Get capital of the selected country
        correct_answer.append(data_file_yaml.get(os.path.basename(question)[0:-4]))
        #If there are two capitals, choose one of them. correct_answer is list of list
        if len(correct_answer) > 1:
            correct_answer = random.choices(correct_answer[0])
        #Choose 2 random options and append to answer_options_speech list
        #answer_options_speech.append(choose_sample(capitals_tts_folder, "3", 2))
        three_variants_speech = list()
        three_variants_speech.append(correct_answer)
        #Choose 2 different variants + the correct_answer
        #Append 3 options (including the correct_answer) to three_variants_speech list
        #Folder 3 contains mp3 files with names of capitals
        while True:
            three_variants_speech = choose_options(capitals_variants_speech, 2)
            if correct_answer not in three_variants_speech:
                three_variants_speech.append(os.path.join(capitals_variants_speech, correct_answer[0] + '.mp3'))
                break
        #Random shuffle answer_options_speech list
        random.shuffle(three_variants_speech)
        utils.load_play_tts_clip(options_speech)
        for i, option in enumerate(three_variants_speech):
            utils.play_tts_clip(options_number_speech[i])
            utils.play_tts_clip(option)

        result = process_answer(think_time_speech, think_time_end_speech, stt, vad_audio, three_variants_speech, correct_answer)
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
            score +=1
            continue

    utils.load_play_tts_clip(score_speech, specific = str(score))
    if 0 <= score <= 3:
        utils.load_play_tts_clip(low_result_speech)
    if 4 <= score <= 6:
        utils.load_play_tts_clip(middle_result_speech)
    if 7 <= score <= 9:
        utils.load_play_tts_clip(high_result_speech)
    if score == 10:
        utils.load_play_tts_clip(perfect_result_speech)
