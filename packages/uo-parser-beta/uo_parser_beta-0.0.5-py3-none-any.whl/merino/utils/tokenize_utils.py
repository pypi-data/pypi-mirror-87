import os
import re
import json
import sys
from .base_utils import *
from copy import deepcopy

NEWLINE_WHITESPACE_RE = re.compile(r'\n\s*\n')
NUMERIC_RE = re.compile(r'^([\d]+[,\.]*)+$')
WHITESPACE_RE = re.compile(r'\s')
PARAGRAPH_BREAK = re.compile(r'\n\s*\n')
MWT_SPLIT = '<mwt-split>'

PUNCTUATION = re.compile(
    r'''["’'\(\)\[\]\{\}<>:\,‒–—―…!\.«»\-‐\?‘’“”;/⁄␠·&@\*\\•\^¤¢\$€£¥₩₪†‡°¡¿¬\#№%‰‱¶′§~¨_\|¦⁂☞∴‽※"]''')

SPECIAL_MAP = {
    '...': '…'
}


def pseudo_tokenize(sent_text):
    tokens_by_space = sent_text.split()
    pseudo_tokens = []
    for token in tokens_by_space:
        if len(PUNCTUATION.findall(token)) > 0:
            tmp = ''
            for char in token:
                if PUNCTUATION.match(char):
                    if tmp != '':
                        pseudo_tokens.append(tmp)
                        tmp = ''
                    pseudo_tokens.append(char)
                else:
                    tmp += char
            if tmp != '':
                pseudo_tokens.append(tmp)
        else:
            pseudo_tokens.append(token)

    assert len(''.join(sent_text.split())) == len(''.join(pseudo_tokens))
    return pseudo_tokens


def get_startchar_idx(word, text):
    # ******* search for first non-space character *******
    start_char_idx = 0
    for k in range(len(text)):
        if len(text[k].strip()) > 0:
            start_char_idx = k
            break
    text = text[start_char_idx + len(word):]
    return text, start_char_idx


def get_character_locations(string_units, text):
    tmp_text = deepcopy(text)
    offset = 0
    end_positions = []
    for str_unit in string_units:
        tmp_text, start_position = get_startchar_idx(str_unit, tmp_text)
        start_position += offset
        end_position = start_position + len(str_unit) - 1
        end_positions.append(end_position)
        offset = start_position + len(str_unit)
    return end_positions


def get_mapping_wp_character_to_or_character(wordpiece_splitter, wp_single_string, or_single_string):
    wp_char_to_or_char = {}
    converted_text = ''
    for char_id, char in enumerate(or_single_string):
        converted_chars = ''.join([c if not c.startswith('▁') else c[1:] for c in wordpiece_splitter.tokenize(char) if c != '▁'])

        for converted_c in converted_chars:
            c_id = len(converted_text)
            wp_char_to_or_char[c_id] = char_id
            converted_text += converted_c
    assert wp_single_string == converted_text
    return wp_char_to_or_char


def wordpiece_tokenize_from_raw_text(wordpiece_splitter, sent_text, sent_labels, sent_position_in_paragraph,
                                     treebank_name):
    if 'Chinese' in treebank_name or 'Japanese' in treebank_name:
        pseudo_tokens = [c for c in sent_text]  # characters as pseudo tokens
    else:
        pseudo_tokens = pseudo_tokenize(sent_text)
    end_pids = set()
    group_pieces = [wordpiece_splitter.tokenize(t) for t in
                    pseudo_tokens]  # texts could be considered as a list of pseudo tokens
    flat_wordpieces = []
    for group in group_pieces:
        if len(group) > 0:
            for p in group:
                if p != '▁':
                    pid = len(flat_wordpieces)
                    flat_wordpieces.append((p, pid))
            end_pids.add(len(flat_wordpieces) - 1)

    single_original_string = ''.join([c.strip() for c in sent_text])

    original_characters = [c for c in single_original_string]
    character_locations = get_character_locations(original_characters, sent_text)

    single_wordpiece_string = ''.join([p if not p.startswith('▁') else p.lstrip('▁') for p, pid in flat_wordpieces])

    wp_character_2_or_character = get_mapping_wp_character_to_or_character(wordpiece_splitter, single_wordpiece_string,
                                                                           single_original_string)

    flat_wordpiece_labels = []
    flat_wordpiece_ends = []
    offset = 0
    for wordpiece, _ in flat_wordpieces:
        if wordpiece.startswith('▁'):
            str_form = wordpiece[1:]
        else:
            str_form = wordpiece
        end_char = offset + len(str_form) - 1
        ori_char = wp_character_2_or_character[end_char]
        location_in_sentence = character_locations[ori_char]
        wp_label = int(sent_labels[location_in_sentence])
        wp_end = sent_position_in_paragraph + location_in_sentence
        flat_wordpiece_labels.append(wp_label)
        flat_wordpiece_ends.append(wp_end)

        offset = end_char + 1

    return flat_wordpieces, flat_wordpiece_labels, flat_wordpiece_ends, end_pids


