import pickle
import os
import numpy as np
from keras.preprocessing.text import Tokenizer
from timeit import default_timer as timer


def save_vocabulary(vocab):
    print("Save vocabulary object to file in directory %s" % os.getcwd() + "/" + Vocabulary.dict_file)
    start = timer()
    with open(Vocabulary.dict_file, 'wb') as f:
        pickle.dump(vocab, f)
    end = timer()
    print("INFO - Saved vocabulary to file in %s seconds." % (end - start))


class Vocabulary(object):
    # fixed the name of the vocabulary, class variable
    dict_file = 'aol_vocab.pkl'

    def __init__(self, max_prune_words=90000, file_input_path=None):

        self.file_input_path = file_input_path

        if file_input_path is None:
            self._vocab = Tokenizer(nb_words=max_prune_words)
            self._index_w_dict = None
        else:
            self.load_vocab()
            self.make_index_word_dict()

    @property
    def keras_tokenizer(self):
        return self._vocab

    @property
    def index_word_dict(self):
        return self._index_w_dict

    @property
    def word_counts(self):
        return self._vocab.word_counts

    @property
    def word_index(self):
        return self._vocab.word_index

    def fit_on_texts(self, texts):
        self._vocab.fit_on_texts(texts)

    def make_index_word_dict(self):
        self._index_w_dict = {item: k for k, item in self._vocab.word_index.iteritems()}

    def save_vocab(self):

        print("Save objects to files in directory %s" % os.getcwd() + "/" + Vocabulary.dict_file)
        start = timer()
        with open(self.dict_file, 'wb') as f:
            pickle.dump(self._vocab, f)
        end = timer()
        print("INFO - Saved vocab to file in %s seconds." % (end - start))

    def load_vocab(self):

        with open(self.file_input_path, 'rb') as f:
            self._vocab = pickle.load(f)
        print "INFO - Load vocab from directory %s contains %d words" % (self.file_input_path,
                len(self._vocab.word_counts))

    def queryw_in_vocab(self, query_w):
        """
        :param query_w: query words as list
        :return: returns a boolean mask for query word sequence
        """
        return [False if wl == [] else True for wl in self._vocab.texts_to_sequences(query_w)]

    def queryw_to_queryw(self, query_w):
        return [query_w[idx] if ind else "UNK" for idx, ind in enumerate(self.queryw_in_vocab(query_w))]

    def query_to_sequence(self, query_w):
        q_w_list = [[0] if wl == [] else wl for wl in
                    self._vocab.texts_to_sequences(query_w)]
        # reshaping the result of tokenizer to numpy array, in order to get rid
        # of 1 list dimension
        return np.reshape(q_w_list, (len(q_w_list)))

    def seq_to_words(self, seq):
        return [self._index_w_dict[s] for s in seq]






