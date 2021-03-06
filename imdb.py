from __future__ import absolute_import, division, print_function

__author__ = 'Team Alpha'

import tensorflow as tf
from tensorflow import keras
from helper import Helper, arg_parser
from keras.layers import Dense, LSTM, Embedding, Flatten
from keras.layers import Conv1D, GlobalMaxPooling1D
from keras.models import Sequential
from nltk.corpus import stopwords
from keras import optimizers
from keras import backend as K
import numpy as np
import random as rand
import nltk


class IMDb(Helper):
    vocab_size = 20000
    maxlen = 512

    def __init__(self, combination, learning_rate, epochs, batches, seed):
        Helper.__init__(self)
        self.combination = int(combination)
        self.learning_rate = float(learning_rate)
        self.epochs = int(epochs)
        self.batches = int(batches)
        self.seed = int(seed)
        self.run_combination(self.combination)

    def run_combination(self, combination):
        train_data, train_labels, test_data, test_labels = self.prepare_data()
        if combination == 1:
            model = self.run_first_combo()
            modelname = "imdb_1_" + str(self.learning_rate) + "_" + str(self.epochs) + "_" + str(self.batches) + "_" + str(self.seed) + ""
        elif combination == 2:
            model = self.run_second_combo()
            modelname = "imdb_2_" + str(self.learning_rate) + "_" + str(self.epochs) + "_" + str(self.batches) + "_" + str(self.seed) + ""
        else:
            raise Exception("Please input 1 or 2 for the combination to run")
        modelname = "imdb-model"
        data = train_data, train_labels, test_data, test_labels
        result = Helper.fit_and_evaluate(self, model, data, self.batches, self.epochs, modelname)
        #Helper.plot_loss_acc(self, result.epoch, result.history['loss'], result.history['acc'],
        #                     result.history['val_loss'], result.history['val_acc'], modelname)
        
    def prepare_data(self):
        config = tf.ConfigProto(inter_op_parallelism_threads=1)
        session = tf.Session(config=config)
        K.set_session(session)
        rand.seed(self.seed)
        np.random.seed(self.seed)
        tf.set_random_seed(self.seed)

        nltk.download('stopwords')
        stopwords_eng = set(stopwords.words("english"))
        stopwords_eng.remove('no')
        stopwords_eng.remove('not')
        stopwords_eng.remove("shouldn't")
        stopwords_eng.remove("wasn't")
        stopwords_eng.remove("weren't")
        stopwords_eng.remove("wouldn't")
        stopwords_eng.remove("won't")
        stopwords_eng.remove("but")
        stopwords_eng.remove("aren't")
        stopwords_eng.remove("aren")
        stopwords_eng.remove("couldn")
        stopwords_eng.remove("couldn't")
        stopwords_eng.remove("didn")
        stopwords_eng.remove("didn't")
        stopwords_eng.remove("very")

        imdb = keras.datasets.imdb
        (train_data, train_labels), (test_data, test_labels) = imdb.load_data(num_words=self.vocab_size)
    
        # A dictionary mapping words to an integer index
        word_index = imdb.get_word_index()
        word_index = {k:(v+3) for k,v in word_index.items()}
        word_index["<PAD>"] = 0
        word_index["<START>"] = 1
        word_index["<UNK>"] = 2  # unknown
        word_index["<UNUSED>"] = 3

        reverse_word_index = dict([(value, key) for (key, value) in word_index.items()])

        def stopword_removal(data):
            processed_reviews = []
            for review in data:
                word_review = ' '.join([reverse_word_index.get(i, '?') for i in review])
                words = [word for word in word_review.split() if word not in stopwords_eng]
                indexed_words = []
                for w in words:
                    index = word_index.get(w)
                    indexed_words.append(index)
                processed_reviews.append(indexed_words)

            return processed_reviews
    
        clean_train_data = stopword_removal(train_data)
        clean_test_data = stopword_removal(test_data)
                    
        train_data = keras.preprocessing.sequence.pad_sequences(clean_train_data,
                                                            maxlen=self.maxlen)

        test_data = keras.preprocessing.sequence.pad_sequences(clean_test_data,
                                                           maxlen=self.maxlen)
        
        return train_data, train_labels, test_data, test_labels
        
    def run_first_combo(self):
        model = Sequential()
        model.add(Embedding(self.vocab_size, 250, input_length=self.maxlen))                  # 250 -> 50 for Example o
        model.add(Conv1D(filters=250, kernel_size=3, padding='same', activation='relu'))      # 250 -> 50 for Example o
        model.add(GlobalMaxPooling1D())
        # model.add(Dropout(0.5))                               # Unhash for Example n
        model.add(Dense(400, activation='relu'))
        # model.add(Dense(250, activation='relu'))              # Unhash for Example l
        # model.add(Dense(100, activation='relu'))              # Unhash for Example l
        model.add(Dense(1, activation='sigmoid'))

        adam = optimizers.Adam(lr=self.learning_rate)

        model.compile(loss='binary_crossentropy',
                      optimizer=adam,
                      metrics=['acc'])

        model.summary()
        return model
        
    def run_second_combo(self):
        model = Sequential()
        model.add(Embedding(self.vocab_size, 100, input_length=self.maxlen))
        # model.add(LSTM(128, dropout=0.02, recurrent_dropout=0.02))        # Unhash for Example r, s
        model.add(Flatten())                                            # Hash for Example r, s


        model.add(Dense(250, activation=tf.nn.relu))              # Hash for Example r, s
        model.add(Dense(100, activation=tf.nn.relu))              # Hash for Example r, s, t
        model.add(Dense(50, activation=tf.nn.relu))               # Hash for Example q, r, t
        model.add(Dense(1, activation=tf.nn.sigmoid))

        adam = optimizers.Adam(lr=self.learning_rate)

        model.compile(optimizer=adam,
                      loss='binary_crossentropy',
                      metrics=['acc'])
        model.summary()
        return model


if __name__ == "__main__":
    args = arg_parser()
    IMDb(args.combination, args.learning_rate, args.epochs, args.batches, args.seed)
