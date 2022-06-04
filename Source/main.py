import os
import yaml
import subprocess
from Games.Capitals import capitals
from Games.Twenty_one import twenty_one
from STT import stt
from QA import qa
#from Music import music
from Courses import courses
from Utils import utils#, lights

if __name__ == "__main__":
    #Set current directory
    main_dir = os.getcwd()
    #main_dir = "/home/pi/Aralez/Source"

    #Load configurations for startup
    config_file_path = os.path.join(main_dir, "config.yaml")
    config_file =  open(config_file_path, 'r+')
    main_config = yaml.safe_load(config_file)

    #Contains languages list and corresponding ID's
    languages = main_config["Languages"]

    #Get startup language ID (En: 0, Ru: 1)
    language = str(main_config["Language"])

    stt_folder = main_config["STT"]["Model Folder"]
    stt_folder = os.path.join(main_dir, stt_folder)

    qa_data_folder = main_config["QA"]["Data Folder"]
    qa_data_folder = os.path.join(main_dir, qa_data_folder)

    capitals_questions_number = main_config["Games"]["Capitals"]["Questions Number"]

    capitals_data_folder = main_config["Games"]["Capitals"]["Data Folder"]
    capitals_data_folder = os.path.join(main_dir, capitals_data_folder)

    capitals_tts_folder = main_config["Games"]["Capitals"]["TTS Folder"]
    capitals_tts_folder = os.path.join(main_dir, capitals_tts_folder)

    twenty_one_tts_folder = main_config["Games"]["Twenty-one"]["TTS Folder"]
    twenty_one_tts_folder = os.path.join(main_dir, twenty_one_tts_folder)

    riddles_data_folder = main_config["Games"]["Riddles"]["Data Folder"]
    riddles_data_folder = os.path.join(main_dir, riddles_data_folder)

    riddles_tts_folder = main_config["Games"]["Riddles"]["TTS Folder"]
    riddles_tts_folder = os.path.join(main_dir, riddles_tts_folder)

    conversation_tts_folder = main_config["Conversation"]["TTS Folder"]
    conversation_tts_folder = os.path.join(main_dir, conversation_tts_folder)

    startup_tts_folder = main_config["Startup"]["TTS Folder"]
    startup_tts_folder = os.path.join(main_dir, startup_tts_folder)

    song_folder = main_config["Music"]["Song Folder"]
    song_folder = os.path.join(main_dir, song_folder)

    lullaby_folder = main_config["Music"]["Lullaby Folder"]
    lullaby_folder = os.path.join(main_dir, lullaby_folder)

    courses_tts_folder =  main_config["Courses"]["TTS Folder"]
    courses_tts_folder = os.path.join(main_dir, courses_tts_folder)

    courses_data_folder =  main_config["Courses"]["Data Folder"]
    courses_data_folder = os.path.join(main_dir, courses_data_folder)

    #Boolean for enable/disable wav savings during courses
    courses_save_data =  main_config["Courses"]["Save Data"]

    courses_collection_folder =  main_config["Courses"]["Saved Data Folder"]
    courses_collection_folder = os.path.join(main_dir, courses_collection_folder)

    #Preprocess voice activity detection and load STT model with conversation scorer
    model_path = os.path.join(stt_folder, language)

    # Start audio with VAD
    vad_audio = stt.VADAudio(aggressiveness = 3, input_rate=16000)

    vad_audio.set_model(model_path, 'model.tflite')
    vad_audio.set_scorer(model_path, 'conversation.scorer')

    #Play startup speech
    utils.load_play_tts_clip(os.path.join(startup_tts_folder, language, "0"))

    #Declare Music class object
    #self_music = music.Music()

    #Declare Lights class object
    #self_lights = lights.Lights()
    #self_lights.set_led_color(0)

    while True:
        speech = vad_audio.listen_audio()
        print("STT result: %s" % speech)
        if speech != "":
            resp = str(qa.get_answer(speech, os.path.join(qa_data_folder, language)))
            #Response cases
            all_files = []
            if resp != "-1":
                if resp == "15":
                    utils.load_play_tts_clip(os.path.join(conversation_tts_folder, language, resp))
                    #Load capitals scorer
                    vad_audio.set_scorer(model_path, 'capitals.scorer')
                    capitals.capitals(capitals_questions_number, os.path.join(capitals_data_folder, language), os.path.join(capitals_tts_folder, language), vad_audio)
                    vad_audio.set_scorer(model_path, 'conversation.scorer')
                    continue
                if resp == "16":
                    utils.load_play_tts_clip(os.path.join(conversation_tts_folder, language, resp))
                    #Load twenty one scorer
                    vad_audio.set_scorer(model_path, 'twenty_one.scorer')
                    twenty_one.twenty_one(os.path.join(twenty_one_tts_folder, language), vad_audio)
                    vad_audio.set_scorer(model_path, 'conversation.scorer')
                    continue
                if resp == "19":
                    #Play song
                    self_music.play_music(song_folder, self_lights, choice = 0)
                    continue
                if resp == "21":
                    #Forward
                    #self_move.forward()
                    continue
                if resp == "22":
                    #Back
                    #self_move.backward()
                    continue
                if resp == "23":
                    #Left
                    #self_move.left()
                    continue
                if resp == "24":
                    #Right
                    #self_move.right()
                    continue
                if resp == "25":
                    #Turn around
                    #self_move.turn_back()
                    continue
                if resp == "26":
                    #Change resp ID
                    #Play lullaby
                    self_music.play_music(lullaby_folder, self_lights, choice = 1)
                    subprocess.call(["shutdown", "-h", "now"])
                if resp == "29":
                    #Prevent same language course
                    if language == "0" and ("english" in speech):
                        continue
                    if language == "1" and ("русском" in speech):
                        continue
                    native_language_id, course_language_id = language, str(1 - int(language))
                    #Toggle language ID
                    new_model_path = os.path.join(stt_folder, course_language_id)
                    #Load curse language STT model
                    utils.change_language(vad_audio, new_model_path, change_config = False)
                    #Start the course
                    #Check for data saving
                    if courses_save_data:
                        #Make data collection path for language
                        collection_folder = os.path.join(courses_collection_folder, course_language_id)
                        courses.start_course(os.path.join(courses_tts_folder, native_language_id), os.path.join(courses_data_folder, native_language_id), vad_audio, new_model_path, main_config, config_file, collection_folder)
                    else:
                        courses.start_course(os.path.join(courses_tts_folder, native_language_id), os.path.join(courses_data_folder, native_language_id), vad_audio, new_model_path, main_config, config_file)
                    #Restore language back
                    new_model_path = os.path.join(stt_folder, native_language_id)
                    utils.change_language(vad_audio, new_model_path, change_config = False)
                    continue
                if resp == "31":
                    utils.load_play_tts_clip(os.path.join(conversation_tts_folder, language, resp))
                    continue
                if resp == "32":
                    utils.load_play_tts_clip(os.path.join(conversation_tts_folder, language, resp))
                    #Toggle language ID
                    new_model_path = os.path.join(stt_folder, str(1 - int(language)))
                    language = utils.change_language(vad_audio, new_model_path, main_config, config_file)
                    continue
                #Configure scorer for riddles
                if resp == "":
                    utils.load_play_tts_clip(os.path.join(conversation_tts_folder, language, resp))
                    #Load capitals scorer
                    vad_audio.set_scorer(model_path, 'riddles.scorer')
                    capitals.capitals(os.path.join(riddles_data_folder, language), os.path.join(riddles_tts_folder, language), vad_audio)
                    vad_audio.set_scorer(model_path, 'conversation.scorer')
                    continue
                ###
                utils.load_play_tts_clip(os.path.join(conversation_tts_folder, language, resp))
            else:
                utils.load_play_tts_clip(os.path.join(conversation_tts_folder, language, resp))
    config_file.close()
