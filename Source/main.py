import os
from Games.Capitals import capitals
from Games.Twenty_one import twenty_one
from STT import stt
from QA import qa
import yaml
import time
import random
import subprocess

from Actions.Dance import dance
from Actions.Movement import movement

#For disabling terminal logs
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

#Set new language ang change config in YAML file
def set_language(vad_audio, new_model_path, yaml_file_data, yaml_file):
    #new_model_path contains the name of the requested language
    requested_language = os.path.basename(new_model_path)
    #Set/load requested language model and scorer
    vad_audio.set_model(new_model_path, 'model.tflite')
    vad_audio.set_scorer(new_model_path, "conversation.scorer")
    yaml_file_data["Language"] = requested_language
    #Reset file pointer and clear YAML config file
    yaml_file.seek(0)
    yaml_file.truncate(0) #Need '0' when using r+
    #Rewrite YAML file content with modified language
    yaml.dump(yaml_file_data, yaml_file, default_flow_style=False, sort_keys=False)
    current_language = requested_language
    return current_language


#Function to load all tts clips from directory
def load_play_tts_clips(tts_folder, language, resp):
    all_files = []
    for file in os.listdir(os.path.join(tts_folder, language, resp)):
        if file.endswith(".mp3"):
            all_files.append(os.path.join(tts_folder, language, resp, file))

    play = random.choice(all_files)
    os.system("mpg321 %s --stereo" % ('"' + play + '"'))

if __name__ == "__main__":
    main_dir = os.getcwd()

    #Load configurations for startup
    config_file_path = os.path.join(main_dir, "config.yaml")
    config_file =  open(config_file_path, 'r+')
    main_config = yaml.safe_load(config_file)

    #Contains languages list and corresponding ID's
    languages = main_config["Languages"]

    #Get startup language ID
    language = main_config["Language"]
    #Get startup language name (En, Ru, etc.)
    #language = get_key(language, languages)
    #if(language == -1):
        #break

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

    conversation_tts_folder = main_config["Conversation TTS"]["Clips Folder"]
    conversation_tts_folder = os.path.join(main_dir, conversation_tts_folder)

    startup_tts_folder = main_config["Startup TTS"]["Clips Folder"]
    startup_tts_folder = os.path.join(main_dir, startup_tts_folder)

    dance_music_folder = main_config["Actions"]["Dance"]["Music Folder"]
    dance_music_folder = os.path.join(main_dir, dance_music_folder)

    #Preprocess voice activity detection and load STT model with conversation scorer
    model_path = os.path.join(stt_folder, language)

    # Start audio with VAD
    vad_audio = stt.VADAudio(aggressiveness = 3, input_rate=16000)
    vad_audio.set_model(model_path, 'model.tflite')
    vad_audio.set_scorer(model_path, 'conversation.scorer')

    #Play startup speech
    load_play_tts_clips(startup_tts_folder, language, "0")
    ####For test
    #Load capitals scorer
    #vad_audio.set_scorer(model_path, 'capitals.scorer')
    #capitals.capitals(capitals_questions_number, os.path.join(capitals_data_folder, language), os.path.join(capitals_tts_folder, language), stt, vad_audio)


    while True:
        speech = stt.listen_audio(vad_audio)
        print("STT result: %s" % speech)
        '''
        if speech != "":
            resp = str(qa.strings_to_id(speech, language))
            #Response cases
            all_files = []
            if resp != "-1":
                if resp == "14":
                    load_play_tts_clips(conversation_tts_folder, language, resp)
                    #Load capitals scorer
                    vad_audio.set_scorer(model_path, 'capitals.scorer')
                    capitals.capitals(capitals_questions_number, os.path.join(capitals_data_folder, language), os.path.join(capitals_tts_folder, language), stt, vad_audio)
                    vad_audio.set_scorer(model_path, 'conversation.scorer')
                    continue
                if resp == "15":
                    load_play_tts_clips(conversation_tts_folder, language, resp)
                    #Load capitals scorer
                    vad_audio.set_scorer(model_path, 'twenty_one.scorer')
                    twenty_one.twenty_one(os.path.join(twenty_one_tts_folder, language), stt, vad_audio)
                    vad_audio.set_scorer(model_path, 'conversation.scorer')
                    continue
                if resp == "18":
                    #Start to dance
                    os.system("mpg321 %s --stereo" % ('"' + "/home/varuzhan/Desktop/Aralez/Source/Actions/Dance/Music/0.mp3" + '"'))
                    continue
                if resp == "20":
                    #Forward
                    continue
                if resp == "21":
                    #Back
                    continue
                if resp == "22":
                    #Left
                    continue
                if resp == "23":
                    #Right
                    continue
                #if resp == "24":
                    #subprocess.call(["shutdown", "-h", "now"])
                if resp == "27":
                    load_play_tts_clips(conversation_tts_folder, language, resp)
                    continue
                if resp == "28":
                    load_play_tts_clips(conversation_tts_folder, language, resp)
                    #Toggle language ID
                    new_model_path = os.path.join(stt_folder, str(1 - int(language)))
                    language = set_language(vad_audio, new_model_path, main_config, config_file)
                    continue
                load_play_tts_clips(conversation_tts_folder, language, resp)
            else:
                load_play_tts_clips(conversation_tts_folder, language, resp)
            '''
    config_file.close()
