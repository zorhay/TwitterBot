from src.poebot.utils import _shuffle_text


def generate(**kwargs):
    pass
    # TODO: replace with generate function on word Rnn fork


class RnnWordGenerator(object):
    def __init__(self):
        pass

    def get_line(self, syllable_count):
        if syllable_count <= 0:
            return ''
        words = self._generate(prime=None, words=syllable_count).split(' ')

        while True:
            for word in words:
                taken_syllables = len(self.language.divided_into_syllables(word))
            if taken_syllables > syllable_count:
                words.pop()
            else:
                return ' '.join(words)

    def end_with(self, line_ending, syllable_count, exception_word=''):
        pass

    def _find_word_with_ending(self, ending, exception_word):
        shuffled_words = _shuffle_text(self.text_words)
        for word in self.text_words:
            if word.endswith(ending) and word != exception_word:
                return word
        else:
            return exception_word

    def _shuffle_text(self):
        pass

    def _generate(self, prime, words):
        return generate(data_src='data/', checkpoint='./model.pt', prime=prime, words=words,
                        seed=1111, cuda=False, temperature=1.0, log_interval=100)