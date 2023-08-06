# -*- coding: utf-8 -*-
###############################################################################
#
# Copyright (c) 2020 p-cube.cn, Inc. All Rights Reserved
#
###############################################################################
"""
deep cross recommender

Authors: fubo01
Date: 2020/03/11 00:00:00
"""

import json
import os
import copy
import logging

from typing import List, Dict

import torch
import torch.jit
from torch.utils.data import Dataset, DataLoader

from ..base.abstract import AbstractDataSet, AbstractModelApp
from ..base.common import ModelDataType, BerType, ModelState, Const
from ..base.common import CoachSettings, ModelSettings, DeviceSettings, ExportModelSettings
from ..base.model import SentDeepCrossModel
from ..base.model_data import SparseFeatureTag, RecommenderSample
from ..base.model_dict import TagsDict, AbstractTagger
from ..base.tokenizer import BertTokenizer, AbstractTokenizer


class SentDeepCrossRankingModelSettings(ModelSettings):
    """ 模型配置 """
    # user最大token长度
    user_max_input_tokens: int = 0
    user_sent_encode_dim: int = 0
    user_attention_vector_size: int = 0

    user_dense_feature_sizes: int = 0
    user_sparse_feature_sizes: List[SparseFeatureTag] = []

    item_max_input_tokens: int = 0
    item_sent_encode_dim: int = 0
    item_attention_vector_size: int = 0

    item_dense_feature_sizes: int = 0
    item_sparse_feature_sizes: List[SparseFeatureTag] = []

    cross_layer_num: int = 0
    deep_layer_sizes: List[int] = []


class SentDeepCrossRankingCoachSettings(CoachSettings):
    """ 训练参数配置 """
    pass


class SentDeepCrossRankingExportedModelSettings(ExportModelSettings):
    """ Query相似模型导出模型配置 """

    # 最大tokens长度 user
    user_max_input_tokens: int = 0
    # 最大tokens长度 item
    item_max_input_tokens: int = 0

    # dense特征长度 user
    user_dense_feature_dim: int = 0
    # dense特征长度 item
    item_dense_feature_dim: int = 0

    # sparse特征映射文件 user
    user_sparse_feature_file: List[str] = []

    # sparse特征映射文件 user
    item_sparse_feature_file: List[str] = []


class SentDeepCrossRankingDataSet(AbstractDataSet):
    """
    推荐模型数据集管理
    {
        "score": 1.0
        "user_text": "XXX",
        "user_dense": [0.1, 0.2,...],
        "user_sparse": ["U_A", "U_B", ...],
        "item_text": "XXX",
        "item_dense": [0.1, 0.2,...],
        "item_sparse": ["I_A", "I_B", ...],
    }
    """
    def __init__(
            self,
            user_tokenizer: AbstractTokenizer, item_tokenizer: AbstractTokenizer,
            user_taggers: List[AbstractTagger], item_taggers: List[AbstractTagger]
    ):
        super().__init__()
        self.__user_tokenizer = user_tokenizer
        self.__item_tokenizer = item_tokenizer
        self.__user_taggers = user_taggers
        self.__item_taggers = item_taggers

    def parse_sample(self, line: str) -> Dict:
        """
        解析样本数据
        :param line:
        :return:
        """
        try:
            sample = RecommenderSample.parse_raw(line)
        except Exception as exp:
            logging.warning("Error line %s %s" % (line.strip("\r\n"), exp))
            return {}

        if len(sample.user_sparse) != len(self.__user_taggers):
            logging.warning("Error user sparse count")
            return {}

        if len(sample.item_sparse) != len(self.__item_taggers):
            logging.warning("Error item sparse count")
            return {}

        user_tokens = self.__user_tokenizer.tokenize(sample.user_text)
        item_tokens = self.__item_tokenizer.tokenize(sample.item_text)
        user_dense_feature = sample.user_dense
        item_dense_feature = sample.user_dense
        user_sparse_feature = [self.__user_taggers[index].tag2id(tag) for index, tag in enumerate(sample.user_sparse)]
        item_sparse_feature = [self.__item_taggers[index].tag2id(tag) for index, tag in enumerate(sample.item_sparse)]
        output = {
            "score": sample.score,
            "user_tokens": copy.deepcopy(user_tokens.padding_tokens),
            "item_tokens": copy.deepcopy(item_tokens.padding_tokens),
            "user_dense": copy.deepcopy(user_dense_feature),
            "item_dense": copy.deepcopy(item_dense_feature),
            "user_sparse": copy.deepcopy(user_sparse_feature),
            "item_sparse": copy.deepcopy(item_sparse_feature)
        }
        return output

    def __getitem__(self, index):
        return self.data[index]["score"], \
               self.data[index]["user_tokens"], \
               self.data[index]["user_dense"], \
               self.data[index]["user_sparse"],\
               self.data[index]["item_tokens"], \
               self.data[index]["item_dense"], \
               self.data[index]["item_sparse"]

    def __len__(self):
        return len(self.data)

    @staticmethod
    def collate_fn(batch):
        """
        数据封装
        :param batch: 数据batch
        :return:
        """
        score, user_tokens, user_dense, user_sparse, item_tokens, item_dense, item_sparse = zip(*batch)
        score = torch.FloatTensor([score])
        return torch.transpose(score, dim0=1, dim1=0), \
               torch.LongTensor(user_tokens), \
               torch.FloatTensor(user_dense), \
               torch.LongTensor(user_sparse), \
               torch.LongTensor(item_tokens), \
               torch.FloatTensor(item_dense), \
               torch.LongTensor(item_sparse)


