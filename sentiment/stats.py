"""Evaulate a Sentiment Analysis model.

Usage:
  stats.py -c <directory>
  stats.py -h | --help

Options:
  -c <corpus>   Directory where all TASS corpus are stored.

  -h --help     Show this screen.
"""
from docopt import docopt

from tass import InterTASSReader
from collections import Counter, defaultdict



if __name__ == '__main__':
    opts = docopt(__doc__)

    corpus = defaultdict()

    directory = opts['-c'] 
    corpus["ES"] = directory+"/ES/intertass-ES-train-tagged.xml"
    corpus["CR"] = directory+"/CR/intertass-CR-train-tagged.xml"
    corpus["PE"] = directory+"/PE/intertass-PE-train-tagged.xml"


    for l, f in corpus.items():
    	reader = InterTASSReader(f)
    	X, y_true = list(reader.X()), list(reader.y())
    	print("Corpus "+ l)
    	print("\tLength:", len(X))
    	print("\t Polarity: ")

    	stats = Counter(y_true)
    	for sent, count in stats.items():
    		print("\t\t\t", sent , count)
