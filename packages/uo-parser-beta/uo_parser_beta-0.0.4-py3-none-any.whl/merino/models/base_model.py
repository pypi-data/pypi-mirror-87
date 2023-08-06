import torch.nn as nn
import torch
from transformers import AdapterType, XLMRobertaModel
from transformers import AdapterConfig
from ..utils.base_utils import *
import torch.nn.functional as F

LANG_2_ADAPTER_NAME = {
    'arabic': 'ar/wiki@ukp',
    'chinese': 'zh/wiki@ukp',
    'classical_chinese': 'zh/wiki@ukp',
    'simplified_chinese': 'zh/wiki@ukp',
    'english': 'en/wiki@ukp',
    'spanish': 'es/wiki@ukp',
    'vietnamese': 'vi/wiki@ukp',
    'estonian': 'et/wiki@ukp',
    'greek': "el/wiki@ukp",
    'ancient_greek': "el/wiki@ukp",
    'german': "de/wiki@ukp",
    'hindi': "hi/wiki@ukp",
    'Indonesian': "id/wiki@ukp",
    'irish': "it/wiki@ukp",
    'italian': "it/wiki@ukp",
    'japanese': "ja/wiki@ukp",
    'russian': "ru/wiki@ukp",
    'old_russian': "ru/wiki@ukp",
    'tamil': "ta/wiki@ukp",
    'turkish': "tr/wiki@ukp"
}


def convert_to_charlevel(predicted_mwt_types, mwt_span_idxs, mwt_nums, predicted_wordpiece_labels):
    predicted_mwt_labels = torch.zeros_like(predicted_wordpiece_labels)
    batch_size = predicted_wordpiece_labels.shape[0]
    for bid in range(batch_size):
        for span_id, span in enumerate(mwt_span_idxs[bid][: mwt_nums[bid]]):
            start, end = span
            predicted_mwt_labels[bid][end - 1] = predicted_mwt_types[bid][span_id]
    return predicted_mwt_labels


def compute_span_reprs(wordpiece_reprs, span_idxs):
    '''
    word_reprs.shape: [batch size, num wordpieces, rep dim]
    span_idxs.shape: [batch size, num spans, 2]
    '''
    batch_span_reprs = []
    batch_size, _, _ = wordpiece_reprs.shape
    _, num_spans, _ = span_idxs.shape
    for bid in range(batch_size):
        span_reprs = []
        for sid in range(num_spans):
            start, end = span_idxs[bid][sid]
            words = wordpiece_reprs[bid][start: end]  # [span size, rep dim]
            span_reprs.append(torch.mean(words, dim=0))
        span_reprs = torch.stack(span_reprs, dim=0)  # [num spans, rep dim]
        batch_span_reprs.append(span_reprs)
    batch_span_reprs = torch.stack(batch_span_reprs, dim=0)  # [batch size, num spans, rep dim]

    return batch_span_reprs


def get_span_idxs(wordpiece_pred_labels):
    # wordpiece_pred_labels.shape = [batch size, num wordpieces]
    batch_tmp = []
    batch_size = wordpiece_pred_labels.shape[0]
    max_mwt_num = -1
    for bid in range(batch_size):
        wp_labels = wordpiece_pred_labels[bid].data.cpu().numpy().tolist()

        mwt_span_idxs = []
        start_token = -1
        for wp_id, wp_label in enumerate(wp_labels):
            if start_token == -1:
                start_token = wp_id

            if wp_label > 0:
                if wp_label == 3 or wp_label == 4:
                    mwt_span_idxs.append([start_token, wp_id + 1])

                start_token = -1
        batch_tmp.append(mwt_span_idxs)
        max_mwt_num = max(max_mwt_num, len(mwt_span_idxs))

    batch_mwt_nums = [len(x) for x in batch_tmp]
    batch_mwt_span_idxs = []
    for bid in range(batch_size):
        batch_mwt_span_idxs.append(batch_tmp[bid] + [[0, 1]] * (max_mwt_num - len(batch_tmp[bid])))

    batch_mwt_span_idxs = torch.cuda.LongTensor(batch_mwt_span_idxs)
    return batch_mwt_span_idxs, batch_mwt_nums, max_mwt_num


