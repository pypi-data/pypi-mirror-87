#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : zb
# @Time    : 2020/11/18 10:03
# @Blog    : https://blog.zbmain.com

from __future__ import absolute_import, division, print_function, unicode_literals
from utils import time
import tensorflow as tf
import os


class GRU(object):
    '''
    GRU生成模式
    '''
    def __init__(self, vocab_size, embedding_dim, rnn_units, batch_size, buffer_size=10000,
                 checkpoint_dir='./training_checkpoints'):
        '''
        创建模型
        :param vocab_size: 词汇数，所有特征的数量
        :param embedding_dim: 词嵌入维度
        :param rnn_units: 隐藏层节点数
        :param batch_size: 批次
        :param dataset: 数据
        :param buffer_size: 数据缓存区大小
        '''
        self.vocab_size = vocab_size
        self.embedding_dim = embedding_dim
        self.rnn_units = rnn_units
        self.batch_size = batch_size
        self.buffer_size = buffer_size
        # 默认
        self.checkpoint_dir = checkpoint_dir
        self.checkpoint_prefix = os.path.join(self.checkpoint_dir, 'ckpt_{epoch}')

    def loss(self, labels, logits):
        return tf.keras.losses.sparse_categorical_crossentropy(labels, logits, from_logits=True)

    def __call__(self, dataset):
        self.dataset = dataset
        self.optimizer = tf.keras.optimizers.Adam()
        self.model = self.build_model()
        return self.model

    def build_model(self, vocab_size='', embedding_dim='', rnn_units='', batch_size=0):
        """构建模型并返回"""
        # vocab_size 不设置则拿初始化值
        vocab_size = vocab_size or self.vocab_size
        embedding_dim = embedding_dim or self.embedding_dim
        rnn_units = rnn_units or self.rnn_units
        batch_size = batch_size or self.batch_size

        model = tf.keras.Sequential([
            # embbeding层
            tf.keras.layers.Embedding(vocab_size, embedding_dim, batch_input_shape=[batch_size, None]),
            # GRU模型
            tf.keras.layers.GRU(rnn_units, return_sequences=True, stateful=True,
                                recurrent_initializer='glorot_uniform'),
            # 线性层调整输出维度
            tf.keras.layers.Dense(vocab_size)
        ])
        return model

    # 定义损失函数
    def loss(labels, logits):
        """返回损失函数对象"""
        return tf.keras.losses.sparse_categorical_crossentropy(labels, logits, from_logits=True)


    def train_step(self, inp, target):
        with tf.GradientTape() as tape:
            predictions = self.model(inp)
            loss = tf.reduce_mean(
                tf.keras.losses.sparse_categorical_crossentropy(target, predictions, from_logits=True))

        grads = tape.gradient(loss, self.model.trainable_variables)
        self.optimizer.apply_gradients(zip(grads, self.model.trainable_variables))
        return loss

    def train(self, epochs: int = 10):
        for epoch in range(epochs):
            start = time.time()
            hidden = self.model.reset_states()
            for (batch_n, (inp, target)) in enumerate(self.dataset):
                loss = self.train_step(inp, target)
                if batch_n % 100 == 0:
                    template = 'Epoch {} Batch {} Loss {}'
                    print(template.format(epoch + 1, batch_n, loss))
            if (epoch + 1) % 5 == 0:
                self.model.save_weights(self.checkpoint_prefix.format(epoch=epoch + 1))
            print('Epoch {} Loss {:.4f}'.format(epoch + 1, loss))
            print('Time taken for 1 epoch {} sec\n'.format(time.time() - start))
        self.model.save_weights(self.checkpoint_prefix.format(epoch=epoch + 1))  # 保存最后一次
        return self.batch_size

    def loadModel(self, vocab_size='', embedding_dim='', rnn_units='', batch_size=0):
        vocab_size = vocab_size or self.vocab_size
        embedding_dim = embedding_dim or self.embedding_dim
        rnn_units = rnn_units or self.rnn_units
        batch_size = batch_size or self.batch_size
        print(batch_size)
        self.model = self.build_model(vocab_size, embedding_dim, rnn_units, batch_size)
        # 加载model
        self.model.load_weights(tf.train.latest_checkpoint(checkpoint_dir=self.checkpoint_dir))
        return self.model
