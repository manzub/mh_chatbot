import nltk
from nltk.stem import WordNetLemmatizer
import json
import pickle
import numpy as np
from keras.models import Sequential
from keras.layers import Dense, Activation, Dropout
from keras.optimizers import SGD
import random
import tflearn
import tensorflow as tf

lemmatizer = WordNetLemmatizer()
# all unique words - vocabulary
words = []
# labels - intents
classes = []
# combination between patterns and intents - story&label
documents = []
ignore_words = ['?', '!']
data_file = open('data.json').read()
intents = json.loads(data_file)

for intent in intents['intents']:
  for pattern in intent['patterns']:
    # tokenize each word
    w = nltk.word_tokenize(pattern)
    words.extend(w)
    # add word to corpus
    documents.append((w, intent['tag']))
    # if word not in classes then add to class/labels list
    if intent['tag'] not in classes:
      classes.append(intent['tag'])

# lemmatize and lower each word
words = [lemmatizer.lemmatize(w.lower()) for w in words if w not in ignore_words]
# sort each word and remove duplicates
words = sorted(list(set(words)))
classes = sorted(list(set(classes)))

print("documents: ", len(documents))
print("classes: ", len(classes), classes)
print("all unique lemmatized words", len(words), words)

# save the preprocessed data locally
pickle.dump(words, open('texts.pkl', 'wb'))
pickle.dump(classes, open('labels.pkl', 'wb'))

# create training data
training = []
# create an empty arrow for output
output_empty = [0] * len(classes)
# training set/ bag of words for each sentence
for doc in documents:
  # initialize bag of words
  bag = []
  # list of tokenized words for the pattern
  pattern_words = doc[0]
  # lemmatize each word - create base word, in attempt to represent related words
  pattern_words = [lemmatizer.lemmatize(word.lower()) for word in pattern_words]
  # create bag of words with 1 if word match found in current pattern
  for w in words:
    bag.append(1) if w in pattern_words else bag.append(0)
    
  # output is a '0' for each tag and '1' for current tag (for each pattern)
  output_row = list(output_empty)
  output_row[classes.index(doc[1])] = 1

  training.append([bag, output_row])

# shuffle features and turn into np.array
random.shuffle(training)
training = np.array(training)

# create train test splits. X - patterns, y - intents/labels
train_x = list(training[:,0])
train_y = list(training[:,1])
print("Training data created")

# create model - 3 layers.
# First layer 128 neurons, second layer 64 neurons
# third layer contains no. of neurons equal to no. of intents to predict output intent with softmax
model = Sequential()
model.add(Dense(128, input_shape=(len(train_x[0]),), activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(64, activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(len(train_y[0]), activation='softmax'))

# compile model. Stochastic gradient descent with Nesterov accelerated gradient gives good results for this model
sgd = SGD(lr=0.01, decay=1e-6, momentum=0.9, nesterov=True)
model.compile(loss='categorical_crossentropy', optimizer=sgd, metrics=['accuracy'])

# fitting and saving the model
hist = model.fit(np.array(train_x), np.array(train_y), epochs=500, batch_size=5, verbose=1)
model.save('model.h5', hist)
print('model saved and created')