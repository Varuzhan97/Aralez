import yaml
import random
import os
import time
import random

#Convert number name to digit
def strings_to_numbers(argument):
    switcher = {
        "zero": 0,
        "one": 1,
        "two": 2,
        "three": 3,
        "four": 4,
        "five": 5,
        "six": 6,
        "seven": 7,
        "eight": 8,
        "nine": 9,
        "ten": 10,
        "eleven": 11,
        "twelve": 12,
        "thirteen": 13,
        "fourteen": 14,
        "fifteen": 15,
        "sixteen": 16,
        "seventeen": 17,
        "eighteen": 18,
        "nineteen": 19,
        "twenty": 20,
        "twenty one": 21,
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

def process_answer(current_number, range_limit, wrong_speech, correct_speech, stt, model, vad_audio):
    while True:
        answer = stt.listen_audio(model, vad_audio)
        ##################################################3
        if answer == '':
            continue
        if answer == 'stop' or answer == 'stop the game' or answer == 'the game' or answer == 'one the game' or answer == 'game':
            return -1
        if answer == 'one' or answer == 'two' or answer == 'three':
            ##################################################
            answer_number = strings_to_numbers(answer)
            print("this is: ", answer_number)
            if (answer_number < current_number+1) or (answer_number > current_number+range_limit):
                time.sleep(1)
                speech = random.choice(wrong_speech)
                os.system("mpg321 %s --stereo" % ('"' + speech + '"'))
                #os.system("mpg321 %s --stereo" % ('"' + os.path.join("/home/varuzhan/Desktop/***PROJECT***/Oberon/TTS/Conversation", language, resp) + '"'))
                continue
            break
        ###################################################

    time.sleep(1)
    speech = random.choice(correct_speech)
    os.system("mpg321 %s --stereo" % ('"' + speech + '"'))
    return answer_number

def generate_number(current_number, range_limit, numbers_speech, think_time_speech, think_time_end_speech):
    if (current_number+range_limit) >= 21:
        generated_number = 21
        time.sleep(1)
        os.system("mpg321 %s --stereo" % ('"' + os.path.join(numbers_speech, str(generated_number) + ".mp3") + '"'))
        return generated_number
    else:
        generated_number = random.randint(current_number+1, current_number+range_limit)
        print("Range: ", current_number+1, current_number+range_limit)
        print("Number: ", generated_number)
        time.sleep(1)
        os.system("mpg321 %s --stereo" % ('"' + os.path.join(numbers_speech, str(generated_number) + ".mp3") + '"'))

        time.sleep(1)
        os.system("mpg321 %s --stereo" % ('"' + think_time_speech + '"'))
        time.sleep(5)
        os.system("mpg321 %s --stereo" % ('"' + think_time_end_speech + '"'))
        return generated_number

def twenty_one(twenty_one_tts_folder, stt, model, vad_audio):

    start_speech = choose_sample(twenty_one_tts_folder, "0", 1)
    first_start_speech = choose_all_sample(twenty_one_tts_folder, "1")
    first_start_speech.sort()
    prequestion_speech = choose_all_sample(twenty_one_tts_folder, "2")
    numbers_speech = choose_all_sample(twenty_one_tts_folder, "3")
    correct_speech = choose_all_sample(twenty_one_tts_folder, "4")
    wrong_speech = choose_all_sample(twenty_one_tts_folder, "5")
    winner_speech = choose_sample(twenty_one_tts_folder, "6", 1)
    loser_speech = choose_sample(twenty_one_tts_folder, "7", 1)

    think_time_speech = choose_sample(twenty_one_tts_folder, "8", 1)
    think_time_end_speech = choose_sample(twenty_one_tts_folder, "9", 1)
    stop_speech = choose_sample(twenty_one_tts_folder, "10", 1)

    time.sleep(1)
    os.system("mpg321 %s --stereo" % ('"' + start_speech + '"'))

    # Winner/Starter 0 -> robot | 1 -> child
    winner = 0
    current_number = -1
    range_limit = 3
    random.seed(time.clock())
    # Choose first to start // 0 -> robot | 1 -> child
    first_start = random.randint(0, 1)
    print(first_start)

    time.sleep(1)
    os.system("mpg321 %s --stereo" % ('"' + os.path.join(twenty_one_tts_folder, "First Start", str(first_start) + ".mp3") + '"'))

    while True:
        if first_start:
            # Get answer
            current_number = process_answer(current_number, range_limit, wrong_speech, correct_speech, stt, model, vad_audio)
            if current_number == -1:
                time.sleep(1)
                os.system("mpg321 %s --stereo" % ('"' + stop_speech + '"'))
                return
            winner = 1
            # Generate a random integer N such that (current_number+1) <= N <= (current_number+range_limit)
            speech = random.choice(prequestion_speech)
            time.sleep(1)
            os.system("mpg321 %s --stereo" % ('"' + speech + '"'))
            current_number = generate_number(current_number, range_limit, numbers_speech, think_time_speech, think_time_end_speech)
            winner = 0
            print ("Current: ", current_number)
        else:
            # Generate a random integer N such that (current_number+1) <= N <= (current_number+range_limit)
            speech = random.choice(prequestion_speech)
            time.sleep(1)
            os.system("mpg321 %s --stereo" % ('"' + speech + '"'))
            current_number = generate_number(current_number, range_limit, numbers_speech, think_time_speech, think_time_end_speech)
            winner = 0
            # Get answer
            current_number = process_answer(current_number, range_limit, wrong_speech, correct_speech, stt, model, vad_audio)
            if current_number == -1:
                os.system("mpg321 %s --stereo" % ('"' + stop_speech + '"'))
                return
            winner = 1
            print ("Current: ", current_number)

        if current_number == 21:
            print("Winner is:", winner)
            if winner == 0:
                time.sleep(1)
                os.system("mpg321 %s --stereo" % ('"' + loser_speech + '"'))
            else:
                time.sleep(1)
                os.system("mpg321 %s --stereo" % ('"' + winner_speech + '"'))
            break

    return winner
