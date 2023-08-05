#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AppZoo.
# @File         : nh_bert
# @Time         : 2020/11/19 3:34 下午
# @Author       : yuanjie
# @Email        : yuanjie@xiaomi.com
# @Software     : PyCharm
# @Description  : tf2 bert4keras


from meutils.pipe import *

os.environ['TF_KERAS'] = '1'

from meutils.zk_utils import get_zk_config

from bert4keras.backend import keras, search_layer, K
from bert4keras.tokenizers import Tokenizer
from bert4keras.models import build_transformer_model
from bert4keras.optimizers import Adam
from bert4keras.snippets import sequence_padding, DataGenerator
from bert4keras.snippets import open
from tensorflow.keras.layers import Lambda, Dense
from tensorflow.keras.utils import to_categorical

cfg = get_zk_config('/mipush/nh_model')
vocab_url = cfg['vocab_url']
model_url = cfg['nh_content_bert_model_url']

if not Path('vocab.txt').exists():
    download(vocab_url, 'vocab.txt')
tokenizer = Tokenizer('vocab.txt', do_lower_case=True)

model_name = 'model.h5'
if not Path(model_name).exists():
    download(model_url, model_name)  #
model = keras.models.load_model(model_name, compile=False)  # todo: 3当正样本 model_loose

maxlen = 64


@lru_cache(100000)
def text2seq(text):
    token_ids, segment_ids = tokenizer.encode(text, maxlen=maxlen)
    batch_token_ids = sequence_padding([token_ids], length=maxlen)
    batch_segment_ids = sequence_padding([segment_ids], length=maxlen)
    return batch_token_ids, batch_segment_ids


def texts2seq(texts=['紫金矿业63岁董事长迎娶38岁妻子']):
    batch_token_ids, batch_segment_ids = [], []
    for text in texts:
        token_ids, segment_ids = tokenizer.encode(text, maxlen=maxlen)
        batch_token_ids.append(token_ids)
        batch_segment_ids.append(segment_ids)
    batch_token_ids = sequence_padding(batch_token_ids)
    batch_segment_ids = sequence_padding(batch_segment_ids)
    return batch_token_ids, batch_segment_ids


# Api
def predict_one(**kwargs):
    text = kwargs.get("text", "请输入一个文本")
    scores = model.predict(texts2seq(text))[:, 1].tolist()
    return list(zip([text], scores))


def predict_batch(**kwargs):
    texts = kwargs.get("texts", ["请输入一批文本"])
    scores = model.predict(texts2seq(texts))[:, 1].tolist()
    return list(zip(texts, scores))


logger.info(predict_one())

if __name__ == '__main__':
    from appzoo import App

    app = App()
    app.add_route('/nh_bert/predict_one', predict_one, method="GET")
    app.add_route('/nh_bert/predict_one', predict_one, method="POST")
    app.add_route('/nh_bert/predict_batch', predict_batch, method="POST")

    app.run(port=9966, access_log=False)


