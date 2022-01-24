import yaml
import os
from Levenshtein import ratio

#Function is used to get printable results
def get_result(question, data_file_yaml, fn):
    answer = fn(question, data_file_yaml)
    return answer

def get_approximate_answer(question_string, data_file_yaml):
    max_score = 0
    answer = ""
    prediction = ""

    # Iterating over values
    for row, id in data_file_yaml.items():
        score = ratio(row, question_string)
        #Answer founded, stop here
        if score >= 0.9:
            return id
        #Answer was not founded, continue
        elif score > max_score:
            max_score = score
            answer = id
            prediction = row

    #Treshold
    if max_score > 0.8:
        return answer
    return -1

def get_answer(question_string, data_file_yaml_path):
    answer_id = 1
    #Load YAML file that contains question-answer_id pairs
    data_file_yaml = None
    with open(os.path.join(data_file_yaml_path, "data.yaml"), 'r') as file:
        #data_file =  open(os.path.join(data_file_yaml_path, "data.yaml"), 'r')
        data_file_yaml = yaml.full_load(file)
    answer_id = get_result(question_string, data_file_yaml, get_approximate_answer)
    return answer_id
