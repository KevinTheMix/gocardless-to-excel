#!/usr/bin/env python3

def capitalize(text, keep_words):
    return ' '.join(word if word in keep_words else word.capitalize() for word in text.split())

