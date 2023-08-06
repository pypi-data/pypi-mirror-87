#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : BertZoo.
# @File         : utils
# @Time         : 2020/11/25 3:27 下午
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
from bert4keras.snippets import sequence_padding, AutoRegressiveDecoder


def texts2vec(encoder, tokenizer, texts, batch_size=1000, maxlen=64, is_lite=1, is_gc=False):
    X = []
    S = []
    for text in texts:
        token_ids, segment_ids = tokenizer.encode(text, maxlen=maxlen)
        X.append(token_ids)
        S.append(segment_ids)

    data = [sequence_padding(X, length=maxlen), sequence_padding(S, length=maxlen)]

    if is_gc:
        del text, X, S
        gc.collect()

    vecs = encoder.predict(data, batch_size=batch_size)

    if is_lite:
        vecs = vecs[:, range(0, 768, 4)]

    return normalize(vecs)