class SentDeepCrossRanking(AbstractModelApp):
    """ 基于sent的DCN 排序 """

    def __init__(
            self, device_settings: DeviceSettings,
            coach_settings: SentDeepCrossRankingCoachSettings = SentDeepCrossRankingCoachSettings(),
            model_settings: SentDeepCrossRankingModelSettings = SentDeepCrossRankingModelSettings(),
            export_settings: SentDeepCrossRankingExportedModelSettings = SentDeepCrossRankingExportedModelSettings()
    ):
        super().__init__(device_settings, coach_settings, model_settings, export_settings)
        self.device_settings = device_settings
        self.model_settings = model_settings
        self.coach_settings = coach_settings
        self.export_settings = export_settings
        self.user_tokenizer = AbstractTokenizer()
        self.item_tokenizer = AbstractTokenizer()
        self.user_sparse_taggers = [
            TagsDict(tags_file=elem.tag_file) for elem in model_settings.user_sparse_feature_sizes
        ]
        self.item_sparse_taggers = [
            TagsDict(tags_file=elem.tag_file) for elem in model_settings.item_sparse_feature_sizes
        ]

    def load_third_dict(self) -> bool:
        # 加载分词
        self.user_tokenizer = BertTokenizer(
            max_sent_len=self.model_settings.user_max_input_tokens,
            bert_type=BerType.LITE_BERT
        )
        self.item_tokenizer = BertTokenizer(
            max_sent_len=self.model_settings.item_max_input_tokens,
            bert_type=BerType.LITE_BERT
        )
        return True

    def define_data_pipe(self) -> Dataset:
        """ 创建数据集计算pipe """
        return SentDeepCrossRankingDataSet(
            user_tokenizer=self.user_tokenizer,
            item_tokenizer=self.item_tokenizer,
            user_taggers=self.user_sparse_taggers,
            item_taggers=self.item_sparse_taggers
        )

    def define_model(self) -> bool:
        """
        定义模型
        :return: bool
        """

        user_sparse_feature_sizes = []
        for index, elem in enumerate(self.model_settings.user_sparse_feature_sizes):
            user_sparse_feature_sizes.append(
                {"vocab_num": self.user_sparse_taggers[index].get_size(), "dim": elem.dim}
            )

        item_sparse_feature_sizes = []
        for index, elem in enumerate(self.model_settings.item_sparse_feature_sizes):
            item_sparse_feature_sizes.append(
                {"vocab_num": self.item_sparse_taggers[index].get_size(), "dim": elem.dim}
            )

        self.model = SentDeepCrossModel(
            user_max_input_tokens=self.model_settings.user_max_input_tokens,
            user_sent_encode_dim=self.model_settings.user_sent_encode_dim,
            user_attention_vector_size=self.model_settings.user_attention_vector_size,
            user_dense_feature_sizes=self.model_settings.user_dense_feature_sizes,
            user_sparse_feature_sizes=user_sparse_feature_sizes,
            item_max_input_tokens=self.model_settings.item_max_input_tokens,
            item_sent_encode_dim=self.model_settings.item_sent_encode_dim,
            item_attention_vector_size=self.model_settings.item_attention_vector_size,
            item_dense_feature_sizes=self.model_settings.item_dense_feature_sizes,
            item_sparse_feature_sizes=item_sparse_feature_sizes,
            cross_layer_num=self.model_settings.cross_layer_num,
            deep_layer_sizes=self.model_settings.deep_layer_sizes
        )
        return True

    def load_model_ckpt(self, model_path_ckpt) -> bool:
        """
        加载ckpt模型
        :param model_path_ckpt:
        :return:
        """
        # 模型配置文件
        config_file = model_path_ckpt + "/" + self.coach_settings.model_conf_file
        with open(config_file, "r") as fp:
            config_data = json.load(fp)
        self.coach_settings = SentDeepCrossRankingCoachSettings.parse_obj(config_data["coach_settings"])
        self.model_settings = SentDeepCrossRankingModelSettings.parse_obj(config_data["model_settings"])

        # 加载模型文件
        model_file = model_path_ckpt + "/" + self.coach_settings.model_file
        if self.define_model() is False:
            logging.error("Failed to define sent_similarity_model")
            return False
        try:
            self.model.load_state_dict(torch.load(model_file, map_location=torch.device("cpu")))
        except Exception as exp:
            logging.error("load sent_similarity_model params failed %s" % exp)
            return False

        return True

    def create_loss_optimizer(self) -> bool:
        """
        创建loss function和optimizer
        :return: bool
        """
        self.loss_func = torch.nn.MSELoss()
        self.optimizer = torch.optim.Adam(
            self.get_model_params(),
            lr=self.coach_settings.lr,
            weight_decay=self.coach_settings.lr_weight_decay
        )
        return True

    def stop_criteria(self) -> (bool, int):
        """
        停止训练条件，如果不重载，则默认训练最长次数
        :return: bool, int
        """
        return False, -1

    def show_network_tf(self) -> bool:
        """
        在tensor board上画出network
        不实现函数则不画出网络图
        :return: bool
        """
        self.set_model_state(ModelState.INFERENCE)
        x = self.model.get_dummy_input()
        user_tokens = x[0].cuda() if self.use_cuda else x[0]
        user_dense_feature = x[1].cuda() if self.use_cuda else x[1]
        user_sparse_feature = x[2].cuda() if self.use_cuda else x[2]
        item_tokens = x[3].cuda() if self.use_cuda else x[3]
        item_dense_feature = x[4].cuda() if self.use_cuda else x[4]
        item_sparse_feature = x[5].cuda() if self.use_cuda else x[5]
        self.tb_logger.add_graph(
            self.model,
            (user_tokens, user_dense_feature, user_sparse_feature, item_tokens, item_dense_feature, item_sparse_feature)
        )
        self.set_model_state(ModelState.TRAIN)
        return True

    def epoch_train(self) -> bool:
        """
        使用训练数据进行一个epoch的训练
        :return: bool
        """
        train_data_loader = DataLoader(
            self.data_pipe_train,
            batch_size=self.coach_settings.train_batch_size,
            shuffle=True,
            collate_fn=SentDeepCrossRankingDataSet.collate_fn,
        )
        self.set_model_state(model_state=ModelState.TRAIN)
        for _, (y, x1, x2, x3, x4, x5, x6) in enumerate(train_data_loader):
            y = y.cuda() if self.use_cuda else y
            user_tokens = x1.cuda() if self.use_cuda else x1
            user_dense_feature = x2.cuda() if self.use_cuda else x2
            user_sparse_feature = x3.cuda() if self.use_cuda else x3
            item_tokens = x4.cuda() if self.use_cuda else x4
            item_dense_feature = x5.cuda() if self.use_cuda else x5
            item_sparse_feature = x6.cuda() if self.use_cuda else x6
            y_ = self.model(
                user_tokens, user_dense_feature, user_sparse_feature,
                item_tokens, item_dense_feature, item_sparse_feature
            )
            loss = self.loss_func(y, y_)
            self.optimizer.zero_grad()
            loss.backward()
            self.optimizer.step()
        return True

    def validation(self, epoch, data_type=ModelDataType.VALID) -> (bool, float):
        """
        验证当前效果
        :param epoch:
        :param data_type:
        :return: bool, average loss
        """
        all_loss = 0
        all_count_loss = 0
        data_loader = None
        if data_type == ModelDataType.VALID:
            data_loader = DataLoader(
                self.data_pipe_valid,
                batch_size=self.coach_settings.valid_batch_size,
                shuffle=False,
                collate_fn=SentDeepCrossRankingDataSet.collate_fn,
            )
        if data_type == ModelDataType.TRAIN:
            data_loader = DataLoader(
                self.data_pipe_train,
                batch_size=self.coach_settings.train_batch_size,
                shuffle=False,
                collate_fn=SentDeepCrossRankingDataSet.collate_fn,
            )
        if data_loader is None:
            return False, 0.0

        self.set_model_state(model_state=ModelState.INFERENCE)
        for _, (y, x1, x2, x3, x4, x5, x6) in enumerate(data_loader):
            y = y.cuda() if self.use_cuda else y
            user_tokens = x1.cuda() if self.use_cuda else x1
            user_dense_feature = x2.cuda() if self.use_cuda else x2
            user_sparse_feature = x3.cuda() if self.use_cuda else x3
            item_tokens = x4.cuda() if self.use_cuda else x4
            item_dense_feature = x5.cuda() if self.use_cuda else x5
            item_sparse_feature = x6.cuda() if self.use_cuda else x6
            y_ = self.model(
                user_tokens, user_dense_feature, user_sparse_feature,
                item_tokens, item_dense_feature, item_sparse_feature
            )
            loss = self.loss_func(y, y_)
            all_loss = all_loss + float(loss)
            all_count_loss = all_count_loss + 1
        # 平均loss
        ave_loss = (1.0 * all_loss) / (all_count_loss + Const.MIN_POSITIVE_NUMBER)

        logging.info("Validation %s data Loss=%s" % (str(data_type), str(ave_loss)))
        return True, ave_loss

    def release_model(self, model_path_ckpt: str, model_path_script: str) -> bool:
        """
        发布模型（TorchScript模型）
        :param model_path_ckpt ckpt的模型文件夹
        :param model_path_script torch script模型文件夹
        :return:
        """
        model_name = "deep_cross_recommender_model"
        os.system("rm -rf %s" % model_path_script)
        os.system("mkdir -p %s" % model_path_script)

        # 生成模型配置清单
        export_model_settings = SentDeepCrossRankingExportedModelSettings(
            model_config_file="config.json",
            model_file="%s.pt" % model_name,
            third_dict_dir="dict",
            user_max_input_tokens=self.model_settings.user_max_input_tokens,
            item_max_input_tokens=self.model_settings.item_max_input_tokens,
            user_dense_feature_dim=self.model_settings.user_dense_feature_sizes,
            item_dense_feature_dim=self.model_settings.item_dense_feature_sizes,
            user_sparse_feature_file=[
                elem.tag_file.split(os.sep)[-1] for elem in self.model_settings.user_sparse_feature_sizes
            ],
            item_sparse_feature_file=[
                elem.tag_file.split(os.sep)[-1] for elem in self.model_settings.item_sparse_feature_sizes
            ]
        )
        dict_path = model_path_script + "/" + export_model_settings.third_dict_dir
        model_file = model_path_script + "/" + export_model_settings.model_file
        config_file = model_path_script + "/" + export_model_settings.model_config_file
        try:
            with open(config_file, "w") as fp:
                fp.write(export_model_settings.json())
        except Exception as ex:
            logging.error("Failed to save %s %s" % (export_model_settings.model_config_file, ex))
            return False

        # 打包第三方词典
        os.system("mkdir -p %s/user" % dict_path)
        os.system("mkdir -p %s/item" % dict_path)
        for elem in self.model_settings.user_sparse_feature_sizes:
            os.system("cp -rf %s %s/user/" % (elem.tag_file, dict_path))

        for elem in self.model_settings.item_sparse_feature_sizes:
            os.system("cp -rf %s %s/item/" % (elem.tag_file, dict_path))

        # 生成torch script模型文件
        try:
            self.model.eval()
            dummy_input = self.model.get_dummy_input()
            torch.jit.trace(self.model, dummy_input).save(model_file)
        except Exception as ex:
            logging.error("Failed to export %s %s" % (model_name, ex))
            return False
        return True

    def load_released_model(self, model_path_script: str) -> bool:
        """
        加载发布的模型及其相关的词典（TorchScript模型）
        :param model_path_script torch script模型文件夹
        :return:
        """
        # 解析model config
        config_file = model_path_script + "/config.json"
        try:
            export_model_settings = SentDeepCrossRankingExportedModelSettings.parse_file(path=config_file)
        except Exception as ex:
            logging.error("Failed to load sent_similarity_model config file %s " % ex)
            return False

        dict_path = model_path_script + "/" + export_model_settings.third_dict_dir
        model_file = model_path_script + "/" + export_model_settings.model_file

        # 加载模型文件
        self.model = torch.jit.load(model_file, map_location=torch.device('cpu'))

        # 加载分词
        self.user_tokenizer = BertTokenizer(
            max_sent_len=export_model_settings.user_max_input_tokens,
            bert_type=BerType.LITE_BERT
        )
        self.item_tokenizer = BertTokenizer(
            max_sent_len=export_model_settings.item_max_input_tokens,
            bert_type=BerType.LITE_BERT
        )

        # 定义datapipe
        self.data_pipe = SentDeepCrossRankingDataSet(
            user_tokenizer=self.user_tokenizer,
            item_tokenizer=self.item_tokenizer,
            user_taggers=[
                TagsDict(
                    tags_file=dict_path + os.sep + "user" + os.sep + tag_file
                ) for tag_file in export_model_settings.user_sparse_feature_file
            ],
            item_taggers=[
                TagsDict(
                    tags_file=dict_path + os.sep + "item" + os.sep + tag_file
                ) for tag_file in export_model_settings.item_sparse_feature_file
            ]
        )

        return True

    def inference(self, data_str) -> (bool, float):
        """
        inference 接口
        :param data_str:
        :return:
        """
        if self.data_pipe is None:
            logging.error("No valid data pipe")
            return False, 0

        result = self.data_pipe.parse_sample(data_str)

        user_tokens = torch.LongTensor([result["user_tokens"]])
        user_dense_feature = torch.FloatTensor([result["user_dense"]])
        user_sparse_feature = torch.LongTensor([result["user_sparse"]])
        item_tokens = torch.LongTensor([result["item_tokens"]])
        item_dense_feature = torch.FloatTensor([result["item_dense"]])
        item_sparse_feature = torch.LongTensor([result["item_sparse"]])

        score = self.model(
            user_tokens=user_tokens,
            user_dense_feature=user_dense_feature,
            user_sparse_feature=user_sparse_feature,
            item_tokens=item_tokens,
            item_dense_feature=item_dense_feature,
            item_sparse_feature=item_sparse_feature
        )
        return True, score

