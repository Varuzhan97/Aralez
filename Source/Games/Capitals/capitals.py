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

#Choose N audio clips from path
def choose_sample(samples_path, folder, speech_number):
    temp_result_speech = random.sample(os.listdir(os.path.join(samples_path, folder)), speech_number)
    result_speech = []
    for speech in temp_result_speech:
        result_speech.append(os.path.join(samples_path, folder, speech))
    if len(result_speech) == 1:
        result_speech = result_speech[0]
        return result_speech
    else:
        return result_speech

#Choose all audio clips from path
def choose_all_sample(samples_path, folder):
    temp_result_speech = os.listdir(os.path.join(samples_path, folder))
    result_speech = []
    for speech in temp_result_speech:
        result_speech.append(os.path.join(samples_path, folder, speech))
    return result_speech

def ask(prequestion, questions, capitals_tts_folder, correct_speech, wrong_speech, options_speech, options_number_speech, think_time_speech, think_time_end_speech, do_not_know_speech, data_file_yaml, stt, model, vad_audio):
    score = 0
    for question in questions:
        time.sleep(1)
        os.system("mpg321 %s --stereo" % ('"' + random.choice(prequestion) + '"'))
        time.sleep(1)
        os.system("mpg321 %s --stereo" % ('"' + question + '"'))

        correct_answer = list()
        answer_options_speech = list()

        #Get capital of the selected country
        correct_answer.append(data_file_yaml.get(os.path.basename(question)[0:-4]))

        #If there are two capitals, choose one of them. correct_answer is list of list
        if len(correct_answer) > 1:
            correct_answer = random.choices(correct_answer[0])

        #Choose 2 random options and append to answer_options_speech list
        answer_options_speech.append(choose_sample(capitals_tts_folder, "3", 2))
        #Append 3 options (including the correct_answer) to answer_options_speech list
        #Folder 3 contains mp3 files with names of capitals
        answer_options_speech[0].append(os.path.join(capitals_tts_folder, "3", correct_answer[0] + '.mp3'))
        answer_options_speech = answer_options_speech[0]
        #Random shuffle answer_options_speech list
        random.shuffle(answer_options_speech)

        #Play 3 options
        time.sleep(1)
        os.system("mpg321 %s --stereo" % ('"' + options_speech + '"'))
        i = 0
        for option in answer_options_speech:
            time.sleep(1)
            os.system("mpg321 %s --stereo" % ('"' + options_number_speech[i] + '"'))
            i += 1
            time.sleep(1)
            os.system("mpg321 %s --stereo" % ('"' + option + '"'))
            time.sleep(1)

        #5 seconds to think
        time.sleep(1)
        os.system("mpg321 %s --stereo" % ('"' + think_time_speech + '"'))
        time.sleep(5)
        os.system("mpg321 %s --stereo" % ('"' + think_time_end_speech + '"'))
        #After 5 seconds inform
        while True:
            answer = stt.listen_audio(model, vad_audio)
            print(answer)
            if answer == '':
                continue
            if answer == 'stop' or answer == 'stop the game' or answer == 'the game' or answer == 'one the game' or answer == 'game':
                return -1
            if answer == 'i can not answer' or answer == 'i do not know':
                time.sleep(1)
                os.system("mpg321 %s --stereo" % ('"' + do_not_know_speech + '"'))
                continue
            if answer == 'one' or answer == 'two' or answer == 'three':
                answer_number = strings_to_numbers(answer)
                print(answer_number, correct_answer[0], answer_options_speech[answer_number-1])
                if(correct_answer[0] == os.path.basename(answer_options_speech[answer_number-1])[0:-4]):
                    speech = random.choice(correct_speech)
                    time.sleep(1)
                    os.system("mpg321 %s --stereo" % ('"' + speech + '"'))
                    score += 1
                else:
                    speech = random.choice(wrong_speech)
                    time.sleep(1)
                    os.system("mpg321 %s --stereo" % ('"' + speech + '"'))
                break
    return score

def capitals(capitals_questions_number, capitals_data_folder, capitals_tts_folder, stt, model, vad_audio):
    data_file =  open(os.path.join(capitals_data_folder, "data.yaml"), 'r')
    data_file_yaml = yaml.full_load(data_file)

    start_speech = choose_sample(capitals_tts_folder, "0", 1)
    prequestion_speech = choose_all_sample(capitals_tts_folder, "1")
    question_speech = list()
    question_speech = choose_sample(capitals_tts_folder, "2", capitals_questions_number)
    correct_speech = choose_all_sample(capitals_tts_folder, "4")
    wrong_speech = choose_all_sample(capitals_tts_folder, "5")
    score_speech = choose_all_sample(capitals_tts_folder, "6")
    score_speech.sort()
    low_result_speech = choose_sample(capitals_tts_folder, "7", 1)
    middle_result_speech = choose_sample(capitals_tts_folder, "8", 1)
    high_result_speech = choose_sample(capitals_tts_folder, "9", 1)
    perfect_result_speech = choose_sample(capitals_tts_folder, "10", 1)
    ##########################################################################
    options_speech = choose_sample(capitals_tts_folder, "11", 1)
    options_number_speech = choose_all_sample(capitals_tts_folder, "12")
    options_number_speech.sort()
    think_time_speech = choose_sample(capitals_tts_folder, "13", 1)
    think_time_end_speech = choose_sample(capitals_tts_folder, "14", 1)
    do_not_know_speech = choose_sample(capitals_tts_folder, "15", 1)
    stop_speech = choose_sample(capitals_tts_folder, "16", 1)

    time.sleep(1)
    os.system("mpg321 %s --stereo" % ('"' + start_speech + '"'))
    score = ask(prequestion_speech, question_speech, capitals_tts_folder, correct_speech, wrong_speech, options_speech, options_number_speech, think_time_speech, think_time_end_speech, do_not_know_speech, data_file_yaml, stt, model, vad_audio)

    if score == -1:
        os.system("mpg321 %s --stereo" % ('"' + stop_speech + '"'))
        return
    os.system("mpg321 %s --stereo" % ('"' + score_speech[score] + '"'))
    print("Score:", score)

    if 0 <= score <= 3:
        time.sleep(1)
        os.system("mpg321 %s --stereo" % ('"' + low_result_speech + '"'))
    if 4 <= score <= 6:
        time.sleep(1)
        os.system("mpg321 %s --stereo" % ('"' + middle_result_speech + '"'))
    if 7 <= score <= 9:
        time.sleep(1)
        os.system("mpg321 %s --stereo" % ('"' + high_result_speech + '"'))
    if score == 10:
        time.sleep(1)
        os.system("mpg321 %s --stereo" % ('"' + perfect_result_speech + '"'))