def split_to_sentences(paragraph_text, charlabels, mwtlabels, treebank_name):
    sent_text = ''
    sent_labels = ''
    sent_mwt_labels = []
    sentences = []
    start = 0
    mwt_id = 0
    for k in range(len(charlabels)):
        sent_text += paragraph_text[k]
        sent_labels += charlabels[k]
        if charlabels[k] == '3' or charlabels[k] == '4':
            sent_mwt_labels.append(mwtlabels[mwt_id])
            mwt_id += 1
        if charlabels[k] == '2' or charlabels[k] == '4':
            end = k  # (start, end) local position in REFURBISHED paragraph (REFURBISHED means the \newline characters are removed from a paragraph text
            sentences.append((deepcopy(sent_text), deepcopy(sent_labels), deepcopy(sent_mwt_labels), start, end))
            start = end + 1
            sent_text = ''
            sent_labels = ''
            sent_mwt_labels = []

    if len(sentences) > 0:  # case: train data
        # a paragraph not always ends with a 2 or 4 label
        if not (len(sent_text) == 0 and len(sent_labels) == 0 and len(
                sent_mwt_labels) == 0):
            sentences.append(
                (deepcopy(sent_text), deepcopy(sent_labels), deepcopy(sent_mwt_labels), start, len(paragraph_text) - 1))
    else:
        sentences = [(paragraph_text, charlabels, mwtlabels, 0, len(paragraph_text) - 1)]
    return sentences


def split_to_subsequences(wordpieces, wordpiece_labels, sent_mwt_labels, wordpiece_ends, end_piece_ids,
                          max_input_length):
    subsequences = []
    subseq = [[], [], [], []]
    sub_mwt_labels = []
    mwt_id = 0
    for wp_wpid, wl, we in zip(wordpieces, wordpiece_labels, wordpiece_ends):
        wp, wpid = wp_wpid
        subseq[0].append((wp, wpid))
        subseq[1].append(wl)
        if wl == 3 or wl == 4:
            sub_mwt_labels.append(sent_mwt_labels[mwt_id])
            mwt_id += 1
        subseq[3].append(we)
        if wpid in end_piece_ids and len(subseq[0]) >= max_input_length - 10:
            subsequences.append((subseq[0], subseq[1], sub_mwt_labels, subseq[3], end_piece_ids))

            subseq = [[], [], [], []]
            sub_mwt_labels = []

    if len(subseq[0]) > 0:
        subsequences.append((subseq[0], subseq[1], sub_mwt_labels, subseq[3], end_piece_ids))
    return subsequences


