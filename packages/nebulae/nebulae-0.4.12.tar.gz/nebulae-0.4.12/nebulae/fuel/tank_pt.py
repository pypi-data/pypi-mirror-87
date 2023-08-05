#!/usr/bin/env python
'''
Created by Seria at 02/11/2018 3:38 PM
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
import h5py
from multiprocessing import cpu_count
from math import ceil
from torch.utils.data import Dataset, DataLoader


class Tank(object):
    def __init__(self, data_path, data_key, batch_size, shuffle=True, in_same_size=True,
                 fetch_fn=None, collate_fn=None):
        name = os.path.basename(data_path).split('.')[0]
        rank = int(os.environ.get('RANK', -1))
        nworld = int(os.environ.get('WORLD_SIZE', 1))

        class TData(Dataset):
            def __init__(self, verbose=True):
                with h5py.File(data_path, 'r') as f:
                    # make sure that the first dimension is batch
                    self.length = len(f[data_key])
                if verbose:
                    print('+' + (49 * '-') + '+')
                    print('| \033[1;35m%-20s\033[0m fuel tank has been mounted |'% name)
                    print('+' + (49 * '-') + '+')

            def openH5(self):
                self.hdf5 = h5py.File(data_path, 'r')

            def __getitem__(self, idx: int):
                if not hasattr(self, 'hdf5'):
                    self.openH5()
                item = fetch_fn(self.hdf5, idx)
                return item

            def __len__(self):
                return self.length

        self.name = name
        self.rank = rank
        self.tdata = TData(rank<=0)
        self.counter = 0
        self.batch_size = batch_size
        if in_same_size:
            self.MPE = len(self.tdata) // (batch_size * nworld)
        else:
            self.MPE = ceil(len(self.tdata) / (batch_size * nworld))
        ncpus = cpu_count()
        if rank >= 0:
            from torch.utils.data import distributed as dist
            self.sampler = dist.DistributedSampler(self.tdata)
            self.tloader = DataLoader(self.tdata, batch_size, sampler=self.sampler,
                                      collate_fn=collate_fn, drop_last=in_same_size, num_workers=ncpus)
        else:
            self.tloader = DataLoader(self.tdata, batch_size, shuffle,
                                      collate_fn=collate_fn, drop_last=in_same_size, num_workers=ncpus)

    @property
    def data(self):
        return self.tdata.hdf5

    def __del__(self):
        if self.rank<=0:
            print('+' + (53 * '-') + '+')
            print('| \033[1;35m%-20s\033[0m fuel tank is no longer mounted |' % self.name)
            print('+' + (53 * '-') + '+')

    def next(self):
        if self.counter == 0: # create a new iterator at the begining of an epoch
            self.iterator = self.tloader.__iter__()
        self.counter += 1
        if self.counter == self.MPE:
            self.counter = 0
        return self.iterator.__next__()