import argparse
import json
import nltk
from nltk.collocations import BigramCollocationFinder, TrigramCollocationFinder
from nltk.corpus import stopwords

en_stopwords = set(w for w in stopwords.words('english'))


def tweet_as_terms(tweets):
    tweets = tweets.lower()
    tweets = tweets.replace('-', ' ')
    tweets = tweets.replace('"', ' ')

    tweets_split = [term for term in tweets.split() if term not in en_stopwords]
    return tweets_split


def extract_top_collocations(json_cleaned, return_top_n=10, use_trigrams=False):
    if use_trigrams:
        measures = nltk.collocations.TrigramAssocMeasures()
    else:
        measures = nltk.collocations.BigramAssocMeasures()

    items = json_cleaned
    tweets = "\n".join(item['tweet'] for item in items)
    tweets_split = tweet_as_terms(tweets)

    # change this to read in your data
    if use_trigrams:
        finder = TrigramCollocationFinder.from_words(tweets_split)
    else:
        finder = BigramCollocationFinder.from_words(tweets_split)

    # only bigrams that appear 3+ times
    finder.apply_freq_filter(3)

    # return the 10 n-grams with the highest PMI
    top_collocations = finder.nbest(measures.pmi, return_top_n)
    return top_collocations


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Extract information from streaming tweet set')
    parser.add_argument('--json-cleaned', help='Cleaned input json')
    args = parser.parse_args()

    items = []
    for line in open(args.json_cleaned):
        items.append(json.loads(line))
    top_collocations = extract_top_collocations(items)
    #print finder.nbest(trigram_measures.pmi, 10)
    print top_collocations
