# -*- coding:utf-8 -*-
#
# Copyright (C) 2019-2020 Alibaba Group Holding Limited


from __future__ import print_function

import threadpool
from yoctools import *


class Install(Command):
    common = True
    helpSummary = "Install component into project environment"
    helpUsage = """
%prog [option] [<component>...]
"""
    helpDescription = """
Install component into project environment
"""

    def _Options(self, p):
        self.jobs = 1
        p.add_option('-j', '--jobs',
                     dest='jobs', action='store', type='int',
                     help="projects to fetch simultaneously (default %d)" % self.jobs)
        p.add_option('-f', '--force',
                     dest='force', action='store_true',
                     help='install component force if exist already')
        p.add_option('-b', '--branch',
                     dest='branch', action='store', type='string',
                     help='the branch for component to download')

    def Execute(self, opt, args):
        if opt.jobs:
            jobs = opt.jobs
        else:
            jobs = 4
        put_string("Start to install components...")
        yoc = YoC()
        components = ComponentGroup()
        if len(args) > 0:
            for name in args:
                update = False
                if name == args[0]:
                    update = True
                cmpt = yoc.check_cmpt_download(name, update=True, force=opt.force)
                if cmpt:
                    components.add(cmpt)
        else:
            yoc.update()
            components = yoc.occ_components
        
        exe_dld_cmpt_list = ComponentGroup()
        if len(components) > 0:
            dled_cmpts =[]
            while len(components) > 0:
                cmpts = components
                self.download(jobs, cmpts, opt.branch)
                for c in cmpts:
                    if c.name not in dled_cmpts:
                        dled_cmpts.append(c.name)
                components = ComponentGroup()
                for c in cmpts:
                    exe_dld_cmpt_list.add(c)
                    ret = c.load_package()
                    if ret:
                        yoc.update_version(c.depends)
                        cmpt_list = self.get_need_download_cmpts(args, dled_cmpts, c.depends)
                        for component in yoc.occ_components:
                            if component.name in cmpt_list:
                                components.add(component)

            # check file
            for c in exe_dld_cmpt_list:
                if not c.check_file_integrity():
                    put_string("Component:%s maybe not fetch integrallty, Please check the branch is right." % c.name)
            put_string('Download components finish.')
        else:
            put_string("No component need to install.")

    def get_need_download_cmpts(self, origin_list, downloaded_list, depends):
        cmpt_list = []
        for name in depends:
            if type(name) == dict:
                name = list(name.keys())[0]
                if (name not in origin_list) and (name not in downloaded_list):
                    cmpt_list.append(name)
        return cmpt_list

    def download(self, jobs, components, branch):
        task_pool = threadpool.ThreadPool(jobs)
        tasks = []
        for component in components:
            tasks.append(component)

        def thread_execture(component):
            component.download(branch)

        requests = threadpool.makeRequests(thread_execture, tasks)
        for req in requests:
            task_pool.putRequest(req)
        task_pool.wait()
        task_pool.dismissWorkers(jobs, do_join=True)
