import yaml
import random
import os
import time

#Convert number name to digit
def strings_to_numbers(argument):
    switcher = {
        "one": 1,
        "two": 2,
        "three": 3,
    }
    #get() method of dictionary data type returns value of passed argument if it is present in dictionary.
    #Otherwise second argument will be assigned as default value of passed argument
    return switcher.get(argument, -1)

#Function to load and play one random or specific tts clip from directory
def load_play_tts_clip(tts_folder, specific = None, stop_time = 1):
    #Timer for a short stop befor speech
    time.sleep(int(stop_time))
    if specific is not None:
        play = os.path.join(tts_folder, specific + ".mp3")
        os.system("mpg321 %s --stereo" % ('"' + play + '"'))
    else:
        all_files = []
        for file in os.listdir(tts_folder):
            if file.endswith(".mp3"):
                all_files.append(os.path.join(tts_folder, file))
        play = random.choice(all_files)
        os.system("mpg321 %s --stereo" % ('"' + play + '"'))

#Function to play a clip
def play_tts_clip(clip_path, stop_time = 1):
    #Timer for a short stop befor speech
    time.sleep(int(stop_time))
    os.system("mpg321 %s --stereo" % ('"' + clip_path + '"'))

#Function to choose (N = speech_number) options from samples_path directory
def choose_options(samples_path, speech_number):
    temp_result_speech = random.sample(os.listdir(samples_path), speech_number)
    result_speech = []
    for speech in temp_result_speech:
        result_speech.append(os.path.join(samples_path, speech))
    return result_speech

def process_answer(think_time_speech, think_time_end_speech, stt, vad_audio, three_variants_speech, correct_answer):
    #Think time and ending speeches
    load_play_tts_clip(think_time_speech)
    #Timer for a 5 seconds think time
    time.sleep(5)
    #After 5 seconds inform
    load_play_tts_clip(think_time_end_speech)

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
            answer_number = strings_to_numbers(answer)
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
        load_play_tts_clip(prequestion_speech)
        play_tts_clip(question)
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
        load_play_tts_clip(options_speech)
        for i, option in enumerate(three_variants_speech):
            play_tts_clip(options_number_speech[i])
            play_tts_clip(option)

        result = process_answer(think_time_speech, think_time_end_speech, stt, vad_audio, three_variants_speech, correct_answer)
        if result == -2:
            load_play_tts_clip(stop_speech)
            return
        if result == -1:
            load_play_tts_clip(do_not_know_speech)
            continue
        if result == 0:
            load_play_tts_clip(wrong_speech)
            continue
        if result == 1:
            load_play_tts_clip(correct_speech)
            score +=1
            continue

    load_play_tts_clip(score_speech, specific = str(score))
    if 0 <= score <= 3:
        load_play_tts_clip(low_result_speech)
    if 4 <= score <= 6:
        load_play_tts_clip(middle_result_speech)
        time.sleep(1)
    if 7 <= score <= 9:
        load_play_tts_clip(high_result_speech)
        time.sleep(1)
    if score == 10:
        load_play_tts_clip(perfect_result_speech)
