#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : MeUtils.
# @File         : log_utils
# @Time         : 2020/11/12 11:40 上午
# @Author       : yuanjie
# @Email        : yuanjie@xiaomi.com
# @Software     : PyCharm
# @Description  : 


import os
from random import uniform
from loguru import logger

LOG_PATH = os.environ.get('LOG_PATH')
LOG_LEVEL = os.environ.get('LOG_LEVEL', "INFO")
if LOG_PATH:
    logger.add(
        LOG_PATH,
        rotation="100 MB",
        enqueue=True,  # 异步
        encoding="utf-8",
        backtrace=True,
        diagnose=True,
        level=LOG_LEVEL
    )

# 日志采样输出：按时间 按条数
def log_sampler(log, bins=10):
    if uniform(0, bins) < 1:
        logger.info(log)


# todo:
#  add zk/es/mongo/hdfs logger
# logger = logger.patch(lambda r: r.update(name=__file__))


if __name__ == '__main__':
    logger.info("xx")
