from src.poebot.generators.RandomWordGenerator import RandomWordGenerator
from src.poebot.language_analysers.ArmenianLanguage import ArmenianLanguage
from src.poebot.utils import get_poem_default_source


class PoemBase(object):
    def __init__(self, structure=None, source=None, language=None, generator=None):
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
        :param generator
        Word generator object like RnnWordGenerator.
        """
        self.structure = structure or [(9, 1), (8, 0), (9, 3), (8, 2)]
        self.source = source or get_poem_default_source()
        self.language = language or ArmenianLanguage()
        self.generator = generator or RandomWordGenerator(self.source)
        self.last_room = []
        self.poem = []

    def _generate(self):
        poem = []
        no_repetitions = True

        for i, line_config in enumerate(self.structure):
            if i <= line_config[1]:
                line = self.generator.get_line(syllable_count=line_config[0])
            else:
                last_syllable = self.language.get_last_syllable(poem[line_config[1]], min_char_count=3)
                exception_word = poem[line_config[1]].split()[-1]
                line = self.generator.get_line_with_end(line_ending=last_syllable, syllable_count=line_config[0], exception_word=exception_word)
                if (line.split()[-1] == exception_word):
                    no_repetitions = False

            poem.append(line)
        return [poem, no_repetitions]

    def word_rand_generate(self, structure=None):
        if structure:
            self.structure = structure
        for _ in range(10):
            result = self._generate()
            self.last_room = result[0]
            if result[1]:
               break

        self.poem.extend([*self.last_room, ""])

    def to_print(self):
        poem_string = ''
        for line in self.poem:
            poem_string += line + '\n'
        return poem_string[:-1]
