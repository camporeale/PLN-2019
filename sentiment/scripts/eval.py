"""Evaulate a Sentiment Analysis model.

Usage:
  eval.py -c <corpus> -i <file> -d "comment"
  eval.py -h | --help

Options:
  -c <corpus>   Evaluation corpus.
  -i <file>     Trained model file.
  -f --final    Use final test set instead of development.
  -d "improvements" comment improvements to the model
  -h --help     Show this screen.
"""
from docopt import docopt
import pickle
from pprint import pprint
from collections import defaultdict
import sys

sys.path.append("/home/camporeale/ML/Cursos/plnFamaf2019/PLN-2019/")

from sentiment.evaluator import Evaluator
from sentiment.tass import InterTASSReader
import pandas as pd
from pathlib import Path
import os

if __name__ == '__main__':
    opts = docopt(__doc__)

    # load model
    filename = opts['-i']
    f = open(filename, 'rb')
    model = pickle.load(f)
    f.close()

    # load evaluation corpus
    corpus = opts['-c']
    reader = InterTASSReader(corpus)
    X, y_true = list(reader.X()), list(reader.y())

    # normalize
    #X = model.normalize(X)

    # classify
    y_pred = model.predict(X)

    # evaluate and print
    evaluator = Evaluator()
    evaluator.evaluate(y_true, y_pred)
    evaluator.print_results()
    evaluator.print_confusion_matrix()

    # detailed confusion matrix, for result analysis
    cm_items = defaultdict(list)
    for i, (true, pred) in enumerate(zip(y_true, y_pred)):
        cm_items[true, pred] += [i]

    # Save results to file
    my_file = Path("results.csv")
    f_exists =  my_file.is_file()
    res = evaluator.get_results()

    if "ES" in opts['-c']:
      corpus = "ES"
    elif "PE" in opts['-c']:
      corpus = "PE"
    else:
      corpus = "CR"

    res.insert(0,corpus)
    res.insert(1,opts['-i'])
    res.insert(2,opts['-d'])

    if not f_exists:
      df = pd.DataFrame(columns=["Corpus","Classifier","Comment","P_Precision","P_Recall",
        "P_F1","N_Precision","N_Recall","N_F1","NEU_Precision","NEU_Recall","NEU_F1",
        "None_Precision","None_Recall","None_F1","Accuracy","M-Precision","M-Recall","Macro-F1"])
    else:
      df = pd.read_csv("results.csv")

    df.loc[len(df)] = res
    df.to_csv("results.csv",index=False)


    
    
