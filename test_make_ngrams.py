#!/usr/bin/env python
"""1 liner to explain this project"""
# -*- coding: utf-8 -*-
import unittest
import make_ngrams


class Test(unittest.TestCase):
    def setUp(self):
        pass

    def test_lowercase_sentence_start_if_required(self):
        # take a prepared sentence, only lowercase first char if the rest of
        # the sentence isn't capitalised
        s = "Hello there"
        e = "hello there"
        r = make_ngrams.lowercase_sentence_start_if_required(s)
        self.assertEqual(r, e)

        s = "Hello There"
        e = "Hello There"
        r = make_ngrams.lowercase_sentence_start_if_required(s)
        self.assertEqual(r, e)

    def test_lowercasing1(self):
        #s = "Hello There! This is a test"
        #e = ["Hello There", "this is a test"]
        #r = make_ngrams.lowercase_split(s)
        #self.assertEqual(r, e)

        s = "hello there! This is a test"
        e = ["hello there", "this is a test"]
        r = make_ngrams.lowercase_split(s)
        self.assertEqual(r, e)

        s = "hello there! This? is: a test; here, over here"
        e = ["hello there", "this", "is", "a test", "here", "over here"]
        r = make_ngrams.lowercase_split(s)
        self.assertEqual(r, e)

        s = "hello there. this is a test"
        e = ["hello there", "this is a test"]
        r = make_ngrams.lowercase_split(s)
        self.assertEqual(r, e)

        s = "hello there. This is a test"
        e = ["hello there", "this is a test"]
        r = make_ngrams.lowercase_split(s)
        self.assertEqual(r, e)

        s = "% of tutorials at PyData 2013 that use IPython Notebook to do demos and keep history of explorations? 100"
        e = ["% of tutorials at PyData 2013 that use IPython Notebook to do demos and keep history of explorations", "100"]
        r = make_ngrams.lowercase_split(s)
        self.assertEqual(r, e)

        s = "Me taking a hit of an #ipython acid tab at #pydata whilst Peter @norvig talks. I see multicolor lambda funcs @ivanov "
        e = ["Me taking a hit of an #ipython acid tab at #pydata whilst Peter @norvig talks", "i see multicolor lambda funcs @ivanov"]
        r = make_ngrams.lowercase_split(s)
        self.assertEqual(r, e)

    def test_url_removal(self):
        s = "Me taking a hit of an #ipython acid tab at #pydata whilst Peter @norvig talks. I see multicolor lambda funcs @ivanov http://pic.twitter.com/pEERrxscZU"
        e = "Me taking a hit of an #ipython acid tab at #pydata whilst Peter @norvig talks. I see multicolor lambda funcs @ivanov "
        r = make_ngrams.remove_urls(s)
        self.assertEqual(r, e)

    def test_url_removal2(self):
        s = ["this Looks Good"]
        e = [["Looks", "Good"]]
        r = make_ngrams.get_capitalised_word_sequences(s)
        self.assertEqual(r, e)

        s = ["me taking a hit of an #ipython acid tab at #pydata whilst Peter @norvig talks. i see multicolor lambda funcs @ivanov http://pic.twitter.com/pEERrxscZU"]
        e = [["Peter"]]
        r = make_ngrams.get_capitalised_word_sequences(s)
        self.assertEqual(r, e)

    def test_everything(self):
        s = "Me taking a hit of an #ipython acid tab at #pydata whilst Peter @norvig talks. I see multicolor lambda funcs @ivanov http://pic.twitter.com/pEERrxscZU"
        e = [["Me"], ["Peter"]]
        r = make_ngrams.get_cleaned_capitalised_word_sequences(s)
        self.assertEqual(r, e)

        s = "Stop talking about #pycon. Makes me sad."
        e = []
        r = make_ngrams.get_cleaned_capitalised_word_sequences(s)
        self.assertEqual(r, e)

        s = "Loving this Live KeyNote. Having fun at #PyData today looking at Lots Of Interesting Stuff"
        e = [["Loving"], ["Live", "KeyNote"], ["Having"], ["Lots", "Of", "Interesting", "Stuff"]]
        r = make_ngrams.get_cleaned_capitalised_word_sequences(s)
        self.assertEqual(r, e)


if __name__ == "__main__":
    unittest.main()
