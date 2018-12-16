import collections
import tensorflow as tf
import zipfile
import pandas as pd
import numpy as np
import pickle as pk


def read_data(filename):
    """Extract the first file enclosed in a zip file as a list of words."""
    with zipfile.ZipFile(filename) as f:
        data = tf.compat.as_str(f.read(f.namelist()[0])).split()
    return data

def read_csv(filename):
    df = pd.read_csv(filename,index_col=False,header=None)
    df.rename(columns={0:'feature_name',1:'works',2:'flag'},inplace=True)
    str = ""
    for i in range(0, len(df)):
        str = str +" "+ df.iloc[i][0]
    data = tf.compat.as_str(str).split()
    return data, df

def convertData2Index(data, dictionary):
    result = []
    for i in range(0, len(data)):
        str = data.iloc[i][0]
        words = tf.compat.as_str(str).split()
        indexs = np.array([])
        for word in words:
           indexs =  np.append(indexs,dictionary[word])
        wordList = list(indexs)
        result.append(wordList)
    return np.array(result)



def build_dataset(words, n_words):
    """Process raw inputs into a dataset."""
    count = [['<UNK>', -1]]
    #  [['UNK', -1], ['i', 500], ['the', 498], ['man', 312], ...]
    count.extend(collections.Counter(words).most_common(n_words - 1))
    #  dictionary {'UNK':0, 'i':1, 'the': 2, 'man':3, ...}
    dictionary = dict()
    for word, _ in count:
        dictionary[word] = len(dictionary)
    data = list()
    unk_count = 0
    for word in words:
        if word in dictionary:
            index = dictionary[word]
        else:
            index = 0  # dictionary['UNK']
            unk_count += 1
        data.append(index)
    count[0][1] = unk_count
    reversed_dictionary = dict(zip(dictionary.values(), dictionary.keys()))
    dictionary = {k: (v + 3) for k, v in dictionary.items()}
    dictionary["<PAD>"] = 0
    dictionary["<START>"] = 1
    dictionary["<UNUSED>"] = 2
    with open("dict.file", "wb") as f:
        pk.dump(dictionary, f)
    # data: "I like cat" -> [1, 21, 124]
    # count: [['UNK', 349], ['i', 500], ['the', 498], ['man', 312], ...]
    # dictionary {'UNK':0, 'i':1, 'the': 2, 'man':3, ...}
    # reversed_dictionary: {0:'UNK', 1:'i', 2:'the', 3:'man', ...}
    return data, count, dictionary, reversed_dictionary





# str, df =read_csv("Feature_names.csv")
# data, count, dictionary, reversed_dictionary = build_dataset(str,10000)
# re = convertData2Index(df,dictionary)
# aa = [len(e) for e in re]
# max = np.max(aa)
# print();