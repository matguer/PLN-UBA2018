"""Evaulate a Sentiment Analysis model.

Usage:
  eval.py -i <file> [-f] [-a]
  eval.py -h | --help

Options:
  -i <file>     Trained model file.
  -f --final    Use final test set instead of development.
  -a --all      Print all the evaluation, including print_maxent_features and print_feature_weights_for_item
  -h --help     Show this screen.
"""
from docopt import docopt
import pickle
from pprint import pprint
from collections import defaultdict

from sentiment.evaluator import Evaluator
from sentiment.tass import InterTASSReader
from sentiment.analysis import print_maxent_features, print_feature_weights_for_item

def print_tweet_prediction(tweet):
    print("TWEET: ", tweet)
    print("PREDICTED: ", pipeline.predict([tweet]))

if __name__ == '__main__':
    opts = docopt(__doc__)

    # load model
    filename = opts['-i']
    f = open(filename, 'rb')
    model = pickle.load(f)
    f.close()

    # load corpus
    if not opts['--final']:
        reader = InterTASSReader('TASS/InterTASS/TASS2017_T1_development.xml')
    else:
        reader = InterTASSReader(
            'TASS/InterTASS/TASS2017_T1_test.xml',
            'TASS/InterTASS/TASS2017_T1_test_res.qrel')
    X, y_true = list(reader.X()), list(reader.y())

    # classify
    y_pred = model.predict(X)

    # evaluate and print
    evaluator = Evaluator()
    evaluator.evaluate(y_true, y_pred)
    evaluator.print_results()
    evaluator.print_confusion_matrix()

    # detailed confusion matrix, for result analysis
    cm_items = defaultdict(list)
    for i, (true, pred) in enumerate(zip(y_true, y_pred)):
        cm_items[true, pred] += [i]


    if opts['--all']:
        pipeline = model._pipeline
        vect = pipeline.named_steps['vect']
        clf = pipeline.named_steps['clf']
        print_maxent_features(vect, clf)

        print("CLASES: ")
        print(pipeline.classes_)

        tweet = X[402]
        print_feature_weights_for_item(vect, clf, tweet)
        print_tweet_prediction(tweet)
        print_tweet_prediction(tweet.replace('triste', ';-)'))
        print_tweet_prediction(tweet.replace('triste', ';-)').replace('sin', ''))
        print_tweet_prediction(tweet.replace('un poco más triste', 'más en broma').replace('sin', 'en huelga por'))
