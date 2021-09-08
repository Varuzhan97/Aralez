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

#####################################################################################
capitals
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

def ask(prequestion, questions, capitals_tts_folder, correct_speech, wrong_speech, options_speech, options_number_speech, think_time_speech, think_time_end_speech, do_not_know_speech, data_file_yaml, stt, vad_audio):
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
            answer = stt.listen_audio(vad_audio)
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
