import os
import re
from tqdm import tqdm
import requests
import zipfile
import glob
import torch
import torch.nn as nn
import numpy as np
from .doc import *
from copy import deepcopy
from ..resources.tbinfo import *

SPACE_RE = re.compile(r'\s')


def unzip(dir, filename):
    """
    Fully unzip a file `filename` that's in a directory `dir`.
    """
    print(f'Unzipping: {dir}/{filename}...')
    with zipfile.ZipFile(os.path.join(dir, filename)) as f:
        f.extractall(dir)
    os.remove(os.path.join(dir, filename))


def download(cache_dir, language):
    lang_dir = os.path.join(cache_dir, language)
    save_fpath = os.path.join(cache_dir, language, '{}.zip'.format(language))

    if not os.path.exists(os.path.join(lang_dir, '{}.downloaded'.format(language))):
        print('Downloading saved models for {} ...'.format(language))
        url = "https://ix.cs.uoregon.edu/~minhnv/merino/{}.zip".format(language)

        response = requests.get(url, stream=True)
        total_size_in_bytes = int(response.headers.get('content-length', 0))
        block_size = 1024  # 1 Kibibyte
        progress_bar = tqdm(total=total_size_in_bytes, unit='iB', unit_scale=True)

        ensure_dir(lang_dir)
        with open(save_fpath, 'wb') as file:
            for data in response.iter_content(block_size):
                progress_bar.update(len(data))
                file.write(data)
        progress_bar.close()
        unzip(lang_dir, '{}.zip'.format(language))
        if total_size_in_bytes != 0 and progress_bar.n != total_size_in_bytes:
            print("Failed to download saved models for {}!".format(language))
        else:
            with open(os.path.join(lang_dir, '{}.downloaded'.format(language)), 'w') as f:
                f.write('')
            print('Done!')


def create_treebank_dir_with_dev(original_treebank_dir, new_treebank_dir):
    original_train_conllu_fpath = glob.glob(os.path.join(original_treebank_dir, '*-train.conllu'))[0]
    original_train_text_fpath = glob.glob(os.path.join(original_treebank_dir, '*-train.txt'))[0]
    original_test_conllu_fpath = glob.glob(os.path.join(original_treebank_dir, '*-test.conllu'))[0]
    original_test_text_fpath = glob.glob(os.path.join(original_treebank_dir, '*-test.txt'))[0]

    shorthand = os.path.basename(original_train_conllu_fpath).replace('-ud-train.conllu', '')
    new_shorthand = shorthand + '2'

    # files in new tree bank dir
    new_train_conllu_fpath = os.path.join(new_treebank_dir, os.path.basename(original_train_conllu_fpath)).replace(
        shorthand, new_shorthand)
    new_train_text_fpath = os.path.join(new_treebank_dir, os.path.basename(original_train_text_fpath)).replace(
        shorthand, new_shorthand)
    new_dev_conllu_fpath = os.path.join(new_treebank_dir, os.path.basename(original_train_conllu_fpath).rstrip(
        '-train.conllu') + '-dev.conllu').replace(
        shorthand, new_shorthand)
    new_dev_text_fpath = os.path.join(new_treebank_dir, os.path.basename(original_train_text_fpath).rstrip(
        '-train.txt') + '-dev.txt').replace(
        shorthand, new_shorthand)
    new_test_conllu_fpath = os.path.join(new_treebank_dir, os.path.basename(original_test_conllu_fpath)).replace(
        shorthand, new_shorthand)
    new_test_text_fpath = os.path.join(new_treebank_dir, os.path.basename(original_test_text_fpath)).replace(
        shorthand, new_shorthand)

    ensure_dir(new_treebank_dir)
    # keep original test
    os.system('cp -a {} {}'.format(original_test_conllu_fpath, new_test_conllu_fpath))
    os.system('cp -a {} {}'.format(original_test_text_fpath, new_test_text_fpath))

    # split train -> 2 parts
    with open(original_train_text_fpath) as f:
        train_txt_docs = [pt.rstrip() for pt in f.read().split('\n\n') if pt.rstrip()]

    with open(original_train_conllu_fpath) as f:
        train_conllu_docs = ['# newdoc id' + doc.strip() for doc in f.read().split('# newdoc id')][1:]

    if len(train_txt_docs) > 10:
        new_train_size = int(len(train_txt_docs) * 8. / 9)
        # new train
        with open(new_train_text_fpath, 'w') as f:
            f.write('\n\n'.join(train_txt_docs[:new_train_size]))

        with open(new_train_conllu_fpath, 'w') as f:
            f.write('\n\n'.join(train_conllu_docs[:new_train_size]) + '\n\n')
        # new dev
        with open(new_dev_text_fpath, 'w') as f:
            f.write('\n\n'.join(train_txt_docs[new_train_size:]))
        with open(new_dev_conllu_fpath, 'w') as f:
            f.write('\n\n'.join(train_conllu_docs[new_train_size:]) + '\n\n')
        return True
    else:
        # data is too small
        os.system('cp -a {} {}'.format(original_train_conllu_fpath, new_train_conllu_fpath))
        os.system('cp -a {} {}'.format(original_train_text_fpath, new_train_text_fpath))

        os.system('cp -a {} {}'.format(original_train_conllu_fpath, new_dev_conllu_fpath))
        os.system('cp -a {} {}'.format(original_train_text_fpath, new_dev_text_fpath))
        return False


