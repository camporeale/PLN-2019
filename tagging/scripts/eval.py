"""Evaulate a tagger.

Usage:
  eval.py -i <file> [-c]
  eval.py -h | --help

Options:
  -c            Show confusion matrix.
  -i <file>     Tagging model file.
  -h --help     Show this screen.
"""
from docopt import docopt
import pickle
from tagging.evaluator import Evaluator

from tagging.ancora import SimpleAncoraCorpusReader


if __name__ == '__main__':
    opts = docopt(__doc__)

    # load the model
    filename = opts['-i']
    f = open(filename, 'rb')
    model = pickle.load(f)
    f.close()

    # load the data
    files = '3LB-CAST/.*\.tbf\.xml'
    corpus = SimpleAncoraCorpusReader('ancora/ancora-3.0.1es/', files)
    sents = list(corpus.tagged_sents())

    # tag and evaluate
    # WORK HERE!!
    model_tags = []
    true_tags = []
    unk_tags = []
    labels = []

    for sent in sents:
        model_tags.extend(model.tag([x[0] for x in sent]))
        unk_tags.extend([model.unknown(x[0]) for x in sent])
        true_tags.extend([x[1] for x in sent])

    evaluator = Evaluator()
    evaluator.evaluate(true_tags, model_tags, unk_tags)
    evaluator.print_results()
    evaluator.print_confusion_matrix()



