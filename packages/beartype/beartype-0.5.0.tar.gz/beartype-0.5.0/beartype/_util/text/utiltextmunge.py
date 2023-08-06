#!/usr/bin/env python3
# --------------------( LICENSE                           )--------------------
# Copyright (c) 2014-2020 Cecil Curry.
# See "LICENSE" for further details.

'''
**Beartype string munging utilities** (i.e., callables transforming passed
strings into new strings with generic string operations).

This private submodule is *not* intended for importation by downstream callers.
'''

# ....................{ IMPORTS                           }....................
import re

# ....................{ CASERS                            }....................
def uppercase_char_first(text: str) -> str:
    '''
    Uppercase *only* the first character of the passed string.

    Whereas the standard :meth:`str.capitalize` method both uppercases the
    first character of this string *and* lowercases all remaining characters,
    this function *only* uppercases the first character. All remaining
    characters remain unmodified.

    Parameters
    ----------
    text : str
        String whose first character is to be uppercased.

    Returns
    ----------
    str
        This string with the first character uppercased.
    '''
    assert isinstance(text, str), '{!r} not string.'.format(text)

    # For great justice!
    return text[0].upper() + text[1:] if text else ''

# ....................{ NUMBERERS                         }....................
def number_lines(text: str) -> str:
    '''
    Passed string munged to prefix each line of this string with the 1-based
    number of that line padded by zeroes out to four digits for alignment.

    Parameters
    ----------
    text : str
        String whose lines are to be numbered.

    Returns
    ----------
    str
        This string with all lines numbered.
    '''
    assert isinstance(text, str), '{!r} not string.'.format(text)

    # For radical benevolence!
    return '\n'.join(
        '(line {:0>4d}) {}'.format(text_line_number, text_line)
        for text_line_number, text_line in enumerate(
            text.splitlines(), start=1)
    )

# ....................{ SUFFIXERS                         }....................
def suffix_unless_suffixed(text: str, suffix: str) -> str:
    '''
    Passed string either suffixed by the passed suffix if this string is not
    yet suffixed by this suffix *or* this string as is otherwise (i.e., if this
    string is already suffixed by this suffix).

    Parameters
    ----------
    text : str
        String to be conditionally suffixed.
    suffix : str
        Suffix to be conditionally appended to this string.

    Returns
    ----------
    str
        Either:

        * If this string is *not* yet suffixed by this suffix, this string
          suffixed by this suffix.
        * Else, this string as is.
    '''
    assert isinstance(text, str), '{!r} not string.'.format(text)
    assert isinstance(suffix, str), '{!r} not string.'.format(suffix)

    # Suffix us up the redemption arc.
    return text if text.endswith(suffix) else text + suffix