def parse_report(report_fpath):
    with open(report_fpath) as f:
        lines = [line.strip() for line in f if line.strip()][2:]
    score = {
        'tokens': 0,
        'sentences': 0,
        'words': 0,
        'upos': 0,
        'xpos': 0,
        'ufeats': 0,
        'alltags': 0,
        'lemmas': 0,
        'uas': 0,
        'las': 0,
        'clas': 0,
        'mlas': 0,
        'blex': 0
    }
    if not lines[0].startswith('Tokens'):
        score['average'] = 0
        return score
    else:
        score['tokens'] = float(lines[0].split('|')[-2].strip())
        score['sentences'] = float(lines[1].split('|')[-2].strip())
        score['words'] = float(lines[2].split('|')[-2].strip())
        score['upos'] = float(lines[3].split('|')[-2].strip())
        score['xpos'] = float(lines[4].split('|')[-2].strip())
        score['ufeats'] = float(lines[5].split('|')[-2].strip())
        score['alltags'] = float(lines[6].split('|')[-2].strip())
        score['lemmas'] = float(lines[7].split('|')[-2].strip())
        score['uas'] = float(lines[8].split('|')[-2].strip())
        score['las'] = float(lines[9].split('|')[-2].strip())
        score['clas'] = float(lines[10].split('|')[-2].strip())
        score['mlas'] = float(lines[11].split('|')[-2].strip())
        score['blex'] = float(lines[12].split('|')[-2].strip())

        score['average'] = np.mean(list(score.values()))
        return score


def process_doc(conllu_doc):
    out_doc = []
    num_sents = len(conllu_doc)
    for sent_id in range(num_sents):
        sent = conllu_doc[sent_id]
        out_sent = []

        start2mwt = {}
        for mwt in sent['mwts']:
            start2mwt[mwt['start']] = mwt

        num_words = len(sent.keys()) - 1
        for word_id in range(1, num_words + 1):
            word = sent[word_id]
            assert word['id'] == word_id
            if word_id in start2mwt:
                mwt = start2mwt[word_id]
                out_sent.append({ID: '{}-{}'.format(mwt['start'], mwt['end']), TEXT: mwt['text']})

            out_sent.append({ID: f'{word_id}', TEXT: word[TEXT],
                             UPOS: word.get(UPOS, '_'), XPOS: word.get(XPOS, '_'), FEATS: word.get(FEATS, '_'),
                             HEAD: word.get(HEAD, f'{word_id - 1}'), DEPREL: word.get(DEPREL, '_')})
        out_doc.append(out_sent)
    return out_doc


