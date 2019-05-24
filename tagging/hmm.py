import math
from collections import defaultdict


class HMM:
 
    def __init__(self, n, tagset, trans, out):
        """
        n -- n-gram size.
        tagset -- set of tags.
        trans -- transition probabilities dictionary.
        out -- output probabilities dictionary.
        """
        self._n = n
        self._tagset = tagset
        self._trans = trans
        self._out = out
 
    def tagset(self):
        """Returns the set of tags.
        """
        return self._tagset
 
    def trans_prob(self, tag, prev_tags):
        """Probability of a tag.
 
        tag -- the tag.
        prev_tags -- tuple with the previous n-1 tags (optional only if n = 1).
        """
        n = self._n
        if n == 1:
            return self._trans[tag]
        if prev_tags:
            return self._trans[prev_tags].get(tag, 0.0)

    def trans_log_prob(self, tag, prev_tags):
        """Probability of a tag.

        tag -- the tag.
        prev_tags -- tuple with the previous n-1 tags (optional only if n = 1).
        """
        prob = self.trans_prob(tag,prev_tags)

        if prob == 0.0:
            return -math.inf
        else:
            return math.log2(prob)

    def out_prob(self, word, tag):
        """Probability of a word given a tag.
 
        word -- the word.
        tag -- the tag.
        """
        return self._out[tag].get(word, 0.0)

    def out_log_prob(self, word, tag):
        """Probability of a word given a tag.

        word -- the word.
        tag -- the tag.
        """
        prob = self.out_prob(word,tag)
        if prob == 0.0:
            return -math.inf
        else:
            return math.log2(prob)

    def tag_prob(self, y):
        """
        Probability of a tagging.
        Warning: subject to underflow problems.
 
        y -- tagging.
        
        """
        n = self._n
        tagging = tuple(["<s>"] * (n-1) + y + ["</s>"])

        prob = 1
        for i in range(len(tagging)-n+1):
            prob *= self.trans_prob(tagging[i+n-1], (tagging[i:i+n-1]))

        return prob

    def prob(self, x, y):
        """
        Joint probability of a sentence and its tagging.
        Warning: subject to underflow problems.
 
        x -- sentence.
        y -- tagging.
        """
        prior = self.tag_prob(y)
        prob = prior

        for word, tag in zip(x, y):
            prob *= self.out_prob(word, tag)

        return prob

    def tag_log_prob(self, y):
        """
        Log-probability of a tagging.
 
        y -- tagging.
        """
        n = self._n
        tagging = tuple(["<s>"] * (n-1) + y + ["</s>"])

        prob = 0
        for i in range(len(tagging)-n+1):
            prob += math.log2(self.trans_prob(tagging[i+n-1], (tagging[i:i+n-1])))

        return prob

    def log_prob(self, x, y):
        """
        Joint log-probability of a sentence and its tagging.
 
        x -- sentence.
        y -- tagging.
        """
        prior = self.tag_log_prob(y)
        prob = prior

        for word, tag in zip(x, y):
            prob += math.log2(self.out_prob(word, tag))

        return prob

    def tag(self, sent):
        """Returns the most probable tagging for a sentence.
 
        sent -- the sentence.
        """


class ViterbiTagger:
 
    def __init__(self, hmm):
        """
        hmm -- the HMM.
        """
        self._hmm = hmm

    def tag(self, sent):
        """Returns the most probable tagging for a sentence.
 
        sent -- the sentence.
        """
        hmm = self._hmm
        n = hmm._n

        self._pi = pi = {0: {("<s>",) * (n - 1): (math.log2(1), [])}}

        m = len(sent)
        tagset = hmm.tagset()

        for k in range(1, m+1):
            # print("column: ", k)
            pi[k] = {}
            for t in tagset:  # solo iterar sobre aquellos que tienen out_prob(sent[k-1], t) > 0
                for prevtags in pi[k-1].keys():
                    prevtags = prevtags[1:]  # controlar si la tupla viene vacía
                    tags = prevtags + (t,)
                    # print("row: ", tags)
                    maxlogprob = -math.inf
                    maxtag = None
                    for w in tagset | {"<s>"}:
                        # print((w,)+prevtags)
                        if (w,)+prevtags in pi[k-1]:
                            trans = hmm.trans_log_prob(t, ((w,) + prevtags))
                            out = hmm.out_log_prob(sent[k-1], t)
                            prob = pi[k-1][((w,)+prevtags)][0] + trans + out
                            if prob > maxlogprob:
                                maxlogprob = prob
                                maxtag = pi[k-1][(w,)+prevtags][1]
                    if maxlogprob > -math.inf:
                        pi[k][tags] = (maxlogprob, maxtag + [t])

        maxlogprob = -math.inf
        sequence = None
        for p, t in pi[k].items():
            print("P: ",p," T: ",t)
            prob = hmm.trans_log_prob("</s>", p) + t[0]
            print("prob:",prob," maxlogprodb:", maxlogprob)
            if prob > maxlogprob:
                maxlogprob = prob
                sequence = t[1]

        return sequence


