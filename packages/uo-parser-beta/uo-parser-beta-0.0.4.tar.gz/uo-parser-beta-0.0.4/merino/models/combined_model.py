from .base_model import *
from ..utils.base_utils import *

TOK_MAP = {
    'not-eot': 0,
    'eot,not-eos': 1,
    'eot,eos': 2,
    'eot,eomwt,not-eos': 3,
    'eot,eomwt,eos': 4
}


class TaggerClassifier(nn.Module):
    def __init__(self, config, treebank_name):
        super().__init__()
        self.config = config

        self.xlmr_dim = 768
        self.upos_embedding = nn.Embedding(
            num_embeddings=len(config.vocabs[treebank_name][UPOS]),
            embedding_dim=50
        )
        # pos tagging
        self.upos_ffn = nn.Linear(self.xlmr_dim, len(config.vocabs[treebank_name][UPOS]))
        self.xpos_ffn = nn.Linear(self.xlmr_dim + 50, len(config.vocabs[treebank_name][XPOS]))
        self.feats_ffn = nn.Linear(self.xlmr_dim, len(config.vocabs[treebank_name][FEATS]))

        self.down_dim = self.xlmr_dim // 4
        self.down_project = nn.Linear(self.xlmr_dim, self.down_dim)
        # dependency parsing
        self.unlabeled = DeepBiaffineScorer(self.down_dim, self.down_dim,
                                            self.down_dim, 1, pairwise=True,
                                            dropout=0.5)
        self.deprel = DeepBiaffineScorer(self.down_dim, self.down_dim,
                                         self.down_dim, len(config.vocabs[treebank_name][DEPREL]), pairwise=True,
                                         dropout=0.5)
        # load pretrained weights
        self.initialized_weights = self.state_dict()
        language = treebank2lang[treebank_name]
        self.pretrained_tagger_weights = torch.load(os.path.join(self.config.cache_dir, language,
                                                                 '{}.tagger.mdl'.format(
                                                                     language)))['adapters']

        for name, value in self.pretrained_tagger_weights.items():
            if name in self.initialized_weights:
                self.initialized_weights[name] = value
        self.load_state_dict(self.initialized_weights)
        print('Loaded tagger for treebank {} ...'.format(treebank_name))

    def forward(self, batch):
        return None

    def predict(self, batch, word_reprs, cls_reprs):
        # upos
        upos_scores = self.upos_ffn(word_reprs)
        predicted_upos = torch.argmax(upos_scores, dim=2)
        # edits
        xpos_reprs = torch.cat(
            [word_reprs, self.upos_embedding(predicted_upos)], dim=2
        )  # [batch size, num words, xlmr dim + 50]
        # xpos
        xpos_scores = self.xpos_ffn(xpos_reprs)
        predicted_xpos = torch.argmax(xpos_scores, dim=2)
        # feats
        feats_scores = self.feats_ffn(word_reprs)
        predicted_feats = torch.argmax(feats_scores, dim=2)

        # head
        dep_reprs = torch.cat(
            [cls_reprs, word_reprs], dim=1
        )  # [batch size, 1 + max num words, xlmr dim] # cls serves as ROOT node
        dep_reprs = self.down_project(dep_reprs)
        unlabeled_scores = self.unlabeled(dep_reprs, dep_reprs).squeeze(3)

        diag = torch.eye(batch.head_idxs.size(-1) + 1, dtype=torch.bool).cuda().unsqueeze(0)
        unlabeled_scores.masked_fill_(diag, -float('inf'))

        # deprel
        deprel_scores = self.deprel(dep_reprs, dep_reprs)
        dep_preds = []
        dep_preds.append(F.log_softmax(unlabeled_scores, 2).detach().cpu().numpy())
        dep_preds.append(deprel_scores.max(3)[1].detach().cpu().numpy())
        return predicted_upos, predicted_xpos, predicted_feats, dep_preds


class TokenizerClassifier(nn.Module):
    def __init__(self, config, treebank_name):
        super().__init__()
        self.config = config
        self.xlmr_dim = 768
        self.tokenizer_ffn = nn.Linear(self.xlmr_dim, len(TOK_MAP))

        language = treebank2lang[treebank_name]
        # load pretrained weights
        self.pretrained_tokenizer_weights = torch.load(os.path.join(self.config.cache_dir, language,
                                                                    '{}.tokenizer.mdl'.format(
                                                                        language)))['adapters']
        self.initialized_weights = self.state_dict()

        for name, value in self.pretrained_tokenizer_weights.items():
            if name in self.initialized_weights:
                self.initialized_weights[name] = value

        self.load_state_dict(self.initialized_weights)
        print('Loaded tokenizer for treebank {} ...'.format(treebank_name))

    def forward(self, batch):
        return None

    def predict(self, batch, wordpiece_reprs):
        wordpiece_scores = self.tokenizer_ffn(wordpiece_reprs)
        predicted_wordpiece_labels = torch.argmax(wordpiece_scores, dim=2)  # [batch size, num wordpieces]

        return predicted_wordpiece_labels, batch.wordpiece_ends, batch.paragraph_index
