import nltk
from nltk.stem import WordNetLemmatizer
import pickle
import numpy as np
import tensorflow as tf
import tensorflow.python.keras as keras
from tensorflow.python.keras.models import load_model

import json
import random

# load the pretrained model
model = load_model('model.h5')
intents = json.loads(open('data.json').read())
words = pickle.load(open('texts.pkl', 'rb'))
classes = pickle.load(open('labels.pkl', 'rb'))


# processing user input
lemmatizer = WordNetLemmatizer()

def clean_up_sentences(sentence):
  sentence_words = nltk.word_tokenize(sentence)
  sentence_words = [lemmatizer.lemmatize(word.lower()) for word in sentence_words]
  return sentence_words

# clean up sentences and create a bag of words
def bag_of_words(sentence, words, show_details=True):
  sentence_words = clean_up_sentences(sentence)
  bag = [0] * len(words)
  for s in sentence_words:
    # Loop through each word in the list of words
    for i, w in enumerate(words):
      # If word in sentence is in list of words, set corresponding position in bag to 1
      if w == s:
        bag[i] = 1
        if show_details:
          print("found in bag: %s" % w)
  return np.array(bag)


def predict_class(sentence, model):
  # create bag of words
  p = bag_of_words(sentence, words, show_details=True)
  # predict probability of each tag
  res = model.predict(np.array([p]))[0]
  # set error threshold
  ERROR_THRESHOLD = 0.25
  # get tags with probability above error threshold
  results = [[i, r] for i, r in enumerate(res) if r >  ERROR_THRESHOLD]
  results.sort(key=lambda x: x[1], reverse=True)
  return_list=[]
  for r in results:
    return_list.append({"intent": classes[r[0]], "probability": str(r[1])})

  return return_list


# match predicted intent with intents in json
def getResponse(ints, intents_json):
  tag = ints[0]['intent']
  list_of_intents = intents_json['intents']
  for i in list_of_intents:
    if i['tag'] == tag:
      result = random.choice(i['responses'])
      break;
  return result


# provide response to user input
def chatbot_response(msg):
  chatbotResponse = 'Loading bot response.....'

  ints = predict_class(msg, model)
  res = getResponse(ints, intents)
  chatbotResponse = res

  return chatbotResponse