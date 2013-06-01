import argparse
import json
import nltk
from nltk.collocations import BigramCollocationFinder, TrigramCollocationFinder
from nltk.corpus import stopwords
#import extract_clean_tweet_content


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
    parser.add_argument('--plain-text', help='File of plain text')
    args = parser.parse_args()

    items = []
    if args.json_cleaned:
        for line in open(args.json_cleaned):
            items.append(json.loads(line))
    if args.plain_text:
        for line in open(args.plain_text):
            items.append({'tweet': line.strip()})

    # the following is a hacky way of cleaning a tweet but the results do not
    # markedly improve, so I'm commenting this out (maybe to revisit)
    # force a cleaning of the tweet - ignore URL tweets, lowercase, clean some
    # unicode
    #for item in items:
        #cleaned_set = extract_clean_tweet_content.clean_tweets([json.dumps(item)])
        #cleaned_tweet = ""
        #if len(cleaned_set):
            #cleaned_tweet = cleaned_set.pop()
        #item['tweet'] = cleaned_tweet

    top_collocations = extract_top_collocations(items)
    print top_collocations
    top_collocations = extract_top_collocations(items, use_trigrams=True)
    print top_collocations
