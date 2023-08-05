#!/usr/bin/env python
'''
garage
Created by Seria at 03/01/2019 8:32 PM
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
from math import ceil
from ... import dock
from .architect import ConvG, ConvD



class Discriminator(dock.Craft):
    def __init__(self, in_shape, category_dim, code_dim, scope='DSC'):
        super(Discriminator, self).__init__(scope)
        H, W, C = in_shape
        self.H = H
        self.W = W
        self.C = C

        self.backbone = ConvD(in_shape)

        self.sftm = dock.Sftm()
        self.cls = dock.Dense(ceil(H/16) * ceil(W/16) * 128, 1)
        self.category = dock.Dense(ceil(H/16) * ceil(W/16) * 128, category_dim)
        self.code = dock.Dense(ceil(H/16) * ceil(W/16) * 128, code_dim)


    def run(self, x):
        bs = x.shape[0]
        self['input'] = x
        x = self.backbone(x)

        self['cls'] = self.cls(x)
        self['category'] = self.sftm(self.category(x))
        self['code'] = self.code(x)

        return self['cls'], self['category'], self['code']



class InfoGAN(dock.Craft):
    def __init__(self, in_shape, category_dim, code_dim, latent_dim=128, scope='INFOGAN'):
        super(InfoGAN, self).__init__(scope)
        self.G = ConvG(in_shape, category_dim + code_dim + latent_dim)
        self.D = Discriminator(in_shape, category_dim, code_dim)

    def run(self):
        pass