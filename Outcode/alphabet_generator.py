import os
import argparse

def parse_args():
    parser = argparse.ArgumentParser(description='Arguments and Their Descriptions.')
    parser.add_argument('--input_path', required = True,
                        help='An Argument For Absolute Path Of Input Text File.')
    parser.add_argument('--output_path', required = True,
                        help='An Argument For Absolute Path Of Output Text File.')
    args = parser.parse_args()
    return args

if __name__ == "__main__":
    params = parse_args()
    all_text = set()
    with open(params.input_path, 'r') as f:
        data = f.readlines()
        for line in data:
            all_text |= set(line.strip())

    with open(os.path.join(params.output_path, 'Alphabet.txt'), "w") as alphabet_file:
        for char in list(all_text):
            alphabet_file.write(char + '\n')
