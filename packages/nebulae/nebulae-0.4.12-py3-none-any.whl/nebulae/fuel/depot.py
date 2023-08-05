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
from ..law import Constant

__all__ = ('Tank', 'Comburant')

core = Constant.CORE.upper()
if core == 'TENSORFLOW':
    from .tank_tf import ComponentTF
    Craft = ComponentTF(False, True)
elif core == 'MXNET':
    from .tank_mx import ComponentMX
    Craft = ComponentMX(True, True)
elif core == 'PYTORCH':
    from .tank_pt import Tank
    from .comburant_pt import *
    from . import comburant_pt
    __all__ += comburant_pt.__all__
else:
    raise ValueError('NEBULAE ERROR ⨷ %s is an unsupported core.' % core)