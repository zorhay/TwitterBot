# https://vk.com/topic-107588501_33365934
from .text_analysis import ArmenianLanguage
from .rnn_interface import WordRandom


class PoemBase(object):
    def __init__(self, structure=None, source=None, language=None):
        """
        :param structure:
        This is a list, with tuples of pairs of numbers.
        example: [(9, 1), (8, 0), (9, 3), (8, 2)]
        The first number means the number of syllables in a line,
        the second with which line the given line should rhyme.
        If the rhyme index is equal to its own index, this means the string does not rhyme.
        :param source:
        Path to the file from which data should be generated.
        :param language:
        Poem language model object.
        """
        self.structure = structure or [(9, 1), (8, 0), (9, 3), (8, 2)]
        self.source = source
        self.language = language or ArmenianLanguage()

    def _generate(self, content_generator):
        poem = []
        for i, v in enumerate(self.structure):
            if i <= v[1]:
                line = content_generator.get_line(syllable_count=v[0])
            else:
                line_ending = self.language.last_syllable(poem[v[1]], min_char_count=3)
                line = content_generator.end_with(line_ending=line_ending, syllable_count=v[0])
            poem.append(line)
        return poem

    def word_rand_generate(self, source=None):
        source = source or self.source
        if not source:
            raise Exception('Parameter "source" not specified.')
        word_rand = WordRandom(source)
        return self._generate(word_rand)

    def word_rnn_generate(self):
        pass

    def char_rnn_generate(self):
        pass
