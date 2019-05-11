from collections import namedtuple, Counter
from sklearn.metrics import confusion_matrix
import numpy as np
class Evaluator(object):

    def evaluate(self, y_true, y_pred, unk_tags):
        self._y_true = y_true
        self._y_pred = y_pred
        self._labels = labels = list(set(y_pred))
        self._total = total = len(y_pred)

        # build complete confusion matrix to calculate accuracy
        self._CM = CM = confusion_matrix(y_true, y_pred, labels=labels)
        # accuracy
        self._hits = hits = CM.diagonal().sum()  # also m.trace()
        self._acc = acc = float(hits) / total * 100.0

        # get top 10 tags 
        count_tags = Counter(y_pred)
        if len(count_tags)>10:
            toptags = [x[0] for x in count_tags.most_common(10)]
        else:
            toptags = list(set(y_pred))

        self._toptags = toptags
        # get only true and predicted tags of instances of the top 10 tags
        ttag, mtags = zip(*[x for x in zip(y_pred,y_true) if x[0] in toptags and x[1] in toptags])
        # build confusion matrix for top 10 tags
        self._CM10 = CM10 = confusion_matrix(ttag, mtags, labels=toptags)
        # confusion matrix with percentages
        self._CM10_P = np.round((CM10/total*100), decimals = 2)

        # known and unknown words accuracy
        hits_unk = 0
        hits_known = 0

        for x,y,z in zip(y_pred,y_true,unk_tags):
            if x == y:
                if z:
                    hits_unk +=1
                else:
                    hits_known+=1

        self._hits_unk = hits_unk
        self._hits_known = hits_known 
        self._total_unk = total_unk = len([x for x in unk_tags if x])
        self._total_known = total_known = total - total_unk
        self._known_accuracy = (hits_known/total_known)*100
        self._unk_accuracy = (hits_unk/total_unk)*100

    def accuracy(self):
        return self._acc

    def known_accuracy(self):
        return self._known_accuracy

    def unknown_accuracy(self):
        return self._unk_accuracy 

    def print_results(self):
        # print accuray, known words accuracy, unknown words accuracy
        hits = self._hits
        total = self._total
        acc = self._acc

        hits_known = self._hits_known
        total_known = self._total_known
        known_accuracy = self._known_accuracy

        hits_unk = self._hits_unk
        total_unk = self._total_unk
        unknown_accuracy = self._unk_accuracy

        print('Accuracy: {:2.2f}% ({}/{})'.format(acc, hits, total))
        print('Known words accuracy: {:2.2f}% ({}/{})'.format(known_accuracy, hits_known, total_known))
        print('Unknown words accuracy: {:2.2f}% ({}/{})'.format(unknown_accuracy, hits_unk, total_unk))


    def print_confusion_matrix(self):
        labels = self._toptags
        CM = self._CM10_P

        # confusion matrix
        for label in labels:
            print('\t{}'.format(label), end='')
        print('')

        # print table rows
        for i, label1 in enumerate(labels):
            print('{}\t'.format(label1), end='')
            for j, label2 in enumerate(labels):
                print('{}\t'.format(CM[i, j]), end='')
            print('')