def stanza_charlevel_format_to_wordpiece_format(wordpiece_splitter, max_input_length, plaintext, treebank_name):
    corpus_labels = '\n\n'.join(['0' * len(pt.rstrip()) for pt in NEWLINE_WHITESPACE_RE.split(plaintext)])
    corpus_mwt_labels = [[] for pt in NEWLINE_WHITESPACE_RE.split(plaintext)]

    data = [{'text': pt.rstrip(), 'charlabels': pc, 'mwtlabels': pmwt} for pt, pc, pmwt in
            zip(NEWLINE_WHITESPACE_RE.split(plaintext), NEWLINE_WHITESPACE_RE.split(corpus_labels),
                corpus_mwt_labels) if
            len(pt.rstrip()) > 0]

    wordpiece_examples = []
    kept_tokens = 0
    total_tokens = 0
    for paragraph_index, paragraph in enumerate(data):
        paragraph_text = paragraph['text']
        paragraph_labels = paragraph['charlabels']
        paragraph_mwt_labels = paragraph['mwtlabels']
        # split to sentences
        sentences = split_to_sentences(paragraph_text, paragraph_labels, paragraph_mwt_labels, treebank_name)
        tmp_examples = []
        for sent in sentences:
            sent_text, sent_labels, sent_mwt_labels, sent_start, sent_end = sent
            wordpieces, wordpiece_labels, wordpiece_ends, end_piece_ids = wordpiece_tokenize_from_raw_text(
                wordpiece_splitter, sent_text,
                sent_labels, sent_start,
                treebank_name)
            kept_tokens += len([x for x in wordpiece_labels if x != 0])
            total_tokens += len([x for x in sent_labels if x != '0'])
            if len(wordpieces) <= max_input_length - 2:  # minus 2: reserved for <s> and </s>
                tmp_examples.append((wordpieces, wordpiece_labels, sent_mwt_labels, wordpiece_ends, end_piece_ids))
            else:
                subsequences = split_to_subsequences(wordpieces, wordpiece_labels, sent_mwt_labels, wordpiece_ends,
                                                     end_piece_ids,
                                                     max_input_length)
                for subseq in subsequences:
                    tmp_examples.append(subseq)
        # merge consecutive sentences/subsequences
        new_example = [[], [], [], []]
        for example in tmp_examples:
            if len(new_example[0]) + len(example[0]) > max_input_length - 2:
                num_extra_wordpieces = min(max_input_length - 2 - len(new_example[0]), len(example[0]))
                end_piece_ids = example[-1]
                takeout_position = 0
                for tmp_id in range(num_extra_wordpieces):
                    wp, wpid = example[0][tmp_id]
                    if wpid in end_piece_ids:
                        takeout_position = tmp_id + 1
                num_extra_wordpieces = takeout_position
                new_example[0] += deepcopy(example[0][: num_extra_wordpieces])
                new_example[1] += deepcopy(example[1][: num_extra_wordpieces])

                extra_mwt_labels = []
                mwt_id = 0
                for pid in range(num_extra_wordpieces):
                    if example[1][pid] == 3 or example[1][pid] == 4:
                        extra_mwt_labels.append(deepcopy(example[2][mwt_id]))
                        mwt_id += 1
                new_example[2] += extra_mwt_labels

                new_example[3] += deepcopy(example[3][: num_extra_wordpieces])
                wordpiece_examples.append(
                    ([wp for wp, wpid in new_example[0]], new_example[1], new_example[2], new_example[3],
                     paragraph_index))
                # start new example
                new_example = [[], [], [], []]

            new_example[0] += deepcopy(example[0])
            new_example[1] += deepcopy(example[1])
            new_example[2] += deepcopy(example[2])
            new_example[3] += deepcopy(example[3])
        if len(new_example[0]) > 0:
            wordpiece_examples.append(
                ([wp for wp, wpid in new_example[0]], new_example[1], new_example[2], new_example[3], paragraph_index))

    final_examples = []
    for wp_example in wordpiece_examples:
        wordpieces, wordpiece_labels, seq_mwt_labels, wordpiece_ends, paragraph_index = wp_example
        final_examples.append({
            'wordpieces': wordpieces,
            'wordpiece_labels': wordpiece_labels,
            'mwt_labels': seq_mwt_labels,
            'wordpiece_ends': wordpiece_ends,
            'paragraph_index': paragraph_index
        })

    return final_examples