def process_sentence(sentence):
    sent = []
    i = 0
    for tok, wp_p, additional_info in sentence:
        if len(tok) <= 0:
            continue
        if wp_p == 3 or wp_p == 4:
            additional_info['MWT'] = 'Yes'
        infostr = None if len(additional_info) == 0 else '|'.join(
            [f"{k}={additional_info[k]}" for k in additional_info])
        sent.append({ID: f'{i + 1}', TEXT: tok})
        if infostr is not None: sent[-1][MISC] = infostr
        i += 1
    return sent


def normalize_token(treebank_name, token):
    token = SPACE_RE.sub(' ', token.lstrip())

    if 'chinese' in treebank_name.lower() or 'korean' in treebank_name.lower() or 'japanese' in treebank_name.lower():
        token = token.replace(' ', '')

    return token


def ensure_dir(dir_path):
    os.makedirs(dir_path, exist_ok=True)


def printlog(logger, message, printout=True):
    logger.info(message)
    if printout:
        print(message)


def harmonic_mean(a, weights=None):
    if any([x == 0 for x in a]):
        return 0
    else:
        assert weights is None or len(weights) == len(
            a), 'Weights has length {} which is different from that of the array ({}).'.format(len(weights), len(a))
        if weights is None:
            return len(a) / sum([1 / x for x in a])
        else:
            return sum(weights) / sum(w / x for x, w in zip(a, weights))


def compute_binary_reprs(obj1_reprs, obj2_reprs):  # note that, (obj1, obj2) != (obj2, obj1)
    batch_size, _, rep_dim = obj1_reprs.shape
    num_obj1 = obj1_reprs.shape[1]
    num_obj2 = obj2_reprs.shape[1]

    cloned_obj1s = obj1_reprs.repeat(1, 1, num_obj2).view(batch_size, -1, rep_dim)
    cloned_obj2s = obj2_reprs.repeat(1, num_obj1, 1).view(batch_size, -1, rep_dim)
    return cloned_obj1s, cloned_obj2s


def compute_span_reprs(word_reprs, span_idxs):
    '''
    word_reprs.shape: [batch size, num words, word dim]
    span_idxs.shape: [batch size, num spans, 2]
    '''
    batch_span_reprs = []
    batch_size, _, _ = word_reprs.shape
    _, num_spans, _ = span_idxs.shape
    for bid in range(batch_size):
        span_reprs = []
        for sid in range(num_spans):
            start, end = span_idxs[bid][sid]
            words = word_reprs[bid][start: end]  # [span size, word dim]
            span_reprs.append(torch.mean(words, dim=0))
        span_reprs = torch.stack(span_reprs, dim=0)  # [num spans, word dim]
        batch_span_reprs.append(span_reprs)
    batch_span_reprs = torch.stack(batch_span_reprs, dim=0)  # [batch size, num spans, word dim]
    return batch_span_reprs


def compute_word_reprs_first(piece_reprs, first_idxs):
    '''
    piece_reprs.shape: [batch size, max length, rep dim]
    first_idxs.shape: [batch size, num words]
    '''
    batch_word_reprs = []
    batch_size, _, _ = piece_reprs.shape
    _, num_words = first_idxs.shape
    for bid in range(batch_size):
        word_reprs = []
        for wid in range(num_words):
            word_reprs.append(piece_reprs[bid][first_idxs[bid][wid]])
        word_reprs = torch.stack(word_reprs, dim=0)  # [ num words, rep dim]
        batch_word_reprs.append(word_reprs)
    batch_word_reprs = torch.stack(batch_word_reprs, dim=0)  # [batch size, num words, rep dim]
    return batch_word_reprs


def compute_word_reps_avg(piece_reprs, component_idxs):
    '''
        piece_reprs.shape: [batch size, max length, rep dim]
        component_idxs.shape: [batch size, num words, 2]
    '''
    batch_word_reprs = []
    batch_size, _, _ = piece_reprs.shape
    _, num_words, _ = component_idxs.shape
    for bid in range(batch_size):
        word_reprs = []
        for wid in range(num_words):
            wrep = torch.mean(piece_reprs[bid][component_idxs[bid][wid][0]: component_idxs[bid][wid][1]], dim=0)
            word_reprs.append(wrep)
        word_reprs = torch.stack(word_reprs, dim=0)  # [num words, rep dim]
        batch_word_reprs.append(word_reprs)
    batch_word_reprs = torch.stack(batch_word_reprs, dim=0)  # [batch size, num words, rep dim]
    return batch_word_reprs


