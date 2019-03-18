# https://vk.com/topic-107588501_33365934
from .text_analysis import ArmenianLanguage
from . import rnn_interface


class PoemBase(object):
    structure = []


class Poem49892(PoemBase):
    structure = [(9, 0), (8, 3), (9, 2), (2, 1)]

    def __init__(self):
        pass

    def generate(self, source=None):
        poem = []
        word_rnn = rnn_interface.WordRNN(source)
        for i, v in enumerate(self.structure):
            if i <= v[1]:
                line = word_rnn.get_line(syllable_count=v[0])
            else:
                line_ending = ArmenianLanguage.last_syllable(poem[v[1]], min_char_count=3)
                line = word_rnn.end_with(line_ending=line_ending, syllable_count=v[0])
            poem.append(line)
        return poem


class Poem298(PoemBase):
    structure = [9, 8]

    def __init__(self):
        pass


class Poem49898(PoemBase):
    structure = [9, 8, 9, 8]


class Poem46565(PoemBase):
    structure = [6, 5, 6, 5]


class CustomPoem(PoemBase):
    pass
