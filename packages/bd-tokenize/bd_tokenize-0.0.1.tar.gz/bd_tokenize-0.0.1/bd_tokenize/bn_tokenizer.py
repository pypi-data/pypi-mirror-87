import string 
import re
from string import punctuation
import pandas as pd


# if the input text is string
def text_to_word(sent):
    word_text = re.compile(r'[।\s+\|{}]+'.format(re.escape(punctuation)))
    word_listing_ = [i for i in word_text.split(sent) if i]

    return word_listing_



class Ekush_tokenizer(object):
  def __init__(self, oov_token=None, num_bn_words=None, char_level=False, not_list=None):
      self.oov_token = oov_token
      self.num_bn_words = num_bn_words
      self.bn_word_index = {}
      self.bn_index_word = {}
      self.char_level = char_level
      self.not_list = not_list

  def fit_on_text(self, sentence):
      word_count = {}
      for sent in sentence:
        if self.char_level or isinstance(sent, list):
          if isinstance(sent, list):
            word_tok = [word for word in sent]
          else:
            word_tok = sent
        else:
          if isinstance(sent, str):
            word_tok = text_to_word(sent)
          else:
            word_tok = self.not_list(sent)
        for w in word_tok:
          if w in word_count:
            word_count[w] += 1
          else:
            word_count[w] = 1
        common_words = sorted(word_count, key=word_count.get, reverse=True)
        self.bn_word_index = dict(zip(common_words, list(range(1, len(common_words) + 1))))
        self.bn_index_word = {n:m for m, n in self.bn_word_index.items()}