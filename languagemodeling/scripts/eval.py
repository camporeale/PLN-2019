"""Evaulate a language model using a test set.

Usage:
  eval.py -i <file>
  eval.py -h | --help

Options:
  -i <file>     Language model file.
  -h --help     Show this screen.
"""
from docopt import docopt
import pickle
import math
import sys
from nltk.corpus import PlaintextCorpusReader
sys.path.append('/home/camporeale/ML/Cursos/plnFamaf2019/PLN-2019/languagemodeling')

from ngram import NGram, AddOneNGram, InterpolatedNGram

if __name__ == '__main__':
    opts = docopt(__doc__)

    # load the model
    filename = opts['-i']
    f = open(filename, 'rb')
    model = pickle.load(f)
    f.close()

    # load the data
    # WORK HERE!! LOAD YOUR EVALUATION CORPUS
    corpus = PlaintextCorpusReader('.', 'euro_eval.txt')
    sents = corpus.sents()

    # compute the cross entropy
    # WORK HERE!!
    
    log_prob, e, p = model.perplexity(sents)


    print('Log probability: {0:.2f}'.format(log_prob))
    print('Cross entropy: {0:.2f}'.format(e))
    print('Perplexity: {0:.2f}'.format(p))
