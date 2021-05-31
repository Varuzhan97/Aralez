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

def process_answer(current_number, range_limit):
    while True:
        #answer = vad.listen_audio(model)
        answer = input('---| Enter Number ---> ')
        #remove spaces and make lowercase
        #answer = answer.replace(" ", "")
        answer_number = strings_to_numbers(answer)
        print("this is: ", answer_number)

        if (answer_number < current_number+1) or (answer_number > current_number+range_limit):
            print('---| Enter again |---', flush=True)
            #os.system("mpg321 %s --stereo" % ('"' + os.path.join("/home/varuzhan/Desktop/***PROJECT***/Oberon/TTS/Conversation", language, resp) + '"'))
            continue
        break
    return answer_number

def generate_number(current_number, range_limit):
    generated_number = random.randint(current_number+1, current_number+range_limit)
    print("Range: ", current_number+1, current_number+range_limit)
    print("Number: ", generated_number)
    return generated_number

#def ask(vad, model):
def ask():
    # 0 -> robot | 1 -> child
    winner = 0
    current_number = -1
    range_limit = 3

    random.seed(time.clock())

    # Choose first to start // 0 -> robot | 1 -> child
    first_start = random.randint(0, 1)
    print(first_start)

    while True:
        if first_start:
            # Get answer
            current_number = process_answer(current_number, range_limit)
            winner = 1
            # Generate a random integer N such that (current_number+1) <= N <= (current_number+range_limit)
            current_number = generate_number(current_number, range_limit)
            winner = 0
            print ("Current: ", current_number)
        else:
            # Generate a random integer N such that (current_number+1) <= N <= (current_number+range_limit)
            current_number = generate_number(current_number, range_limit)
            winner = 0
            # Get answer
            current_number = process_answer(current_number, range_limit)
            winner = 1
            print ("Current: ", current_number)

        if current_number == 21:
            print("Winner is:", winner)
            break

    return winner

if __name__ == "__main__":
    ask()

    '''
def twenty_one(capitals_questions_number, capitals_data_folder, capitals_tts_folder, vad, model):
    start_speech = random.choice(os.listdir(os.path.join(capitals_tts_folder, "Start")))
    start_speech = os.path.join(capitals_tts_folder, "Start", start_speech)

    prequestion_speech = random.choice(os.listdir(os.path.join(capitals_tts_folder, "Prequestion")))
    prequestion_speech = os.path.join(capitals_tts_folder, "Prequestion", prequestion_speech)

    temp_question_speech = random.sample(os.listdir(os.path.join(capitals_tts_folder, "Question")), capitals_questions_number)
    question_speech = []
    for speech in temp_question_speech:
        question_speech.append(os.path.join(capitals_tts_folder, "Question", speech))

    temp_score_speech = os.listdir(os.path.join(capitals_tts_folder, "Score"))
    score_speech = []
    for speech in temp_score_speech:
        score_speech.append(os.path.join(capitals_tts_folder, "Score", speech))

    temp_correct_speech = os.listdir(os.path.join(capitals_tts_folder, "Correct"))
    correct_speech = []
    for speech in temp_correct_speech:
        correct_speech.append(os.path.join(capitals_tts_folder, "Correct", speech))

    temp_wrong_speech = os.listdir(os.path.join(capitals_tts_folder, "Wrong"))
    wrong_speech = []
    for speech in temp_wrong_speech:
        wrong_speech.append(os.path.join(capitals_tts_folder, "Wrong", speech))

    low_result_speech = random.choice(os.listdir(os.path.join(capitals_tts_folder, "Low Result")))
    low_result_speech = os.path.join(capitals_tts_folder, low_result_speech)

    #middle_result_speech = random.choice(os.listdir(os.path.join(capitals_tts_folder, "Middle Result")))
    #middle_result_speech = os.path.join(capitals_tts_folder, middle_result_speech)

    high_result_speech = random.choice(os.listdir(os.path.join(capitals_tts_folder, "High Result")))
    high_result_speech = os.path.join(capitals_tts_folder, high_result_speech)

    #perfect_result_speech = random.choice(os.listdir(os.path.join(capitals_tts_folder, "Perfect Result")))
    #perfect_result_speech = os.path.join(capitals_tts_folder, perfect_result_speech)

    time.sleep(1)
    os.system("mpg321 %s --stereo" % ('"' + start_speech + '"'))
    time.sleep(1)
    os.system("mpg321 %s --stereo" % ('"' + prequestion_speech + '"'))
    score = ask(question_speech, correct_speech, wrong_speech, data_file_yaml, vad, model)
    print("Score:", score)
    if 0 <= score <= 2:
        time.sleep(1)
        os.system("mpg321 %s --stereo" % ('"' + low_result_speech + '"'))
    if 3 <= score <= 5:
        time.sleep(1)
        os.system("mpg321 %s --stereo" % ('"' + middle_result_speech + '"'))
    if 6 <= score <= 8:
        time.sleep(1)
        os.system("mpg321 %s --stereo" % ('"' + high_result_speech + '"'))
    if score == 0:
        time.sleep(1)
        os.system("mpg321 %s --stereo" % ('"' + high_result_speech + '"'))
    '''
