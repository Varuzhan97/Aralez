import yaml
import random
import os
import time
from Utils import utils

#Function to get player speech
def process_answer(current_number, range_limit, wrong_speech, correct_speech, vad_audio, think_time_speech, think_time_end_speech):
    #Think time and ending speeches
    utils.load_play_tts_clip(think_time_speech)
    #Timer for a 5 seconds think time
    #After 5 seconds inform
    utils.load_play_tts_clip(tts_folder = think_time_end_speech, stop_time = 5)

    #Get and validate answer
    while True:
        answer = vad_audio.listen_audio()
        if answer == '':
            continue
        if answer == 'stop' or answer == 'stop the game':
            return -1
        #if answer == 'one' or answer == 'two' or answer == 'three':
        answer_number = utils.strings_to_numbers(answer)
        #If number is out if range listen again, else break
        if (answer_number < current_number+1) or (answer_number > current_number+range_limit):
            utils.load_play_tts_clip(wrong_speech)
            continue
        break
    utils.load_play_tts_clip(correct_speech)
    return answer_number

#Function to generate robot number
def generate_number(current_number, range_limit, numbers_speech):
    #If the next number can be in range of [19,21] then return 21
    if (current_number+range_limit) >= 21:
        generated_number = 21
        utils.load_play_tts_clip(numbers_speech, specific = str(generated_number))
        return generated_number
    else:
        generated_number = random.randint(current_number+1, current_number+range_limit)
        utils.load_play_tts_clip(numbers_speech, specific = str(generated_number))
        return generated_number

def player_answer(current_number, range_limit, wrong_speech, correct_speech, winner_speech, stop_speech, vad_audio, think_time_speech, think_time_end_speech):
    # Get answer with VAD
    current_number = process_answer(current_number, range_limit, wrong_speech, correct_speech, vad_audio, think_time_speech, think_time_end_speech)
    #Check for STOP SIGNAL
    if current_number == -1:
        utils.load_play_tts_clip(stop_speech)
        return -1
    #Check for WINNER SIGNAL
    if current_number == 21:
        utils.load_play_tts_clip(winner_speech)
        return 1
    return current_number

def robot_answer(current_number, range_limit, prequestion_speech, numbers_speech, loser_speech):
    # Generate a random integer N such that (current_number+1) <= N <= (current_number+range_limit)
    utils.load_play_tts_clip(prequestion_speech)
    current_number = generate_number(current_number, range_limit, numbers_speech)
    #Check for WINNER SIGNAL
    if current_number == 21:
        utils.load_play_tts_clip(loser_speech)
        return 1
    return current_number

def twenty_one(twenty_one_tts_folder, vad_audio):
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
    random.seed(time.process_time())
    #Choose first to start // 0 -> robot | 1 -> child
    first_start = random.randint(0, 1)

    utils.load_play_tts_clip(first_start_speech, specific = str(first_start))
    while True:
        #If starts child
        if first_start:
            current_number = player_answer(current_number, range_limit, wrong_speech, correct_speech, winner_speech, stop_speech, vad_audio, think_time_speech, think_time_end_speech)
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
            current_number = player_answer(current_number, range_limit, wrong_speech, correct_speech, winner_speech, stop_speech, vad_audio, think_time_speech, think_time_end_speech)
            #If returned STOP SIGNAL or WINNER SIGNAL
            if current_number == -1 or current_number == 1:
                return
    return 0
