CodeWhisper
===========

CodeWhisper is yet another parsing library, designed for rapid development and
easy maintenance of complex parsers.  Languages with over a thousand rules and
dozens of token types should parse thousands of strings in under a minute,
without being impossible to understand or debug.

The design is heavily based on Jared Forsyth's CodeTalker, but has been
rebuilt from the ground up in Cython for Python 3, with a slightly different
feature set.  CodeWhisper is not a drop-in replacement, but even complex
grammars should be relatively simple to adapt.

CodeWhisper takes a three-step approach to processing a string: tokenization,
parsing, and translation.


Tokenization
------------

Tokenization is the process of breaking a string down into atomic chunks.
Not every grammar works better with an explicit tokenization step, but for
many grammars, it speeds up the parsing process.

CodeWhisper tokens are defined as subclasses of the `codewhisper.tokens.Token`
class, with a `match` method that determines whether and how much of the input
can be part of that token class.  For example:

```python
class CHARACTER(Token):
    r'''A Token that matches any single character.
    '''#"""#'''
    
    @staticmethod
    def match(text, position):
        return 1
```

The `CHARACTER` class matches any single character.  Because it is generally
useful for many grammars, it is included in the `codewhisper.tokens` module.

The `codewhisper.tokens.CharacterToken` class offers a fast and convenient way
to match a single character from a limited set:

```python
class SYMBOL(CharacterToken):
    characters = ',:[]{}'

class WHITESPACE(CharacterToken):
    characters = ' \n\r\t'
```

When you need to match sets of strings with more than one character, try the
`codewhisper.tokens.StringToken` class:

```python
class CONSTANT(StringToken):
    strings = [
        'true',
        'false',
        'null',
    ]
```

The `codewhisper.tokens` module also contains `DelimitedToken` for finding
strings that start and end with specific characters, `PatternToken` for
finding strings that match a regular expression, and `KeywordToken` for
finding any of a list of strings when they aren't followed by a letter or
number.

For more complex tokens, custom Token subclasses can override the `match`
method:

```python
class INT(Token):
    @classmethod
    def match(cls, text, position):
        if text[position] == "0":
            return 1
        result = None
        for length, c in enumerate(text[position:]):
            if not c.isdigit():
                break
            result = length + 1
        return result
```

By convention, Token subclasses meant to be used by a grammar are given
`ALL_CAPS` names, whereas those meant to be used as base classes are named
with `CapitalizedWords`.  This, however, is merely to make things easier for
the developer; CodeWhisper itself doesn't care what you name anything.


Parsing
-------

Parsing is the process of determining which tokens relate to each other,
and what they might mean.  This is often the slowest of the three steps,
because it may have to consider multiple options before it finds the right way
to interpret the input.  These options are defined by rule functions, using a
syntax reminiscent of Wirth syntax, written in real Python code:

```python
def value(rule):
    rule | STRING | CONSTANT | NUMBER
    rule | json_object | json_list

def json_object(rule):
    rule | ('{', [commas(STRING, ':', value)], '}')

def json_list(rule):
    rule | ('[', [commas(value)], ']')
```

Essentially, each grammar rule is defined by a function with a single
parameter.  That parameter should be piped with one or more elements, where
each elements may be:

- A token class, matching any token of that class;
- A string, matching any token with that exact string as its value;
- A grammar rule, matching if and only if the rule does;
- A tuple of elements, matching if each of its elements does, in that exact sequence;
- A list of elements, matching each of its elements, or without consuming any tokens;
- A set of elements, matching if any one of its elements matches; or
- A `codewhisper.parsing.Parser` instance, for more complex behavior.

Notably, elements may be computed when the rule function is run.  For example,
the `commas` function used above, defined in `codewhisper.special`, is a
normal Python function that that happens to return a tuple.  Since the rule
function is only run when it first gets used by a Grammar or another rule
function, it can refer to itself, even indirectly, or to rules defined later.

Each rule tries to match the token string against each of its options, in
order.  Like a parsing expression grammar (PEG), if a rule is ambiguous, the
first available option is used if possible.  Unlike a PEG, if that option
doesn't allow an outer rule to parse the remaining tokens, subsequent options
that match a different number of tokens will be attempted.  This makes
CodeWhisper slightly slower than a good PEG implementation for unambiguous
grammars, but makes accidental ambiguity much easier to handle.

Special caveats apply to sets.  They offer a convenient syntax for including a
group of options inside a larger sequence, but they don't define an order, and
they can't include lists or tuples of lists.  If order is important, or a
choice includes optional items, use either a subrule or a Parser instance.
For example:

