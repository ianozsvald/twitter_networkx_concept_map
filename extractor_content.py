#!/usr/bin/env python
"""1 liner to explain this project"""
# -*- coding: utf-8 -*-
# http://www.python.org/dev/peps/pep-0263/
import argparse
import json
import sys
import logging
from ttp import ttp
import maksim_utils
import networkx as nx
import matplotlib.pyplot as plt

plt.__str__  # silly way to stop pylint error (use plt in IPython)

# Usage:
# load datasets into memory, also output a text file for later parsing
# $ %run extractor_content.py --json-raw /media/2ndDrive/data/streaming-twitter-data/pycon/tweets_pycon0.json /media/2ndDrive/data/streaming-twitter-data/pycon/tweets_pycon.json -o clean_pycon.json


LOG_FILE = "extractor.log"
logging.basicConfig(filename=LOG_FILE, level=logging.DEBUG)


def get_tweets(tweets):
    """Generator to return entry from valid JSON lines"""
    for tweet in tweets:
        # load with json to validate
        try:
            tw = json.loads(tweet)
            yield tw
        except ValueError as err:
            logging.debug("Odd! We have a ValueError when json.loads(tweet): %r" % repr(err))


def filter_http(tweets):
    """Ignore links with http links (can be useful to ignore spam)"""
    for tweet in tweets:
        try:
            if 'http' not in tweet['text']:
                yield tweet
        except KeyError as err:
            logging.debug("Odd! We have a KeyError: %r" % repr(err))


def get_tweet_text(tweets):
    """Get tweets, ignore ReTweets"""
    for tweet in tweets:
        try:
            if 'text' in tweet:
                if not tweet['text'].startswith('RT'):
                    yield tweet
        except KeyError as err:
            logging.debug("Odd! We have a KeyError: %r" % repr(err))


def get_useful_information(tweet_parser, tweets):
    """Extract a set of useful information about the tweets that we want to graph"""
    for tweet in tweets:
        text = tweet['text']
        # replace newlines with nothing
        text = text.replace('\r', '')
        text = text.replace('\n', '')

        screen_name = tweet['user']['screen_name'].lower()
        result = tweet_parser.parse(text)
        hashtags = [tag.lower() for tag in result.tags]
        users = [user.lower() for user in result.users]
        #items = {'hashtags': ['#' + h for h in hashtags], 'tweet': text, 'screen_name': screen_name, 'users': ['@' + usr for usr in users]}
        items = {'hashtags': ['#' + h for h in hashtags], 'screen_name': screen_name, 'users': ['@' + usr for usr in users]}
        yield items


def files(file_list):
    """Yield lines from a list of input json data files"""
    for filename in file_list:
        f = open(filename)
        for line in f:
            yield line


def add_node(G, node_name):
    """Add a node to graph, make a label, increase weight if seen before"""
    label = node_name[1:]
    if node_name.startswith('#'):
        typ = 0
    if node_name.startswith('@'):
        typ = 1

    if not G.has_node(node_name):
        G.add_node(node_name, label=label, type=typ, weight=-1)
    G.node[node_name]['weight'] += 1


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Extract information from streaming tweet set')
    parser.add_argument('--json-raw', nargs="*", help='Input to analyse e.g. tweets.json')
    parser.add_argument('--output', "-o", help="Output to write (else stdout) e.g. -o pycon.json")
    parser.add_argument('--json-cleaned', help='Cleaned input json')
    parser.add_argument('--remove-nodes', nargs="*", help='Remove named nodes e.g. "--remove-nodes #pycon @pycon"')
    parser.add_argument('--draw-networkx', action="store_true", help='Draw the graph using networkX')
    parser.add_argument('--write-graphml', help='Filename for graphml output')
    args = parser.parse_args()

    if args.json_raw:
        tweet_parser = ttp.Parser()

        # stream through a list of user-provided filenames
        all_json_lines = files(args.json_raw)
        tweets = get_tweets(all_json_lines)

        # get tweets (ignore rubbish from streaming api), extract useful info
        stream = get_tweet_text(tweets)
        stream = get_useful_information(tweet_parser, stream)
        if args.output:
            output = open(args.output, 'w')
        else:
            output = sys.stdout  # use stdout if no file specified
        items = []
        for item in stream:
            outstr = json.dumps(item)
            output.write("%s\n" % (outstr))
            items.append(item)

        if args.output:
            output.close()  # don't close sys.stdout by mistake

    if args.json_cleaned:
        items = []
        for line in open(args.json_cleaned):
            items.append(json.loads(line))

        hashtag_net = nx.Graph()

        for item in items:
            # combine hashtags and users into one list of things to pair up
            all_items = item['hashtags'] + item['users']
            for t1 in all_items:
                for t2 in all_items:
                    if t1 is not t2:
                        add_node(hashtag_net, t1)
                        add_node(hashtag_net, t2)
                        maksim_utils.add_or_inc_edge(hashtag_net, t1, t2)

        for node in hashtag_net.nodes():
            if node.startswith('@'):
                if hashtag_net.node[node]['weight'] < 50:
                    hashtag_net.remove_node(node)
            if node.startswith('#'):
                if hashtag_net.node[node]['weight'] < 2:
                    hashtag_net.remove_node(node)

        # remove nodes that too many people might be connected to
        for removal in args.remove_nodes:
            hashtag_net.remove_node(removal)

        # remove singularly connected nodes until none left
        while True:
            nbr_of_nodes = hashtag_net.number_of_nodes()
            logging.info("Trimming, currently we have %d nodes" % (nbr_of_nodes))
            hashtag_net = maksim_utils.trim_degrees(hashtag_net)
            if hashtag_net.number_of_nodes() == nbr_of_nodes:
                break

        if args.draw_networkx:
            # we can draw a network using networkx, optionally using graphviz
            # for improved layout
            graphviz = True
            try:
                import pygraphviz
                pygraphviz.release.version  # stupid statement to avoid pylint error
            except ImportError as err:
                graphviz = False
            if graphviz:
                logging.info("Drawing using GraphViz layout engine")
                nx.draw_graphviz(hashtag_net)
            else:
                logging.info("Drawing using NetworkX layout engine")
                nx.draw_networkx(hashtag_net)
            plt.show()

        if args.write_graphml:
            nx.write_graphml(hashtag_net, open(args.write_graphml, "w"))