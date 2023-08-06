import copy
import itertools
import json
import os
import random
import torch
from torch.utils.data import Dataset
from collections import Counter, namedtuple, defaultdict
import glob
from ..utils.tokenize_utils import conllu_to_stanza_charlevel_format, stanza_charlevel_format_to_wordpiece_format

# for sents
instance_fields = [
    'paragraph_index',
    'wordpieces', 'wordpiece_labels', 'wordpiece_ends',
    'piece_idxs', 'attention_masks', 'token_type_idxs',
    'wordpiece_num'
]

batch_fields = [
    'paragraph_index',
    'wordpieces', 'wordpiece_labels', 'wordpiece_ends',
    'piece_idxs', 'attention_masks', 'token_type_idxs',
    'wordpiece_num'
]

Instance = namedtuple('Instance', field_names=instance_fields)

Batch = namedtuple('Batch', field_names=batch_fields)


class TokenizeDatasetLive(Dataset):
    def __init__(self, config, raw_text):
        """
        :param path (str): path to the data file.
        :param max_length (int): max sentence length.
        :param gpu (bool): use GPU (default=False).
        :param ignore_title (bool): Ignore sentences that are titles (default=False).
        """
        self.config = config
        self.treebank_name = config.treebank_name
        self.raw_text = raw_text

        self.data = []
        self.load_data()

    def __len__(self):
        return len(self.data)

    def __getitem__(self, item):
        return self.data[item]

    def load_data(self):
        self.data = stanza_charlevel_format_to_wordpiece_format(
            wordpiece_splitter=self.config.wordpiece_splitter,
            max_input_length=self.config.max_input_length,
            plaintext=self.raw_text,
            treebank_name=self.config.treebank_name
        )

    def numberize(self, wordpiece_splitter):  # wordpiece tokenizer
        data = []
        for inst in self.data:
            wordpieces = inst['wordpieces']
            wordpiece_labels = inst['wordpiece_labels']
            wordpiece_ends = inst['wordpiece_ends']
            paragraph_index = inst['paragraph_index']
            # Pad word pieces with special tokens
            piece_idxs = wordpiece_splitter.encode(
                wordpieces,
                add_special_tokens=True,
                max_length=self.config.max_input_length
            )
            assert len(piece_idxs) <= self.config.max_input_length

            pad_num = self.config.max_input_length - len(piece_idxs)
            attn_masks = [1] * len(piece_idxs) + [0] * pad_num
            piece_idxs = piece_idxs + [0] * pad_num

            # token type idxs
            token_type_idxs = [-100 if piece_id >= len(wordpieces) else wordpiece_labels[piece_id] for piece_id in
                               range(len(piece_idxs) - 2)]

            instance = Instance(
                paragraph_index=paragraph_index,
                wordpieces=wordpieces,
                wordpiece_labels=wordpiece_labels,
                wordpiece_ends=wordpiece_ends,
                piece_idxs=piece_idxs,
                attention_masks=attn_masks,
                token_type_idxs=token_type_idxs,
                wordpiece_num=len(wordpieces)
            )
            data.append(instance)
        self.data = data

    def collate_fn(self, batch):
        batch_paragraph_index = []
        batch_wordpieces = []
        batch_wordpiece_labels = []
        batch_wordpiece_ends = []

        batch_piece_idxs = []
        batch_attention_masks = []
        batch_token_type_idxs = []
        batch_wordpiece_num = []

        for inst in batch:
            batch_paragraph_index.append(inst.paragraph_index)
            batch_wordpieces.append(inst.wordpieces)
            batch_wordpiece_labels.append(inst.wordpiece_labels)
            batch_wordpiece_ends.append(inst.wordpiece_ends)

            batch_piece_idxs.append(inst.piece_idxs)
            batch_attention_masks.append(inst.attention_masks)

            batch_token_type_idxs.append(inst.token_type_idxs)

            batch_wordpiece_num.append(inst.wordpiece_num)

        batch_piece_idxs = torch.cuda.LongTensor(batch_piece_idxs)
        batch_attention_masks = torch.cuda.LongTensor(batch_attention_masks)
        batch_token_type_idxs = torch.cuda.LongTensor(batch_token_type_idxs)
        batch_wordpiece_num = torch.cuda.LongTensor(batch_wordpiece_num)

        return Batch(
            paragraph_index=batch_paragraph_index,
            wordpieces=batch_wordpieces,
            wordpiece_labels=batch_wordpiece_labels,
            wordpiece_ends=batch_wordpiece_ends,
            piece_idxs=batch_piece_idxs,
            attention_masks=batch_attention_masks,
            token_type_idxs=batch_token_type_idxs,
            wordpiece_num=batch_wordpiece_num
        )
