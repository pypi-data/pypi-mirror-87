import string 
import re
from string import punctuation

class Ekush_word_tokenizer:
    def __init__(self):
        pass

    def ekush_word_tokenizer(self, sent):
        sentence = re.compile(r'[।\s+\|{}]+'.format(re.escape(punctuation)))
        word_listing_ = [i for i in sentence.split(sent) if i]
        return word_listing_
    
    def ekush_sent_tokenizer(self, sent):
        sent_tok_ = re.compile(r'।\s*')
        sent_list = [p for p in sent_tok_.split(sent) if p]
        return sent_list