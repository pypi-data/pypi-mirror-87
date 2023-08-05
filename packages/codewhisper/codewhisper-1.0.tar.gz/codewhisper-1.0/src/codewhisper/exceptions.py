def listed(items, conjunction='and', default='nothing'):
    items = [str(item) for item in items]
    if items:
        bits = [items.pop(0)]
        if len(items) > 1:
            bits.append(',')
        while len(items) > 1:
            bits.extend([' ', items.pop(0), ','])
        if items:
            bits.extend([' ', conjunction, ' ', items.pop(0)])
        result = ''.join(bits)
    else:
        result = default
    return result


class WhisperException(Exception):
    pass


class RuleError(WhisperException, SyntaxError):
    pass


class InputError(ValueError, Exception):
    pass

class ParseError(InputError):
    def __init__(self, text, token, expected=None):
        message = f"Unable to parse {token} at line {token.line}, character {token.character}; expected {listed(sorted(expected), 'or')}"
        super().__init__(message)
        self.text = text
        self.token = token
        self.expected = expected

class TokenizationError(InputError):
    def __init__(self, text, line, character, snippet):
        message = f"Unknown token at line {line}, character {character}: {snippet!r}"
        super().__init__(message)
        self.text = text
        self.line = line
        self.character = character