def log_sum_exp(tensor, dim=0, keepdim: bool = False):
    """LogSumExp operation used by CRF."""
    m, _ = tensor.max(dim, keepdim=keepdim)
    if keepdim:
        stable_vec = tensor - m
    else:
        stable_vec = tensor - m.unsqueeze(dim)
    return m + (stable_vec.exp().sum(dim, keepdim=keepdim)).log()


def sequence_mask(lens, max_len=None):
    """Generate a sequence mask tensor from sequence lengths, used by CRF."""
    batch_size = lens.size(0)
    if max_len is None:
        max_len = lens.max().item()
    ranges = torch.arange(0, max_len, device=lens.device).long()
    ranges = ranges.unsqueeze(0).expand(batch_size, max_len)
    lens_exp = lens.unsqueeze(1).expand_as(ranges)
    mask = ranges < lens_exp
    return mask


def word_lens_to_offsets(word_lens):
    max_token_num = max([len(x) for x in word_lens])
    offsets = []
    for seq_token_lens in word_lens:
        seq_offsets = [0]
        for l in seq_token_lens[:-1]:
            seq_offsets.append(seq_offsets[-1] + l)
        offsets.append(seq_offsets + [-1] * (max_token_num - len(seq_offsets)))
    return offsets


def word_lens_to_idxs(word_lens):
    max_token_num = max([len(x) for x in word_lens])
    max_token_len = max([max(x) for x in word_lens])
    idxs = []
    for seq_token_lens in word_lens:
        seq_idxs = []
        offset = 0
        for token_len in seq_token_lens:
            seq_idxs.append([offset, offset + token_len])
            offset += token_len
        seq_idxs.extend([[-1, 0]] * (max_token_num - len(seq_token_lens)))
        idxs.append(seq_idxs)
    return idxs, max_token_num, max_token_len


def graphs_to_node_idxs(batch, graphs):
    """
    :param graphs (list): A list of Graph objects.
    :return: mention/trigger index matrix, mask tensor, max number, and max length
    """
    mention_idxs = []
    trigger_idxs = []

    max_mention_num = max(max(graph.mention_num for graph in graphs), 1)
    max_trigger_num = max(max(graph.trigger_num for graph in graphs), 1)
    max_mention_len = max(max([e[1] - e[0] for e in graph.mentions] + [1])
                          for graph in graphs)
    max_trigger_len = max(max([t[1] - t[0] for t in graph.triggers] + [1])
                          for graph in graphs)
    for bid, graph in enumerate(graphs):
        seq_mention_idxs = []
        seq_trigger_idxs = []

        for mention in graph.mentions:
            mention_len = mention[1] - mention[0]
            seq_mention_idxs.append([mention[0], mention[1]])
        seq_mention_idxs.extend([[0, 1]] * (max_mention_num - graph.mention_num))
        mention_idxs.append(seq_mention_idxs)

        for trigger in graph.triggers:
            seq_trigger_idxs.append([trigger[0], trigger[1]])

        seq_trigger_idxs.extend([[0, 1]] * (max_trigger_num - graph.trigger_num))

        trigger_idxs.append(seq_trigger_idxs)

    return (
        mention_idxs, max_mention_num, max_mention_len,
        trigger_idxs, max_trigger_num, max_trigger_len
    )


