#!/usr/bin/env python
'''
time_machine
Created by Seria at 23/12/2018 8:34 PM
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
from ..law import Constant

def TimeMachine(config=None, ckpt_path=None, save_path=None):
    rank = int(os.environ.get('RANK', -1))
    if config is None:
        param = {'ckpt_path': ckpt_path, 'save_path': save_path, 'rank': rank}
    else:
        config['ckpt_path'] = config.get('ckpt_path', ckpt_path)
        config['save_path'] = config.get('save_path', save_path)
        config['rank'] = config.get('rank', rank)
        param = config

    core = Constant.CORE.upper()
    if core == 'TENSORFLOW':
        from .time_machine_tf import TimeMachineTF
        return TimeMachineTF(param)
    elif core == 'MXNET':
        from .time_machine_mx import TimeMachineMX
        return TimeMachineMX(param)
    elif core == 'PYTORCH':
        from .time_machine_pt import TimeMachinePT
        return TimeMachinePT(param)
    else:
        raise ValueError('NEBULAE ERROR ⨷ %s is an unsupported core.' % core)