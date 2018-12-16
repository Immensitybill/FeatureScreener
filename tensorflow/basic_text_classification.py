
import tensorflow as tf
from tensorflow import keras
import pandas as pd



imdb = keras.datasets.imdb
(train_data, train_labels), (test_data, test_labels) = imdb.load_data(num_words=10000)


# A dictionary mapping words to an integer index
word_index = imdb.get_word_index()

# The first indices are reserved
word_index = {k:(v+3) for k,v in word_index.items()}
word_index["<PAD>"] = 0
word_index["<START>"] = 1
word_index["<UNK>"] = 2  # unknown
word_index["<UNUSED>"] = 3

reverse_word_index = dict([(value, key) for (key, value) in word_index.items()])

print(word_index['the'])

def decode_review(text):
    return ' '.join([reverse_word_index.get(i, '?') for i in text])

# print(decode_review(train_data[0]))
#
# print(train_data[0])

train_data = keras.preprocessing.sequence.pad_sequences(train_data,
                                                        value=word_index["<PAD>"],
                                                        padding='post',
                                                        maxlen=256)


test_data = keras.preprocessing.sequence.pad_sequences(test_data,
                                                       value=word_index["<PAD>"],
                                                       padding='post',
                                                       maxlen=256)


print(train_data[0])
print(len(train_data[0]))

# input shape is the vocabulary count used for the movie reviews (10,000 words)
vocab_size = 10000

model = keras.Sequential()
model.add(keras.layers.Embedding(vocab_size, 16))
model.add(keras.layers.GlobalAveragePooling1D())
model.add(keras.layers.Dense(16, activation=tf.nn.sigmoid))
model.add(keras.layers.Dense(1, activation=tf.nn.sigmoid))
model.compile(optimizer=tf.train.AdamOptimizer(),
              loss='binary_crossentropy',
              metrics=['accuracy'])

x_val = train_data[:10000]
partial_x_train = train_data[10000:]

y_val = train_labels[:10000]
partial_y_train = train_labels[10000:]

history = model.fit(partial_x_train,
                    partial_y_train,
                    epochs=1,
                    batch_size=512,
                    validation_data=(x_val, y_val),
                    verbose=2)
layer_model0 = keras.Model(inputs=model.input, outputs = model.layers[0].output)

output0 = layer_model0.predict(partial_x_train)

csv = pd.DataFrame(output0[0])
pd.DataFrame.to_csv(csv,path_or_buf="layer_0.csv")

layer_model1 = keras.Model(inputs=model.input, outputs = model.layers[1].output)

output1 = layer_model1.predict(partial_x_train)

csv = pd.DataFrame(output1)
pd.DataFrame.to_csv(csv,path_or_buf="layer_1.csv")


# print(output)
# print(history)

# results = model.evaluate(test_data, test_labels)
#
# print(results)