from tensorflow import keras
import pandas as pd
import numpy as np
import tensorflow as tf
import dictionary_creater as dc
import pickle as pk

def load_dict():
    with open("F:\\PyWorkSpace\\FeatureScreener\\tensorflow\\dict.file", "rb") as f:
        d = pk.load(f)
        return d

def convertText2Index(text, dict):
    data = tf.compat.as_str(text)
    data = data.replace('-', ' ')
    data = data.split()
    result = np.array([])
    for word in data:
        if (word in dict.keys()):
            index = dict[word]
        else:
            index = dict['<UNK>']
        result = np.append(result, index)
    return result


def predict(text):
    model = keras.models.load_model(filepath="F:\\PyWorkSpace\\FeatureScreener\\tensorflow\\model\\my_model1.h5")
    dict1 = load_dict()

    convertd = convertText2Index(text, dict1)
    seque = []
    lis = list(convertd)
    seque.append(lis)

    sequence = keras.preprocessing.sequence.pad_sequences(seque,
                                                            value=dict1["<PAD>"],
                                                            padding='post',
                                                            maxlen=60)
    print(sequence)
    result = model.predict(sequence)
    return result


# text1 = "5GC000585-CFAM-CP2 - AEUB Nokia AirScale AAS 28 GHz"
# result = predict(text1)
# print(result)