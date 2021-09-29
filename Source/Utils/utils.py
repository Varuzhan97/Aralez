import os
import time
import random
import subprocess
import yaml

#For csv generation and update during data collection
import csv
'''
#Movement
import RPi.GPIO as GPIO


# GPIO Mode (BOARD / BCM)
GPIO.setmode(GPIO.BCM)

# set GPIO Pins
GPIO_TRIGGER = 18
GPIO_ECHO = 15

# set GPIO direction (IN / OUT)
GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)
'''
def get_distance():
    # set Trigger to HIGH
    GPIO.output(GPIO_TRIGGER, True)

    # set Trigger after 0.01ms to LOW
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER, False)

    start_time = time.time()
    stop_time = time.time()

    while GPIO.input(GPIO_ECHO) == 0:
        start_time = time.time()

    while GPIO.input(GPIO_ECHO) == 1:
        stop_time = time.time()

    time_elapsed = stop_time - start_time
    # multiply with the sonic speed (34300 cm/s)
    # and divide by 2, because there and back
    return (time_elapsed * 34300) / 2


def detect_distance(expected_distance: int):
    try:
        if distance() < expected_distance:
            print("Distance less than % cm:  %.1f cm" % expected_distance)
            return False
    except KeyboardInterrupt:
        print("Measurement stopped by User")
        GPIO.cleanup()

#Load course checkpoint in YAML file
def load_course_checkpoint(course_language_id, yaml_file_data):
    checkpoint = int()
    if course_language_id == "0":
        checkpoint = yaml_file_data["Courses"]["Checkpoint English"]
    if course_language_id == "1":
        checkpoint = yaml_file_data["Courses"]["Checkpoint Russian"]
    return checkpoint

#Save course checkpoint in YAML file
def save_course_checkpoint(course_language_id, checkpoint, yaml_file_data, yaml_file):
    if course_language_id == "0":
        yaml_file_data["Courses"]["Checkpoint English"] = checkpoint
    if course_language_id == "1":
        yaml_file_data["Courses"]["Checkpoint Russian"] = checkpoint

    #Reset file pointer and clear YAML config file
    yaml_file.seek(0)
    yaml_file.truncate(0) #Need '0' when using r+
    #Rewrite YAML file content with modified language
    yaml.dump(yaml_file_data, yaml_file, default_flow_style=False, sort_keys=False)

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
