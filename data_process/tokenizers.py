from abc import ABCMeta, abstractmethod

from nltk import RegexpTokenizer


class AbstractTokenizer(metaclass=ABCMeta):

    @abstractmethod
    def tokenize(self,text):
        pass


class DefaultTokenizer(AbstractTokenizer):

    def tokenize(self,text):
        tokens = [t for t in text.split()]
        return tokens

class myTokenizer(AbstractTokenizer):

    def tokenize(self,text):
        tokenizer = RegexpTokenizer('\w*')
        return tokenizer.tokenize(text)



# def test():
#     t = DefaultTokenizer()
#     aa = t.tokenize("DL 4x4 MIMO is supported on licensed carriers only. Up to 20 MIMO layers per a UE is supported.")
#     print(aa)
#
# test()