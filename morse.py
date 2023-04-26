from enum import Enum
from itertools import repeat
from re import finditer


class MorseTranslator:

    morse_patterns = {
        # LETTERS
        'A': '.-', 'B': '-...', 'C': '-.-.', 'D': '-..', 'E': '.',
        'F': '..-.', 'G': '--.', 'H': '....', 'I': '..',  'J': '.---',
        'K': '-.-', 'L': '.-..', 'M': '--', 'N': '-.', 'O': '---',
        'P': '.--.', 'Q': '--.-', 'R': '.-.', 'S': '...', 'T': '-', 
        'U': '..-', 'V': '...-', 'W': '.--', 'X': '-..-', 'Y': '-.--',
        'Z': '--..',
        # DIGITS
        '1': '.----', '2': '..---', '3': '...--', '4': '....-', '5': '.....',
        '6': '-....', '7': '--...', '8': '---..', '9': '----.', '0': '-----',
        # PUNCTATION
        '.': '.-.-.-', ',': '--..--', '?': '..--..', '=': '-...-', '/': '-..--',
        # NONSTANDARD
        '+': '.-.-.', '<AR>': '.-.-.', '<AS>': '.-...', '<BT>': '-...-', 
        '<HH>': '........', '<KN>': '-.--.', '<RN>': '.-.-.', '<SK>': '...-.-',
        '<SOS>': '...---...',
    }

    class MorseElement(Enum):
        DIT = 1
        DAH = 2
        INTERNAL_GAP = 3
        LETTER_GAP = 4
        WORD_GAP = 5

    def __init__(self) -> None:
        self._dit = '\u2501'
        self._dah = '\u2501\u2501\u2501'
        self._intgap = ' '
        self._lettergap = '   '
        self._wordgap = '       '

    def token(self, text, param=None):
        if text not in MorseTranslator.morse_patterns:
            raise ValueError(f"Unknown token '{text}'")
        pattern = MorseTranslator.morse_patterns[text]
        last_element_idx = len(pattern) - 1
        for element_idx, element_value in enumerate(pattern):
            match element_value:
                case '.' | '*':
                    # yield self.MorseElement.DIT
                    self.dit_visit(text, param)
                case '-' | '_':
                    # yield self.MorseElement.DAH
                    self.dah_visit(text, param)
                case _:
                    continue
            if element_idx != last_element_idx:
                # yield self.MorseElement.INTERNAL_GAP
                self.internalgap_visit(text, param)

    def tokenize(self, text, param):
        morse_char_list = list(finditer("(<[A-Z]{2,5}>)|([A-Z0-9.,?=/+])", text))
        last_token_idx = len(morse_char_list) - 1
        for token_idx, token_value in enumerate(morse_char_list):
            self.token_enter(token_value.group(0), param)
            self.token(token_value.group(0), param)
            self.token_exit(token_value.group(0), param)
            if token_idx != last_token_idx:
                self.lettergap_visit(token_value.group(0), param)

    def phrase(self, text, param=None):
        morse_word_iter = finditer("(\S+)|(\s)", text)
        self.phrase_enter(text, param)
        for word_match in morse_word_iter:
            if word_match.group(1):
                # entire word
                self.word_enter(word_match.group(1), param)
                self.tokenize(word_match.group(1), param)
                self.word_exit(word_match.group(1), param) 
            else:
                # single space
                self.wordgap_visit(word_match.group(2), param)
        self.phrase_exit(text, param)

    def phrase_enter(self, text, param):
        pass

    def phrase_exit(self, text, param):
        print()

    def word_enter(self, text, param):
        pass

    def word_exit(self, text, param):
        pass

    def token_enter(self, text, param):
        self.tmp = ''

    def token_exit(self, text, param):
        if param == 1:
            print(text.center(len(self.tmp), ' '), end='')
        if param == 2:
            print(self.tmp, end='')
        self.tmp = ''

    def dit_visit(self, text, param):
        self.tmp += self._dit

    def dah_visit(self, text, param):
        self.tmp += self._dah

    def internalgap_visit(self, text, param):
        self.tmp += self._intgap

    def lettergap_visit(self, text, param):
        print(self._lettergap, end='')

    def wordgap_visit(self, text, param):
        print(self._wordgap, end='')


morse = MorseTranslator()
text = 'CQ DE XYZ <RN> K'
morse.phrase(text, param=1)
morse.phrase(text, param=2)
