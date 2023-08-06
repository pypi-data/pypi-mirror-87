#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AppZoo.
# @File         : zk_utils
# @Time         : 2020/11/11 5:49 下午
# @Author       : yuanjie
# @Email        : yuanjie@xiaomi.com
# @Software     : PyCharm
# @Description  : 


import yaml
from kazoo.client import KazooClient


def get_zk_config(zk_path="/mipush/cfg", hosts='00011:vrs.poodah.kz.gnigatsqwjt'[::-1], mode='yaml'):
    zk = KazooClient(hosts)
    zk.start()

    data, stat = zk.get(zk_path)

    if mode == 'yaml':
        return yaml.safe_load(data)
    else:
        return data


if __name__ == '__main__':
    print(get_zk_config("/mipush/cfg"))
