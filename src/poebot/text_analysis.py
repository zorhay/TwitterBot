class LanguageModelBase(object):
    pass


class ArmenianLanguage(LanguageModelBase):
    lower_alphabet = {
        'ա', 'բ', 'գ', 'դ', 'ե', 'զ', 'է', 'ը', 'թ',
        'ժ', 'ի', 'լ', 'խ', 'ծ', 'կ', 'հ', 'ձ', 'ղ',
        'ճ', 'մ', 'յ', 'ն', 'շ', 'ո', 'չ', 'պ', 'ջ',
        'ռ', 'ս', 'վ', 'տ', 'ր', 'ց', '&', 'փ', 'ք',
        'և', 'օ', 'ֆ'
    }
    lower_vowels = {
        'ա', 'ե', 'է', 'ը',
        'ի', 'ո', '&', 'օ'
    }
    lower_non_vowel = lower_alphabet - lower_vowels

    upper_alphabet = {i.upper() for i in lower_alphabet}
    upper_vowels = {i.upper() for i in lower_vowels}
    upper_non_vowel = {i.upper for i in lower_non_vowel}

    punctuation_marks = {',', '․', '։', '՞', '՝', '՜', '՛', '«', '»', '֊', '(', ')', ' '}

    def divide_words(self, line):
        while '  ' in line:
            line = line.replace('  ', ' ')
        return [word.strip("".join(self.punctuation_marks)) for word in line.split(' ')]

    @staticmethod
    def _normalize_for_algorithm(text):
        text = text.lower()
        while 'ու' in text:
            text = text.replace('ու', '&')
        return text

    @staticmethod
    def _normalize_for_human(text, capitalize=False):
        text = text.lower()
        while '&' in text:
            text = text.replace('&', 'ու')
        return text.capitalize() if capitalize else text

    def divided_into_syllables(self, word):
        word = self._normalize_for_algorithm(word)
        syllables = ['']
        word = word[::-1]
        size = len(word)
        index = 0
        while index < size:
            syllables[-1] += word[index]
            if word[index] in self.lower_vowels:
                try:
                    if word[index+1] in self.lower_non_vowel:
                        if self.lower_vowels.intersection(set(word[index+1:])):
                            syllables[-1] += word[index+1]
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

    def last_syllable(self, line, min_char_count):
        line = self.divided_into_syllables(line)
        line_ending = ''
        while len(line_ending) < min_char_count:
            line_ending = line.pop() + line_ending
        return line_ending.strip()

    def reverse(self, text):
        text = self._normalize_for_algorithm(text)[::-1]
        text = text[::-1]
        return self._normalize_for_human(text)


if __name__ == '__main__':
    pass
