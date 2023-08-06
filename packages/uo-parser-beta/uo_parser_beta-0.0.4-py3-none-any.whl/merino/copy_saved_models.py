import os, sys

no_train_treebanks = ['UD_Estonian-EWT', 'UD_Galician-TreeGal',
                      'UD_Kazakh-KTB', 'UD_Kurmanji-MG',
                      'UD_Slovenian-SST',
                      'UD_Latin-Perseus']
os.system('mkdir -p resources/merino')
trained_treebanks = os.listdir('../../ud-training/datasets/tagger/')
from resources.tbinfo import tbname2shorthand, tbname2training_id, treebank2lang

for tbname in trained_treebanks:
    tbname = tbname.rstrip('2')

    language = treebank2lang[tbname]
    os.system('mkdir -p resources/merino/{}'.format(language))

    if tbname not in no_train_treebanks:

        os.system(
            'cp -a ../../ud-training/datasets/tokenize/{}/{}.best-tokenizer.mdl resources/merino/{}/{}.tokenizer.mdl'.format(
                tbname,
                tbname,
                language, language))
        os.system(
            'cp -a ../../ud-training/datasets/tagger/{}/train.vocabs.json resources/merino/{}/{}.vocabs.json'.format(
                tbname,
                language, language))
        os.system(
            'cp -a ../../ud-training/datasets/tagger/{}/{}.best-tagger.mdl resources/merino/{}/{}.tagger.mdl'.format(
                tbname,
                tbname,
                language, language))
        if tbname2training_id[tbname] % 2 == 1:
            os.system(
                'cp -a ../../ud-training/stanza_src/saved_models/mwt/{}_mwt_expander.pt resources/merino/{}/{}_mwt_expander.pt'.format(
                    tbname2shorthand[tbname], language, language
                ))
        os.system(
            'cp -a ../../ud-training/stanza_src/saved_models/lemma/{}_lemmatizer.pt resources/merino/{}/{}_lemmatizer.pt'.format(
                tbname2shorthand[tbname], language, language
            )
        )
    else:
        os.system(
            'cp -a ../../ud-training/datasets/tokenize/{}2/{}2.best-tokenizer.mdl resources/merino/{}/{}.best-tokenizer.mdl'.format(
                tbname,
                tbname,
                language, language))
        os.system(
            'cp -a ../../ud-training/datasets/tagger/{}2/train.vocabs.json resources/merino/{}/{}.vocabs.json'.format(
                tbname,
                language, language))
        os.system(
            'cp -a ../../ud-training/datasets/tagger/{}2/{}2.best-tagger.mdl resources/merino/{}/{}.tagger.mdl'.format(
                tbname, tbname,
                language, language))
        if tbname2training_id[tbname] % 2 == 1:
            os.system(
                'cp -a ../../ud-training/stanza_src/saved_models/mwt/{}2_mwt_expander.pt resources/merino/{}/{}_mwt_expander.pt'.format(
                    tbname2shorthand[tbname], language, language
                ))
        os.system(
            'cp -a ../../ud-training/stanza_src/saved_models/lemma/{}2_lemmatizer.pt resources/merino/{}/{}_lemmatizer.pt'.format(
                tbname2shorthand[tbname], language, language
            )
        )
