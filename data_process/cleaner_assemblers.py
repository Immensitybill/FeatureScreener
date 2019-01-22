import nltk
from data_process.text_cleaners import StopwordsRemover, LowercaseTransformer, Stemmer
from data_process.tokenizers import DefaultTokenizer


class CleanerAssembler():

    def __init__(self,tokenizer=DefaultTokenizer()):
        self.tokenizer = tokenizer
        self.cleaner_list = []
        self.text = ""

    def add(self,text_cleaner):
        self.cleaner_list.append(text_cleaner)

    def set_tokens(self,tokens):
        self.tokens = tokens

    def set_tokenizer(self,tokenizer):
        self.tokenizer = tokenizer

    def do_cleaning(self, text):
        self.text = text
        tokens = self.tokenizer.tokenize(self.text)
        for cleaner in self.cleaner_list:
            tokens = cleaner.clean(tokens)
        return tokens



# def test():
#     text="fish fished fishing"
#     ca =CleanerAssembler()
#     ca.add(Stemmer())
#     # ca.add(StopwordsRemover())
#     # ca.add(LowercaseTransformer())
#     clean_tokens = ca.do_cleaning(text)
#
#     print(len(clean_tokens))
#     freq = nltk.FreqDist(clean_tokens)
#     freq.plot(20, cumulative=False)
#     for key,val in freq.items():
#         print (str(key) + ':' + str(val))
# test()



