# https://docs.python.org/3/library/collections.html
from collections import defaultdict
import math

inf = float('inf')

class LanguageModel(object):

    def sent_prob(self, sent):
        """Probability of a sentence. Warning: subject to underflow problems.

        sent -- the sentence as a list of tokens.
        """
        return 0.0

    def sent_log_prob(self, sent):
        """Log-probability of a sentence.

        sent -- the sentence as a list of tokens.
        """
        return -inf

    def log_prob(self, sents):
        result = 0.0
        for i, sent in enumerate(sents):
            lp = self.sent_log_prob(sent)
            if lp == -inf:
                return lp
            result += lp
        return result

    def cross_entropy(self, sents):
        log_prob = self.log_prob(sents)
        n = sum(len(sent) + 1 for sent in sents)  # count '</s>' events
        e = - log_prob / n
        return e

    def perplexity(self, sents):
        return math.pow(2.0, self.cross_entropy(sents))


class NGram(LanguageModel):

    def __init__(self, n, sents):
        """
        n -- order of the model.
        sents -- list of sentences, each one being a list of tokens.
        """
        assert n > 0
        self._n = n

        count = defaultdict(int)

        for sent in sents:
            count[()] += len(sent) + 1
            for k in range(max(1,n-1), n + 1):
                marked_sent = self.add_markers(sent)
                for i in range(len(marked_sent) - k + 1):
                    ngram = tuple(marked_sent[i:i + k])
                    count[ngram] += 1

        self._count = dict(count)

    def count(self, tokens):
        """Count for an n-gram or (n-1)-gram.

        tokens -- the n-gram or (n-1)-gram tuple.
        """
        return self._count.get(tokens, 0)

    def cond_prob(self, token, prev_tokens=None):
        """Conditional probability of a token.

        token -- the token.
        prev_tokens -- the previous n-1 tokens (optional only if n = 1).
        """
        if prev_tokens is None:
            prev_tokens = ()
        count_prev_tokens = self.count(prev_tokens)
        if count_prev_tokens == 0:
            return 0
        else:
            tokens = prev_tokens + (token,)
            count_tokens = self.count(tokens)
            return count_tokens / count_prev_tokens

    def sent_prob(self, sent):
        """Probability of a sentence. Warning: subject to underflow problems.

        sent -- the sentence as a list of tokens.
        """
        n = self._n
        sent = self.add_markers(sent)

        from functools import reduce
        return reduce(lambda x, y: x * y,
                      map(lambda tokens: self.cond_prob(token=tokens[-1], prev_tokens=tokens[:-1]),
                        [tuple(sent[i-n+1:i+1]) for i in range(n-1, len(sent))]
                        )
                      )

    def sent_log_prob(self, sent):
        """Log-probability of a sentence.

        sent -- the sentence as a list of tokens.
        """
        n = self._n
        sent = self.add_markers(sent)

        def log_cond_prob(tokens):
            cond_prob = self.cond_prob(token=tokens[-1], prev_tokens=tokens[:-1])
            return math.log2(cond_prob) if cond_prob != 0 else - inf

        return sum(log_cond_prob(tuple(sent[i-n+1:i+1])) for i in range(n-1, len(sent)))

    def add_markers(self, sent):
        return ['<s>']*(self._n-1) + sent + ['</s>']

    def word_types(self, sents):
        types = set(['</s>'])
        for sent in sents:
            for token in sent:
                types.add(token)
        return types


class AddOneNGram(NGram):

    def __init__(self, n, sents):
        """
        n -- order of the model.
        sents -- list of sentences, each one being a list of tokens.
        """
        # call superclass to compute counts
        super().__init__(n, sents)

        # compute vocabulary
        self._voc = voc = self.word_types(sents)
        self._V = len(voc)  # vocabulary size

    def V(self):
        """Size of the vocabulary.
        """
        return self._V

    def cond_prob(self, token, prev_tokens=None):
        """Conditional probability of a token.

        token -- the token.
        prev_tokens -- the previous n-1 tokens (optional only if n = 1).
        """
        n = self._n
        if not prev_tokens:
            # if prev_tokens not given, assume 0-uple:
            prev_tokens = ()
        assert len(prev_tokens) == n - 1

        count_prev_tokens = self.count(prev_tokens) + self.V()
        if count_prev_tokens == 0:
            return 0
        else:
            tokens = prev_tokens + (token,)
            count_tokens = self.count(tokens) + 1
            return count_tokens / count_prev_tokens


