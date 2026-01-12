#!/usr/bin/env python3

def capitalize(text, preserve_words):
    """ Capitalize (ie uppercase first letter of) all words except those in preserve_words. """
    return ' '.join(word if word in preserve_words else word.capitalize() for word in text.split())

