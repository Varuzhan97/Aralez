import os
from Games.Capitals import capitals
from STT import stt
from QA import qa
import yaml
import time
import random

#For disabling terminal logs
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

#Functions to toggle language
def get_key(val, input_dict):
    for key, value in input_dict.items():
         if val == value:
             return key

def toggle_language(value, languages):
    new_language = get_key(1-value, languages)
    model = stt.preprocess(os.path.join(stt_folder, new_language))
    return model, new_language

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

    #Preprocess voice activity detection and load STT model
    model = stt.preprocess(os.path.join(stt_folder, language))

    # Start audio with VAD
    vad_audio = stt.VADAudio(aggressiveness = 3,
                         #device=ARGS.device,
                         input_rate=16000)
                         #file=ARGS.file)

    while True:
        speech = stt.listen_audio(model,vad_audio)
        print("STT result: %s" % speech)
        if speech != "":
            resp, context = qa.response(speech, os.path.join(qa_folder, language))
            print("Response: %s, Context: %s" % (resp, context))
            #Response cases
            all_files = []
            if resp != "Sorry, I didn't get what you said.":
                for file in os.listdir(os.path.join('/home/varuzhan/Desktop/Aralez/Source/TTS/Conversation/En', resp)):
                    if file.endswith(".mp3"):
                        all_files.append(os.path.join('/home/varuzhan/Desktop/Aralez/Source/TTS/Conversation/En', resp, file))
                play = random.choice(all_files)
                #os.system("mpg321 %s --stereo" % ('"' + os.path.join("/home/varuzhan/Desktop/***PROJECT***/Oberon/TTS/Conversation", language, resp) + '"'))
                os.system("mpg321 %s --stereo" % play)
            else:
                print("Sorry, I didn't get what you said.")
            #if context == 'En': capitals.capitals(capitals_questions_number, os.path.join(capitals_data_folder, language), os.path.join(capitals_tts_folder, language), stt, model)
            #if context=='En' or context=='Ru':
                #if context != language:
                    #model, language = toggle_language(languages.get(language), languages, main_config)
            #if context == 'En': model, language = toggle_language(languages.get(language), languages)

            #if context == 'Ru':
                #model, language = toggle_language(languages.get(language), languages)

            #if context == 'Capitals': capitals.capitals(capitals_questions_number, capitals_data_file, capitals_tts_folder, language)
            #if context == 'Capitals': capitals.capitals(main_dir, language)
