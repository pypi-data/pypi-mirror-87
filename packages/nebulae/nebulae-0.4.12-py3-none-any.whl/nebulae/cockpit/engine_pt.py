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
import os
import torch
from ..toolkit.utility import getAvailabelGPU

class EnginePT(object):
    '''
    Param:
    device: 'gpu' or 'cpu'
    available_gpus
    gpu_mem_fraction
    if_conserve
    least_mem
    '''
    def __init__(self, param):
        self.param = param
        # look for available gpu devices
        if self.param['device'].lower() == 'gpu':
            if self.param['if_conserve'] and self.param['rank']<=0:
                print('NEBULAE WARNING ♨︎ controlling gpu memory is not available using pytorch.')
            if len(self.param['available_gpus']) == 0:
                gpus = getAvailabelGPU(self.param['ngpus'], self.param['least_mem'])
            else:
                gpus = self.param['available_gpus']
            if len(gpus) < self.param['ngpus']:
                raise Exception('NEBULAE ERROR ⨷ no enough available gpu.')
            # convert gpu list to string
            gpustr = ''
            for g in gpus:
                gpustr += str(g) + ','
            gpus = gpustr[:-1]
            # set environment variable
            os.environ['CUDA_VISIBLE_DEVICES'] = gpus
            self.device = [torch.device('cuda:%d'%i) for i in range(self.param['ngpus'])]
            if self.param['rank']<=0:
                print('+' + ((24 + len(gpus)) * '-') + '+')
                print('| Reside in Device: \033[1;36mGPU-%s\033[0m |' % gpus)
                print('+' + ((24 + len(gpus)) * '-') + '+')
        elif self.param['device'].lower() == 'cpu':
            assert self.param['rank']<0
            self.device = ['cpu']
            print('+' + (23 * '-') + '+')
            print('| Reside in Device: \033[1;36mCPU\033[0m |')
            print('+' + (23 * '-') + '+')
        else:
            raise KeyError('NEBULAE ERROR ⨷ given device should be either cpu or gpu.')

    def coat(self, datum):
        if not isinstance(datum, torch.Tensor): # numpy array
            if datum.shape==(): # scalar
                datum = torch.tensor(datum)
            else:
                datum = torch.from_numpy(datum)

        if self.param['device'] == 'gpu':
            if self.param['rank']<0:
                return datum.cuda()
            else:
                return datum.to(self.device[self.param['rank']])
        elif self.param['device'] == 'cpu':
            return datum.cpu()
        else:
            raise KeyError('NEBULAE ERROR ⨷ given device should be either cpu or gpu.')

    def shell(self, datum, as_np=True):
        datum = datum.detach()
        if as_np:
            if datum.size == 1:
                datum = datum.detach().cpu().numpy()[0]
            else:
                datum = datum.detach().cpu().numpy()
        return datum