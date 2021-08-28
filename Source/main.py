import os
from Games.Capitals import capitals
from Games.Twenty_one import twenty_one
from STT import stt
from QA import qa
import yaml
import time
import random

#For disabling terminal logs
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

def set_language(stt_folder, current_language, language, current_resp, resp, model):
    if current_language != language:
        load_play_tts_clips(tts_folder, current_language, current_resp)
        #model, language = toggle_language(languages.get(language), languages)
        model = stt.preprocess(os.path.join(stt_folder, language))
        model = stt.load_scorer(model, model_scorer_path, "conversation.scorer")
    else:
        load_play_tts_clips(tts_folder, language, current_resp)
    current_language = language
    return model, current_language


#Function to load all tts clips from directory
def load_play_tts_clips(tts_folder, language, resp):
    for file in os.listdir(os.path.join(tts_folder, language, resp)):
        if file.endswith(".mp3"):
            all_files.append(os.path.join(tts_folder, language, resp, file))

    play = random.choice(all_files)
    #os.system("mpg321 %s --stereo" % play)
    os.system("mpg321 %s --stereo" % ('"' + play + '"'))

if __name__ == "__main__":
    main_dir = os.getcwd()

    #Load configurations for startup
    config_file_path = os.path.join(main_dir, "config.yaml")
    config_file =  open(config_file_path, 'r')
    main_config = yaml.full_load(config_file)

    languages = main_config["Languages"]

    language = main_config["Language"]
    stt_folder = main_config["STT"]["Model Folder"]
    stt_folder = os.path.join(main_dir, stt_folder)

    qa_folder = main_config["QA"]["Model Folder"]
    qa_folder = os.path.join(main_dir, qa_folder)

    capitals_questions_number = main_config["Games"]["Capitals"]["Questions Number"]

    capitals_data_folder = main_config["Games"]["Capitals"]["Data Folder"]
    capitals_data_folder = os.path.join(main_dir, capitals_data_folder)

    capitals_tts_folder = main_config["Games"]["Capitals"]["TTS Folder"]
    capitals_tts_folder = os.path.join(main_dir, capitals_tts_folder)

    twenty_one_tts_folder = main_config["Games"]["Twenty-one"]["TTS Folder"]
    twenty_one_tts_folder = os.path.join(main_dir, twenty_one_tts_folder)

    tts_folder = main_config["TTS"]["Clips Folder"]
    tts_folder = os.path.join(main_dir, tts_folder)

    #Preprocess voice activity detection and load STT model with conversation scorer
    model_scorer_path = os.path.join(stt_folder, language)
    model = stt.preprocess(model_scorer_path)
    model = stt.load_scorer(model, model_scorer_path, "conversation.scorer")

    # Start audio with VAD
    vad_audio = stt.VADAudio(aggressiveness = 3,
                         #device=ARGS.device,
                         input_rate=16000)
                         #file=ARGS.file)

    while True:
        speech = stt.listen_audio(model,vad_audio)
        print("STT result: %s" % speech)
        if speech != "":
            resp = qa.response(speech, os.path.join(qa_folder, language))
            #Response cases
            all_files = []
            if resp != -1:
                if resp == "14":
                    load_play_tts_clips(tts_folder, language, resp)
                    #Load capitals scorer
                    model = stt.load_scorer(model, model_scorer_path, "capitals.scorer")
                    capitals.capitals(capitals_questions_number, os.path.join(capitals_data_folder, language), os.path.join(capitals_tts_folder, language), stt, model, vad_audio)
                    model = stt.load_scorer(model, model_scorer_path, "conversation.scorer")
                    continue
                if resp == "15":
                    load_play_tts_clips(tts_folder, language, resp)
                    #Load capitals scorer
                    model = stt.load_scorer(model, model_scorer_path, "twenty_one.scorer")
                    twenty_one.twenty_one(os.path.join(twenty_one_tts_folder, language), stt, model, vad_audio)
                    model = stt.load_scorer(model, model_scorer_path, "conversation.scorer")
                    continue
                if resp == "18":
                    #Start to dance
                    os.system("mpg321 %s --stereo" % ('"' + "/home/varuzhan/Desktop/Aralez/Source/Actions/Dance/Music/0.mp3" + '"'))
                    continue
                #if resp == "20":
                    #Forward
                    #continue
                #if resp == "21":
                    #Back
                    #continue
                #if resp == "22":
                    #Left
                    #continue
                #if resp == "23":
                    #Right
                    #continue
                if resp == "27":
                    model, language = set_language(stt_folder, language, "Ru", resp, "28", model)
                    continue
                if resp == "28":
                    model, language = set_language(stt_folder, language, "En", resp, "27", model)
                    continue
                load_play_tts_clips(tts_folder, language, resp)
            else:
                print("Sorry, I didn't get what you said.")