def stanza_tokenize_scorer(labels, all_preds, treebank_name):
    def f1(pred, gold, mapping):
        pred = [mapping[p] for p in pred]
        gold = [mapping[g] for g in gold]

        lastp = -1
        lastg = -1
        tp = 0
        fp = 0
        fn = 0
        for i, (p, g) in enumerate(zip(pred, gold)):
            if p == g > 0 and lastp == lastg:
                lastp = i
                lastg = i
                tp += 1
            elif p > 0 and g > 0:
                lastp = i
                lastg = i
                fp += 1
                fn += 1
            elif p > 0:
                # and g == 0
                lastp = i
                fp += 1
            elif g > 0:
                lastg = i
                fn += 1

        if tp == 0:
            return 0
        else:
            return 2 * tp / (2 * tp + fp + fn)

    f1tok = f1(all_preds, labels, {0: 0, 1: 1, 2: 1, 3: 1, 4: 1})
    f1sent = f1(all_preds, labels, {0: 0, 1: 0, 2: 1, 3: 0, 4: 1})
    f1mwt = f1(all_preds, labels, {0: 0, 1: 1, 2: 1, 3: 2, 4: 2})
    print(
        f"{treebank_name}: token F1 = {f1tok * 100:.2f}, sentence F1 = {f1sent * 100:.2f}, mwt F1 = {f1mwt * 100:.2f}")
    return harmonic_mean([f1tok, f1sent, f1mwt], [1, 1, .01])


