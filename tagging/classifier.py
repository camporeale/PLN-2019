from sklearn.pipeline import Pipeline, FeatureUnion
from sklearn.feature_extraction import DictVectorizer
from sklearn.svm import LinearSVC
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import MultinomialNB
from tagging.fasttext import FasttextDictVectorizer

classifiers = {
    'lr': LogisticRegression,
    'svm': LinearSVC,
    'mnb': MultinomialNB
}


def feature_dict(sent, i):
    """Feature dictionary for a given sentence and position.

    sent -- the sentence.
    i -- the position.
    """
    # WORK HERE!!
    assert 0 <= i < len(sent)

    fdict = {}
    features = {'w': str.lower, 'wu': str.isupper, 'wt': str.istitle, 'wd': str.isdigit}

    # Current word
    words = {' ': sent[i]}

    # Previous word
    if i == 0:
        words['p'] = '<s>'
    else:
        words['p'] = sent[i - 1]

    # Next word
    if i == len(sent) - 1:
        words['n'] = '</s>'
    else:
        words['n'] = sent[i + 1]

    for key, value in words.items():
        if value == '<s>':
            fdict['pw'] = value.lower()
        elif value == '</s>':
            fdict['nw'] = value.lower()
        else:
            for name, feature in features.items():
                fdict[key.lstrip()+name] = feature(value)

    return fdict


class ClassifierTagger:
    """Simple and fast classifier based tagger.
    """

    def __init__(self, tagged_sents, clf='lr'):
        """
        clf -- classifying model, one of 'svm', 'lr' (default: 'lr').
        """
        # WORK HERE!!
        self.vocab = set()

        self._pipeline = Pipeline([
            ('vect', DictVectorizer()),
            ('clf', classifiers[clf]()),
        ])

        self.fit(tagged_sents)

    def fit(self, tagged_sents):
        """
        Train.

        tagged_sents -- list of sentences, each one being a list of pairs.
        """
        # WORK HERE!!

        X, y = self.get_features(tagged_sents)
        self._pipeline.fit(X, y)

    def tag_sents(self, sents):
        """Tag sentences.

        sent -- the sentences.
        """
        # WORK HERE!!
        return [self.tag(sent) for sent in sents]

    def tag(self, sent):
        """Tag a sentence.

        sent -- the sentence.
        """
        # WORK HERE!!
        x = []
        for i in range(len(sent)):
            x.append(feature_dict(sent, i))

        tags = list(self._pipeline.predict(x))
        return tags

    def unknown(self, w):
        """Check if a word is unknown for the model.

        w -- the word.
        """
        # WORK HERE!!
        if w in self.vocab:
            return False
        else:
            return True

    def get_features(self, tagged_sents):
        features = []
        tags = []
        vocab = set()
        for sent in tagged_sents:
            if not sent:
                continue
            s, t = zip(*sent)
            vocab.update(s)
            for i in range(len(sent)):
                features.append(feature_dict(s, i))
                tags.append((t[i]))
        self.vocab = vocab
        return features, tags


class FastTextClassifier(ClassifierTagger):
    def __init__(self, tagged_sents, clf='lr'):

        self._pipeline = Pipeline([
            ('vect', FeatureUnion([
                ('ft', FasttextDictVectorizer('tagging/models/cc.es.300.bin', ['w'])),
                ('twv', DictVectorizer())
            ])),
            ('clf', classifiers[clf]())
        ])

        self.fit(tagged_sents)
