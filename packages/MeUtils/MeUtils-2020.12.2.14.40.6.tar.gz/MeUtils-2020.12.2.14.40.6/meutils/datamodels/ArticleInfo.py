#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : MeUtils.
# @File         : ArticleInfo
# @Time         : 2020/12/2 10:44 上午
# @Author       : yuanjie
# @Email        : yuanjie@xiaomi.com
# @Software     : PyCharm
# @Description  :
from typing import *
from pydantic import BaseModel, ValidationError
from datetime import datetime
from meutils.hash_utils import murmurhash


class ArticleInfo(BaseModel):
    id: str = None
    title: str = None
    category: str = None
    subCategory: str = None
    cpApi: str = None
    cType: str = None
    source: str = None

    sourceLevel: float = None
    contentLevel: float = None
    professionalLevel: float = None
    imgNum: float = None
    bodyLen: float = None
    staticQuality: float = None
    dynamicQuality: float = None
    textAdScore: float = None
    pornRank: float = None
    politicalSensitive: float = None
    dedupScore: float = None
    contentScore: float = None
    authorScore: float = None

    createTime: datetime = None
    publishTime: datetime = None

    def __init__(self, **data: Any):
        super().__init__(**data)

        # todo: 封装通用的部分 
        for k in data:
            if k in self.__dict__:
                v = self.__getattribute__(k)

                if isinstance(v, str):
                    self.__setattr__(k, murmurhash(v, bins=10000))
                    # print(k)

                elif isinstance(v, datetime):
                    pass


if __name__ == '__main__':
    ac = ArticleInfo(authorScore='111')
    print(ac.dict())
    print(ac.__getattribute__('authorScore'))