```python
def json_float(rule):
    integral = {"0", (Notahead("0"), Plus(DIGIT))}
    fractional = (".", Plus(DIGIT))
    exponential = ({"e", "E"}, [{"-", "+"}], Plus(DIGIT))
    rule | (["-"], integral, Parser((fractional, [exponential]), exponential))
```

Here, sets are used for the `integral` and `exponential` portions of the rule,
but since lists are unhashable, `(fractional, [exponential])` uses an explicit
Parser.  That it happens to always check for a decimal point before checking
for an exponent is a minor bonus.

That example also showcases `Notahead` and `Plus`, which use Parser subclasses
to match any number of digits, in one case only when the first digit is
non-zero. They're found in the `codetalker.special` module, along with
`Avoid`, `Consume`, `Lookahead`, `Seek`, `Sequence`, and `Star`.

By convention, rule functions are given `lower_case` names, to distinguish
them from token classes.  Parser subclasses and functions that transform
parser sequences have been given `TitleCase` names, though the fact that they
get called within a rule function also helps distinguish them from rules and
tokens, which can be important for translation purposes.


Translation
-----------

Parse trees by themselves aren't very useful, so the Grammar class offers a
way to translate them into what you really want.  By default, a token will be
translated into its string value, but that can be overridden:

```python
class NUMBER(PatternToken):
    pattern = r"(?:0|[1-9][0-9]*)(?:\.[0-9]+|)(?:[eE][-+]?[0-9]+|)"
    
    def translate(self, scope):
        return float(self.value)
```

Rules are by default translated into a list of translated tokens and subrules.
To get a subset of those, assign a list of rules and/or token classes to
`rule.result`:

```python
def json_list(rule):
    rule | ('[', [{commas(value), WHITESPACE}], ']')
    rule.result = [value]
```

A single rule or token class can be selected by assigning just that item.
If no such item exists in the final parse, it will end up as None instead.
A single one of multiple rules or tokens can be chosen by assigning a set:

```python
def value(rule):
    val = {CONSTANT, json_object, json_list, json_int, json_float, json_string}
    rule | ([WHITESPACE], val, [WHITESPACE])
    rule.result = val
```

Multiple such items can be combined into a dictionary by assigning one to
`rule.result` with such a list, set, rule, or token class as each value:

```python
def expression(rule):
    rule | (term, Star("+", term), ["-", term])
    rule.result = {
        'operators': [SYMBOL],
        'terms': [term],
    }
```

For more interesting translations, the result can be passed to a translator
function:

```python
def json_int(rule):
    rule | (["-"], "0")
    rule | (["-"], Notahead("0"), Plus(DIGIT))
    def int_translator(node, scope):
        return int("".join(token.value for token in node))
    rule.translator = int_translator
```

Note, however, that the tokens and subrules are not translated before being
passed to that function.  It can translate them by using `scope.translate`
with or without extra information:

```python
def json_object(rule):
    rule | ('{', [commas(json_string, ':', value)], '}')
    rule.result = {'keys': [json_string], 'values': [value]}
    def object_translator(node, scope):
        return {
            scope.translate(key): scope.translate(value)
            for key, value in zip(node['keys'], node['values'])
        }
    rule.translator = object_translator
```


Grammar
-------

Each of those steps are governed by the Grammar class:

```python
tokens = [SYMBOL, WHITESPACE, CONSTANT, NUMBER, STRING]
grammar = Grammar(start=value, tokens=tokens, ignore=[WHITESPACE])
result = grammar.parse(text)
```

Each grammar's `start` rule is function defining the language that the text
must match in order to parse successfully.  It and any other rules it uses
will be evaluated as part of the Grammar creation, so they must already exist.
Each grammar rule will be evaluated only once, even if it is used in multiple
grammars.

The list of `tokens` will be used to tokenize the text.  Each token class will
be checked in order; if two or more would match at the same position in the
text, the first one in the list takes precedence.

Any tokens in the optional `ignore` list will be ignored by grammar rules,
essentially as if they didn't exist.  Instead, they will be added to the
`ignored` attribute of the following token.  As a convenience,
`codewhisper.tokens.join_tokens` will include the value of any ignored tokens
within the sequence passed to it.

The `parse` function runs unicode text through tokenization, parsing, and
translation.  It is not intended to accept bytestrings, but pull requests that
can make it do so will be considered.


Examples
--------

The `examples` directory contains a few working grammars, including two
different ways to parse JavaScript Object Notation.  These do not, however,
showcase the full range of the parser, much less the special functions.
Indeed, this parser is probably at its best with the kind of large, complex
system that wouldn't fit well in a single file.
