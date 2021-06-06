import yaml
import random
import os
import time
import random
#from STT.VAD import vad

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

    # get() method of dictionary data type returns
    # value of passed argument if it is present
    # in dictionary otherwise second argument will
    # be assigned as default value of passed argument
    return switcher.get(argument, -1)

def process_answer(current_number, range_limit, wrong_speech, correct_speech, stt, model, vad_audio):
    while True:
        #answer = vad.listen_audio(model)
        #answer = input('---| Enter Number ---> ')
        answer = stt.listen_audio(model, vad_audio)
        #remove spaces and make lowercase
        #answer = answer.replace(" ", "")
        answer_number = strings_to_numbers(answer)
        print("this is: ", answer_number)

        if (answer_number < current_number+1) or (answer_number > current_number+range_limit):
            time.sleep(1)
            speech = random.choice(wrong_speech)
            os.system("mpg321 %s --stereo" % ('"' + speech + '"'))
            print('---| Enter again |---', flush=True)
            #os.system("mpg321 %s --stereo" % ('"' + os.path.join("/home/varuzhan/Desktop/***PROJECT***/Oberon/TTS/Conversation", language, resp) + '"'))
            continue
        break
    time.sleep(1)
    speech = random.choice(correct_speech)
    os.system("mpg321 %s --stereo" % ('"' + speech + '"'))
    return answer_number

def generate_number(current_number, range_limit, numbers_speech):
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
        return generated_number

def twenty_one(twenty_one_tts_folder, stt, model, vad_audio):
    intro_speech = os.path.join(twenty_one_tts_folder, "Intro", "intro.mp3")

    first_start_speech = os.path.join(twenty_one_tts_folder, "First Start")

    temp_prequestion_speech = os.listdir(os.path.join(twenty_one_tts_folder, "Prequestion"))
    prequestion_speech = []
    for speech in temp_prequestion_speech:
        prequestion_speech.append(os.path.join(twenty_one_tts_folder, "Prequestion", speech))


    numbers_speech = os.path.join(twenty_one_tts_folder, "Numbers")

    temp_correct_speech = os.listdir(os.path.join(twenty_one_tts_folder, "Correct"))
    correct_speech = []
    for speech in temp_correct_speech:
        correct_speech.append(os.path.join(twenty_one_tts_folder, "Correct", speech))

    temp_wrong_speech = os.listdir(os.path.join(twenty_one_tts_folder, "Wrong"))
    wrong_speech = []
    for speech in temp_wrong_speech:
        wrong_speech.append(os.path.join(twenty_one_tts_folder, "Wrong", speech))

    winner_speech = random.choice(os.listdir(os.path.join(twenty_one_tts_folder, "Winner")))
    winner_speech = os.path.join(twenty_one_tts_folder, winner_speech)

    loser_speech = random.choice(os.listdir(os.path.join(twenty_one_tts_folder, "Loser")))
    loser_speech = os.path.join(twenty_one_tts_folder, loser_speech)

    time.sleep(1)
    #os.system("mpg321 %s --stereo" % ('"' + intro_speech + '"'))

    #################################################################################################
    # 0 -> robot | 1 -> child
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
            winner = 1
            # Generate a random integer N such that (current_number+1) <= N <= (current_number+range_limit)
            speech = random.choice(prequestion_speech)
            time.sleep(1)
            os.system("mpg321 %s --stereo" % ('"' + speech + '"'))
            current_number = generate_number(current_number, range_limit, numbers_speech)
            winner = 0
            print ("Current: ", current_number)
        else:
            # Generate a random integer N such that (current_number+1) <= N <= (current_number+range_limit)
            speech = random.choice(prequestion_speech)
            time.sleep(1)
            os.system("mpg321 %s --stereo" % ('"' + speech + '"'))
            current_number = generate_number(current_number, range_limit, numbers_speech)
            winner = 0
            # Get answer
            current_number = process_answer(current_number, range_limit, wrong_speech, correct_speech, stt, model, vad_audio)
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
