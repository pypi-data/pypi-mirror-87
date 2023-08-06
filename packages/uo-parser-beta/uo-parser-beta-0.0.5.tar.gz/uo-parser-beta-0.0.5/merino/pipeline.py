import os
import json
import copy
import torch
from .train import config as master_config
from torch.utils.data import DataLoader
from .models.base_model import EmbeddingModel
from .models.combined_model import TokenizerClassifier, TaggerClassifier
from .iterators.tokenize_iterators import TokenizeDatasetLive
from .iterators.tagger_iterators import TaggerDatasetLive
from .utils.tokenize_utils import *
from collections import defaultdict
from .utils.doc import *
from .utils.conll import CoNLL
from .resources.tbinfo import tbname2training_id, tbname2shorthand, lang2treebank
from .utils.chuliu_edmonds import *
from .stanza.models.mwt_expander import get_mwt_model
from .stanza.models.mwt.data import DataLoader as MWTDataLoader
from .stanza.models.lemma.data import DataLoader as LemmaDataLoader
from .stanza.utils.conll import CoNLL as stanzaCoNLL
from .stanza.models.lemmatizer import get_lemma_model
from .stanza.models.identity_lemmatizer import get_identity_lemma_model
from transformers import XLMRobertaTokenizer


class MWTWrapper:
    def __init__(self, config, treebank_name):
        self.config = config
        self.shorthand = tbname2shorthand[treebank_name]
        self.model, self.args, self.loaded_args, self.vocab = get_mwt_model(config.cache_dir,
                                                                            language=treebank2lang[treebank_name])
        print('Loaded multi-word expander for {}'.format(treebank2lang[treebank_name]))

    def predict(self, tokenized_doc):
        args = self.args
        loaded_args = self.loaded_args
        vocab = self.vocab
        # load data
        # write to buffer
        CoNLL.dict2conll(tokenized_doc,
                         os.path.join(self.config.cache_dir, 'buff.tok.{}'.format(self.config.default_language)))
        # load from buffer
        doc = Document(
            stanzaCoNLL.conll2dict(
                os.path.join(self.config.cache_dir, 'buff.tok.{}'.format(self.config.default_language))))
        batch = MWTDataLoader(doc, args['batch_size'], loaded_args, vocab=vocab, evaluation=True)

        if len(batch) > 0:
            dict_preds = self.model.predict_dict(batch.doc.get_mwt_expansions(evaluation=True))
            # decide trainer type and run eval
            if loaded_args['dict_only']:
                preds = dict_preds
            else:
                preds = []
                for i, b in enumerate(batch):
                    preds += self.model.predict(b)

                if loaded_args.get('ensemble_dict', False):
                    preds = self.model.ensemble(batch.doc.get_mwt_expansions(evaluation=True), preds)
        else:
            # skip eval if dev data does not exist
            preds = []

        # write to file and score
        doc = copy.deepcopy(batch.doc)
        doc.set_mwt_expansions(preds)
        expanded_doc = doc.to_dict()
        return expanded_doc


