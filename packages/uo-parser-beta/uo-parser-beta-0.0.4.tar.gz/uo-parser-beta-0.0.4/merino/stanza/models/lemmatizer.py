"""
Entry point for training and evaluating a lemmatizer.

This lemmatizer combines a neural sequence-to-sequence architecture with an `edit` classifier 
and two dictionaries to produce robust lemmas from word forms.
For details please refer to paper: https://nlp.stanford.edu/pubs/qi2018universal.pdf.
"""

import sys
import os
import shutil
import time
from datetime import datetime
import argparse
import numpy as np
import random
import torch
from torch import nn, optim

from .lemma.data import DataLoader
from .lemma.trainer import Trainer
from .lemma import scorer, edit
from .common.doc import *
from ..utils.conll import CoNLL


def parse_args():
    args = {
        'train_file': '',
        'eval_file': '',
        'output_file': '',
        'gold_file': '',
        'mode': 'predict',
        'lang': '',
        'ensemble_dict': True,
        'dict_only': False,
        'hidden_dim': 200,
        'emb_dim': 50,
        'num_layers': 1,
        'emb_dropout': 0.5,
        'dropout': 0.5,
        'max_dec_len': 50,
        'beam_size': 1,
        'attn_type': 'soft',
        'pos_dim': 50,
        'pos_dropout': 0.5,
        'edit': True,
        'num_edit': len(edit.EDIT_TO_ID),
        'alpha': 1.0,
        'pos': True,
        'sample_train': 1.0,
        'optim': 'adam',
        'lr': 1e-3,
        'lr_decay': 0.9,
        'decay_epoch': 30,
        'num_epoch': 15,
        'batch_size': 50,
        'max_grad_norm': 5.0,
        'log_step': 20,
        'seed': 1234,
        'cuda': True,
        'cpu': False
    }

    return args


def get_lemma_model(cache_dir, language):
    args = parse_args()
    args['shorthand'] = language
    # load model
    model_file = os.path.join(cache_dir, '{}/{}_lemmatizer.pt'.format(language, language))
    args['data_dir'] = os.path.join(cache_dir, language)
    args['model_dir'] = os.path.join(cache_dir, language)
    use_cuda = args['cuda'] and not args['cpu']
    trainer = Trainer(model_file=model_file, use_cuda=use_cuda)
    loaded_args, vocab = trainer.args, trainer.vocab

    for k in args:
        if k.endswith('_dir') or k.endswith('_file') or k in ['shorthand']:
            loaded_args[k] = args[k]

    return trainer, args, loaded_args, vocab
