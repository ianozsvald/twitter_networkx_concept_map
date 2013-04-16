#!/usr/bin/env python
"""Extract tweets between a set period (using filtering)"""
# -*- coding: utf-8 -*-
# http://www.python.org/dev/peps/pep-0263/
import datetime
import argparse
import pytz
import dateutil.parser as dt_parser
import functools
import json
import tweet_generators


def filter_until(tweets, filter_from, filter_to):
    for tweet in tweets:
        if tweet['created_at'] < filter_to:
            if tweet['created_at'] > filter_from:
                yield tweet
        else:
            raise StopIteration


if __name__ == "__main__":
    filter_from = datetime.datetime.now() - datetime.timedelta(days=30)
    filter_from = filter_from.replace(tzinfo=pytz.utc)
    #filter_from_str = time.strftime("%Y-%m-%dT%H:%M%Z", filter_from.timetuple())
    filter_from_str = filter_from.isoformat()
    filter_to = datetime.datetime.now()
    filter_to = filter_to.replace(tzinfo=pytz.utc)
    filter_to_str = filter_to.isoformat()
    #filter_to_str = time.strftime("%Y-%m-%dT%H:%M", filter_to.timetuple())
    parser = argparse.ArgumentParser(description='Extract information from streaming tweet set')
    parser.add_argument('--json-raw', nargs="*", help='Input to analyse e.g. tweets.json')
    parser.add_argument('--ff', type=str, default=filter_from_str, help="Filter From date range, defaults to '--ff %s'" % (filter_from_str))
    parser.add_argument('--ft', type=str, default=filter_to_str, help="Filter To date range, defaults to '--ff %s'" % (filter_to_str))
    parser.add_argument('--text-file', help="Filename for just the tweet update text, one per line e.g. '--updates-file tweetsonly.txt'")
    parser.add_argument('--output', "-o", help="Output to write e.g. -o coords.txt")
    args = parser.parse_args()

    print args.json_raw

    all_json_lines = tweet_generators.files(args.json_raw)
    tweets = tweet_generators.get_tweets(all_json_lines)
    stream = tweet_generators.get_tweet_body(tweets)

    # default will be to look at the last 30 days only
    if args.ff:
        filter_from = dt_parser.parse(args.ff)
        filter_from = filter_from.replace(tzinfo=pytz.utc)
    if args.ft:
        filter_to = dt_parser.parse(args.ft)
        filter_to = filter_to.replace(tzinfo=pytz.utc)
    print("Filtering from {} to {}".format(filter_from, filter_to))

    filter_until_partial = functools.partial(filter_until, filter_from=filter_from, filter_to=filter_to)
    stream = filter_until_partial(stream)

    if args.output:
        outfile = open(args.output, "w")
        dthandler = lambda obj: obj.isoformat() if isinstance(obj, datetime.datetime) else None
        for tweet in stream:
            outfile.write(json.dumps(tweet, default=dthandler) + "\n")
        outfile.close()

    if args.text_file:
        outfile = open(args.text_file, "w")
        for tweet in stream:
            text = tweet['text'].encode('utf-8')
            outfile.write(text + "\n")
        outfile.close()
