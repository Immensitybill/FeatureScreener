import nltk
from data_process.text_cleaners import StopwordsRemover, LowercaseTransformer
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
#     text=" The eNode B accepts UEs with, accessStratumRelease; set to Rel. 15. The eNode B initiates a fullConfig handover if ue-ConfigRelease-r9 is greater than 'rel 15'. A target eNode B releases all Rel15 functionality that has been configured by a source eNode B and are not supported by the target eNode B. 3GPP compliant handling of not supported S1AP, X2AP or M3AP messages Support for the 3GPP release specific extensions of Iuant ALD interface (3GPP TS 25.46x) Individual changes request from later 3GPP baselines might be introduced as well. The list of additionally implemented CRs will be added at a later point in time."
#     ca =CleanerAssembler()
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



