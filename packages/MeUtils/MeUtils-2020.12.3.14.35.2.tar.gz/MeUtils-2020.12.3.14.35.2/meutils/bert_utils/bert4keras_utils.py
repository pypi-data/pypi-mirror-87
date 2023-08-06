#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : MeUtils.
# @File         : bert4keras_utils
# @Time         : 2020/11/23 3:45 下午
# @Author       : yuanjie
# @Email        : yuanjie@xiaomi.com
# @Software     : PyCharm
# @Description  : 


from meutils.pipe import *

os.environ['TF_KERAS'] = '1'
from bert4keras.backend import keras
from bert4keras.models import build_transformer_model

from bert4keras.tokenizers import Tokenizer
from bert4keras.snippets import sequence_padding, DataGenerator

maxlen = 64


def load_model(filepath='nh_bert_v1.h5'):
    model = keras.models.load_model(filepath, compile=False)
    return model


@lru_cache(100000)
def text2seq(text, tokenizer=None):
    token_ids, segment_ids = tokenizer.encode(text, maxlen=maxlen)
    batch_token_ids = sequence_padding([token_ids], length=maxlen)
    batch_segment_ids = sequence_padding([segment_ids], length=maxlen)
    return batch_token_ids, batch_segment_ids


def texts2seq(texts=['紫金矿业63岁董事长迎娶38岁妻子'], tokenizer=None):
    batch_token_ids, batch_segment_ids = [], []
    for text in texts:
        token_ids, segment_ids = tokenizer.encode(text, maxlen=maxlen)
        batch_token_ids.append(token_ids)
        batch_segment_ids.append(segment_ids)
    batch_token_ids = sequence_padding(batch_token_ids)
    batch_segment_ids = sequence_padding(batch_segment_ids)
    return batch_token_ids, batch_segment_ids
