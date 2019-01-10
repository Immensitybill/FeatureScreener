from abc import ABCMeta, abstractmethod

from nltk.corpus import stopwords


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
