import os
import sys
import time
import utils
from gtts import gTTS
from datetime import datetime

def g_tts(transcript, language, output_folder, index):
    tts = gTTS(text=transcript, lang=language)
    #tts = gTTS(text=transcript, lang=language, slow = True)
    
    #Take first 3 characters of transcript for the file name
    file = os.path.join(output_folder, transcript[0:3] + '.mp3')
    tts.save(file)
    return file

def generate_clean_db(language, batch_size, sleep_time, parameters):
    lines = []
    clips_output_path = ''
    index = 0
    if parameters.checkpoint_path is not None:
        if not os.path.isdir(parameters.checkpoint_path):
            print ('Checkpoint Path Not Exist.')
            sys.exit()
        print('Loading Checkpoint.')
        clips_output_path = os.path.join(parameters.checkpoint_path, 'clips')
        index, lines = utils.load_checkpoint(parameters.checkpoint_path)
    else:
        if (not os.path.isdir(parameters.input_path)) and (not os.path.isfile(parameters.input_path)):
            print ('Input Text File/Folder Not Exist.')
            sys.exit()
        if not os.path.isdir(parameters.output_path):
            print ('Output Path Not Exist.')
            sys.exit()
        now = datetime.now().strftime('%Y-%m-%d*%H-%M-%S')
        clips_output_path = os.path.join(parameters.output_path, 'corpus-' + now, 'clips')
        os.makedirs(clips_output_path)
        all_files = []
        if os.path.isfile(parameters.input_path):
            print('Input Is A Text File.')
            all_files.append(parameters.input_path)
        for file in all_files:
            current_file = open(file, 'r')
            for line in current_file:
                lines.append(line.strip())
        utils.create_checkpoint(os.path.split(clips_output_path)[0], lines, all_files)
    print('Converting Text To Speech And Generating Dataset.')
    print('Dataset Path: %s.' % os.path.split(clips_output_path)[0])
    for line in lines[index:]:
        pair = []
        current_file = g_tts(line, language, clips_output_path, index)
        current_file_size = os.path.getsize(current_file)
        print('Processing Item: %d/%d, Type: Normal.' % (index+1, len(lines)))
        size = os.path.getsize(current_file)
        pair.append([os.path.basename(current_file), str(size), line.strip().lower()])
        utils.save_checkpoint(os.path.split(clips_output_path)[0], pair, index)
        index += 1
        if index%batch_size==0:
            print('Sleep (%d Seconds).' % sleep_time)
            time.sleep(sleep_time)
    return clips_output_path
