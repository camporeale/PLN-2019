from collections import defaultdict
import random
import operator
from numpy import random


class NGramGenerator(object):

    def __init__(self, model):
        """
        model -- n-gram model.
        """
        self._n = model._n
        n = self._n
        # compute the probabilities
        probs = defaultdict(dict)
        # WORK HERE!!
        ngrams = []
        # create list of ngrams of length n only
        for ngram in model._count:
            if len(ngram) == n:
                ngrams.append(ngram)

        for ngram in ngrams:
            token  = ngram[n-1]
            prevtokens = ngram[:n-1]
            prob       = model.cond_prob(token, tuple(prevtokens))

            probs[prevtokens][token] = prob

        self._probs = dict(probs)
        # sort in descending order for efficient sampling
        self._sorted_probs = sorted_probs = {}
        # WORK HERE!!
        #print(probs,"\n")

        for prob in probs.items():
            #print(prob)
            sorted_value = sorted(prob[1].items(), key=operator.itemgetter(1),reverse=True)
            #print(sorted_value)
            sorted_probs[prob[0]] = sorted_value  


    def generate_sent(self):
        n = self._n

        """Randomly generate a sentence."""
        # WORK HERE!!

        sent = ["<s>"] * (n - 1)
        #print(sent)
        #print(sent[1-n:])
        while True:
            #print(sent[1-n:])
            if n == 1:
                token = self.generate_token()
            else:
                token = self.generate_token(tuple(sent[1-n:]))
            sent.append(token)
            if sent[-1] == "</s>": break


        return sent[n-1:-1]            

       
    def generate_token(self, prev_tokens=None):
        """Randomly generate a token, given prev_tokens.
        prev_tokens -- the previous n-1 tokens (optional only if n = 1).
        """
        n = self._n
        if n == 1 or prev_tokens is None:
            prev_tokens = tuple()

        tokens = self._sorted_probs[prev_tokens]
        ptoken = []
        probs = []
        for t, p in tokens:
            ptoken.append(t)
            probs.append(p)

       # print(ptoken[0:10],probs[0:10],sum(probs))
       #print(sum(probs))
        #import pdb; pdb.set_trace()
        choice = random.choice(ptoken, size=1, p=probs)
       # print(choice[0])
        return  choice[0]




