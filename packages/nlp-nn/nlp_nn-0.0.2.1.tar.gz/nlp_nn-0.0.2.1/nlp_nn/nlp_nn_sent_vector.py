# -*- coding: utf-8 -*-
###############################################################################
#
# Copyright (c) 2019 p-cube.cn, Inc. All Rights Reserved
#
###############################################################################
"""
文本转向量模型

Authors: fubo
Date: 2019/11/28 00:00:00
"""
from typing import List

import torch
from .base.common import DeviceSettings
from .model.sent_similarity import SentSimilarity


class SentVector(object):
    def __init__(self, model_path: str):
        self.__embedding = SentSimilarity(device_settings=DeviceSettings(gpu_idx=-1))
        if self.__embedding.load_released_model(model_path_script=model_path) is False:
            raise ValueError

    def sent2vec(self, query: str) -> torch.FloatTensor:
        """
        短文本转向量
        :param query:
        :return:
        """
        return self.__embedding.sent_encode(query=query)

    def sent_encode_batch(self, queries: List[str]) -> List[torch.FloatTensor]:
        """
        短文本转向量
        :param query:
        :return:
        """
        return self.__embedding.sent_encode_batch(queries=queries)