#!/usr/bin/env python
'''
engine_mx
Created by Seria at 12/02/2019 3:45 PM
Email: zzqsummerai@yeah.net

                    _ooOoo_
                  o888888888o
                 o88`_ . _`88o
                 (|  0   0  |)
                 O \   。   / O
              _____/`-----‘\_____
            .’   \||  _ _  ||/   `.
            |  _ |||   |   ||| _  |
            |  |  \\       //  |  |
            |  |    \-----/    |  |
             \ .\ ___/- -\___ /. /
         ,--- /   ___\<|>/___   \ ---,
         | |:    \    \ /    /    :| |
         `\--\_    -. ___ .-    _/--/‘
   ===========  \__  NOBUG  __/  ===========

'''
# -*- coding:utf-8 -*-
import torch
import os
import multiprocessing as mp
# from apex import parallel
from types import MethodType


class DDP(torch.nn.parallel.DistributedDataParallel):
    #     def __init__(self, module, delay_allreduce):
    def __init__(self, module, device_ids, output_device):
        #         super(DDP, self).__init__(module, delay_allreduce=delay_allreduce)
        super(DDP, self).__init__(module, device_ids=device_ids, output_device=output_device)

    def __getattr__(self, name: str):
        if '_parameters' in self.__dict__:
            _parameters = self.__dict__['_parameters']
            if name in _parameters:
                return _parameters[name]
        if '_buffers' in self.__dict__:
            _buffers = self.__dict__['_buffers']
            if name in _buffers:
                return _buffers[name]
        if '_modules' in self.__dict__:
            modules = self.__dict__['_modules']
            if name in modules:
                return modules[name]
        if hasattr(self, 'module'):
            if hasattr(self.module, name):
                return getattr(self.module, name)
        raise AttributeError("'{}' object has no attribute '{}'".format(type(self).__name__, name))


# DDP = parallel.DistributedDataParallel

class Multiverse(object):
    '''
    Args:
    nworld: world size
    '''

    def __init__(self, universe, nworld=1):
        self.universe = universe
        self.nworld = nworld
        self.rank = -1
        self.env = os.environ.copy()
        self.env["MASTER_ADDR"] = '127.0.0.1'
        self.env["MASTER_PORT"] = '29500'
        self.env["WORLD_SIZE"] = str(nworld)
        self.env["OMP_NUM_THREADS"] = '1'

    def __call__(self):
        # mp.set_start_method('spawn')
        ps = []
        for r in range(self.nworld):
            self.rank = r
            self.env['RANK'] = str(r)
            self.env['LOCAL_RANK'] = str(r)
            p = mp.Process(target=self.universe, args=(self,))
            p.start()
            ps.append(p)
        for p in ps:
            p.join()

    def init(self):
        for k, v in self.env.items():
            os.environ[k] = v

    def setup(self):
        torch.backends.cudnn.benchmark = True
        torch.cuda.set_device(self.rank)
        torch.distributed.init_process_group(backend='nccl', init_method='env://')

    def collect(self, model):
        scope = model.scope
        #         model = parallel.convert_syncbn_model(model)
        model = torch.nn.SyncBatchNorm.convert_sync_batchnorm(model)
        model = model.to(torch.device('cuda:%d' % self.rank))
        #         model = DDP(model, delay_allreduce=True)
        model = DDP(model, device_ids=[self.rank], output_device=self.rank)

        def gear(self, gr):
            if isinstance(gr, bool):
                if gr:
                    self.train()
                else:
                    self.eval()
            else:
                raise Exception('NEBULAE ERROR ⨷ %s is not a valid type of collected gear.' % type(gr))

        model.gear = MethodType(gear, model)
        model.scope = scope
        return model

    def reduce(self, tensor):
        rt = tensor.clone()
        torch.distributed.all_reduce(rt, op=torch.distributed.ReduceOp.SUM)
        rt /= self.nworld
        return rt