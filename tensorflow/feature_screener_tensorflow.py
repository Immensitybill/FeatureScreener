import dictionary_creater as dc
import tensorflow as tf
from tensorflow import keras
import matplotlib.pyplot as plt


def main():
    str, df =dc.read_csv("fun_desc.csv")
    data, count, dictionary, reversed_dictionary = dc.build_dataset(str,10000)

    convertedData_full = dc.convertData2Index(df,dictionary)

    train_data_full = keras.preprocessing.sequence.pad_sequences(convertedData_full,
                                                            value=dictionary["<PAD>"],
                                                            padding='post',
                                                            maxlen=1050)

    label_full = df['flag'].values

    trainingData = train_data_full[:66]
    trainingLabel = label_full[:66]

    validatData = train_data_full[66:88]
    validatLabel = label_full[66:88]

    testData = train_data_full[88:]
    testLabel = label_full[88:]


    vocab_size = 10000

    model = keras.Sequential()
    model.add(keras.layers.Embedding(vocab_size, 16))
    model.add(keras.layers.GlobalAveragePooling1D())
    # model.add(keras.layers.Dense(26,kernel_regularizer=keras.regularizers.l2(0.01), activation=tf.nn.relu))
    # model.add(keras.layers.Dropout(0.3))
    model.add(keras.layers.Dense(1, activation=tf.nn.sigmoid))
    model.compile(optimizer=tf.train.AdamOptimizer(),
                  loss='binary_crossentropy',
                  metrics=['accuracy'])


    history = model.fit(trainingData,
                        trainingLabel,
                        epochs=600,
                        batch_size=16,
                        validation_data=(validatData, validatLabel),
                        verbose=1)

    results = model.evaluate(testData, testLabel)
    print(results)

    draw_plot(history)

    # layer_model1 = keras.Model(inputs=model.input, outputs = model.layers[3].output)


    # output1 = model.predict(trainingData[0:1])

    model.save(filepath="./model/my_model1.h5")

    # model = keras.models.load_model(filepath="./model/my_model1.h5")

    # output2 = model.predict(trainingData[0:1])
    #
    # print(trainingData[0:1])
    # print(output1)
    # print(output2)

def draw_plot(history):
    history_dict = history.history
    history_dict.keys()

    acc = history.history['acc']
    val_acc = history.history['val_acc']
    loss = history.history['loss']
    val_loss = history.history['val_loss']

    epochs = range(1, len(acc) + 1)

    # "bo" is for "blue dot"
    plt.plot(epochs, loss, 'bo', label='Training loss')
    # b is for "solid blue line"
    plt.plot(epochs, val_loss, 'b', label='Validation loss')
    plt.title('Training and validation loss')
    plt.xlabel('Epochs')
    plt.ylabel('Loss')
    plt.legend()

    plt.show()

    plt.clf()  # clear figure
    acc_values = history_dict['acc']
    val_acc_values = history_dict['val_acc']

    plt.plot(epochs, acc, 'bo', label='Training acc')
    plt.plot(epochs, val_acc, 'b', label='Validation acc')
    plt.title('Training and validation accuracy')
    plt.xlabel('Epochs')
    plt.ylabel('Accuracy')
    plt.legend()

    plt.show()

main()