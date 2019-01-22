from tensorflow import keras
import numpy as np
import tensorflow as tf
import pickle as pk
import os

from data_process.cleaner_assemblers import CleanerAssembler
from data_process.text_cleaners import StopwordsRemover, LowercaseTransformer, PunctuationRemover


def load_dict():
    with open(os.path.join(os.path.dirname(__file__), "dict.file"), "rb") as f:
        d = pk.load(f)
        return d

def convertText2Index(text, dict):
    ca = CleanerAssembler()
    ca.add(PunctuationRemover())
    ca.add(StopwordsRemover())
    ca.add(LowercaseTransformer())
    data = ca.do_cleaning(text)
    result = np.array([])
    for word in data:
        if (word in dict.keys()):
            index = dict[word]
        else:
            index = dict['<UNK>']
        result = np.append(result, index)
    return result


def predict(text):
    model = keras.models.load_model(filepath=os.path.join(os.path.dirname(__file__), "./model/my_model1.h5"))
    dict1 = load_dict()

    convertd = convertText2Index(text, dict1)
    seque = []
    lis = list(convertd)
    seque.append(lis)

    sequence = keras.preprocessing.sequence.pad_sequences(seque,
                                                            value=dict1["<PAD>"],
                                                            padding='post',
                                                            maxlen=1050)
    print(sequence)
    result = model.predict(sequence)
    return result


# text1 = "ddd"
# result = predict(text1)
# print(result)