def graphs_to_node_idxs_doc(batch, graphs):
    """
    :param graphs (list): A list of Graph objects.
    :return: mention/trigger index matrix, mask tensor, max number, and max length
    """
    mention_idxs = []

    max_mention_num = max(max(graph.mention_num for graph in graphs), 1)
    max_mention_len = max(max([e[1] - e[0] for e in graph.mentions] + [1])
                          for graph in graphs)

    for bid, graph in enumerate(graphs):
        seq_mention_idxs = []

        for mention in graph.mentions:
            seq_mention_idxs.append([mention[0], mention[1]])
        seq_mention_idxs.extend([[0, 1]] * (max_mention_num - graph.mention_num))
        mention_idxs.append(seq_mention_idxs)

    return (
        mention_idxs, max_mention_num, max_mention_len
    )


def generate_pairwise_idxs(num1, num2):
    idxs = []
    distance_idxs = []
    for i in range(num1):
        for j in range(num2):
            idxs.append(i)
            idxs.append(j + num1)
            distance_idxs.append(np.abs(i - j))
    return idxs, distance_idxs


def tag_paths_to_spans(paths, token_nums, vocab, vocab_type):
    """Convert predicted tag paths to a list of spans (entity mentions or event
    triggers).
    :param paths: predicted tag paths.
    :return (list): a list (batch) of lists (sequence) of spans.
    """
    batch_mentions = []
    itos = {i: s for s, i in vocab.items()}
    for i, path in enumerate(paths):
        mentions = []
        cur_mention = None
        path = path.tolist()[:token_nums[i].item()]
        for j, tag in enumerate(path):
            tag = itos[tag]
            if tag == 'O':
                prefix = tag = 'O'
            else:
                prefix, tag = tag.split('-', 1)

            if prefix == 'B':
                if cur_mention:
                    mentions.append(cur_mention)
                cur_mention = [j, j + 1, tag]
            elif prefix == 'I':
                if cur_mention is None:
                    # treat it as B-*
                    cur_mention = [j, j + 1, tag]
                elif cur_mention[-1] == tag:
                    cur_mention[1] = j + 1
                else:
                    # treat it as B-*
                    mentions.append(cur_mention)
                    cur_mention = [j, j + 1, tag]
            else:
                if cur_mention:
                    mentions.append(cur_mention)
                cur_mention = None
        if cur_mention:
            mentions.append(cur_mention)
        mentions = [(i, j, vocab_type[tag]) for i, j, tag in mentions]
        batch_mentions.append(mentions)
    return batch_mentions


def get_sentence_distances(trigger_sent_ids, graphs, max_sentence_distance):
    max_trigger_num = len(trigger_sent_ids[0])
    dist_ids = []
    for bid, graph in enumerate(graphs):
        distances = []
        for i in range(graph.trigger_num):
            for j in range(graph.trigger_num):
                abs_dist = np.abs(trigger_sent_ids[bid][i] - trigger_sent_ids[bid][j])
                abs_dist = min(max_sentence_distance, abs_dist)
                distances.append(abs_dist)
            distances.extend([max_sentence_distance] * (max_trigger_num - graph.trigger_num))
        distances.extend([max_sentence_distance] * max_trigger_num * (max_trigger_num - graph.trigger_num))
        dist_ids.append(distances)
    return dist_ids


class Linears(nn.Module):
    """Multiple linear layers with Dropout."""

    def __init__(self, dimensions, activation='relu', dropout_prob=0.0, bias=True):
        super().__init__()
        assert len(dimensions) > 1
        self.layers = nn.ModuleList([nn.Linear(dimensions[i], dimensions[i + 1], bias=bias)
                                     for i in range(len(dimensions) - 1)])
        self.activation = getattr(torch, activation)
        self.dropout = nn.Dropout(dropout_prob)

    def forward(self, inputs):
        for i, layer in enumerate(self.layers):
            if i > 0:
                inputs = self.activation(inputs)
                inputs = self.dropout(inputs)
            inputs = layer(inputs)
        return inputs


