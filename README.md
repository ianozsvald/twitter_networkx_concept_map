twitter_networkx_concept_map
============================

Take streaming tweets, extract hashtags &amp; usernames, create graph, export graphml for Gephi visualisation

Write-ups:

  * http://ianozsvald.com/2013/03/22/analysing-pydata-london-and-brighton-tweets-for-concept-mapping/
  * http://ianozsvald.com/2013/03/18/semantic-map-of-pycon2013-twitter-topics/

Asknowledgements:
----------------

The code here is based on Maksim Tsvetovat's tutorial at PyCon 2013 https://us.pycon.org/2013/schedule/presentation/29/

Goal:
----

Turn a set of streamed Twitter firehose JSON tweets into a Twitter concept net showing commonly discussed pairs of hashtags and users.

Here we see a plot from my blog post http://ianozsvald.com/2013/03/18/semantic-map-of-pycon2013-twitter-topics/ demonstrating the hashtags and usernames that were grouped together at PyCon 2013. White is #hashtags, purple is @usernames:

![Example usernames hashtags for pycon2013](pycon_output/pycon2013_hashtags_usernames.png?raw=true)

Using the above data inside Gephi I extract a set of communities:

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

Other arguments:

    --remove_usernames_below n  # strip users with less than n occurrences
    --remove_hashtags_below n  # strip hashtags with less than n occurrences


Output just the text from tweets in the named period:

    $ python extract_tweet_updates_to_file.py --json-raw <something>.json --text-file text.txt --ff 2013-04-11T22:00:10.044491+00:00 --ft 2013-04-11T23:00:00+00:00

To output just a filtered set of data (keeping anything except RTs in the date range):

    $ extract_tweet_updates_to_file.py --json-raw <something>.json --output reduced_raw.json --ff 2013-04-11T22:00:10.044491+00:00 --ft 2013-04-11T23:00:00+00:00


License
-------

*MIT*

Copyright (c) 2013 Ian Ozsvald.

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.

Copyright (c) 2013 Ian Ozsvald



Todo:
----

Remove various types of quotes to normalise phrases:
  * how we all lost\u2019 (double quotes)
  * how we all lost' (single quote)
  * consider adding root URLs (e.g. bbc.co.uk) or URL titles

Perhaps following URL link shortners and then take the domain name as a new link in the graph (e.g. bbc.co.uk, techcrunch.com).
