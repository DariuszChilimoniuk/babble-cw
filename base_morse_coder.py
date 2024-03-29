from dataclasses import dataclass
from re import finditer

class BaseMorseCoder():

    _morse_patterns = {
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
        '+': '.-.-.', '<AR>': '.-.-.', '<EC>': '.-.-.', '<RN>': '.-.-.', 
        '<AA>': '.-.-', '<RT>': '.-.-',
        '<AS>': '.-...', 
        '<BT>': '-...-', # same as '='
        '<HH>': '........', 
        '<KA>': '-.-.-', '<CT>': '-.-.-',
        '<KN>': '-.--.',  
        '<SK>': '...-.-',
        '<SOS>': '...---...',
    }

    def __init__(self) -> None:
        self.dit = '\u2501'
        self.dah = 3 * '\u2501'
        self.gap1 = ' '
        self.gap3 = 3 * self.gap1
        self.gap7 = 7 * self.gap1

    def _symbol(self, ctx) -> None:
        text = str(ctx)
        if text not in BaseMorseCoder._morse_patterns:
            raise ValueError(f"Unknown symbol '{text}'")
        pattern = BaseMorseCoder._morse_patterns[text]
        last_element_idx = len(pattern) - 1
        for element_idx, element_value in enumerate(pattern):
            match element_value:
                case '.' | '*':
                    self.visit_dit(ctx)
                case '-' | '_':
                    self.visit_dah(ctx)
                case _:
                    continue
            if element_idx != last_element_idx:
                self.visit_gap1(ctx)

    def _tokenize_group(self, ctx) -> None:
        text = str(ctx)
        morse_char_list = list(
            finditer("(<[A-Z]{2,5}>)|([A-Z0-9.,?=/+])", text))
        last_token_idx = len(morse_char_list) - 1
        for token_idx, token_value in enumerate(morse_char_list):
            symbol_ctx = TextContex(
                ctx.text, ctx.start+token_value.start(), ctx.start+token_value.end())
            tmp = str(symbol_ctx)
            self.enter_char(symbol_ctx)
            self._symbol(symbol_ctx)
            self.exit_char(symbol_ctx)
            if token_idx != last_token_idx:
                lettergap_ctx = TextContex(
                    ctx.text, ctx.start+token_value.start(), ctx.start+token_value.end()+1)
                self.visit_gap3(lettergap_ctx)

    def render(self, text, param=None) -> None:
        if param:
            self.param = param
        text = text.upper()
        morse_word_iter = finditer("(\S+)|(\s)", text)
        phrase_ctx = TextContex(text, 0, len(text))
        self.enter_phrase(phrase_ctx)
        for word_match in morse_word_iter:
            word_ctx = TextContex(text, word_match.start(), word_match.end())
            if word_match.group(1):
                # entire word
                self.enter_group(word_ctx)
                self._tokenize_group(word_ctx)
                self.exit_group(word_ctx)
            else:
                # single space
                self.visit_gap7(word_ctx)
        self.exit_phrase(phrase_ctx)

    def enter_phrase(self, ctx) -> None:
        pass

    def exit_phrase(self, ctx) -> None:
        pass

    def enter_group(self, ctx) -> None:
        print(ctx, end='')
        pass

    def exit_group(self, ctx) -> None:
        pass

    def enter_char(self, ctx) -> None:
        pass

    def exit_char(self, ctx) -> None:
        pass

    def visit_dit(self, ctx) -> None:
        print(self.dit, end='')

    def visit_dah(self, ctx) -> None:
        print(self.dah, end='')

    def visit_gap1(self, ctx) -> None:
        print(self.gap1, end='')

    def visit_gap3(self, ctx) -> None:
        print(self.gap3, end='')

    def visit_gap7(self, ctx) -> None:
        print()


@dataclass(frozen=True)
class TextContex:
    text: str
    start: int  # first element of contex
    end: int  # element after the last one in context

    def __str__(self):
        if not self.text:
            return ''
        if self.start < 0:
            return ''
        if self.end <= 0:
            return ''
        if len(self.text) < self.start or len(self.text) < self.end:
            return ''
        return self.text[self.start:self.end]

