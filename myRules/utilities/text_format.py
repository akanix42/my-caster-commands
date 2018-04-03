# -*- mode: python -*-
# (c) Copyright 2015 by James Stout
# Licensed under the LGPL, see <http://www.gnu.org/licenses/>

#---------------------------------------------------------------------------
# Here we define various functions for formatting text.
# Each of these functions must have a docstring which defines its
#  spoken-form.  This docstring must include the "<dictation>" extra.
#  See below for various examples.

import re
import _text_utils as text

# Format: some_words
def format_score(dictation):          # Function name must start with "format_".
    """ score <dictation> """         # Docstring defining spoken-form.
    return "_".join(text.split_dictation(dictation))  # Put underscores between words.

# Format: SomeWords
def format_pascal(dictation):
    """ studley <dictation> """
    words = [word.capitalize() for words in text.split_dictation(dictation)
             for word in re.findall(r"(\W+|\w+)", words)]
    return "".join(words)

# Format: somewords
def format_one_word(dictation):
    """ [all] one word <dictation> """
    return "".join(text.split_dictation(dictation))

# Format: SOMEWORDS
def format_upper_one_word(dictation):
    """ upper one word <dictation> """
    words = [word.upper() for word in text.split_dictation(dictation)]
    return "".join(words)

# Format: SOME_WORDS
def format_upper_score(dictation):
    """ upper score <dictation> """
    words = [word.upper() for word in text.split_dictation(dictation)]
    return "_".join(words)

# Format: SOME WORDS
def format_upper(dictation):
    """ upper <dictation> """
    words = [word.upper() for word in text.split_dictation(dictation)]
    return " ".join(words)

# Format: someWords
def format_camel(dictation):
    """ camel <dictation> """
    words = text.split_dictation(dictation)
    return words[0] + "".join(w.capitalize() for w in words[1:])

# Format: some-words
def format_dashes(dictation):
    """ dashes <dictation> """
    return "-".join(text.split_dictation(dictation))

# Format: some words
def format_spaces(dictation):
    """ spaces <dictation> """
    return " ".join(text.split_dictation(dictation))

