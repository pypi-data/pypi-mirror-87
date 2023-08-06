# -*- coding: utf-8 -*-
###############################################################################
#
# Copyright (c) 2019 p-cube.cn, Inc. All Rights Reserved
#
###############################################################################
"""
模型定义

Authors: fubo01
Date: 2019/11/28 00:00:00
"""

import logging
from collections import OrderedDict
import torch

from .layer import CrossLayer, LinearLayer, SelfAttentionLayer
from .layer import BertSentEncodeSelfAttentionLayer, EmbeddingLayer, BertEmbeddingLayer, BertSentEncodeTermLevelLayer
from .abstract import AbstractModel


class QueryClassifyModel(AbstractModel):

    def __init__(
            self, sent_encode_dim: int, attention_vector_size: int, class_count: int,
            dropout_prob: float, max_tokens: int = 20
    ):
        """
        :param sent_encode_dim: 句向量维度
        :param attention_vector_size: attention 向量维度
        :param class_count: 类别数量
        :param dropout_prob: dropout概率
        :param max_tokens: 最大token长度
        """
        super().__init__()
        self.max_tokens = max_tokens
        # query layer
        self.sent_encoding_layer = BertSentEncodeSelfAttentionLayer(
            sent_encode_dim=sent_encode_dim,
            attention_vector_size=attention_vector_size
        )

        # drop out layer
        self.drop_out_layer = torch.nn.Dropout(p=dropout_prob)

        # classify layer
        self.classify_layer = LinearLayer(n_input_dim=sent_encode_dim, n_output_dim=class_count, with_bias=False)

    def get_dummy_input(self):
        """
        获取dummy数据
        :return:
        """
        x = torch.LongTensor([[0] * self.max_tokens])
        return x

    def forward(self, x):
        """
        forward 计算
        :param x:
        :return:
        """
        x = self.sent_encoding_layer(x)
        x = self.drop_out_layer(x)
        x = self.classify_layer(x)
        x = torch.log_softmax(x, dim=1)
        return x


class IntentSlotModel(AbstractModel):

    def __init__(
            self, intent_class_count: int, entity_class_count: int,
            dropout_prob: float = 0.3, max_tokens: int = 20
    ):
        """
        :param sent_encode_dim: 句向量维度
        :param attention_vector_size: attention 向量维度
        :param class_count: 类别数量
        :param dropout_prob: dropout概率
        :param max_tokens: 最大token长度
        """
        super().__init__()
        self.max_tokens = max_tokens
        # bert embedding layer
        self.bert_embedding_layer = BertEmbeddingLayer()

        # drop out layer
        self.drop_out_layer = torch.nn.Dropout(p=dropout_prob)

        # intent classifier
        self.intent_layer = LinearLayer(
            n_input_dim=self.bert_embedding_layer.hidden_size,
            n_output_dim=intent_class_count
        )

        # entity classifier
        self.entity_layer = LinearLayer(
            n_input_dim=self.bert_embedding_layer.hidden_size,
            n_output_dim=entity_class_count
        )

    def get_dummy_input(self):
        """
        获取dummy数据
        :return:
        """
        x = torch.LongTensor([[0] * self.max_tokens])
        return x

    def forward(self, x):
        """
        forward 计算
        :param x:
        :return:
        """
        res = self.bert_embedding_layer(x)
        x_token, x_intent = res[0], res[1]
        x_token = self.entity_layer(self.drop_out_layer(x_token))
        x_intent = self.intent_layer(self.drop_out_layer(x_intent))
        x_token = torch.log_softmax(x_token, dim=2)
        x_intent = torch.log_softmax(x_intent, dim=1)

        return x_intent, x_token


