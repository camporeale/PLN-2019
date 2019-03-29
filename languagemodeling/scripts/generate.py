"""Generate natural language sentences using a language model.

Usage:
  generate.py -i <file> -n <n>
  generate.py -h | --help

Options:
  -i <file>     Language model file.
  -n <n>        Number of sentences to generate.
  -h --help     Show this screen.
"""
from docopt import docopt
import pickle
import sys
sys.path.append('/home/camporeale/ML/Cursos/plnFamaf2019/PLN-2019/languagemodeling')
from ngram_generator import NGramGenerator


if __name__ == '__main__':
    opts = docopt(__doc__)

    # load the model
    filename = opts['-i']
    f = open(filename, 'rb')
    model = pickle.load(f)
    f.close()

    # build generator
    generator = NGramGenerator(model)
    #print(generator._probs[()]['</s>'])

    # generate sentences
    n = int(opts['-n'])
    for i in range(n):
        sent = generator.generate_sent()
        print(' '.join(sent))