def conllu_to_stanza_charlevel_format(plaintext_file, conllu_file, char_labels_output_fpath,
                                      mwt_labels_output_fpath, mwt_output_fpath):
    # this function is borrowed from stanza library.
    # `charlevel_output` will be aligned with `plaintext_file` at character-level.
    # each character in `charlevel_output` tells the type of the corresponding character in `plaintext_file`.
    # there are 5 types of a character in `plaintext_file`:
    #  0: NOT an end-of-token
    #  1: an end-of-token, NOT an end-of-sentence
    #  2: an end-of-token, also an end-of-sentence
    #  3: an end-of-token, also an end-of-multi-word-token, NOT an end-of-sentence
    #  4: an end-of-token, also an end-of-multi-word-token, an end-of-sentence
    with open(plaintext_file, 'r') as f:
        corpus_text = ''.join(f.readlines())
    textlen = len(corpus_text)

    ensure_dir(os.path.abspath(os.path.join(char_labels_output_fpath, '..')))
    output = open(char_labels_output_fpath, 'w')

    index = 0  # character offset in rawtext

    def is_para_break(index, text):
        """ Detect if a paragraph break can be found, and return the length of the paragraph break sequence. """
        if text[index] == '\n':
            para_break = PARAGRAPH_BREAK.match(text[index:])
            if para_break:
                break_len = len(para_break.group(0))
                return True, break_len
        return False, 0

    def find_next_word(index, text, word, output):
        """
        Locate the next word in the text. In case a paragraph break is found, also write paragraph break to labels.
        """
        idx = 0
        word_sofar = ''
        yeah = False
        while index < len(text) and idx < len(word):
            para_break, break_len = is_para_break(index, text)
            if para_break:
                # multiple newlines found, paragraph break
                if len(word_sofar) > 0:
                    assert re.match(r'^\s+$',
                                    word_sofar), 'Found non-empty string at the end of a paragraph that doesn\'t match any token: |{}|'.format(
                        word_sofar)
                    word_sofar = ''

                output.write('\n\n')
                index += break_len - 1
            elif re.match(r'^\s$', text[index]) and not re.match(r'^\s$', word[idx]):
                # whitespace found, and whitespace is not part of a word
                word_sofar += text[index]
            else:
                # non-whitespace char, or a whitespace char that's part of a word
                word_sofar += text[index]
                assert text[index].replace('\n', ' ') == word[
                    idx], "Character mismatch: raw text contains |%s| but the next word is |%s|." % (word_sofar, word)
                idx += 1
            index += 1
        return index, word_sofar

    mwt_vocab = {'not-mwt-token': 0}
    mwt_expansions = []

    found_mwt_ids = []
    with open(conllu_file, 'r') as f:
        buf = ''
        mwtbegin = 0
        mwtend = -1
        expanded = []
        last_comments = ""
        for line in f:
            line = line.strip()
            if len(line):
                if line[0] == "#":
                    # comment, don't do anything
                    if len(last_comments) == 0:
                        last_comments = line
                    continue

                line = line.split('\t')
                if '.' in line[0]:
                    # the tokenizer doesn't deal with ellipsis
                    continue

                word = line[1]
                if '-' in line[0]:
                    # multiword token
                    mwtbegin, mwtend = [int(x) for x in line[0].split('-')]
                    lastmwt = word
                    expanded = []
                elif mwtbegin <= int(line[0]) < mwtend:
                    expanded += [word]
                    continue
                elif int(line[0]) == mwtend:
                    expanded += [word]
                    expanded = [x.lower() for x in expanded]  # evaluation doesn't care about case
                    mwt_expansions += [(lastmwt, tuple(expanded))]

                    mwt_vocab[MWT_SPLIT.join(expanded)] = mwt_vocab.get(MWT_SPLIT.join(expanded),
                                                                        len(mwt_vocab))
                    found_mwt_ids.append(mwt_vocab[MWT_SPLIT.join(expanded)])

                    if lastmwt[0].islower() and not expanded[0][0].islower():
                        print('Sentence ID with potential wrong MWT expansion: ', last_comments)
                    mwtbegin = 0
                    mwtend = -1
                    lastmwt = None
                    continue

                if len(buf):
                    output.write(buf)
                index, word_found = find_next_word(index, corpus_text, word, output)
                buf = '0' * (len(word_found) - 1) + ('1' if '-' not in line[0] else '3')
            else:
                # sentence break found
                if len(buf):
                    assert int(buf[-1]) >= 1
                    output.write(buf[:-1] + '{}'.format(int(buf[-1]) + 1))
                    buf = ''

                last_comments = ''

    output.close()

    with open(char_labels_output_fpath) as f:
        corpus_wp_labels = ''.join(f.readlines()).rstrip()

    paragraph_wp_labels = [pc for pc in
                           NEWLINE_WHITESPACE_RE.split(corpus_wp_labels)]

    corpus_mwt_labels = []
    count = 0
    for wp_labels in paragraph_wp_labels:
        mwt_labels = []
        for char in wp_labels:
            if char == '3' or char == '4':
                mwt_labels.append(found_mwt_ids[count])
                count += 1
        corpus_mwt_labels.append(mwt_labels)

    with open(mwt_labels_output_fpath, 'w') as f:
        json.dump(corpus_mwt_labels, f)

    from collections import Counter
    mwts = Counter(mwt_expansions)
    if mwt_output_fpath is None:
        print('MWTs:', mwts)
    else:
        with open(mwt_output_fpath, 'w') as f:
            json.dump(list(mwts.items()), f)

        print('{} unique MWTs found in data'.format(len(mwts)))
    return mwt_vocab


if __name__ == '__main__':
    text_fpath = sys.argv[1]
    conllu_fpath = sys.argv[2]
    charlevel_output = 'charlevel_output.txt'
    mwt_output = 'mwt_output.json'

    conllu_to_stanza_charlevel_format(
        plaintext_file=text_fpath,
        conllu_file=conllu_fpath,
        char_labels_output_fpath=charlevel_output,
        mwt_output_fpath=mwt_output
    )
    from transformers import XLMRobertaTokenizer

    tokenizer = XLMRobertaTokenizer.from_pretrained('xlm-roberta-base')
    stanza_charlevel_format_to_wordpiece_format(
        wordpiece_splitter=tokenizer,
        max_input_length=256,
        plaintext_file=text_fpath,
        wordpiece_labels_output_fpath='wordpiece_examples.json',
        char_labels_output_fpath=charlevel_output
    )
    # sample command:
    # python -m utils.tokenize_utils datasets/ud-treebanks-v2.5/UD_English-EWT/en_ewt-ud-train.txt datasets/ud-treebanks-v2.5/UD_English-EWT/en_ewt-ud-train.conllu
