import webbrowser
import nltk
from nltk.stem import WordNetLemmatizer
import pickle
import numpy as np
from keras.models import load_model
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