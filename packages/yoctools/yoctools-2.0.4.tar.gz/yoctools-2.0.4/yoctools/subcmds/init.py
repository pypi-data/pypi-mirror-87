# -*- coding:utf-8 -*-
#
# Copyright (C) 2019-2020 Alibaba Group Holding Limited


from __future__ import print_function

import os
from yoctools import *

class Init(Command):
    common = True
    helpSummary = "Initialize yoc workspace in the current directory"
    helpUsage = """
%prog [repo] [option] <branch>
"""
    helpDescription = """
Initialize yoc workspace in the current directory.
"""
    def _Options(self, p):
        p.add_option('-b', '--branch',
                     dest='branch', action='store', type='string',
                     help='the manifest repo branch')

    def Execute(self, opt, args):
        conf = Configure()
        if conf.init:
            put_string("Workspace is initialized already.")
            put_string("The workspace is `%s`" % conf.yoc_path)
            put_string("If you want to init again,please remove the .yoc file")
            return
        try:
            urlretrieve('https://yoctools.oss-cn-beijing.aliyuncs.com/yoc_new', '.yoc')
        except:
            pass
        if os.path.isfile('.yoc'):
            conf.load(os.path.join(conf.yoc_path, '.yoc'))
        if opt.branch:
            conf.branch = opt.branch
        if len(args) > 0:
            conf.repo = args[0] # repourl
        conf.save()
