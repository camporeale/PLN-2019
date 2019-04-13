# https://docs.python.org/3/library/collections.html
from collections import defaultdict
import math


class LanguageModel(object):

    def __init__(self, n, sents):
        """
        n -- order of the model.
        sents -- list of sentences, each one being a list of tokens.
        """

    def sent_prob(self, sent):
        """Probability of a sentence. Warning: subject to underflow problems.
        
        sent -- the sentence as a list of tokens.
        """
        
        return 0.0

    def sent_log_prob(self, sent):
        """Log-probability of a sentence.

        sent -- the sentence as a list of tokens.
        """
        return -math.inf

    def log_prob(self, sents):
        """Log-probability of a list of sentences.

        sents -- the sentences.
        """
        # WORK HERE!!
        logprob = 0

        for sent in sents:
            logprob += self.sent_log_prob(sent)

        self._logprob = logprob
        return self._logprob


    def cross_entropy(self, sents):
        """Cross-entropy of a list of sentences.

        sents -- the sentences.
        """
        # WORK HERE!!
        total_words = 0
        logprob = self.log_prob(sents)

        for sent in sents:
            total_words+= len(sent)

        crossentropy = -(logprob / total_words)

        self._crossentropy = crossentropy

        return self._crossentropy

    def perplexity(self, sents):
        """Perplexity of a list of sentences.

        sents -- the sentences.
        """
        # WORK HERE!!
        crossentropy = self.cross_entropy(sents)
        perplexity = 2 ** crossentropy
        
        self._perplexity = perplexity
        return self._logprob, self._crossentropy, self._perplexity



class NGram(LanguageModel):

    def __init__(self, n, sents):
        """
        n -- order of the model.
        sents -- list of sentences, each one being a list of tokens.
        """
        assert n > 0
        self._n = n

        count = defaultdict(int)


        # WORK HERE!!
        
        for sent in sents:
            sent = ["<s>"] * (n-1) + sent + ["</s>"]
            for i in range(len(sent) - n + 1):
                ngram = tuple(sent[i:i+n])
                ngram_1= tuple(sent[i:i+n-1])
                count[ngram] += 1
                count[ngram_1]+= 1
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
        # WORK HERE!!
        probability = 0
        if prev_tokens is None:
            prev_tokens = tuple()

        ngram = prev_tokens + (token,)
        ngram_counts = self.count(ngram)
        prev_counts  = self.count(prev_tokens)

        if ngram_counts == 0 or prev_counts == 0:
            probability = 0
        else:
            probability = float(ngram_counts/prev_counts)
        
        return probability



    def sent_prob(self, sent):
        """Probability of a sentence. Warning: subject to underflow problems.

        sent -- the sentence as a list of tokens.
        """
        # WORK HERE !!

        sent = ["<s>"] * (self._n-1) + sent + ["</s>"]

        probability = self.cond_prob(sent[self._n-1], tuple(sent[0:self._n-1]))

        for i in range(1, len(sent) - self._n + 1):
            probability *= self.cond_prob(sent[i+self._n-1],tuple(sent[i:i+self._n-1]))


        return probability


    def sent_log_prob(self, sent):
        """Log-probability of a sentence.

        sent -- the sentence as a list of tokens.
        """
        # WORK HERE!!

        sent = ["<s>"] * (self._n-1) + sent + ["</s>"]

        try:
            probability = math.log2(self.cond_prob(sent[self._n-1], tuple(sent[0:self._n-1])))
            for i in range(1, len(sent) - self._n + 1):
                probability += math.log2(self.cond_prob(sent[i+self._n-1],tuple(sent[i:i+self._n-1])))
        except ValueError:
            return float('-inf')

        return probability

