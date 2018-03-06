from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.svm import LinearSVC
from sklearn.linear_model import LogisticRegression
from nltk import TweetTokenizer
from nltk.corpus import stopwords

classifiers = {
    'maxent': LogisticRegression,
    'mnb': MultinomialNB,
    'svm': LinearSVC,
}

def default_count_vectorizer():
    """
    default: Se utiliza el count vectorizer sin mejoras
    """
    return CountVectorizer()

def binary_count_vectorizer_improvement():
    """
    improvment 1: Se utiliza un count vectorizer binario
    """
    return CountVectorizer(binary=True)

def tweet_tokenizer_count_vectorizer_improvement():
    """
    improvment 2: Se utiliza el tweet tokenizer de nltk para contemplar emojis y signos
    """
    tokenizer = TweetTokenizer()
    return CountVectorizer(tokenizer=tokenizer.tokenize)

def stopwords_count_vectorizer_improvement():
    """
    improvment 3: Se filtran las stopwords
    """
    return CountVectorizer(stop_words=stopwords.words('spanish'))

def not_tokenizer(sent):
    negation_window = 5
    tokens = sent.split()
    new_tokens = []
    negate = False
    window_count = 0
    for token in tokens:
        if token in ['no', 'tampoco']:
            negate = True
            window_count = 0
        elif token == '.' or window_count == negation_window:
            negate = False
        elif negate:
            token = 'NOT_' + token
            window_count += 1
        new_tokens.append(token)

    return ' '.join(new_tokens)

def not_count_vectorizer_improvement():
    """
    improvment 4: Agregar el prefijo NOT_ a las siguientes palabras post aparición de 'no' o 'tampoco'.
    Se pone el prefijo en las siguientes palabras hasta el punto o hasta una ventana de 5 palabras.
    """
    return CountVectorizer(tokenizer=not_tokenizer)

class SentimentClassifier(object):

    def __init__(self, clf='svm'):
        """
        clf -- classifying model, one of 'svm', 'maxent', 'mnb' (default: 'svm').
        """
        self._clf = clf
        self._pipeline = pipeline = Pipeline([
            ('vect', not_count_vectorizer_improvement()),
            ('clf', classifiers[clf]()),
        ])

    def fit(self, X, y):
        self._pipeline.fit(X, y)

    def predict(self, X):
        return self._pipeline.predict(X)