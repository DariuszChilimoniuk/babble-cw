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

    def token(self, token, param=None):
        if token not in MorseTranslator.morse_patterns:
            raise ValueError(f"Unknown token '{token}'")
        pattern = MorseTranslator.morse_patterns[token]
        self.token_enter(param, token)
        last_element_idx = len(pattern) - 1
        for element_idx, element_value in enumerate(pattern):
            match element_value:
                case '.' | '*':
                    # yield self.MorseElement.DIT
                    self.dit_visit(param)
                case '-' | '_':
                    # yield self.MorseElement.DAH
                    self.dah_visit(param)
                case _:
                    continue
            if element_idx != last_element_idx:
                # yield self.MorseElement.INTERNAL_GAP
                self.internalgap_visit(param)
        self.token_exit(param, token)

    def tokenize(self, text):
        morse_char_iter = finditer("(<[A-Z]{2,5}>)|([A-Z0-9.,?=/+\n\t ])", text)
        for morse_match in morse_char_iter:
            if morse_match.group(1):
                # phrase
                yield morse_match.group(1)
            else:
                # single character
                yield morse_match.group(2)

    def phrase(self, text, param=None):
        word = False

        def watch_word_exit(word):
            if word:
                self.word_exit(param)
                word = False

        last_character = None
        self.phrase_enter(param)
        for character in self.tokenize(text):
            match character:
                case ' ':
                    # yield self.MorseElement.WORD_GAP
                    word = watch_word_exit(word)
                    self.wordgap_visit(param)
                    last_character = None
                case '\n':
                    # yield self.MorseElement.WORD_GAP
                    word = watch_word_exit(word)
                    self.wordgap_visit(param)
                    # /yield from self.token('=')
                    self.word_enter(param)
                    self.token('=', param)
                    self.word_exit(param)
                    # yield self.MorseElement.WORD_GAP
                    self.wordgap_visit(param)
                    last_character = None
                case '\t':
                    # yield from repeat(self.MorseElement.WORD_GAP, 4)
                    word = watch_word_exit(word)
                    for f in repeat(self.wordgap_visit, 4):
                        f(self)
                    last_character = None
                case _:
                    if last_character:
                        # yield self.MorseElement.LETTER_GAP
                        self.lettergap_visit(param)
                    else:
                        self.word_enter(param)
                        word = True
                    # yield from self.token(character)
                    self.token(character, param)
                    last_character = character
        word = watch_word_exit(word)
        self.phrase_exit(param)

    def phrase_enter(self, param):
        pass

    def phrase_exit(self, param):
        print()

    def word_enter(self, param):
        pass

    def word_exit(self, param):
        pass

    def token_enter(self, param, token):
        self.tmp = ''

    def token_exit(self, param, token):
        if param == 1:
            print(token.center(len(self.tmp), ' '), end='')
        if param == 2:
            print(self.tmp, end='')
        self.tmp = ''

    def dit_visit(self, param):
        self.tmp += self._dit

    def dah_visit(self, param):
        self.tmp += self._dah

    def internalgap_visit(self, param):
        self.tmp += self._intgap

    def lettergap_visit(self, param):
        print(self._lettergap, end='')

    def wordgap_visit(self, param):
        print(self._wordgap, end='')


morse = MorseTranslator()
text = 'CQ DE XYZ <RN> K'
morse.phrase(text, param=1)
morse.phrase(text, param=2)


# morse.token('C')