"""
Entry point for training and evaluating a multi-word token (MWT) expander.

This MWT expander combines a neural sequence-to-sequence architecture with a dictionary
to decode the token into multiple words.
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
import copy

from .mwt.trainer import Trainer


def parse_args():
    args = {
        'train_file': '',
        'eval_file': '',
        'output_file': '',
        'gold_file': '',
        'mode': 'predict',
        'lang': '',
        'shorthand': '',
        'ensemble_dict': True,
        'ensemble_early_stop': False,
        'dict_only': False,
        'hidden_dim': 100,
        'emb_dim': 50,
        'num_layers': 1,
        'emb_dropout': 0.5,
        'dropout': 0.5,
        'max_dec_len': 50,
        'beam_size': 1,
        'attn_type': 'soft',
        'sample_train': 1.0,
        'optim': 'adam',
        'lr': 1e-3,
        'lr_decay': 0.9,
        'decay_epoch': 30,
        'num_epoch': 50,
        'batch_size': 50,
        'max_grad_norm': 5.0,
        'log_step': 20,
        'save_name': '',
        'seed': 1234,
        'cuda': True,
        'cpu': False
    }
    return args


def get_mwt_model(cache_dir, language):
    args = parse_args()
    args['shorthand'] = language
    # ############## load model #############
    # file paths
    model_file = os.path.join(cache_dir, '{}/{}_mwt_expander.pt'.format(language, language))
    args['data_dir'] = os.path.join(cache_dir, language)
    args['save_dir'] = os.path.join(cache_dir, language)
    # load model
    use_cuda = args['cuda'] and not args['cpu']
    trainer = Trainer(model_file=model_file, use_cuda=use_cuda)
    loaded_args, vocab = trainer.args, trainer.vocab

    for k in args:
        if k.endswith('_dir') or k.endswith('_file') or k in ['shorthand']:
            loaded_args[k] = args[k]

    return trainer, args, loaded_args, vocab
