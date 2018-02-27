"""Print corpus statistics.

Usage:
  stats.py
  stats.py -h | --help

Options:
  -h --help     Show this screen.
"""
from docopt import docopt
from collections import defaultdict

from sentiment.tass import InterTASSReader


class Stats:
    """Several statistics for a POS tagged corpus.
    """

    def __init__(self, tass_reader):
        """
        tass_reader -- corpus TASS
        """
        self._tweets = list(reader.tweets())  # iterador sobre los tweets
        tweets_iterator = list(reader.X())  # iterador sobre los contenidos de los tweets
        polarity_iterator = list(reader.y())  # iterador sobre las polaridades de los tweets

        self._polarity_count = defaultdict(int)
        for polarity in polarity_iterator:
            self._polarity_count[polarity] += 1

    def tweets_count(self):
        return len(self._tweets)

    def polarity_count(self):
        return self._polarity_count


if __name__ == '__main__':
    opts = docopt(__doc__)

    # load the data
    reader = InterTASSReader('TASS/InterTASS/tw_faces4tassTrain1000rc.xml')

    # compute the statistics
    stats = Stats(reader)

    print('Basic Statistics')
    print('================')
    print('Total Tweets: {}'.format(stats.tweets_count()))

    print('Polarity Counts')
    for polarity, count in stats.polarity_count().items():
        print('{}: {}'.format(polarity, count))