class EntityModel(AbstractModel):

    def __init__(self, entity_class_count: int, dropout_prob: float = 0.3, max_tokens: int = 20):
        """
        :param sent_encode_dim: 句向量维度
        :param attention_vector_size: attention 向量维度
        :param class_count: 类别数量
        :param dropout_prob: dropout概率
        :param max_tokens: 最大token长度
        """
        super().__init__()
        self.max_tokens = max_tokens
        # bert embedding layer
        self.bert_embedding_layer = BertEmbeddingLayer()

        # drop out layer
        self.drop_out_layer = torch.nn.Dropout(p=dropout_prob)

        # entity classifier
        self.entity_layer = LinearLayer(
            n_input_dim=self.bert_embedding_layer.hidden_size,
            n_output_dim=entity_class_count
        )

    def get_dummy_input(self):
        """
        获取dummy数据
        :return:
        """
        x = torch.LongTensor([[0] * self.max_tokens])
        return x

    def forward(self, x):
        """
        forward 计算
        :param x:
        :return:
        """
        res = self.bert_embedding_layer(x)
        x_token, _ = res[0], res[1]
        x_token = self.entity_layer(self.drop_out_layer(x_token))
        x_token = torch.log_softmax(x_token, dim=2)
        return x_token


class TaggingModel(AbstractModel):

    def __init__(self, tags_count: int, dropout_prob: float = 0.3, max_tokens: int = 20):
        """
        :param sent_encode_dim: 句向量维度
        :param attention_vector_size: attention 向量维度
        :param class_count: 类别数量
        :param dropout_prob: dropout概率
        :param max_tokens: 最大token长度
        """
        super().__init__()
        self.max_tokens = max_tokens
        # bert embedding layer
        self.bert_embedding_layer = BertEmbeddingLayer()

        # drop out layer
        self.drop_out_layer = torch.nn.Dropout(p=dropout_prob)

        # expand tags seq layer
        self.expand_layer = LinearLayer(
            n_input_dim=self.max_tokens,
            n_output_dim=tags_count
        )

        # tags classifier
        self.entity_layer = LinearLayer(
            n_input_dim=self.bert_embedding_layer.hidden_size,
            n_output_dim=2
        )

    def get_dummy_input(self):
        """
        获取dummy数据
        :return:
        """
        x = torch.LongTensor([[0] * self.max_tokens])
        return x

    def forward(self, x):
        """
        forward 计算
        :param x:
        :return:
        """
        res = self.bert_embedding_layer(x)
        x_token, _ = res[0], res[1]
        x_token = torch.transpose(x_token, dim0=2, dim1=1)
        x_token = self.expand_layer(self.drop_out_layer(x_token))
        x_token = torch.transpose(x_token, dim0=2, dim1=1)
        x_token = self.entity_layer(self.drop_out_layer(x_token))
        x_token = torch.log_softmax(x_token, dim=2)
        return x_token


class QuerySimilarityModel(AbstractModel):

    def __init__(self, sent_encode_dim: int, attention_vector_size: int, max_tokens: int = 20):
        """
        :param sent_encode_dim: 句向量维度
        :param attention_vector_size: attention 向量维度
        :param max_tokens: 类别数量
        :param max_tokens: 最大token长度
        """
        super().__init__()
        self.max_tokens = max_tokens
        # query layer
        self.sent_encoding_layer = BertSentEncodeSelfAttentionLayer(
            sent_encode_dim=sent_encode_dim,
            attention_vector_size=attention_vector_size
        )

    def get_dummy_input(self):
        """
        获取dummy数据
        :return:
        """
        x_pivot = torch.LongTensor([[0] * self.max_tokens])
        x_positive = torch.LongTensor([[0] * self.max_tokens])
        x_negative = torch.LongTensor([[0] * self.max_tokens])
        return x_pivot, x_positive, x_negative

    def sent_encoding(self, x):
        """

        :param x:
        :return:
        """
        return self.sent_encoding_layer(x)

    def forward(self, x_pivot, x_positive, x_negative):
        """
        forward 计算
        :param x_pivot:
        :param x_positive:
        :param x_negative:
        :return:
        """
        x_pivot = self.sent_encoding(x_pivot)
        x_positive = self.sent_encoding(x_positive)
        x_negative = self.sent_encoding(x_negative)
        return x_pivot, x_positive, x_negative


