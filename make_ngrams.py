#!/usr/bin/env python
"""Turn a tweet into lists of capitalised words"""
# -*- coding: utf-8 -*-
import string
import collections
from ttp import ttp


def get_cleaned_capitalised_word_sequences(sentence):
    """Turn a tweet into a lists of adjacent capitalised words"""
    sent = remove_urls(sentence)
    sentences = lowercase_split(sent)
    capitalised_words = get_capitalised_word_sequences(sentences)
    return capitalised_words


def remove_urls(s):
    p = ttp.Parser()
    result = p.parse(s)
    for url in result.urls:
        s = s.replace(url, "")
    return s


def flatten(l):
    """Flatten arbitrary depth containers of containers"""
    # attrib: http://stackoverflow.com/a/2158532/18688
    for el in l:
        if isinstance(el, collections.Iterable) and not isinstance(el, basestring):
            for sub in flatten(el):
                yield sub
        else:
            yield el


def lowercase_sentence_start_if_required(sentence):
    nbr_capital_letters = [s for s in sentence if s in string.ascii_uppercase]
    if len(nbr_capital_letters) == 1:
        sentence = sentence[0].lower() + sentence[1:]
    return sentence


def lowercase_split(s):
    """Lowercase capital sentence starts, return sentences"""
    sentences = s.split(".")
    for splits in ["!", "?", ":", ";", ","]:
        sentences = [sent.split(splits) for sent in sentences]
        sentences = flatten(sentences)
        sentences = [sent.strip() for sent in sentences]
    # keep >=2 char words if they start with a capital letter
    #import pdb; pdb.set_trace()
    sentences = [lowercase_sentence_start_if_required(sentence) for sentence in sentences if len(sentence) > 1]
    #sentences = [sent[0].lower() + sent[1:] for sent in sentences if len(sent) > 1]
    return sentences


def stopword(word):
    return word in set(["I"])


def get_capitalised_word_sequences(sentences):
    """Build lists of capitalised word sequences"""
    result = []
    for sentence in sentences:
        seq = []
        for word in sentence.split():
            if word[0] in string.ascii_uppercase:
                if not stopword(word):
                    seq.append(word)
            else:
                if len(seq):
                    result.append(seq)
                seq = []
        if len(seq):
            result.append(seq)
    return result
