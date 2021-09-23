import os
import time
import random
import subprocess
import yaml

#For csv generation and update during data collection
import csv

#Set new language ang change configuration in YAML file
def change_language(vad_audio, new_model_path, yaml_file_data = None, yaml_file = None, change_config = True):
    #new_model_path contains the name of the requested language
    requested_language = os.path.basename(new_model_path)
    #Set/load requested language model and scorer
    vad_audio.set_model(new_model_path, 'model.tflite')
    vad_audio.set_scorer(new_model_path, "conversation.scorer")

    if change_config:
        yaml_file_data["Language"] = int(requested_language)
        #Reset file pointer and clear YAML config file
        yaml_file.seek(0)
        yaml_file.truncate(0) #Need '0' when using r+
        #Rewrite YAML file content with modified language
        yaml.dump(yaml_file_data, yaml_file, default_flow_style=False, sort_keys=False)
    current_language = requested_language
    return current_language

#Function to load and play all or one random or a specific tts clip from directory
def load_play_tts_clip(tts_folder, specific = None, stop_time = 1):
    #Timer for a short stop befor speech
    time.sleep(int(stop_time))
    if specific is not None:
        play = os.path.join(tts_folder, specific + ".mp3")
        #os.system("mpg321 %s --stereo" % ('"' + play + '"'))
        p = subprocess.Popen(["mpg321", play, "--stereo"])
        p.wait()
    else:
        all_files = []
        for file in os.listdir(tts_folder):
            if file.endswith(".mp3"):
                all_files.append(os.path.join(tts_folder, file))
        play = random.choice(all_files)
        #os.system("mpg321 %s --stereo" % ('"' + play + '"'))
        p = subprocess.Popen(["mpg321", play, "--stereo"])
        p.wait()

#Function to play a clip
def play_tts_clip(clip_path, stop_time = 1):
    #Timer for a short stop befor speech
    time.sleep(int(stop_time))
    #os.system("mpg321 %s --stereo" % ('"' + clip_path + '"'))
    p = subprocess.Popen(["mpg321", clip_path, "--stereo"])
    p.wait()

def write_to_csv(file_name, file_size, transcription, output_folder):
    #csv_row = []
    #csv_row.append([os.path.basename(file_name), str(file_size), transcription])
    print("hhhhhhhhhhhhhaaaa: ", output_folder)

    validated_file_path = os.path.join(output_folder, 'validated.csv')

    if os.path.isfile(validated_file_path):
        with open(validated_file_path, 'a') as csvfile:
            csvwriter = csv.writer(csvfile, delimiter = ',')
            csvwriter.writerow([os.path.basename(file_name), str(file_size), transcription])
    else:
        csv_header = ['wav_filename','wav_filesize','transcript']
        with open(validated_file_path, 'w') as csvfile:
            csvwriter = csv.writer(csvfile, delimiter = ',')
            csvwriter.writerow(csv_header)
            csvwriter.writerow([os.path.basename(file_name), str(file_size), transcription])

    return validated_file_path
