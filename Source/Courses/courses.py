import os
import yaml
from Utils import utils

def start_course(courses_tts_folder, courses_data_folder, vad_audio, stt, model_path, collection_folder = None):
    #Load YAML file that contains translation pairs with corresponding ID's
    data_file =  open(os.path.join(courses_data_folder, "data.yaml"), 'r')
    data_file_yaml = yaml.full_load(data_file)
    #Configure TTS speech audio clips paths
    #courses_tts_folder is a full path and contains language ID too
    numbers_course_prespeech = os.path.join(courses_tts_folder, "0")
    conversation_course_prespeech = os.path.join(courses_tts_folder, "2")
    numbers_speech = os.path.join(courses_tts_folder, "1")
    conversation_speech = os.path.join(courses_tts_folder, "3")
    repeat_speech = os.path.join(courses_tts_folder, "4")
    again_repeat_speech = os.path.join(courses_tts_folder, "5")
    excellent_speech = os.path.join(courses_tts_folder, "6")

    #Get the data. Each line index of data correspondes to the ID of .mp3 clip
    numbers_data = data_file_yaml.get("Numbers")
    conversation_data = data_file_yaml.get("Conversation")

    #Make list of keys of number data
    numbers_keys_list = list(numbers_data)
    #Make list of keys of conversation data
    conversation_keys_list = list(conversation_data)

    #Load numbers scorer
    vad_audio.set_scorer(model_path, 'twenty_one.scorer')

    utils.load_play_tts_clip(numbers_course_prespeech)

    for i in range(len(numbers_keys_list)):
        utils.play_tts_clip(os.path.join(numbers_speech, str(i) + ".mp3"))
        utils.load_play_tts_clip(repeat_speech)
        #Get answer line from numbers data dictionary
        while True:
            file_name = str()
            file_size = str()
            if collection_folder is not None:
                answer, file_name, file_size = stt.listen_audio(vad_audio, save_wav = True, save_wav_path = collection_folder)
            else:
                answer = stt.listen_audio(vad_audio)
            print(answer)
            if answer == '':
                #Remove saved wav file
                os.remove(file_name)
                continue
            if answer != '' and len(answer) > 0 and answer != numbers_data.get(numbers_keys_list[i]):
                #Remove saved wav file
                os.remove(file_name)
                utils.load_play_tts_clip(again_repeat_speech)
                utils.play_tts_clip(os.path.join(numbers_speech, str(i) + ".mp3"))
                continue
            else:
                if collection_folder is not None:
                    #Update collected data csv
                    utils.write_to_csv(file_name, file_size, answer, collection_folder)
                #Play speech
                utils.load_play_tts_clip(excellent_speech)
                break

    utils.load_play_tts_clip(conversation_course_prespeech)

    #Load conversation scorer
    vad_audio.set_scorer(model_path, 'conversation.scorer')

    for i in range(len(conversation_keys_list)):
        utils.play_tts_clip(os.path.join(conversation_speech, str(i) + ".mp3"))
        utils.load_play_tts_clip(repeat_speech)
        #Get answer line from numbers data dictionary
        while True:
            if collection_folder is not None:
                answer, file_name, file_size = stt.listen_audio(vad_audio, save_wav = True, save_wav_path = collection_folder)
            else:
                answer = stt.listen_audio(vad_audio)
            print(answer)
            if answer == '':
                #Remove saved wav file
                os.remove(file_name)
                continue
            if answer != '' and len(answer) > 0 and answer != conversation_data.get(conversation_keys_list[i]):
                #Remove saved wav file
                os.remove(file_name)
                utils.load_play_tts_clip(again_repeat_speech)
                utils.play_tts_clip(os.path.join(conversation_speech, str(i) + ".mp3"))
                continue
            else:
                if collection_folder is not None:
                    #Update collected data csv
                    utils.write_to_csv(file_name, file_size, answer, collection_folder)
                #Play speech
                utils.load_play_tts_clip(excellent_speech)
                break
