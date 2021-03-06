class ArmenianSymbols:
    LOWER_ALPHABET = {
        'ա', 'բ', 'գ', 'դ', 'ե', 'զ', 'է', 'ը', 'թ',
        'ժ', 'ի', 'լ', 'խ', 'ծ', 'կ', 'հ', 'ձ', 'ղ',
        'ճ', 'մ', 'յ', 'ն', 'շ', 'ո', 'չ', 'պ', 'ջ',
        'ռ', 'ս', 'վ', 'տ', 'ր', 'ց', '&', 'փ', 'ք',
        'և', 'օ', 'ֆ'
    }
    LOWER_VOWELS = {
        'ա', 'ե', 'է', 'ը',
        'ի', 'ո', '&', 'օ'
    }
    PUNCTUATION_MARKS = {',', '․', '։', '՞', '՝', '՜', '՛', '«', '»', '֊', '(', ')', ' '}

    def __init__(self):
        self.LOWER_NON_VOWEL = self.LOWER_ALPHABET - self.LOWER_VOWELS
        self.UPPER_ALPHABET = {i.upper() for i in self.LOWER_ALPHABET}
        self.UPPER_VOWELS = {i.upper() for i in self.LOWER_VOWELS}
        self.UPPER_NON_VOWEL = {i.upper for i in self.LOWER_NON_VOWEL}


class ArmenianLanguage(ArmenianSymbols):
    def __init__(self):
        super().__init__()

    def divide_words(self, line):
        line = ' '.join(line.split())
        return [word.strip("".join(self.PUNCTUATION_MARKS)) for word in line.split(' ')]

    def divided_into_syllables(self, word):
        word = self._normalize_for_algorithm(word)
        syllables = ['']
        word = word[::-1]
        size = len(word)
        index = 0
        while index < size:
            syllables[-1] += word[index]
            if word[index] in self.LOWER_VOWELS:
                try:
                    if word[index + 1] in self.LOWER_NON_VOWEL:
                        if self.LOWER_VOWELS.intersection(set(word[index + 1:])):
                            syllables[-1] += word[index + 1]
                            index += 1
                            syllables.append('')
                        else:
                            syllables[-1] += word[index + 1:]
                            break
                    else:
                        syllables.append('')
                except IndexError:
                    break
            index += 1
        return [self._normalize_for_human(syllable[::-1]) for syllable in syllables][::-1]

    def get_last_syllable(self, line, min_char_count):
        line = self.divided_into_syllables(line)
        line_ending = ''
        while len(line_ending) < min_char_count:
            line_ending = line.pop() + line_ending
        return line_ending.strip()

    def reverse(self, text):
        text = self._normalize_for_algorithm(text)
        text = text[::-1]
        return self._normalize_for_human(text)

    @staticmethod
    def _normalize_for_algorithm(text):
        return text.lower().replace('ու', '&')

    @staticmethod
    def _normalize_for_human(text, capitalize=False):
        text = text.lower().replace('&', 'ու')
        return text.capitalize() if capitalize else text

    @staticmethod
    def clear_text(file_path):
        import re
        with open(file_path, 'r') as f:
            text = f.read()
        cleared_text = re.sub(r'[^ա-ֆԱ-Ֆ ,]', '', text)
        with open(file_path, 'w') as f:
            f.write(cleared_text)
