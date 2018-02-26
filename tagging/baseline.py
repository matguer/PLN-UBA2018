from collections import defaultdict

def inner_default_dict():
    return defaultdict(int)

class BadBaselineTagger:

    def __init__(self, tagged_sents):
        """
        tagged_sents -- training sentences, each one being a list of pairs.
        """
        pass

    def tag(self, sent):
        """Tag a sentence.

        sent -- the sentence.
        """
        return [self.tag_word(w) for w in sent]

    def tag_word(self, w):
        """Tag a word.

        w -- the word.
        """
        return 'nc0s000'

    def unknown(self, w):
        """Check if a word is unknown for the model.

        w -- the word.
        """
        return True


class BaselineTagger:

    def __init__(self, tagged_sents, default_tag='nc0s000'):
        """
        tagged_sents -- training sentences, each one being a list of pairs.
        default_tag -- tag for unknown words.
        """
        # WORK HERE!!
        self._default_tag = default_tag
        self._word_tag_count = defaultdict(inner_default_dict)
        for tagged_sent in tagged_sents:
            for word, tag in tagged_sent:
                self._word_tag_count[word][tag] += 1

    def tag(self, sent):
        """Tag a sentence.

        sent -- the sentence.
        """
        return [self.tag_word(w) for w in sent]

    def tag_word(self, w):
        """Tag a word.

        w -- the word.
        """
        # WORK HERE!!
        if self.unknown(w):
            return self._default_tag
        else:
            tags_count = self._word_tag_count[w]
            return max(tags_count, key=tags_count.get)


    def unknown(self, w):
        """Check if a word is unknown for the model.

        w -- the word.
        """
        # WORK HERE!!
        return w not in self._word_tag_count
