"""
An indentity lemmatizer that mimics the behavior of a normal lemmatizer but directly uses word as lemma.
"""

import os
import argparse
import random

from .lemma.data import DataLoader
from .lemma import scorer
from .common.doc import *
from ..utils.conll import CoNLL


def parse_args():
    args = {
        'data_dir': 'stanza/data/lemma',
        'train_file': '',
        'eval_file': '',
        'output_file': '',
        'gold_file': '',
        'mode': 'predict',
        'lang': '',
        'batch_size': 50,
        'seed': 1234
    }
    return args


def get_identity_lemma_model(shorthand):
    args = parse_args()
    args['shorthand'] = shorthand

    return args


def main():
    args = parse_args()
    random.seed(args.seed)

    args = vars(args)

    print("[Launching identity lemmatizer...]")

    if args['mode'] == 'train':
        print("[No training is required; will only generate evaluation output...]")

    document = Document(CoNLL.conll2dict(input_file=args['eval_file']))
    batch = DataLoader(document, args['batch_size'], args, evaluation=True, conll_only=True)
    system_pred_file = args['output_file']
    gold_file = args['gold_file']

    # use identity mapping for prediction
    preds = batch.doc.get([TEXT])

    # write to file and score
    batch.doc.set([LEMMA], preds)
    CoNLL.dict2conll(batch.doc.to_dict(), system_pred_file)
    if gold_file is not None:
        _, _, score = scorer.score(system_pred_file, gold_file)

        print("Lemma score:")
        print("{} {:.2f}".format(args['lang'], score * 100))


if __name__ == '__main__':
    main()
