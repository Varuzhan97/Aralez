# Generate capitals ask speech text.
# The input file is the country_capital.txt file from /Aralez/Data direction.
# It will not remove duplicates and will generate the 2 same sentences for the country which has 2 capitals.
import os

sentence = 'What is the capital of {}?\n'

def preprocess_data(text):
    with open(text, 'r') as f:
        lines = f.readlines()

    country_capital = []
    # Strips the newline character
    f = open("output.txt", "a")

    for line in lines:
        pair = line.strip().split('<----->')
        f.write((sentence.format(pair[0])))
    f.close()

if __name__ == "__main__":
    current_dir = os.getcwd()
    text = os.path.join(current_dir, 'input.txt')
    preprocess_data(text)
