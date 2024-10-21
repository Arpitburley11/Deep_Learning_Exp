# -*- coding: utf-8 -*-
"""DL_9_Experiment_09.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1xz-lE0k0jOUITPLoqVl0W_YFOfSXvMHA
"""

!pip install wikipedia-api

import numpy as np
import tensorflow as tf
import wikipediaapi
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.models import Sequential
from tensorflow.keras.utils import to_categorical

def fetch_wikipedia_text(topic):
      wiki_wiki = wikipediaapi.Wikipedia(
      language='en',
      extract_format=wikipediaapi.ExtractFormat.WIKI,
      user_agent='my-application/1.0')
      page = wiki_wiki.page(topic)
      return page.text

# Preprocess text
def preprocess_text(text):
    # Convert to lowercase
    text = text.lower()
    # Remove special characters
    text = ''.join(c for c in text if c.isalnum() or c in [' ', '\n'])
    return text

topic = "Artificial Intelligence"
wikipedia_text = fetch_wikipedia_text(topic)
preprocessed_text = preprocess_text(wikipedia_text)
print(preprocessed_text)

text = preprocessed_text
# Prepare the tokenizer and encode the words
tokenizer = Tokenizer()
tokenizer.fit_on_texts([text])
encoded = tokenizer.texts_to_sequences([text])[0]
vocab_size = len(tokenizer.word_index) + 1

# Generate sequences
seq_length = 100
sequences = []
for i in range(seq_length, len(encoded)):
    seq = encoded[i-seq_length:i+1]
    sequences.append(seq)

sequences = np.array(sequences)
X, y = sequences[:,:-1], sequences[:,-1]
y = to_categorical(y, num_classes=vocab_size)

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Embedding, LSTM, Dense

# Define the RNN model
model = Sequential([
    Embedding(vocab_size, 50, input_length=seq_length),
    LSTM(150, return_sequences=True),
    LSTM(100),
    Dense(vocab_size, activation='softmax')
])

# Compile the model
model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

# Train the model
model.fit(X, y, epochs=100,callbacks=[tf.keras.callbacks.ReduceLROnPlateau()])

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Embedding, LSTM, Dense

# Define the RNN model
model2 = Sequential([
    Embedding(vocab_size, 50, input_length=seq_length),
    LSTM(150, return_sequences=True),
    LSTM(100),
    Dense(vocab_size, activation='softmax')
])

# Compile the model
model2.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

# Train the model
model2.fit(X, y, epochs=100,callbacks=[tf.keras.callbacks.ReduceLROnPlateau()])

def generate_text_base_word(model, tokenizer, seed_text, num_words):
    result = []
    in_text = seed_text
    for _ in range(num_words):
        encoded = tokenizer.texts_to_sequences([in_text])[0]
        encoded = pad_sequences([encoded], maxlen=seq_length, truncating='pre')
        yhat = model.predict(encoded, verbose=0)
        yhat = np.argmax(yhat, axis=1)
        out_word = ''
        for word, index in tokenizer.word_index.items():
            if index == yhat:
                out_word = word
                break
        in_text += ' ' + out_word
        result.append(out_word)
    return ' '.join(result)

# Example usage
seed_text = "Artificial Intelligence"
generated_text = generate_text_base_word(model2, tokenizer, seed_text, 50)
print(seed_text,generated_text)