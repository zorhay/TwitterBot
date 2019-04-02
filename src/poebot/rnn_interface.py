# RNN ֊ https://github.com/pytorch/examples/tree/master/word_language_model
from .text_analysis import ArmenianLanguage
import random


class WordRandom(object):
    text = ''
    text_words = []

    def __init__(self, source):
        self.source = source
        self.language = ArmenianLanguage()
        self._read_source(source)
        self._shuffle_text()

    def _read_source(self, source=None):
        source = source or self.source
        with open(source, 'r') as f:
            self.text = f.read()
        return self.text

    def _shuffle_text(self):
        self.text_words = self.text.split()
        random.shuffle(self.text_words)
        return self.text_words

    def _choice_words(self, word_count):
        return random.choices(self.text_words, k=word_count)

    def _find_word_with_ending(self, ending, exception_word):
        self._shuffle_text()
        for word in self.text_words:
            if word.endswith(ending) and word != exception_word:
                return word
        else:
            return None

    def get_line(self, syllable_count):
        if syllable_count <= 0:
            return ''
        words = []
        taken_syllables = 0
        while taken_syllables < syllable_count:
            words.extend(self._choice_words(1))
            taken_syllables = 0
            for word in words:
                taken_syllables += len(self.language.divided_into_syllables(word))
        return ' '.join(words)

    def end_with(self, line_ending, syllable_count, exception_word=''):
        ending_word = self._find_word_with_ending(line_ending, exception_word)
        if not ending_word:
            raise ValueError('Specified ending not found, try again.')
        taken_syllable = len(self.language.divided_into_syllables(ending_word))
        line = self.get_line(syllable_count - taken_syllable)
        return line + ' ' + ending_word


class WordRNN(object):
    pass


class CharRNN(object):
    pass
