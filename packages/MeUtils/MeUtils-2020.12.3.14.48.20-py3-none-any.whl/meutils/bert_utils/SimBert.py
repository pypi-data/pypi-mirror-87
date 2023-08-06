#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : MeUtils.
# @File         : Bert
# @Time         : 2020/11/20 2:59 下午
# @Author       : yuanjie
# @Email        : yuanjie@xiaomi.com
# @Software     : PyCharm
# @Description  : 


from meutils.pipe import *
from meutils.np_utils import normalize

os.environ['TF_KERAS'] = '1'

from bert4keras.backend import keras
from bert4keras.models import build_transformer_model
from bert4keras.tokenizers import Tokenizer

from bert4keras.snippets import sequence_padding


# todo: 增加推理
class SimBert(object):

    def __init__(self, bert_top_dir='/fds/data/bert/chinese_simbert_L-12_H-768_A-12'):
        self.bert_top_dir = Path(bert_top_dir)
        self.config_path = self.bert_top_dir / 'bert_config.json'
        self.checkpoint_path = self.bert_top_dir / 'bert_model.ckpt'
        dict_path = self.bert_top_dir / 'vocab.txt'
        self.tokenizer = Tokenizer(str(dict_path), do_lower_case=True)

        self.simbert_encoder = self.get_model()

    def get_model(self):
        # 建立加载模型
        bert = build_transformer_model(
            str(self.config_path),
            str(self.checkpoint_path),
            with_pool='linear',
            application='unilm',
            return_keras_model=False  # True: bert.predict([np.array([token_ids]), np.array([segment_ids])])
        )
        encoder = keras.models.Model(bert.model.inputs, bert.model.outputs[0])
        return encoder

    def texts2vec(self, texts, batch_size=1000, maxlen=64, is_lite=1, is_gc=False):

        X = []
        S = []
        for text in texts:
            token_ids, segment_ids = self.tokenizer.encode(text, maxlen=maxlen)
            X.append(token_ids)
            S.append(segment_ids)

        data = [sequence_padding(X, length=maxlen), sequence_padding(S, length=maxlen)]

        if is_gc:
            del text, X, S
            gc.collect()

        vecs = self.simbert_encoder.predict(data, batch_size=batch_size)

        if is_lite:
            vecs = vecs[:, range(0, 768, 4)]

        return normalize(vecs)


if __name__ == '__main__':
    bert = SimBert()
    bert.texts2vec(['第一条文本', '第二条文本'])