class InterpolatedNGram(NGram):

    def __init__(self, n, sents, gamma=None, addone=True):
        """
        n -- order of the model.
        sents -- list of sentences, each one being a list of tokens.
        gamma -- interpolation hyper-parameter (if not given, estimate using
            held-out data).
        addone -- whether to use addone smoothing (default: True).
        """
        assert n > 0
        self._n = n

        if gamma is not None:
            # everything is training data
            train_sents = sents
        else:
            # 90% training, 10% held-out
            m = int(0.9 * len(sents))
            train_sents = sents[:m]
            held_out_sents = sents[m:]

        print('Computing counts...')
        # COMPUTE COUNTS FOR ALL K-GRAMS WITH K <= N
        count = defaultdict(int)
        for sent in train_sents:
            count[()] += len(sent) + 1
            for k in range(1,n+1):
                marked_sent = self.add_markers(sent)
                for i in range(len(marked_sent)-k+1):
                    ngram = tuple(marked_sent[i:i+k])
                    count[ngram] += 1

        self._count = dict(count)

        # compute vocabulary size for add-one in the last step
        self._addone = addone
        if addone:
            print('Computing vocabulary...')
            self._voc = voc = set()
            voc = self.word_types(sents)

            self._V = len(voc)

        # compute gamma if not given
        if gamma is not None:
            self._gamma = gamma
        else:
            print('Computing gamma...')
            # use grid search to choose gamma
            min_gamma, min_p = None, float('inf')

            # WORK HERE!! TRY DIFFERENT VALUES BY HAND:
            for gamma in [100 + i * 50 for i in range(10)]:
                self._gamma = gamma
                p = self.perplexity(held_out_sents)
                print('  {} -> {}'.format(gamma, p))

                if p < min_p:
                    min_gamma, min_p = gamma, p

            print('  Choose gamma = {}'.format(min_gamma))
            self._gamma = min_gamma

    def count(self, tokens):
        """Count for an k-gram for k <= n.

        tokens -- the k-gram tuple.
        """
        return self._count.get(tokens, 0)

    def cond_prob(self, token, prev_tokens=None):
        """Conditional probability of a token.

        token -- the token.
        prev_tokens -- the previous n-1 tokens (optional only if n = 1).
        """
        n = self._n
        if not prev_tokens:
            # if prev_tokens not given, assume 0-uple:
            prev_tokens = ()
        assert len(prev_tokens) == n - 1

        # WORK HERE!!
        # SUGGESTED STRUCTURE:
        tokens = prev_tokens + (token,)
        prob = 0.0
        cum_lambda = 0.0  # sum of previous lambdas
        for i in range(n):
            # i-th term of the sum
            if i < n - 1:
                # COMPUTE lambdaa AND cond_ml.
                tokens_count = self.count(tokens[:i + 1])
                prev_tokens_count = self.count(prev_tokens[i:])
                lambdaa = (1 - cum_lambda) * (tokens_count / (tokens_count + self._gamma))
                cond_ml = (float(self.count(tokens[i:])) / prev_tokens_count) if prev_tokens_count != 0 else 0
            else:
                # COMPUTE lambdaa AND cond_ml.
                # LAST TERM: USE ADD ONE IF NEEDED!
                lambdaa = 1 - cum_lambda
                prev_tokens_count = self.count(prev_tokens[i:])
                if self._addone:
                    cond_ml = (float(self.count(tokens[i:])) + 1) / (prev_tokens_count + self._V)
                else:
                    cond_ml = (float(self.count(tokens[i:])) / prev_tokens_count) if prev_tokens_count != 0 else 0

            prob += lambdaa * cond_ml
            cum_lambda += lambdaa

        return prob
