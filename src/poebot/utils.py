# RNN ֊ https://github.com/pytorch/examples/tree/master/word_language_model
import os
import random


def _shuffle_text(text):
    text_words = text.split()
    random.shuffle(text_words)
    return text_words


def get_poem_default_source():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(current_dir, 'data/source.txt')
