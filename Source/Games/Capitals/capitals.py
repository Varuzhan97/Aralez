import yaml
import random
import os
import time
#from STT.VAD import vad

def ask(questions, correct_speech, wrong_speech, data_file_yaml, stt, model, vad_audio):
    score = 0
    for question in questions:
        time.sleep(1)
        os.system("mpg321 %s --stereo" % ('"' + question + '"'))
        correct_answer = list()
        correct_answer.append(data_file_yaml.get(os.path.basename(question)[0:-4]))
        print("type:", correct_answer)
        answer = stt.listen_audio(model, vad_audio)
        correct_answer = [x.lower() for x in correct_answer]
        if (answer in correct_answer):
            speech = random.choice(correct_speech)
            time.sleep(1)
            os.system("mpg321 %s --stereo" % ('"' + speech + '"'))
            score += 1
        else:
            speech = random.choice(wrong_speech)
            time.sleep(1)
            os.system("mpg321 %s --stereo" % ('"' + speech + '"'))
    return score

def capitals(capitals_questions_number, capitals_data_folder, capitals_tts_folder, stt, model, vad_audio):
    data_file =  open(os.path.join(capitals_data_folder, "data.yaml"), 'r')
    data_file_yaml = yaml.full_load(data_file)

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
    score = ask(question_speech, correct_speech, wrong_speech, data_file_yaml, stt, model, vad_audio)
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
