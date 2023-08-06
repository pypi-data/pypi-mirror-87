#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : X.
# @File         : run
# @Time         : 2020/11/12 10:57 上午
# @Author       : yuanjie
# @Email        : yuanjie@xiaomi.com
# @Software     : PyCharm
# @Description  : 


# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : tql-App.
# @File         : app_run
# @Time         : 2020/11/5 4:48 下午
# @Author       : yuanjie
# @Email        : yuanjie@xiaomi.com
# @Software     : PyCharm
# @Description  :
"""
'console_scripts': [
    'app-run=appzoo.app_run:cli'
]
"""
from meutils.pipe import *


class CLIRun(object):
    """doc"""

    def __init__(self, **kwargs):
        pass

    def apps_list(self, apps='apps'):
        """
        apps/apps_streamlit
        """

    def pip(self, *packages):
        """
            mecli - pip "meutils appzoo"
        :param packages:
        :return:
        """
        packages = " ".join(packages)
        cmd = f"pip install -U --no-cache-dir -i https://mirrors.aliyun.com/pypi/simple {packages} && pip install -U {packages}"
        logger.info(cmd)
        os.system(cmd)
        # todo: 增加常用包更新


def cli():
    fire.Fire(CLIRun)


if __name__ == '__main__':
    print(CLIRun().pip())
