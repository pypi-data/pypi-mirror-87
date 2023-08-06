import argparse
import os
import random
import numpy as np
import sys
import torch
import logging
from .utils import *

# set random seeds
os.environ['PYTHONHASHSEED'] = str(1234)
random.seed(1234)
np.random.seed(1234)
torch.manual_seed(1234)
torch.cuda.manual_seed(1234)
torch.cuda.manual_seed_all(1234)
torch.backends.cudnn.deterministic = True
torch.backends.cudnn.benchmark = False

# configuration
parser = argparse.ArgumentParser()
# model hyper-parameters
parser.add_argument('--xlmr_model_name', default='xlm-roberta-base', type=str)
parser.add_argument('--cache_dir', default='resources/xlmr', type=str)
parser.add_argument('--xlmr_dropout', default=0.3, type=float)
parser.add_argument('--hidden_num', default=300, type=int)
parser.add_argument('--linear_dropout', default=0.1, type=float)
parser.add_argument('--linear_bias', default=1, type=int)
parser.add_argument('--linear_activation', default='relu', type=str)
# training hyper-parameters
parser.add_argument(
    '--treebank_dir', default='datasets/ud-treebanks-v2.5/UD_Arabic-PADT', type=str)
parser.add_argument('--log', default='', type=str)
parser.add_argument('--accumulate_step', default=1, type=int)
parser.add_argument('--batch_size', default=16, type=int)
parser.add_argument('--eval_batch_size', default=16, type=int)
parser.add_argument('--max_epoch', default=100, type=int)
parser.add_argument('--adapter_learning_rate', default=1e-4, type=float)
parser.add_argument('--learning_rate', default=1e-3, type=float)
parser.add_argument('--adapter_weight_decay', default=1e-4, type=float)
parser.add_argument('--weight_decay', default=1e-3, type=float)
parser.add_argument('--grad_clipping', default=4.5, type=float)
# data processing
parser.add_argument('--max_input_length', default=512, type=int)
# function mode
parser.add_argument('--tokenize', action='store_true')
parser.add_argument('--mwt', action='store_true')
parser.add_argument('--tagger', action='store_true')
parser.add_argument('--lemma', action='store_true')
parser.add_argument('--depparse', action='store_true')
parser.add_argument('--ner', action='store_true')
parser.add_argument('--jointie', action='store_true')
parser.add_argument('--eval', action='store_true')
parser.add_argument('--debug', action='store_true')
parser.add_argument('--lang', default='arabic', type=str)
parser.add_argument('--pipeline', action='store_true')
parser.add_argument('--input', type=str)
parser.add_argument('--output', type=str)
config = parser.parse_args()

config.working_dir = os.path.dirname(os.path.realpath(__file__))