class LemmaWrapper:
    def __init__(self, config, treebank_name):
        self.config = config
        self.treebank_name = treebank_name
        self.shorthand = tbname2shorthand[self.treebank_name]
        if self.treebank_name in ['UD_Old_French-SRCMF', 'UD_Vietnamese-VTB']:
            self.args = get_identity_lemma_model(self.shorthand)
        else:
            self.model, self.args, self.loaded_args, self.vocab = get_lemma_model(self.config.cache_dir,
                                                                                  treebank2lang[treebank_name])
        print('Loaded lemmatizer for {}'.format(treebank2lang[treebank_name]))

    def predict(self, tagged_doc):
        if self.treebank_name not in ['UD_Old_French-SRCMF', 'UD_Vietnamese-VTB']:
            args = self.args
            loaded_args = self.loaded_args
            vocab = self.vocab
            # load data
            # write to buffer
            stanzaCoNLL.dict2conll(tagged_doc,
                                   os.path.join(self.config.cache_dir,
                                                'buff.lem.{}'.format(self.config.default_language)))
            doc = Document(
                stanzaCoNLL.conll2dict(
                    os.path.join(self.config.cache_dir, 'buff.lem.{}'.format(self.config.default_language))))
            batch = LemmaDataLoader(doc, args['batch_size'], loaded_args, vocab=vocab,
                                    evaluation=True)

            # skip eval if dev data does not exist
            if len(batch) == 0:
                print("Skip evaluation because no dev data is available...")
                print("Lemma score:")
                print("{} ".format(args['lang']))
                sys.exit(0)

            dict_preds = self.model.predict_dict(batch.doc.get([TEXT, UPOS]))

            if loaded_args.get('dict_only', False):
                preds = dict_preds
            else:
                preds = []
                edits = []
                for i, b in enumerate(batch):
                    ps, es = self.model.predict(b, args['beam_size'])
                    preds += ps
                    if es is not None:
                        edits += es
                preds = self.model.postprocess(batch.doc.get([TEXT]), preds, edits=edits)

                if loaded_args.get('ensemble_dict', False):
                    preds = self.model.ensemble(batch.doc.get([TEXT, UPOS]), preds)

            # write to file and score
            batch.doc.set([LEMMA], preds)
            lemmatized_doc = batch.doc.to_dict()
        else:
            args = self.args
            # write to buffer
            stanzaCoNLL.dict2conll(tagged_doc, os.path.join(self.config.cache_dir,
                                                            'buff.lem.{}'.format(self.config.default_language)))
            document = Document(stanzaCoNLL.conll2dict(
                os.path.join(self.config.cache_dir, 'buff.lem.{}'.format(self.config.default_language))))
            batch = LemmaDataLoader(document, args['batch_size'], args, evaluation=True,
                                    conll_only=True)

            # use identity mapping for prediction
            preds = batch.doc.get([TEXT])

            # write to file and score
            batch.doc.set([LEMMA], preds)
            lemmatized_doc = batch.doc.to_dict()
        return lemmatized_doc