class QuerySimilarityCrossModel(AbstractModel):

    def __init__(self, attention_vector_size: int, max_tokens: int = 20):
        """
        :param attention_vector_size: attention 向量维度
        :param max_tokens: 类别数量
        :param max_tokens: 最大token长度
        """
        super().__init__()
        self.max_tokens = max_tokens
        self.bert_term_layer = BertSentEncodeTermLevelLayer()
        # # query layer
        self.converge_layer = SelfAttentionLayer(
            embedding_size=self.bert_term_layer.embedding_layer.hidden_size,
            attention_vector_size=attention_vector_size
        )
        self.output_layer = LinearLayer(
            n_input_dim=self.bert_term_layer.embedding_layer.hidden_size,
            n_output_dim=2,
            with_bias=True
        )

    def get_dummy_input(self):
        """
        获取dummy数据
        :return:
        """
        x_token1 = torch.LongTensor([[0] * self.max_tokens])
        x_token2 = torch.LongTensor([[0] * self.max_tokens])
        return x_token1, x_token2

    def sent_base_encoding(self, x):
        """
        base共享部分 sent encoding
        :param x:
        :return:
        """
        return self.bert_term_layer(x)

    def converge_encoding(self, x_encoding_terms1, x_encoding_terms2):
        """
        汇聚层 两个encoding向量交互计算
        """
        converge_vec, attention = self.converge_layer(x_encoding_terms1 + x_encoding_terms2)
        converge_output = self.output_layer(converge_vec)
        return converge_output, attention

    def run_similarity_base_encoding(self, x_encoding1, x_encoding2):
        """
        base encoding计算相关性
        """
        output, _ = self.converge_encoding(x_encoding1, x_encoding2)
        return torch.log_softmax(output, dim=1)

    def forward(self, x_token1, x_token2):
        """
        forward 计算
        :param x_token1:
        :param x_token2:
        :return:
        """
        vec1 = self.sent_base_encoding(x_token1)
        vec2 = self.sent_base_encoding(x_token2)
        output, _ = self.converge_encoding(vec1, vec2)
        return torch.log_softmax(output, dim=1)