class MLHMM(HMM):
 
    def __init__(self, n, tagged_sents, addone=True):
        """
        n -- order of the model.
        tagged_sents -- training sentences, each one being a list of pairs.
        addone -- whether to use addone smoothing (default: True).
        """
        emm_dict = defaultdict(lambda: defaultdict(int))
        ngram_count = defaultdict(int)
        vocab = set()
        tagset = set()

        # WORK HERE!!
        for sent in tagged_sents:
            # counts for emmision probability calculation, tagset and vocabulary
            tags = []
            for tagged in sent:
                emm_dict[tagged[1]][tagged[0]] += 1
                tags.append(tagged[1])
                vocab.add(tagged[0])
                tagset.add(tagged[1])

            tags = ["<s>"] * (n-1) + tags + ["</s>"]

            # counts for transition probability calculation
            for i in range(len(tags) - n + 1):
                ngram = tuple(tags[i:i+n])
                ngram_count[ngram] += 1
                ngram_count[ngram[:-1]] += 1

        self._n = n
        self._ngram_count = dict(ngram_count)
        self._emm_dict = dict(emm_dict)
        self._vocab = vocab
        self._tagset = tagset
        self._addone = addone
 
    def tcount(self, tokens):
        """Count for an n-gram or (n-1)-gram of tags.
 
        tokens -- the n-gram or (n-1)-gram tuple of tags.
        """
        return self._ngram_count[tokens]

    def unknown(self, w):
        """Check if a word is unknown for the model.
 
        w -- the word.
        """
        if w in self._vocab:
            return False
        else:
            return True

    def tagset(self):
        """Returns the set of tags.
        """
        return self._tagset

    def trans_prob(self, tag, prev_tags):
        """Probability of a tag.

        tag -- the tag.
        prev_tags -- tuple with the previous n-1 tags (optional only if n = 1).
        """
        if prev_tags is None:
            prev_tags = tuple()

        ngram = prev_tags + (tag,)
        tag_counts = self.tcount(ngram)
        prev_counts = self.tcount(prev_tags)

        if self._addone:
            tlen = len(self._tagset)
            probability = float(tag_counts+1 / prev_counts+tlen)
        else:
            if tag_counts == 0 or prev_counts == 0:
                probability = 0
            else:
                probability = float(tag_counts / prev_counts)

        return probability

    def out_prob(self, word, tag):
        """Probability of a word given a tag.

        word -- the word.
        tag -- the tag.
        """
        tag_counts = dict(self._emm_dict[tag])
        # calculate emmision probabilities
        if self.unknown(word):
            probability = 1 / len(self._vocab)
        else:
            probability = tag_counts[word] / sum(tag_counts.values())

        return probability

    def tag_prob(self, y):
        """
        Probability of a tagging.
        Warning: subject to underflow problems.

        y -- tagging.

        """
        n = self._n
        tagging = tuple(["<s>"] * (n - 1) + y + ["</s>"])

        prob = 1
        for i in range(len(tagging) - n + 1):
            prob *= self.trans_prob(tagging[i + n - 1], (tagging[i:i + n - 1]))

        return prob

    def prob(self, x, y):
        """
        Joint probability of a sentence and its tagging.
        Warning: subject to underflow problems.

        x -- sentence.
        y -- tagging.
        """
        prior = self.tag_prob(y)
        prob = prior

        for word, tag in zip(x, y):
            prob *= self.out_prob(word, tag)

        return prob

    def tag_log_prob(self, y):
        """
        Log-probability of a tagging.

        y -- tagging.
        """
        n = self._n
        tagging = tuple(["<s>"] * (n - 1) + y + ["</s>"])

        prob = 0
        for i in range(len(tagging) - n + 1):
            prob += math.log2(self.trans_prob(tagging[i+n-1], (tagging[i:i+n-1])))

        return prob

    def log_prob(self, x, y):
        """
        Joint log-probability of a sentence and its tagging.

        x -- sentence.
        y -- tagging.
        """
        prior = self.tag_log_prob(y)
        prob = prior

        for word, tag in zip(x, y):
            prob += math.log2(self.out_prob(word, tag))

        return prob

    def tag(self, sent):
        """Returns the most probable tagging for a sentence.

        sent -- the sentence.
        """