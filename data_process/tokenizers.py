from abc import ABCMeta, abstractmethod


class AbstractTokenizer(metaclass=ABCMeta):

    @abstractmethod
    def tokenize(self,text):
        pass


class DefaultTokenizer(AbstractTokenizer):

    def tokenize(self,text):
        tokens = [t for t in text.split()]
        return tokens