class SentDeepCrossModel(AbstractModel):
    """ 基于用户sent的DeepCross模型 """

    def __init__(
            self,
            user_max_input_tokens, user_sent_encode_dim, user_attention_vector_size,
            user_dense_feature_sizes, user_sparse_feature_sizes,
            item_max_input_tokens, item_sent_encode_dim, item_attention_vector_size,
            item_dense_feature_sizes, item_sparse_feature_sizes,
            cross_layer_num, deep_layer_sizes
    ):
        """
        :param sent_encode_dim: 句向量维度
        :param max_input_tokens: 输入token的最大长度
        :param attention_vector_size: attention layer向量维度
        :param dense_features_size:     稠密特征维度
        :param sparse_features_sizes:   稀疏特征[(特征1词典大小, 特征1向量维度), (特征2词典大小, 特征2向量维度) ... ]
        :param cross_layer_num:     Cross层
        :param deep_layer_sizes:    Deep层[第一层维度，第二层维度 ... ]
        """
        super().__init__()
        self.user_max_input_tokens = user_max_input_tokens
        self.user_dense_feature_sizes = user_dense_feature_sizes
        self.user_sparse_feature_sizes = user_sparse_feature_sizes

        self.item_max_input_tokens = item_max_input_tokens
        self.item_dense_feature_sizes = item_dense_feature_sizes
        self.item_sparse_feature_sizes = item_sparse_feature_sizes

        # user&item sent layer
        self.user_sent_encoding_layer = BertSentEncodeSelfAttentionLayer(
            sent_encode_dim=user_sent_encode_dim,
            attention_vector_size=user_attention_vector_size
        )

        self.item_sent_encoding_layer = BertSentEncodeSelfAttentionLayer(
            sent_encode_dim=item_sent_encode_dim,
            attention_vector_size=item_attention_vector_size
        )

        # user&item sparse feature layers
        self.user_sparse_feature_embeddings = torch.nn.ModuleList()
        for elem in self.user_sparse_feature_sizes:
            self.user_sparse_feature_embeddings.append(EmbeddingLayer(elem["vocab_num"], elem["dim"]))

        self.item_sparse_feature_embeddings = torch.nn.ModuleList()
        for elem in self.item_sparse_feature_sizes:
            self.item_sparse_feature_embeddings.append(EmbeddingLayer(elem["vocab_num"], elem["dim"]))

        user_input_feature_num = user_sent_encode_dim + user_dense_feature_sizes
        user_input_feature_num = user_input_feature_num + sum([elem["dim"] for elem in self.user_sparse_feature_sizes])

        item_input_feature_num = item_sent_encode_dim + item_dense_feature_sizes
        item_input_feature_num = item_input_feature_num + sum([elem["dim"] for elem in self.item_sparse_feature_sizes])

        input_feature_num = user_input_feature_num + item_input_feature_num

        # cross layer
        self.cross_layer = CrossLayer(
            input_feature_num=input_feature_num,
            cross_layer=cross_layer_num
        )

        # deep layer
        deep_layers = []
        last_layer_size = input_feature_num
        for index, layer_size in enumerate(deep_layer_sizes):
            deep_layers.append(("LinearLayer_%s" % str(index + 1), LinearLayer(last_layer_size, layer_size, True)))
            deep_layers.append(("ReLU_%s" % str(index + 1), torch.nn.ReLU()))
            deep_layers.append(("Dropout_%s" % str(index + 1), torch.nn.Dropout(0.5)))
            last_layer_size = layer_size
        self.deep_layer = torch.nn.Sequential(OrderedDict(deep_layers))

        # merge layer
        self.merge_layer = LinearLayer(
            n_input_dim=input_feature_num + deep_layer_sizes[-1],
            n_output_dim=1
        )

        # output layer
        self.sigmoid_layer = torch.nn.Sigmoid()

    def __embedding_index(self, index):
        """
        计算embedding的实际位置
        :param index:
        :return:
        """

    def get_dummy_input(self):
        """
        获取dummy数据
        :return:
        """
        user_tokens = torch.LongTensor([[0] * self.user_max_input_tokens])
        item_tokens = torch.LongTensor([[0] * self.item_max_input_tokens])
        user_dense_features = torch.FloatTensor([[0.0] * self.user_dense_feature_sizes])
        item_dense_features = torch.FloatTensor([[0.0] * self.item_dense_feature_sizes])
        user_sparse_features = torch.LongTensor([[0] * len(self.user_sparse_feature_sizes)])
        item_sparse_features = torch.LongTensor([[0] * len(self.user_sparse_feature_sizes)])
        return [
            user_tokens, user_dense_features, user_sparse_features,
            item_tokens, item_dense_features, item_sparse_features,
        ]

    def forward(
            self,
            user_tokens, user_dense_feature, user_sparse_feature,
            item_tokens, item_dense_feature, item_sparse_feature
    ):
        """
        forward计算
        :param user_tokens 用户文本数据  batch_size * max_tokens_size
        :param user_dense_feature 用户dense特征 batch_size * dense_feature_size
        :param user_sparse_feature 用户sparse特征 batch_size * sparse_feature_size
        :param item_tokens 物品文本数据 batch_size * max_tokens_size
        :param item_dense_feature 物品dense特征 batch_size * dense_feature_size
        :param item_sparse_feature 物品sparse特征 batch_size * sparse_feature_size
        """
        # 文本encoding
        # start_time = time.time()
        user_token_x = self.user_sent_encoding_layer(user_tokens)
        item_token_x = self.item_sent_encoding_layer(item_tokens)

        # dense feature
        # tokens_time = time.time()
        user_dense_features_x = user_dense_feature  # batch_size * dense_feature_size
        item_dense_features_x = item_dense_feature  # batch_size * dense_feature_size

        # sparse feature
        # dense_time = time.time()
        user_sparse_feature_x = []  # batch_size * sparse_feature_size * sparse_feature_embedding_dim
        item_sparse_feature_x = []  # batch_size * sparse_feature_size * sparse_feature_embedding_dim
        for index, layer in enumerate(self.user_sparse_feature_embeddings):
            user_sparse_feature_x.append(layer(user_sparse_feature[:, index]).squeeze(dim=1))

        for index, layer in enumerate(self.item_sparse_feature_embeddings):
            item_sparse_feature_x.append(layer(item_sparse_feature[:, index]).squeeze(dim=1))

        # merge feature vector
        # sparse_emb_time = time.time()
        user_x = torch.cat([user_token_x, user_dense_features_x] + user_sparse_feature_x, dim=1)
        item_x = torch.cat([item_token_x, item_dense_features_x] + item_sparse_feature_x, dim=1)
        x = torch.cat([user_x, item_x], dim=1)

        # deep layer
        # merge_vec_time = time.time()
        x1 = self.deep_layer(x)

        # cross layer
        # deep_layer_time = time.time()
        x2 = self.cross_layer(x)

        # merge layer
        # cross_layer_time = time.time()
        x = torch.cat((x1, x2), dim=1)
        output = self.sigmoid_layer(self.merge_layer(x))

        # merge_layer_time = time.time()

        # logging.info("tokens: %s" % str((tokens_time - start_time) * 1000))
        # logging.info("dense: %s" % str((dense_time - tokens_time) * 1000))
        # logging.info("sparse emb: %s" % str((sparse_emb_time - dense_time) * 1000))
        # logging.info("merge vector: %s" % str((merge_vec_time - sparse_emb_time) * 1000))
        # logging.info("deep layer: %s" % str((deep_layer_time - merge_vec_time) * 1000))
        # logging.info("cross layer: %s" % str((cross_layer_time - deep_layer_time) * 1000))
        # logging.info("merge layer: %s" % str((merge_layer_time - cross_layer_time) * 1000))
        return output


