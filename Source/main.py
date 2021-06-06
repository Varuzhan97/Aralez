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

    twenty_one_tts_folder = main_config["Games"]["Twenty-one"]["TTS Folder"]
    twenty_one_tts_folder = os.path.join(main_dir, twenty_one_tts_folder)

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
            #Response cases
            all_files = []
            if resp != "Sorry, I didn't get what you said.":
                if resp == 26:
                    for file in os.listdir(os.path.join('/home/varuzhan/Desktop/Aralez/Source/TTS/Conversation/En', resp)):
                        if file.endswith(".mp3"):
                            all_files.append(os.path.join('/home/varuzhan/Desktop/Aralez/Source/TTS/Conversation/En', resp, file))

                    play = random.choice(all_files)
                    #os.system("mpg321 %s --stereo" % ('"' + os.path.join("/home/varuzhan/Desktop/***PROJECT***/Oberon/TTS/Conversation", language, resp) + '"'))
                    os.system("mpg321 %s --stereo" % play)

                    model, language = toggle_language(languages.get(language), languages)
                    continue
                #if resp == "18":
                    #Start to dance
                    #continue
                if resp == "13":
                    for file in os.listdir(os.path.join('/home/varuzhan/Desktop/Aralez/Source/TTS/Conversation/En', resp)):
                        if file.endswith(".mp3"):
                            all_files.append(os.path.join('/home/varuzhan/Desktop/Aralez/Source/TTS/Conversation/En', resp, file))

                    play = random.choice(all_files)
                    os.system("mpg321 %s --stereo" % play)
                    capitals.capitals(capitals_questions_number, os.path.join(capitals_data_folder, language), os.path.join(capitals_tts_folder, language), stt, model, vad_audio)
                    continue
                if resp == "15":
                    for file in os.listdir(os.path.join('/home/varuzhan/Desktop/Aralez/Source/TTS/Conversation/En', resp)):
                        if file.endswith(".mp3"):
                            all_files.append(os.path.join('/home/varuzhan/Desktop/Aralez/Source/TTS/Conversation/En', resp, file))

                    play = random.choice(all_files)
                    os.system("mpg321 %s --stereo" % play)
                    twenty_one.twenty_one(os.path.join(twenty_one_tts_folder, language), stt, model, vad_audio)
                    continue
                #if resp == "27":
                    #Check current language. If it is RU play inform speech, else change to RU and play change speech
                    #continue
                #if resp == "28":
                    #Check current language. If it is EN play inform speech, else change to EN and play change speech
                    #continue
                for file in os.listdir(os.path.join('/home/varuzhan/Desktop/Aralez/Source/TTS/Conversation/En', resp)):
                    if file.endswith(".mp3"):
                        all_files.append(os.path.join('/home/varuzhan/Desktop/Aralez/Source/TTS/Conversation/En', resp, file))

                play = random.choice(all_files)
                #os.system("mpg321 %s --stereo" % ('"' + os.path.join("/home/varuzhan/Desktop/***PROJECT***/Oberon/TTS/Conversation", language, resp) + '"'))
                os.system("mpg321 %s --stereo" % play)
            else:
                print("Sorry, I didn't get what you said.")
