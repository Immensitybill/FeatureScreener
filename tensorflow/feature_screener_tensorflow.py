import dictionary_creater as dc
import tensorflow as tf
from tensorflow import keras
import pandas as pd


str, df =dc.read_csv("Feature_names.csv")
data, count, dictionary, reversed_dictionary = dc.build_dataset(str,10000)

convertedData_full = dc.convertData2Index(df,dictionary)

train_data_full = keras.preprocessing.sequence.pad_sequences(convertedData_full,
                                                        value=dictionary["<PAD>"],
                                                        padding='post',
                                                        maxlen=60)

label_full = df['flag'].values

trainingData = train_data_full[:2000]
trainingLabel = label_full[:2000]

validatData = train_data_full[2000:3000]
validatLabel = label_full[2000:3000]

testData = train_data_full[3000:]
testLabel = label_full[3000:]


vocab_size = 10000

model = keras.Sequential()
model.add(keras.layers.Embedding(vocab_size, 32))
model.add(keras.layers.GlobalAveragePooling1D())
model.add(keras.layers.Dense(32, activation=tf.nn.relu))
model.add(keras.layers.Dense(1, activation=tf.nn.sigmoid))
model.compile(optimizer=tf.train.AdamOptimizer(),
              loss='binary_crossentropy',
              metrics=['accuracy'])


history = model.fit(trainingData,
                    trainingLabel,
                    epochs=200,
                    batch_size=512,
                    validation_data=(validatData, validatLabel),
                    verbose=1)

results = model.evaluate(testData, testLabel)

# layer_model1 = keras.Model(inputs=model.input, outputs = model.layers[3].output)


output1 = model.predict(trainingData[0:1])

model.save(filepath="./model/my_model1.h5")

model = keras.models.load_model(filepath="./model/my_model1.h5")

output2 = model.predict(trainingData[0:1])

print(trainingData[0:1])
print(output1)
print(output2)