class UserItemSiameseModel(AbstractModel):
    """ 基于用户query的孪生回归模型 """

    def __init__(
            self, max_input_tokens, sent_encode_dim, attention_vector_size,
            user_dense_features_size, user_sparse_features_sizes,
            item_dense_features_size, item_sparse_features_sizes,
            user_deep_layer_sizes, item_deep_layer_sizes,
            user_encoding_size, item_encoding_size,
            dropout_prob=0.5
    ):
        """
        :param sent_encode_dim: 句向量维度
        :param max_input_tokens: 输入token的最大长度
        :param attention_vector_size: attention layer向量维度
        :param dense_features_size:     稠密特征维度
        :param sparse_features_sizes:   稀疏特征[(特征1词典大小, 特征1向量维度), (特征2词典大小, 特征2向量维度) ... ]
        :param cross_layer_num:     Cross层
        :param deep_layer_sizes:    Deep层[第一层维度，第二层维度 ... ]
        """
        super(UserItemSiameseModel, self).__init__()
        self.max_input_tokens = max_input_tokens
        self.user_dense_features_size = user_dense_features_size
        self.item_dense_features_size = item_dense_features_size
        self.user_sparse_features_sizes = user_sparse_features_sizes
        self.item_sparse_features_sizes = item_sparse_features_sizes
        self.user_deep_layer_sizes = user_deep_layer_sizes
        self.item_deep_layer_sizes = item_deep_layer_sizes

        # sentence encoding layer
        self.sent_encoding_layer = BertSentEncodeSelfAttentionLayer(
            sent_encode_dim=sent_encode_dim,
            attention_vector_size=attention_vector_size
        )

        # user sparse feature layers
        self.user_sparse_feature_embeddings = torch.nn.ModuleList()
        for elem in self.user_sparse_features_sizes:
            self.user_sparse_feature_embeddings.append(EmbeddingLayer(elem["vocab_num"], elem["dim"]))

        # item sparse feature layers
        self.item_sparse_feature_embeddings = torch.nn.ModuleList()
        for elem in self.item_sparse_features_sizes:
            self.item_sparse_feature_embeddings.append(EmbeddingLayer(elem["vocab_num"], elem["dim"]))

        dims = [elem["dim"] for elem in self.user_sparse_features_sizes]
        user_input_feature_num = self.user_dense_features_size + sum(dims)

        dims = [elem["dim"] for elem in self.item_sparse_features_sizes]
        item_input_feature_num = self.item_dense_features_size + sum(dims)

        # user deep layer
        user_deep_layers = []
        user_last_layer_size = user_input_feature_num + sent_encode_dim
        for index, layer_size in enumerate(self.user_deep_layer_sizes):
            user_deep_layers.append(
                ("LinearLayer_%s" % str(index + 1), LinearLayer(user_last_layer_size, layer_size, True))
            )
            user_deep_layers.append(
                ("ReLU_%s" % str(index + 1), torch.nn.ReLU())
            )
            user_deep_layers.append(
                ("Dropout_%s" % str(index + 1), torch.nn.Dropout(dropout_prob))
            )

            user_last_layer_size = layer_size
        self.user_deep_layers = torch.nn.Sequential(OrderedDict(user_deep_layers))

        # item deep layer
        item_deep_layers = []
        item_last_layer_size = item_input_feature_num + sent_encode_dim
        for index, layer_size in enumerate(self.item_deep_layer_sizes):
            item_deep_layers.append(
                ("LinearLayer_%s" % str(index + 1), LinearLayer(item_last_layer_size, layer_size, True))
            )
            item_deep_layers.append(
                ("ReLU_%s" % str(index + 1), torch.nn.ReLU())
            )
            item_deep_layers.append(
                ("Dropout_%s" % str(index + 1), torch.nn.Dropout(dropout_prob))
            )
            item_last_layer_size = layer_size
        self.item_deep_layers = torch.nn.Sequential(OrderedDict(item_deep_layers))

        # user encoding layer
        self.user_encoding_layer = LinearLayer(self.user_deep_layer_sizes[-1], user_encoding_size, with_bias=True)

        # item encoding layer
        self.item_encoding_layer = LinearLayer(self.item_deep_layer_sizes[-1], item_encoding_size, with_bias=True)

        # output layer
        self.similarity_layer = torch.nn.CosineSimilarity()

    def get_dummy_input(self):
        """
        获取dummy数据
        :return:
        """
        user_tokens = torch.LongTensor([[1] * self.max_input_tokens])

        if self.user_dense_features_size == 0:
            user_dense_feature = None
        else:
            user_dense_feature = torch.rand((1, self.user_dense_features_size))

        if len(self.user_sparse_features_sizes) == 0:
            user_sparse_features = None
        else:
            user_sparse_features = [torch.LongTensor([[0]])] * len(self.user_sparse_features_sizes)

        item_tokens = torch.LongTensor([[1] * self.max_input_tokens])

        if self.item_dense_features_size == 0:
            item_dense_feature = None
        else:
            item_dense_feature = torch.rand((1, self.item_dense_features_size))

        if len(self.item_sparse_features_sizes) == 0:
            item_sparse_features = None
        else:
            item_sparse_features = [torch.LongTensor([[0]])] * len(self.item_sparse_features_sizes)

        result = {
            "user_tokens": user_tokens,
            "user_dense_feature": user_dense_feature,
            "user_sparse_features": user_sparse_features,

            "item_tokens": item_tokens,
            "item_dense_feature": item_dense_feature,
            "item_sparse_features": item_sparse_features
        }
        return result

    def dummy_run(self):
        """
        使用dummy数据执行模型计算
        :return:
        """
        input_dict = self.get_dummy_input()
        return self.forward(
            user_tokens=input_dict["user_tokens"],
            user_dense_feature=input_dict["user_dense_feature"],
            user_sparse_features=input_dict["user_sparse_features"],
            item_tokens=input_dict["item_tokens"],
            item_dense_feature=input_dict["item_dense_feature"],
            item_sparse_features=input_dict["item_sparse_features"]
        )

    def user_encoding(self, user_tokens, user_dense_feature, user_sparse_features):
        """
        User侧进行特征抽取
        :param user_tokens:
        :param user_dense_feature:
        :param user_sparse_features:
        :return:
        """
        # start_time = time.time()

        if user_tokens is None:
            logging.error("Error user query")
            return None
        user_tokens_x = self.sent_encoding_layer(user_tokens)
        # tokens_time = time.time()

        if user_dense_feature is not None and self.user_dense_features_size != user_dense_feature.shape[1]:
            logging.error("Error user dense feature")
            return None

        user_dense_feature_x = user_dense_feature

        if user_sparse_features is None:
            user_sparse_features = []

        if len(user_sparse_features) != len(self.user_sparse_features_sizes):
            logging.error("Error user sparse size")
            return None

        user_sparse_features_x = []
        for index, layer in enumerate(self.user_sparse_feature_embeddings):
            user_sparse_features_x.append(layer(user_sparse_features[index]).squeeze(dim=1))

        if user_dense_feature_x is None:
            x = torch.cat([user_tokens_x] + user_sparse_features_x, dim=1)
        else:
            x = torch.cat([user_tokens_x, user_dense_feature_x] + user_sparse_features_x, dim=1)

        # embedding_time = time.time()

        x = self.user_deep_layers(x)
        # deep_layer_time = time.time()

        vec = self.user_encoding_layer(x)
        # encoding_time = time.time()

        # logging.info("User Tokens EMB time: %s" % str((tokens_time - start_time) * 1000))
        # logging.info("User Spar EMB time: %s" % str((embedding_time - tokens_time) * 1000))
        # logging.info("User Deep time: %s" % str((deep_layer_time - embedding_time) * 1000))
        # logging.info("User Encoding time: %s" % str((encoding_time - deep_layer_time) * 1000))
        return vec

    def item_encoding(self, item_tokens, item_dense_feature, item_sparse_features):
        """
        Item侧进行特征抽取
        :param item_tokens:
        :param item_dense_feature:
        :param item_sparse_features:
        :return:
        """
        # start_time = time.time()

        if item_tokens is None:
            logging.error("Error item query")
            return None
        item_tokens_x = self.sent_encoding_layer(item_tokens)
        # tokens_time = time.time()

        if item_dense_feature is not None and self.item_dense_features_size != item_dense_feature.shape[1]:
            logging.error("Error item dense feature")
            return None

        item_dense_feature_x = item_dense_feature

        if item_sparse_features is None:
            item_sparse_features = []

        if len(item_sparse_features) != len(self.item_sparse_features_sizes):
            logging.error("Error item sparse size")
            return None

        item_sparse_features_x = []
        for index, layer in enumerate(self.item_sparse_feature_embeddings):
            item_sparse_features_x.append(layer(item_sparse_features[index]).squeeze(dim=1))

        if item_dense_feature_x is None:
            x = torch.cat([item_tokens_x] + item_sparse_features_x, dim=1)
        else:
            x = torch.cat([item_tokens_x, item_dense_feature_x] + item_sparse_features_x, dim=1)

        # embedding_time = time.time()

        x = self.item_deep_layers(x)
        # deep_layer_time = time.time()

        vec = self.item_encoding_layer(x)
        # encoding_time = time.time()

        # logging.info("Item Tokens EMB time: %s" % str((tokens_time - start_time) * 1000))
        # logging.info("Item Spar EMB time: %s" % str((embedding_time - tokens_time) * 1000))
        # logging.info("Item Deep time: %s" % str((deep_layer_time - embedding_time) * 1000))
        # logging.info("Item Encoding time: %s" % str((encoding_time - deep_layer_time) * 1000))
        return vec

    def forward(
            self, user_tokens, user_dense_feature, user_sparse_features,
            item_tokens, item_dense_feature, item_sparse_features
    ):
        """ forward计算 """
        user_vector = self.user_encoding(
            user_tokens=user_tokens,
            user_dense_feature=user_dense_feature,
            user_sparse_features=user_sparse_features
        )

        item_vector = self.item_encoding(
            item_tokens=item_tokens,
            item_dense_feature=item_dense_feature,
            item_sparse_features=item_sparse_features
        )
        if user_vector is None:
            return None, None, None

        if item_vector is None:
            return user_vector, None, None

        similarity = self.similarity_layer(user_vector, item_vector)
        return user_vector, item_vector, similarity
