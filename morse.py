from enum import Enum

class MorseElement(Enum):
    DIT = 1
    DAH = 2
    INTERNAL_GAP = 3
    LETTER_GAP = 4
    WORD_GAP = 5

def morse_character(character):
    if character not in morse_patterns:
        raise ValueError(f'Unknown {character}')
    character_pattern = morse_patterns[character]
    last_element_idx = len(character_pattern) - 1
    for element_idx, element_value in enumerate(character_pattern):
        match element_value:
            case '.' | '*':
                yield MorseElement.DIT
            case '_' | '-':
                yield MorseElement.DAH
            case _:
                continue
        if element_idx != last_element_idx:
            yield MorseElement.INTERNAL_GAP


def morse_phrase(text):
    last_character = None
    for character in text:
        match character:
            case ' ' | '\n':
                yield MorseElement.WORD_GAP
                last_character = None
            case _:
                if last_character:
                    yield MorseElement.LETTER_GAP
                yield from morse_character(character)
                last_character = character


morse_patterns = {
    'A': '.-',
    'B': '_...',
    'C': '_._.',
    'D': '_..',
    'E': '.',
    'F': '.._.',
    'G': '__.',
    'H': '....',
    'I': '..',
    'J': '.___',
    'K': '_._',
    'L': '._..',
    'M': '__',
    'N': '_.',
    'O': '___',
    'P': '.__.',
    'Q': '__._',
    'R': '._.',
    'S': '...',
    'T': '_',
    'U': '.._',
    'V': '..._',
    'W': '.__',
    'X': '_.._',
    'Y': '_.__',
    'Z': '__..',
    '1': '.____',
    '2': '..___',
    '3': '...__',
    '4': '...._',
    '5': '.....',
    '6': '_....',
    '7': '__...',
    '8': '___..',
    '9': '____.',
    '0': '_____',
    '.': '._._._',
    ',': '__..__',
    '?': '..__..',
    '=': '_..._',
    '/': '_..__',
}

for a in morse_phrase('HELLO WORLD'):
    print(a)