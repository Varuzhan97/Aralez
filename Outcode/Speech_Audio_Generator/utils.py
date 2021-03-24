import random
import os

def load_checkpoint(checkpoint_path):
    checkpoint_text_file = os.path.join(checkpoint_path, 'checkpoint.text')
    checkpoint_row_file = os.path.join(checkpoint_path, 'checkpoint.row')
    checkpoint_meta_file = os.path.join(checkpoint_path, 'checkpoint.meta')
    with open(checkpoint_meta_file, 'r') as f:
        index_line = f.readline().strip()
    counter = int(index_line.split(':')[1])+1
    with open(checkpoint_text_file, 'r') as f:
        lines = f.readlines()
    return counter, lines

def create_checkpoint(checkpoint_path, text, processed_files):
    checkpoint_text_file = os.path.join(checkpoint_path, 'checkpoint.text')
    checkpoint_meta_file = os.path.join(checkpoint_path, 'checkpoint.meta')
    with open(checkpoint_text_file, 'w') as f:
        for line in text:
            f.write('%s\n' % line)
    with open(checkpoint_meta_file, 'w') as f:
        f.write('Last Index: %d\n' % (-1))
        for file in processed_files:
            f.write('File: %s\n' % file)

def save_checkpoint(checkpoint_path, row, index):
    checkpoint_text_file = os.path.join(checkpoint_path, 'checkpoint.text')
    checkpoint_row_file = os.path.join(checkpoint_path, 'checkpoint.row')
    checkpoint_meta_file = os.path.join(checkpoint_path, 'checkpoint.meta')
    data = []
    with open(checkpoint_meta_file, 'r') as f:
        data = f.readlines()
    with open(checkpoint_meta_file, 'w') as f:
        data[0] = ('Last Index: %d\n' % index)
        for item in data:
            f.write('%s\n' % item.strip())
    with open(checkpoint_row_file, 'a') as f:
        for item in row:
            f.write('%s,%s,%s\n' % (item[0], item[1], item[2]))
