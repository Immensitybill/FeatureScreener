from abc import ABCMeta, abstractmethod

from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer


class TextCleaner(metaclass=ABCMeta):

    @abstractmethod
    def clean(self,tokens):
       pass


class StopwordsRemover(TextCleaner):

    def clean(self,tokens):
        stopwords_set = set(stopwords.words('english'))
        clean_tokens = []
        for token in tokens:
            if token in stopwords_set:
                continue
            else:
                clean_tokens.append(token)
        return clean_tokens

class LowercaseTransformer(TextCleaner):

    def clean(self,tokens):
        clean_tokens = []
        for token in tokens:
            clean_tokens.append(token.lower())
        return clean_tokens

class Stemmer(TextCleaner):
    def clean(self,tokens):
        porter = PorterStemmer()
        return [porter.stem(word) for word in tokens]

class PunctuationRemover(TextCleaner):
    def clean(self,tokens):
        clean_tokens = []
        for token in tokens:
            if token == '-':
                continue
            elif token.isalpha():
                clean_tokens.append(token)
        return clean_tokens

# def test():
#     str = ['aa-bb','-']
#     c = PunctuationRemover()
#     print(c.clean(str))
#
# test()