from enum import Enum
from itertools import repeat
from re import finditer


class MorseElement(Enum):
    DIT = 1
    DAH = 2
    INTERNAL_GAP = 3
    LETTER_GAP = 4
    WORD_GAP = 5

def translate_token(token):
    if token not in morse_patterns:
        raise ValueError(f"Unknown token '{token}'")
    pattern = morse_patterns[token]
    last_element_idx = len(pattern) - 1
    for element_idx, element_value in enumerate(pattern):
        match element_value:
            case '.' | '*':
                yield MorseElement.DIT
            case '-' | '_':
                yield MorseElement.DAH
            case _:
                continue
        if element_idx != last_element_idx:
            yield MorseElement.INTERNAL_GAP

def tokenize(text):
    morse_char_iter = finditer("(<[A-Z]{2,5}>)|([A-Z0-9.,?=/+\n\t ])", text)
    for morse_match in morse_char_iter:
        if morse_match.group(1):
            # phrase
            yield morse_match.group(1)
        else:
            # single character
            yield morse_match.group(2)

def translate_phrase(text):
    last_character = None
    for character in tokenize(text):
        match character:
            case ' ':
                yield MorseElement.WORD_GAP
                last_character = None
            case '\n':
                yield MorseElement.WORD_GAP
                yield from translate_token('=')
                yield MorseElement.WORD_GAP
                last_character = None
            case '\t':
                yield from repeat(MorseElement.WORD_GAP, 8)
                last_character = None
            case _:
                if last_character:
                    yield MorseElement.LETTER_GAP
                yield from translate_token(character)
                last_character = character


morse_patterns = {
    # LETTERS
    'A': '.-',
    'B': '-...',
    'C': '-.-.',
    'D': '-..',
    'E': '.',
    'F': '..-.',
    'G': '--.',
    'H': '....',
    'I': '..',
    'J': '.---',
    'K': '-.-',
    'L': '.-..',
    'M': '--',
    'N': '-.',
    'O': '---',
    'P': '.--.',
    'Q': '--.-',
    'R': '.-.',
    'S': '...',
    'T': '-',
    'U': '..-',
    'V': '...-',
    'W': '.--',
    'X': '-..-',
    'Y': '-.--',
    'Z': '--..',
    # DIGITS
    '1': '.----',
    '2': '..---',
    '3': '...--',
    '4': '....-',
    '5': '.....',
    '6': '-....',
    '7': '--...',
    '8': '---..',
    '9': '----.',
    '0': '-----',
    # PUNCTATION
    '.': '.-.-.-',
    ',': '--..--',
    '?': '..--..',
    '=': '-...-',
    '/': '-..--',
    # NONSTANDARD
    '+':  '.-.-.',
    '<AR>': '.-.-.',
    '<AS>':  '.-...',
    '<BT>': '-...-',
    '<HH>': '........',
    '<KN>': '-.--.',
    '<SK>': '...-.-',
    '<SOS>': '...---...',
}

for a in translate_phrase('CQ DE XYZ <BT>'):
    print(a)

# for a in translate_token('C'):
#     print(a)