import nltk
from nltk.stem.lancaster import LancasterStemmer
stemmer = LancasterStemmer()

import numpy
import tflearn
import tensorflow
#tensorflow.logging.set_verbosity(tensorflow.logging.ERROR)
tensorflow.compat.v1.logging.set_verbosity(tensorflow.compat.v1.logging.ERROR)
import random
import json
import pickle
import os

try:
    nltk.download('punkt')
except:
    pass

def bag_of_words(s, words):
    bag = [0 for _ in range(len(words))]

    s_words = nltk.word_tokenize(s)
    s_words = [stemmer.stem(word.lower()) for word in s_words]

    for se in s_words:
        for i, w in enumerate(words):
            if w == se:
                bag[i] = 1

    return numpy.array(bag)


def response(input, model_path):
    current_dir = '/home/varuzhan/Desktop/***PROJECT***/Oberon/QA'

    with open(os.path.join(model_path, 'intents.json')) as file:
        data = json.load(file)

    with open(os.path.join(model_path, 'data.pickle'), "rb") as f:
        words, labels, training, output = pickle.load(f)

    #tensorflow.reset_default_graph()
    tensorflow.compat.v1.reset_default_graph()

    net = tflearn.input_data(shape=[None, len(training[0])])
    net = tflearn.fully_connected(net, 8)
    net = tflearn.fully_connected(net, 8)
    net = tflearn.fully_connected(net, len(output[0]), activation="softmax")
    net = tflearn.regression(net)

    model = tflearn.DNN(net)
    model.load(os.path.join(model_path, 'model.tflearn'))
    ##############################################################################3
    print("Start talking with the bot (type quit to stop)!")

    results = model.predict([bag_of_words(input, words)])[0]
    results_index = numpy.argmax(results)
    tag = labels[results_index]

    if results[results_index] > 0.95:
        for tg in data["intents"]:
            if tg['tag'] == tag:
                #responses = tg['responses']
                #context = tg['context_set']
                #print('Tag--->', tg['tag'])
                #print('Information--->',tg['information'])
                resp = tg['tag']
                info = tg['information']
        #resp = random.choice(responses)
    else:
        #print('Sorry, I didn\'t get what you said.')
        resp = "Sorry, I didn't get what you said."
        info = -1
    return resp, info
    #return resp, context
