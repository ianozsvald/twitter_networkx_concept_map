twitter_networkx_concept_map
============================

Take streaming tweets, extract hashtags &amp; usernames, create graph, export graphml for Gephi visualisation

Asknowledgements:
----------------

The code here is based on Maksim Tsvetovat's tutorial at PyCon 2013 https://us.pycon.org/2013/schedule/presentation/29/

Goal:
----

Turn a set of streamed Twitter firehose JSON tweets into a Twitter concept net showing commonly discussed pairs of hashtags and users.

![Example usernames hashtags for pycon2013](pycon_output/pycon2013_hashtags_usernames.png?raw=true)

![Example usernames hashtags for pycon2013](pycon_output/pycon_tags_people_communities.png?raw=true)

Requirements:
------------

You need a set of streamed tweets, I can't provide my set as the Twitter Usage Agreement forbids distribution of raw tweets. I've included a summary file which can be used in networkx (and gephi) which does not include tweet text or creation dates (as per the Twitter requirement).

You can get your own set of streamed tweets using:

     $ curl -s -uUSERNAME:PASSWORD -X POST -d 'track=pycon' https://stream.twitter.com/1.1/statuses/filter.json -o tweets_pycon.json

You can leave this running via a script (e.g. get_tweets.sh) using:
    
    nohup curl -s -uUSERNAME:PASSWORD -X POST -d 'track=pycon' https://stream.twitter.com/1.1/statuses/filter.json -o tweets_pycon.json > nohuppycon.log &

You also need the following:

    * twitter-text-python
    * networkx

The easy way to get these is to install:

    $ pip install -r requirements.txt

Usage:
-----

To parse the raw Twitter JSON into a cleaned local version use:

    $ extractor_content.py --json-raw eg_tweets_pycon.json -o clean_pycon.json

Note that you have to provide eg_tweets_pycon.json, I do provide a clean_pyson.json from my data.

To build a graph network from the cleaned data use:

    $ extractor_content.py --json-cleaned clean_pycon.json  --remove-nodes #pycon #python #pycon2013 @pycon 

To build the above and draw the graph use --draw-networkx:

    $ extractor_content.py --json-cleaned clean_pycon.json  --remove-nodes #pycon #python #pycon2013 @pycon --draw-networkx

To save a graphml output (for importing into Gephi) use:

    $ extractor_content.py --json-cleaned clean_pycon.json  --remove-nodes #pycon #python #pycon2013 @pycon --write-graphml pyconout.graphml
