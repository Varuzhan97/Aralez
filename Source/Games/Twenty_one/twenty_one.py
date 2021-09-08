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

#Function to get player speech
def process_answer(current_number, range_limit, wrong_speech, correct_speech, stt, vad_audio, think_time_speech, think_time_end_speech):
    #Think time and ending speeches
    load_play_tts_clip(think_time_speech)
    #Timer for a 5 seconds think time
    time.sleep(5)
    load_play_tts_clip(think_time_end_speech)

    #Get and validate answer
    while True:
        answer = stt.listen_audio(vad_audio)
        if answer == '':
            continue
        if answer == 'stop' or answer == 'stop the game':
            return -1
        #if answer == 'one' or answer == 'two' or answer == 'three':
        answer_number = strings_to_numbers(answer)
        print("this is: ", answer_number)
        #If number is out if range listen again, else break
        if (answer_number < current_number+1) or (answer_number > current_number+range_limit):
            load_play_tts_clip(wrong_speech)
            continue
        break
    load_play_tts_clip(correct_speech)
    return answer_number

#Function to generate robot number
def generate_number(current_number, range_limit, numbers_speech):
    #If the next number can be in range of [19,21] then return 21
    if (current_number+range_limit) >= 21:
        generated_number = 21
        load_play_tts_clip(numbers_speech, specific = str(generated_number))
        return generated_number
    else:
        generated_number = random.randint(current_number+1, current_number+range_limit)
        print("Range: ", current_number+1, current_number+range_limit)
        print("Number: ", generated_number)
        print("aaaaaaaaaaaaa: ", numbers_speech)
        load_play_tts_clip(numbers_speech, specific = str(generated_number))
        return generated_number

def player_answer(current_number, range_limit, wrong_speech, correct_speech, winner_speech, stt, vad_audio, think_time_speech, think_time_end_speech):
    print("Range: ", current_number+1, current_number+range_limit)
    # Get answer with VAD
    current_number = process_answer(current_number, range_limit, wrong_speech, correct_speech, stt, vad_audio, think_time_speech, think_time_end_speech)
    #Check for STOP SIGNAL
    if current_number == -1:
        load_play_tts_clip(stop_speech)
        return -1
    #Check for WINNER SIGNAL
    if current_number == 21:
        load_play_tts_clip(winner_speech)
        return 1
    return current_number

def robot_answer(current_number, range_limit, prequestion_speech, numbers_speech, loser_speech):
    # Generate a random integer N such that (current_number+1) <= N <= (current_number+range_limit)
    load_play_tts_clip(prequestion_speech)
    current_number = generate_number(current_number, range_limit, numbers_speech)
    #Check for WINNER SIGNAL
    if current_number == 21:
        load_play_tts_clip(loser_speech)
        return 1
    print ("Current: ", current_number)
    return current_number

def twenty_one(twenty_one_tts_folder, stt, vad_audio):
    #Configure TTS speech audio clips paths
    #twenty_one_tts_folder is a full path and contains language ID too
    first_start_speech = os.path.join(twenty_one_tts_folder, "1")
    prequestion_speech = os.path.join(twenty_one_tts_folder, "2")
    numbers_speech = os.path.join(twenty_one_tts_folder, "3")
    correct_speech = os.path.join(twenty_one_tts_folder, "4")
    wrong_speech = os.path.join(twenty_one_tts_folder, "5")
    winner_speech = os.path.join(twenty_one_tts_folder, "6")
    loser_speech = os.path.join(twenty_one_tts_folder, "7")
    think_time_speech = os.path.join(twenty_one_tts_folder, "8")
    think_time_end_speech = os.path.join(twenty_one_tts_folder, "9")
    stop_speech = os.path.join(twenty_one_tts_folder, "10")

    #Game starts from -1
    current_number = -1
    range_limit = 3
    random.seed(time.clock())
    #Choose first to start // 0 -> robot | 1 -> child
    first_start = random.randint(0, 1)
    print("sssssssssssssssssssssssss", first_start, first_start_speech, str(first_start))

    load_play_tts_clip(first_start_speech, specific = str(first_start))
    while True:
        #If starts child
        if first_start:
            current_number = player_answer(current_number, range_limit, wrong_speech, correct_speech, winner_speech, stt, vad_audio, think_time_speech, think_time_end_speech)
            #If returned STOP SIGNAL or WINNER SIGNAL
            if current_number == -1 or current_number == 1:
                return
            current_number = robot_answer(current_number, range_limit, prequestion_speech, numbers_speech, loser_speech)
            #If returned WINNER SIGNAL
            if current_number == 1:
                return
        else:
            current_number = robot_answer(current_number, range_limit, prequestion_speech, numbers_speech, loser_speech)
            #If returned WINNER SIGNAL
            if current_number == 1:
                return
            current_number = player_answer(current_number, range_limit, wrong_speech, correct_speech, winner_speech, stt, vad_audio, think_time_speech, think_time_end_speech)
            #If returned STOP SIGNAL or WINNER SIGNAL
            if current_number == -1 or current_number == 1:
                return
    return 0