class Pipeline:
    def __init__(self, language, cache_dir=None):
        super(Pipeline, self).__init__()

        if cache_dir is None:
            master_config.cache_dir = 'cache/merino'
        else:
            master_config.cache_dir = cache_dir

        if not os.path.exists(master_config.cache_dir):
            os.makedirs(master_config.cache_dir, exist_ok=True)

        master_config.wordpiece_splitter = XLMRobertaTokenizer.from_pretrained('xlm-roberta-base',
                                                                               cache_dir=os.path.join(
                                                                                   master_config.cache_dir,
                                                                                   'xlmr'))
        self.lang_list = [language]
        for lang in self.lang_list:
            assert lang in lang2treebank, '{} has not been supported. Currently supported languages: {}'.format(lang,
                                                                                                                list(
                                                                                                                    lang2treebank.keys()))
        self.config = master_config

        # download saved model for initial language
        download(
            cache_dir=self.config.cache_dir,
            language=language
        )

        # load ALL vocabs
        self.load_vocabs()

        # shared multilingual embeddings
        self.embedding_layers = EmbeddingModel(self.config)
        self.embedding_layers.cuda()
        self.embedding_layers.eval()
        # tokenizers
        self.tokenizer = {}
        for lang in self.lang_list:
            self.tokenizer[lang] = TokenizerClassifier(self.config, treebank_name=lang2treebank[lang])
            self.tokenizer[lang].cuda()
            self.tokenizer[lang].eval()
        # taggers
        self.tagger = {}
        for lang in self.lang_list:
            self.tagger[lang] = TaggerClassifier(self.config, treebank_name=lang2treebank[lang])
            self.tagger[lang].cuda()
            self.tagger[lang].eval()

        #     - mwt and lemma: reuse stanza's models
        self.mwt_model = {}
        for lang in self.lang_list:
            treebank_name = lang2treebank[lang]
            if tbname2training_id[treebank_name] % 2 == 1:
                self.mwt_model[lang] = MWTWrapper(self.config, treebank_name=treebank_name)
        self.lemma_model = {}
        for lang in self.lang_list:
            treebank_name = lang2treebank[lang]
            self.lemma_model[lang] = LemmaWrapper(self.config, treebank_name=treebank_name)

        # load and hold the pretrained weights
        self.embedding_weights = self.embedding_layers.state_dict()
        self.set_default_language(language)

    def set_default_language(self, language):
        assert language in self.lang_list
        self.config.default_language = language
        self.default_language = language
        self.config.treebank_name = lang2treebank[language]
        print('Default language: {}'.format(self.config.default_language))

    def add_language(self, lang):
        if lang in self.lang_list:
            print('Language `{}` was already added'.format(lang))
        else:
            # download saved models
            download(
                cache_dir=self.config.cache_dir,
                language=lang
            )
            # update vocabs
            treebank_name = lang2treebank[lang]
            with open(os.path.join(self.config.cache_dir,
                                   '{}/{}.vocabs.json'.format(treebank2lang[treebank_name], treebank2lang[treebank_name]))) as f:
                vocabs = json.load(f)
                self.config.vocabs[treebank_name] = vocabs
            self.config.itos[lang][UPOS] = {v: k for k, v in vocabs[UPOS].items()}
            self.config.itos[lang][XPOS] = {v: k for k, v in vocabs[XPOS].items()}
            self.config.itos[lang][FEATS] = {v: k for k, v in vocabs[FEATS].items()}
            self.config.itos[lang][DEPREL] = {v: k for k, v in vocabs[DEPREL].items()}
            # add tokenizer
            self.tokenizer[lang] = TokenizerClassifier(self.config, treebank_name=lang2treebank[lang])
            self.tokenizer[lang].cuda()
            self.tokenizer[lang].eval()
            # add tagger
            self.tagger[lang] = TaggerClassifier(self.config, treebank_name=lang2treebank[lang])
            self.tagger[lang].cuda()
            self.tagger[lang].eval()
            # mwt if needed
            treebank_name = lang2treebank[lang]
            if tbname2training_id[treebank_name] % 2 == 1:
                self.mwt_model[lang] = MWTWrapper(self.config, treebank_name=treebank_name)
            # lemma
            self.lemma_model[lang] = LemmaWrapper(self.config, treebank_name=treebank_name)
            # later, possibly NER
            self.lang_list.append(lang)

    def load_vocabs(self):
        self.config.vocabs = {}
        self.config.itos = defaultdict(dict)
        for lang in self.lang_list:
            treebank_name = lang2treebank[lang]
            with open(os.path.join(self.config.cache_dir,
                                   '{}/{}.vocabs.json'.format(treebank2lang[treebank_name], treebank2lang[treebank_name]))) as f:
                vocabs = json.load(f)
                self.config.vocabs[treebank_name] = vocabs
            self.config.itos[lang][UPOS] = {v: k for k, v in vocabs[UPOS].items()}
            self.config.itos[lang][XPOS] = {v: k for k, v in vocabs[XPOS].items()}
            self.config.itos[lang][FEATS] = {v: k for k, v in vocabs[FEATS].items()}
            self.config.itos[lang][DEPREL] = {v: k for k, v in vocabs[DEPREL].items()}

    def load_adapter_weights(self, model_name):
        assert model_name in ['tokenizer', 'tagger']
        pretrained_weights = self.tokenizer[
            self.config.default_language].pretrained_tokenizer_weights if model_name == 'tokenizer' else \
            self.tagger[self.config.default_language].pretrained_tagger_weights
        for name, value in pretrained_weights.items():
            if 'adapters.{}.adapter'.format(model_name) in name:
                target_name = name.replace('adapters.{}.adapter'.format(model_name), 'adapters.embedding.adapter')
                self.embedding_weights[target_name] = value
        self.embedding_layers.load_state_dict(self.embedding_weights)

    def tokenize(self, raw_text):
        # load input text
        config = self.config
        test_set = TokenizeDatasetLive(config, raw_text)
        test_set.numberize(config.wordpiece_splitter)

        # load weights of tokenizer into the combined model
        self.load_adapter_weights(model_name='tokenizer')

        # make predictions
        wordpiece_pred_labels, wordpiece_ends, paragraph_indexes = [], [], []
        for batch in DataLoader(test_set, batch_size=self.config.eval_batch_size,
                                shuffle=False, collate_fn=test_set.collate_fn):
            wordpiece_reprs = self.embedding_layers.get_tokenizer_inputs(batch)
            predictions = self.tokenizer[self.config.default_language].predict(batch, wordpiece_reprs)
            wp_pred_labels, wp_ends, para_ids = predictions[0], predictions[1], predictions[2]
            wp_pred_labels = wp_pred_labels.data.cpu().numpy().tolist()

            for i in range(len(wp_pred_labels)):
                wordpiece_pred_labels.append(wp_pred_labels[i][: len(wp_ends[i])])

            wordpiece_ends.extend(wp_ends)
            paragraph_indexes.extend(para_ids)
        # mapping
        para_id_to_wp_pred_labels = defaultdict(list)

        for wp_pred_ls, wp_es, p_index in zip(wordpiece_pred_labels, wordpiece_ends,
                                              paragraph_indexes):
            para_id_to_wp_pred_labels[p_index].extend([(pred, char_position) for pred, char_position in
                                                       zip(wp_pred_ls, wp_es)])
        # get predictions
        corpus_text = raw_text

        paragraphs = [pt.rstrip() for pt in
                      NEWLINE_WHITESPACE_RE.split(corpus_text) if
                      len(pt.rstrip()) > 0]
        all_wp_preds = []
        all_raw = []
        ##############
        for para_index, para_text in enumerate(paragraphs):
            para_wp_preds = [0 for _ in para_text]
            for wp_l, end_position in para_id_to_wp_pred_labels[para_index]:
                para_wp_preds[end_position] = wp_l

            all_wp_preds.append(para_wp_preds)
            all_raw.append(para_text)
        ###########################3
        offset = 0
        doc = []
        for j in range(len(paragraphs)):
            raw = all_raw[j]
            wp_pred = all_wp_preds[j]

            current_tok = ''
            current_sent = []

            for t, wp_p in zip(raw, wp_pred):
                offset += 1
                current_tok += t
                if wp_p >= 1:
                    tok = normalize_token(test_set.treebank_name, current_tok)
                    assert '\t' not in tok, tok
                    if len(tok) <= 0:
                        current_tok = ''
                        continue
                    additional_info = dict()
                    current_sent += [(tok, wp_p, additional_info)]
                    current_tok = ''
                    if (wp_p == 2 or wp_p == 4):
                        doc.append(process_sentence(current_sent))
                        current_sent = []

            if len(current_tok):
                tok = normalize_token(test_set.treebank_name, current_tok)
                assert '\t' not in tok, tok
                if len(tok) > 0:
                    additional_info = dict()
                    current_sent += [(tok, 2, additional_info)]

            if len(current_sent):
                doc.append(process_sentence(current_sent))

        return doc

    def tag_sentence(self, tokenized_sentence):
        temp = []
        for i, word in enumerate(tokenized_sentence):
            temp.append({ID: f'{i + 1}', TEXT: word})
        tokenized_doc = [temp]

        CoNLL.dict2conll(tokenized_doc,
                         os.path.join(self.config.cache_dir, 'buff.tok.{}'.format(self.config.default_language)))
        tokenized_doc = stanzaCoNLL.conll2dict(
            os.path.join(self.config.cache_dir, 'buff.tok.{}'.format(self.config.default_language)))
        return self.tag(tokenized_doc)[0]

    def tag(self, tokenized_doc):
        # load outputs of tokenizer
        config = self.config
        # write to buffer
        stanzaCoNLL.dict2conll(tokenized_doc,
                               os.path.join(self.config.cache_dir,
                                            'buff.tag.{}'.format(self.config.default_language)))
        test_set = TaggerDatasetLive(
            conllu_fpath=os.path.join(self.config.cache_dir, 'buff.tag.{}'.format(self.config.default_language)),
            wordpiece_splitter=config.wordpiece_splitter,
            config=config
        )
        test_set.numberize()

        # load weights of tokenizer into the combined model
        self.load_adapter_weights(model_name='tagger')

        # make predictions

        for batch in DataLoader(test_set, batch_size=self.config.eval_batch_size,
                                shuffle=False, collate_fn=test_set.collate_fn):
            batch_size = len(batch.word_num)

            word_reprs, cls_reprs = self.embedding_layers.get_tagger_inputs(batch)
            predictions = self.tagger[self.config.default_language].predict(batch, word_reprs, cls_reprs)
            predicted_upos = predictions[0]
            predicted_xpos = predictions[1]
            predicted_feats = predictions[2]

            predicted_upos = predicted_upos.data.cpu().numpy().tolist()
            predicted_xpos = predicted_xpos.data.cpu().numpy().tolist()
            predicted_feats = predicted_feats.data.cpu().numpy().tolist()

            # head, deprel
            predicted_dep = predictions[3]
            sentlens = [l + 1 for l in batch.word_num]
            head_seqs = [chuliu_edmonds_one_root(adj[:l, :l])[1:] for adj, l in
                         zip(predicted_dep[0], sentlens)]  # remove attachment for the root
            deprel_seqs = [
                [self.config.itos[self.config.default_language][DEPREL][predicted_dep[1][i][j + 1][h]] for j, h in
                 enumerate(hs)] for
                i, hs
                in
                enumerate(head_seqs)]

            pred_tokens = [[[str(head_seqs[i][j]), deprel_seqs[i][j]] for j in range(sentlens[i] - 1)] for i in
                           range(batch_size)]

            for bid in range(batch_size):
                for i in range(batch.word_num[bid]):
                    sentid = batch.sent_index[bid]
                    wordid = batch.word_ids[bid][i]

                    # upos
                    pred_upos_id = predicted_upos[bid][i]
                    upos_name = self.config.itos[self.config.default_language][UPOS][pred_upos_id]
                    test_set.conllu_doc[sentid][wordid][UPOS] = upos_name
                    # xpos
                    pred_xpos_id = predicted_xpos[bid][i]
                    xpos_name = self.config.itos[self.config.default_language][XPOS][pred_xpos_id]
                    test_set.conllu_doc[sentid][wordid][XPOS] = xpos_name
                    # feats
                    pred_feats_id = predicted_feats[bid][i]
                    feats_name = self.config.itos[self.config.default_language][FEATS][pred_feats_id]
                    test_set.conllu_doc[sentid][wordid][FEATS] = feats_name

                    # head
                    test_set.conllu_doc[sentid][wordid][HEAD] = pred_tokens[bid][i][0]
                    # deprel
                    test_set.conllu_doc[sentid][wordid][DEPREL] = pred_tokens[bid][i][1]
        tagged_doc = process_doc(conllu_doc=test_set.conllu_doc)
        return tagged_doc

    def lemmatize(self, tagged_doc):
        lemmatized_doc = self.lemma_model[self.config.default_language].predict(tagged_doc)
        return lemmatized_doc

    def mwt_expand(self, tokenized_doc):
        expanded_doc = self.mwt_model[self.config.default_language].predict(tokenized_doc)
        return expanded_doc

    def analyze(self, raw_text):
        tokenized_doc = self.tokenize(raw_text)
        if tbname2training_id[self.config.treebank_name] % 2 == 1:
            tokenized_doc = self.mwt_expand(tokenized_doc)
        else:
            CoNLL.dict2conll(tokenized_doc,
                             os.path.join(self.config.cache_dir, 'buff.tok.{}'.format(self.config.default_language)))
            tokenized_doc = stanzaCoNLL.conll2dict(
                os.path.join(self.config.cache_dir, 'buff.tok.{}'.format(self.config.default_language)))
        tagged_doc = self.tag(tokenized_doc)
        final_doc = self.lemmatize(tagged_doc)
        return final_doc