class CRF(nn.Module):
    def __init__(self, label_vocab, bioes=False):
        super(CRF, self).__init__()

        self.label_vocab = label_vocab
        self.label_size = len(label_vocab) + 2
        # self.same_type = self.map_same_types()
        self.bioes = bioes

        self.start = self.label_size - 2
        self.end = self.label_size - 1
        transition = torch.randn(self.label_size, self.label_size)
        self.transition = nn.Parameter(transition)
        self.initialize()

    def initialize(self):
        self.transition.data[:, self.end] = -100.0
        self.transition.data[self.start, :] = -100.0

        for label, label_idx in self.label_vocab.items():
            if label.startswith('I-') or label.startswith('E-'):
                self.transition.data[label_idx, self.start] = -100.0
            if label.startswith('B-') or label.startswith('I-'):
                self.transition.data[self.end, label_idx] = -100.0

        for label_from, label_from_idx in self.label_vocab.items():
            if label_from == 'O':
                label_from_prefix, label_from_type = 'O', 'O'
            else:
                label_from_prefix, label_from_type = label_from.split('-', 1)

            for label_to, label_to_idx in self.label_vocab.items():
                if label_to == 'O':
                    label_to_prefix, label_to_type = 'O', 'O'
                else:
                    label_to_prefix, label_to_type = label_to.split('-', 1)

                if self.bioes:
                    is_allowed = any(
                        [
                            label_from_prefix in ['O', 'E', 'S']
                            and label_to_prefix in ['O', 'B', 'S'],

                            label_from_prefix in ['B', 'I']
                            and label_to_prefix in ['I', 'E']
                            and label_from_type == label_to_type
                        ]
                    )
                else:
                    is_allowed = any(
                        [
                            label_to_prefix in ['B', 'O'],

                            label_from_prefix in ['B', 'I']
                            and label_to_prefix == 'I'
                            and label_from_type == label_to_type
                        ]
                    )
                if not is_allowed:
                    self.transition.data[
                        label_to_idx, label_from_idx] = -100.0

    def pad_logits(self, logits):
        """Pad the linear layer output with <SOS> and <EOS> scores.
        :param logits: Linear layer output (no non-linear function).
        """
        batch_size, seq_len, _ = logits.size()
        pads = logits.new_full((batch_size, seq_len, 2), -100.0,
                               requires_grad=False)
        logits = torch.cat([logits, pads], dim=2)
        return logits

    def calc_binary_score(self, labels, lens):
        batch_size, seq_len = labels.size()

        # A tensor of size batch_size * (seq_len + 2)
        labels_ext = labels.new_empty((batch_size, seq_len + 2))
        labels_ext[:, 0] = self.start
        labels_ext[:, 1:-1] = labels
        mask = sequence_mask(lens + 1, max_len=(seq_len + 2)).long()
        pad_stop = labels.new_full((1,), self.end, requires_grad=False)
        pad_stop = pad_stop.unsqueeze(-1).expand(batch_size, seq_len + 2)
        labels_ext = (1 - mask) * pad_stop + mask * labels_ext
        labels = labels_ext

        trn = self.transition
        trn_exp = trn.unsqueeze(0).expand(batch_size, self.label_size,
                                          self.label_size)
        lbl_r = labels[:, 1:]
        lbl_rexp = lbl_r.unsqueeze(-1).expand(*lbl_r.size(), self.label_size)
        # score of jumping to a tag
        trn_row = torch.gather(trn_exp, 1, lbl_rexp)

        lbl_lexp = labels[:, :-1].unsqueeze(-1)
        trn_scr = torch.gather(trn_row, 2, lbl_lexp)
        trn_scr = trn_scr.squeeze(-1)

        mask = sequence_mask(lens + 1).float()
        trn_scr = trn_scr * mask
        score = trn_scr

        return score

    def calc_unary_score(self, logits, labels, lens):
        """Checked"""
        labels_exp = labels.unsqueeze(-1)
        scores = torch.gather(logits, 2, labels_exp).squeeze(-1)
        mask = sequence_mask(lens).float()
        scores = scores * mask
        return scores

    def calc_gold_score(self, logits, labels, lens):
        """Checked"""
        unary_score = self.calc_unary_score(logits, labels, lens).sum(
            1).squeeze(-1)
        binary_score = self.calc_binary_score(labels, lens).sum(1).squeeze(-1)
        return unary_score + binary_score

    def calc_norm_score(self, logits, lens):
        batch_size, _, _ = logits.size()
        alpha = logits.new_full((batch_size, self.label_size), -100.0)
        alpha[:, self.start] = 0
        lens_ = lens.clone()

        logits_t = logits.transpose(1, 0)
        for logit in logits_t:
            logit_exp = logit.unsqueeze(-1).expand(batch_size,
                                                   self.label_size,
                                                   self.label_size)
            alpha_exp = alpha.unsqueeze(1).expand(batch_size,
                                                  self.label_size,
                                                  self.label_size)
            trans_exp = self.transition.unsqueeze(0).expand_as(alpha_exp)
            mat = logit_exp + alpha_exp + trans_exp
            alpha_nxt = log_sum_exp(mat, 2).squeeze(-1)

            mask = (lens_ > 0).float().unsqueeze(-1).expand_as(alpha)
            alpha = mask * alpha_nxt + (1 - mask) * alpha
            lens_ = lens_ - 1

        alpha = alpha + self.transition[self.end].unsqueeze(0).expand_as(alpha)
        norm = log_sum_exp(alpha, 1).squeeze(-1)

        return norm

    def loglik(self, logits, labels, lens):
        norm_score = self.calc_norm_score(logits, lens)
        gold_score = self.calc_gold_score(logits, labels, lens)
        return gold_score - norm_score

    def viterbi_decode(self, logits, lens):
        """Borrowed from pytorch tutorial
        Arguments:
            logits: [batch_size, seq_len, n_labels] FloatTensor
            lens: [batch_size] LongTensor
        """
        batch_size, _, n_labels = logits.size()
        vit = logits.new_full((batch_size, self.label_size), -100.0)
        vit[:, self.start] = 0
        c_lens = lens.clone()

        logits_t = logits.transpose(1, 0)
        pointers = []
        for logit in logits_t:
            vit_exp = vit.unsqueeze(1).expand(batch_size, n_labels, n_labels)
            trn_exp = self.transition.unsqueeze(0).expand_as(vit_exp)
            vit_trn_sum = vit_exp + trn_exp
            vt_max, vt_argmax = vit_trn_sum.max(2)

            vt_max = vt_max.squeeze(-1)
            vit_nxt = vt_max + logit
            pointers.append(vt_argmax.squeeze(-1).unsqueeze(0))

            mask = (c_lens > 0).float().unsqueeze(-1).expand_as(vit_nxt)
            vit = mask * vit_nxt + (1 - mask) * vit

            mask = (c_lens == 1).float().unsqueeze(-1).expand_as(vit_nxt)
            vit += mask * self.transition[self.end].unsqueeze(
                0).expand_as(vit_nxt)

            c_lens = c_lens - 1

        pointers = torch.cat(pointers)
        scores, idx = vit.max(1)
        paths = [idx.unsqueeze(1)]
        for argmax in reversed(pointers):
            idx_exp = idx.unsqueeze(-1)
            idx = torch.gather(argmax, 1, idx_exp)
            idx = idx.squeeze(-1)

            paths.insert(0, idx.unsqueeze(1))

        paths = torch.cat(paths[1:], 1)
        scores = scores.squeeze(-1)

        return scores, paths

    def calc_conf_score_(self, logits, labels):
        batch_size, _, _ = logits.size()

        logits_t = logits.transpose(1, 0)
        scores = [[] for _ in range(batch_size)]
        pre_labels = [self.start] * batch_size
        for i, logit in enumerate(logits_t):
            logit_exp = logit.unsqueeze(-1).expand(batch_size,
                                                   self.label_size,
                                                   self.label_size)
            trans_exp = self.transition.unsqueeze(0).expand(batch_size,
                                                            self.label_size,
                                                            self.label_size)
            score = logit_exp + trans_exp
            score = score.view(-1, self.label_size * self.label_size) \
                .softmax(1)
            for j in range(batch_size):
                cur_label = labels[j][i]
                cur_score = score[j][cur_label * self.label_size + pre_labels[j]]
                scores[j].append(cur_score)
                pre_labels[j] = cur_label
        return scores