class AddOneNGram(NGram):

    def __init__(self, n, sents):
        """
        n -- order of the model.
        sents -- list of sentences, each one being a list of tokens.
        """
        assert n > 0
        count = defaultdict(int)
        self._n = n

        # compute vocabulary
        self._voc = voc = set()
        # WORK HERE!!
        voc.add("</s>") 

        for sent in sents:
            voc.update(sent)
            sent = ["<s>"] * (n-1) + sent + ["</s>"]
            for i in range(len(sent) - n + 1):
                ngram = tuple(sent[i:i+n])
                ngram_1= tuple(sent[i:i+n-1])
                count[ngram] += 1
                count[ngram_1]+= 1
        self._count = dict(count)

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
        # WORK HERE!!
        probability = 0
        if prev_tokens is None:
            prev_tokens = tuple()

        ngram = prev_tokens + (token,)
        ngram_counts = self.count(ngram)
        prev_counts  = self.count(prev_tokens)

        probability = float((ngram_counts+1)/(prev_counts+self._V))
        
        return probability

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
        self._gamma = 0.0 
        count = defaultdict(int)

        if gamma is not None:
            # everything is training data
            train_sents = sents
        else:
            # 90% training, 10% held-out
            m = int(0.9 * len(sents))
            train_sents = sents[:m]
            print(train_sents)
            held_out_sents = sents[m:]

        print('Computing counts...')
        # WORK HERE!!
        # COMPUTE COUNTS FOR ALL K-GRAMS WITH K <= N
        # iter over sentences
        for sent in train_sents:
            sent = ["<s>"] * (n-1) + sent + ["</s>"]
            #iter over ngrams: 0-gram, unigram, bigram, trigram, etc...
            for j in range(n+1): 
                #iter over individual sent for the current n-gram
                for i in range(n-j, len(sent) - j + 1):
                    ngram = tuple(sent[i:i+j])
                    count[ngram] += 1
        self._count = dict(count)


        # compute vocabulary size for add-one in the last step
        self._addone = addone
        if addone:
            print('Computing vocabulary...')
            self._voc = voc = set()
            # WORK HERE!! 

            for sent in sents:
                voc.update(sent)

            self._V = len(voc)
            print("vocabulary: ",self._V)
        # compute gamma if not given
        if gamma is not None:
            self._gamma = gamma
        else:
            print('Computing gamma...')
            # WORK HERE!!
            # use grid search to choose gamma
            gammas = defaultdict()

            for i in range(1, 1000, 50):
                self._gamma = i
                gammas[i] = self.perplexity(held_out_sents)

            self._gamma = min(gammas, key=gammas.get)



    def count(self, tokens):
        """Count for an k-gram for k <= n.

        tokens -- the k-gram tuple.
        """
        # WORK HERE!! (JUST A RETURN STATEMENT)
        return self._count.get(tokens, 0)


    def cond_prob(self, token, prev_tokens=None):
        """Conditional probability of a token.

        token -- the token.
        prev_tokens -- the previous n-1 tokens (optional only if n = 1).
        """
        # WORK HERE!!
        gamma = self._gamma
        n = self._n
        probability = 0
        lambdas = []

        if prev_tokens is None:
            prev_tokens = tuple()
                              
        for i in range(n-1):
            lambdas.append((1 - sum(lambdas)) * (self.count(prev_tokens[i:]) / (self.count(prev_tokens[i:])+gamma)))
            probability += lambdas[i] * self.cond_prog_ngram(token, prev_tokens[i:])

        lambdas.append(1 - sum(lambdas))        
        probability += lambdas[-1] * self.cond_prog_ngram(token)
        return probability


    def cond_prog_ngram(self, token, prev_tokens=None):
        probability = 0
        unigram = False
        if prev_tokens is None:
            prev_tokens = tuple()
            unigram = True

        ngram = prev_tokens + (token,)
        ngram_counts = self.count(ngram)
        prev_counts  = self.count(prev_tokens)

        if ngram_counts == 0:
            probability = 0
        else:
            if self._addone == True and unigram:
                probability = float((ngram_counts+1)/(prev_counts+self._V))
            else:
                probability = float(ngram_counts/prev_counts)
        
        return probability