#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AppZoo.
# @File         : l
# @Time         : 2020/12/3 12:51 下午
# @Author       : yuanjie
# @Email        : yuanjie@xiaomi.com
# @Software     : PyCharm
# @Description  : 

from lightgbm import LGBMClassifier
import joblib
import os
os.system('wget http://cnbj1.fds.api.xiaomi.com/browser-algo-nanjing/deploy_model/nh_strict_lgb_v1.pkl')
print(joblib.load('nh_strict_lgb_v1.pkl'))


print(joblib.__version__)