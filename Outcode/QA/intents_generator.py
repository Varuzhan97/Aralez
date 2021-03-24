import os
import argparse

def parse_args():
    parser = argparse.ArgumentParser(description='Arguments and Their Descriptions.')
    parser.add_argument('--input_path', default = None,
                        help='An Argument For Absolute Path Of Input Text File.')
    args = parser.parse_args()
    return args

# The input file must contain a group of patterns separated by '###' sequence
# Example:
# ###0###None###
# hello
# hi
# good morning
# good afternoon
# good evening
# ###1###Time-based###
# what is your name
# what's your name
# please say me your name
# ###END###None###

if __name__ == "__main__":
    params = parse_args()
    input_file = open(params.input_path, 'r')
    output_file = open('output.txt', 'w')
    lines = []
    current_tag = ''
    for line in input_file:
        if line.startswith('###'):
            tag = line.split('###')[1]
            info = line.split('###')[2]
            if lines:
                output_file.write('{"tag": \"' + current_tag + '\",' + '\n')
                output_file.write(' "patterns": [')
                for i in lines:
                    if i == lines[-1]:
                        output_file.write('"%s"' % i)
                    else:
                        output_file.write('"%s", ' % i)
                output_file.write('],' + '\n')
                output_file.write(' "information": \"' + info + '\"' + '\n')
                output_file.write('},' + '\n')
                lines.clear()
        else:
            lines.append(line.strip())
            current_tag = tag
    output_file.close()
