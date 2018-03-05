"""Print corpus statistics.

Usage:
  stats.py -c <corpus>
  stats.py -h | --help

Options:
  -c <corpus>      Corpus sobre el cual se calculan las estadísticas
                  inter: InterTASS
                  general: GeneralTASS
  -h --help     Show this screen.
"""
from docopt import docopt
from collections import defaultdict

from sentiment.tass import InterTASSReader, GeneralTASSReader


class Stats:
    """Several statistics for a POS tagged corpus.
    """

    def __init__(self, tweets, polarities):
        """
        tweets: Contenido de cada tweet
        polarity: Clasificación de polaridad de cada tweet
        """
        self._tweets = list(tweets)
        self._polarity_count = defaultdict(int)
        for polarity in polarities:
            self._polarity_count[polarity] += 1

    def tweets_count(self):
        return len(self._tweets)

    def polarity_count(self):
        return self._polarity_count


if __name__ == '__main__':
    opts = docopt(__doc__)

    # load the data
    if opts['-c'] == 'inter':
        reader = InterTASSReader('TASS/InterTASS/tw_faces4tassTrain1000rc.xml')
    elif opts['-c'] == 'general':
        reader = GeneralTASSReader('TASS/GeneralTASS/general-tweets-train-tagged.xml')
    else:
        print("Corpus inexistente")
        exit(1)

    tweets, polarity = reader.X(), reader.y()

    # compute the statistics
    stats = Stats(tweets, polarity)

    print('Basic Statistics')
    print('================')
    print('Total Tweets: {}'.format(stats.tweets_count()))

    print('Polarity Counts')
    for polarity, count in stats.polarity_count().items():
        print('{}: {}'.format(polarity, count))