class PairwiseBilinear(nn.Module):
    ''' A bilinear module that deals with broadcasting for efficient memory usage.
    Input: tensors of sizes (N x L1 x D1) and (N x L2 x D2)
    Output: tensor of size (N x L1 x L2 x O)'''

    def __init__(self, input1_size, input2_size, output_size, bias=True):
        super().__init__()

        self.input1_size = input1_size
        self.input2_size = input2_size
        self.output_size = output_size

        self.weight = nn.Parameter(torch.Tensor(input1_size, input2_size, output_size))
        self.bias = nn.Parameter(torch.Tensor(output_size)) if bias else 0

    def forward(self, input1, input2):
        input1_size = list(input1.size())
        input2_size = list(input2.size())
        output_size = [input1_size[0], input1_size[1], input2_size[1], self.output_size]

        # ((N x L1) x D1) * (D1 x (D2 x O)) -> (N x L1) x (D2 x O)
        intermediate = torch.mm(input1.view(-1, input1_size[-1]),
                                self.weight.view(-1, self.input2_size * self.output_size))
        # (N x L2 x D2) -> (N x D2 x L2)
        input2 = input2.transpose(1, 2)
        # (N x (L1 x O) x D2) * (N x D2 x L2) -> (N x (L1 x O) x L2)
        output = intermediate.view(input1_size[0], input1_size[1] * self.output_size, input2_size[2]).bmm(input2)
        # (N x (L1 x O) x L2) -> (N x L1 x L2 x O)
        output = output.view(input1_size[0], input1_size[1], self.output_size, input2_size[1]).transpose(2, 3)

        return output


class BiaffineScorer(nn.Module):
    def __init__(self, input1_size, input2_size, output_size):
        super().__init__()
        self.W_bilin = nn.Bilinear(input1_size + 1, input2_size + 1, output_size)

        self.W_bilin.weight.data.zero_()
        self.W_bilin.bias.data.zero_()

    def forward(self, input1, input2):
        input1 = torch.cat([input1, input1.new_ones(*input1.size()[:-1], 1)], len(input1.size()) - 1)
        input2 = torch.cat([input2, input2.new_ones(*input2.size()[:-1], 1)], len(input2.size()) - 1)
        return self.W_bilin(input1, input2)


class PairwiseBiaffineScorer(nn.Module):
    def __init__(self, input1_size, input2_size, output_size):
        super().__init__()
        self.W_bilin = PairwiseBilinear(input1_size + 1, input2_size + 1, output_size)

        self.W_bilin.weight.data.zero_()
        self.W_bilin.bias.data.zero_()

    def forward(self, input1, input2):
        input1 = torch.cat([input1, input1.new_ones(*input1.size()[:-1], 1)], len(input1.size()) - 1)
        input2 = torch.cat([input2, input2.new_ones(*input2.size()[:-1], 1)], len(input2.size()) - 1)
        return self.W_bilin(input1, input2)


class DeepBiaffineScorer(nn.Module):
    def __init__(self, input1_size, input2_size, hidden_size, output_size, hidden_func=F.relu, dropout=0,
                 pairwise=True):
        super().__init__()
        self.W1 = nn.Linear(input1_size, hidden_size)
        self.W2 = nn.Linear(input2_size, hidden_size)
        self.hidden_func = hidden_func
        if pairwise:
            self.scorer = PairwiseBiaffineScorer(hidden_size, hidden_size, output_size)
        else:
            self.scorer = BiaffineScorer(hidden_size, hidden_size, output_size)
        self.dropout = nn.Dropout(dropout)

    def forward(self, input1, input2):
        return self.scorer(self.dropout(self.hidden_func(self.W1(input1))),
                           self.dropout(self.hidden_func(self.W2(input2))))


