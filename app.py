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
  pass