#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AppZoo.
# @File         : lite_app
# @Time         : 2020/12/3 2:21 下午
# @Author       : yuanjie
# @Email        : yuanjie@xiaomi.com
# @Software     : PyCharm
# @Description  : 方便联调起的空服务

from meutils.pipe import *
from meutils.datamodels.ArticleInfo import ArticleInfo


def get_feats(ac):
    logger.info(ac)

    _ = ac.pop('category')
    articleInfo = ArticleInfo(**ac)
    d = articleInfo.dict()
    del d['id'], d['title'], d['nCategory1'], d['nSubCategory1']

    dt_feat = d.pop('createTime') + d.pop('publishTime')
    r = list(d.values()) + dt_feat
    return [r]


def predict_strict(**ac):
    X = get_feats(ac)
    text = ac.get("title", "请输入一个文本")

    pred = 1
    _ = {'prob': [1, 1], 'checkSuggestion': 'PASS' if pred > 0.8 else 'REVIEW'}

    return _


def predict_nostrict(**ac):
    X = get_feats(ac)
    text = ac.get("title", "请输入一个文本")

    pred = 1
    _ = {'prob': [1, 1], 'checkSuggestion': 'PASS' if pred > 0.8 else 'REVIEW'}

    return _


if __name__ == '__main__':
    from appzoo import App

    app = App()
    app.add_route('/nh_bert/strict', predict_strict, method="POST")
    app.add_route('/nh_bert/nostrict', predict_nostrict, method="POST")

    app.run(port=8000, access_log=False)