class BaseModel(nn.Module):
    def __init__(self, config, task_name):
        super().__init__()
        self.config = config
        self.task_name = task_name
        # xlmr encoder
        self.xlmr = XLMRobertaModel.from_pretrained(config.xlmr_model_name,
                                                    cache_dir=os.path.join(config.cache_dir, 'xlmr'),
                                                    output_hidden_states=True)
        self.xlmr_dropout = nn.Dropout(p=config.xlmr_dropout)
        # add and load pretrained language and invertible adapters to xlmr encoder
        lang_config = AdapterConfig.load("pfeiffer", non_linearity="relu", reduction_factor=2)
        self.xlmr.load_adapter(LANG_2_ADAPTER_NAME.get(self.config.lang, 'en/wiki@ukp'), "text_lang",
                               config=lang_config)
        # add a new task adapter
        task_config = AdapterConfig.load("pfeiffer", reduction_factor=6)
        self.xlmr.add_adapter(task_name, AdapterType.text_task, config=task_config)
        # specify which adapters will be updated, in this case, only the task adapter will be updated
        self.xlmr.train_adapter([task_name])
        # specify which adapters are used in forward pass, here, we want to use both language adapters (associated with invertible adapters) and the will-be-updated task adapteres
        self.xlmr.set_active_adapters([LANG_2_ADAPTER_NAME.get(self.config.lang, 'en/wiki@ukp'), task_name])
        # after this, all xlmr encoder's paramters are fixed during training except task adapter parameters
        # + the classifier's parameters (defined in children classes of this BaseModel)
        # loss functions
        self.criteria = torch.nn.CrossEntropyLoss()

    def encode(self, piece_idxs, attention_masks):
        batch_size, _ = piece_idxs.size()
        all_xlmr_outputs = self.xlmr(piece_idxs, attention_mask=attention_masks)
        xlmr_outputs = all_xlmr_outputs[0]

        # take all wordpieces except the first (i.e., <s>) and the last (i.e., </s>) wordpiece
        wordpiece_reprs = xlmr_outputs[:, 1:-1, :]  # [batch size, 254, xlmr dim]
        wordpiece_reprs = self.xlmr_dropout(wordpiece_reprs)
        return wordpiece_reprs

    def encode_words(self, piece_idxs, attention_masks, word_lens):
        batch_size, _ = piece_idxs.size()
        all_xlmr_outputs = self.xlmr(piece_idxs, attention_mask=attention_masks)
        xlmr_outputs = all_xlmr_outputs[0]
        cls_reprs = xlmr_outputs[:, 0, :].unsqueeze(1)  # [batch size, 1, xlmr dim]

        # average all pieces for multi-piece words
        idxs, token_num, token_len = word_lens_to_idxs(word_lens)
        idxs = piece_idxs.new(idxs) + 1
        xlmr_outputs = compute_word_reps_avg(xlmr_outputs, idxs)
        xlmr_outputs = self.xlmr_dropout(xlmr_outputs)
        return xlmr_outputs, cls_reprs

    def forward(self, batch):
        raise NotImplementedError


class EmbeddingModel(BaseModel):
    def __init__(self, config):
        super(EmbeddingModel, self).__init__(config, task_name='embedding')
        print('Loaded multilingual embedding layers ...')

    def get_tokenizer_inputs(self, batch):
        wordpiece_reprs = self.encode(
            piece_idxs=batch.piece_idxs,
            attention_masks=batch.attention_masks
        )
        return wordpiece_reprs

    def get_tagger_inputs(self, batch):
        # encoding
        word_reprs, cls_reprs = self.encode_words(
            piece_idxs=batch.piece_idxs,
            attention_masks=batch.attention_masks,
            word_lens=batch.word_lens
        )
        return word_reprs, cls_reprs
