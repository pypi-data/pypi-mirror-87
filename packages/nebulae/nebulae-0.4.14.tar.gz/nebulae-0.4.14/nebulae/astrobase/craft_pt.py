#!/usr/bin/env python
'''
component_pt
Created by Seria at 05/02/2019 1:41 PM
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
from math import ceil, sqrt
import torch
import torch.nn as nn
import torch.nn.functional as F
from ..cockpit.engine_pt import EnginePT

__all__ = ('Craft', 'Rudder', 'Nozzle',
           'NEAREST', 'LINEAR', 'CUBIC',
           'XavierNorm', 'XavierUnif', 'Normal', 'Uniform', 'Orthog', 'Zeros', 'Ones',
           'Conv', 'TransConv', 'Dense', 'Embed', 'Identity',
           'Mean', 'Max', 'Min', 'Sum', 'MatMul', 'Grad',
           'Reshape', 'Permute', 'Upscale', 'MaxPool', 'AvgPool',
           'Concat',
           'Clip', 'Dropout', 'BN', 'CBN', 'IN', 'CIN', 'LN', 'SN',
           'Relu', 'LRelu', 'Tanh', 'Sigm', 'Sftm', 'Sftp',
           'MAE', 'MSE', 'SigmXE', 'SftmXE',
           'AccCls',
           'StepLR', 'PolyLR', 'CosLR', 'ExpLR', 'WavyLR',
           'Momentum', 'Nesterov', 'RMSProp', 'Adam', 'AdaBelief')



NEAREST = 0
LINEAR = 1
CUBIC = 2
PT_INTERP = {NEAREST: 'nearest', LINEAR: 'bilinear', CUBIC: 'bicubic'}




class Craft(nn.Module):
    def __init__(self, scope):
        super(Craft, self).__init__()
        self.scope = scope
        self.__pods = []
        self.__dict = {}
        self.__formulated = False

    def run(self, *args, **kwargs):
        raise NotImplementedError

    def forward(self, *args, **kwargs):
        # assert all([isinstance(a, Tensor) for a in args])
        return self.run(*args, **kwargs)

    def gear(self, gr):
        if isinstance(gr, bool):
            if gr:
                self.train()
            else:
                self.eval()
        elif isinstance(gr, EnginePT):
            if gr.param['device'] == 'gpu':
                if gr.param['rank'] < 0:
                    self.cuda()
                else:
                    self.to(gr.device[gr.param['rank']])
            elif gr.param['device'] == 'cpu':
                self.cpu()
        else:
            raise Exception('NEBULAE ERROR ⨷ %s is not a valid type of gear.' % type(gr))

    def chain(self, t, enable=True):
        if t.requires_grad == enable:
            pass
        else:
            t.requires_grad = enable

    def params(self):
        return self.parameters()

    @property
    def pods(self):
        return self.__pods

    @pods.setter
    def pods(self, pods):
        if not self.__formulated:
            self.__pods = pods
            self.__formulated = True

    def __getitem__(self, key):
        paths = key.split('/')
        craft = self
        for p in paths[:-1]:
            craft = getattr(craft, p)
        if paths[-1] == '':
            return craft
        else:
            return craft.__dict[paths[-1]]

    def __setitem__(self, key, value):
        self.__dict[key] = value



class Rudder(object):
    def __init__(self):
        self.grader = torch.enable_grad()

    def __enter__(self):
        self.grader.__enter__()
        return True

    def __exit__(self, *args):
        self.grader.__exit__()

class Nozzle(object):
    def __init__(self):
        self.grader = torch.no_grad()

    def __enter__(self):
        self.grader.__enter__()
        return False

    def __exit__(self, *args):
        self.grader.__exit__()



# -------------------------------------- Layer --------------------------------------- #

class XavierNorm(object):
    def __init__(self):
        self.iniz = nn.init.xavier_normal_

    def __call__(self, params):
        self.iniz(params)



class XavierUnif(object):
    def __init__(self):
        self.iniz = nn.init.xavier_uniform_

    def __call__(self, params):
        self.iniz(params)



class Normal(object):
    def __init__(self, mean=0, std=1):
        self.mean = mean
        self.std = std
        self.iniz = nn.init.normal_

    def __call__(self, params):
        self.iniz(params, self.mean, self.std)



class Uniform(object):
    def __init__(self, min=-1, max=1):
        self.min_val = min
        self.max_val = max
        self.iniz = nn.init.uniform_

    def __call__(self, params):
        self.iniz(params, a=self.min_val, b=self.max_val)



class Orthog(object):
    def __init__(self):
        self.iniz = nn.init.orthogonal_

    def __call__(self, params):
        self.iniz(params)



class Ones(object):
    def __init__(self):
        self.iniz = nn.init.ones_

    def __call__(self, params):
        self.iniz(params)



class Zeros(object):
    def __init__(self):
        self.iniz = nn.init.zeros_

    def __call__(self, params):
        self.iniz(params)



class Conv(Craft):
    def __init__(self, in_chs, out_chs, kernel: tuple, stride=1, padding=0, dilation=1, group=1,
                 w_init=XavierNorm(), b_init=Zeros(), scope='CONV'):
        '''
        Args:
        - in_chs: input channel
        - out_chs: output channel
        - kernel: kernel size (must be a tuple)
        - stride: moving stride
        - padding: padding size
        - dilation: stride in atrous convolution
        - group: number of groups to be divided
        - w_init: weight initializer
        - w_param: options for initializing weight
        - b_init: bias initializer
        - b_param: options for initializing bias
        - scope: name scope
        '''
        super(Conv, self).__init__(scope)
        dim = len(kernel)
        if dim == 1:
            conv_fn = nn.Conv1d
            pad_fn = nn.ConstantPad1d
        elif dim == 2:
            conv_fn = nn.Conv2d
            pad_fn = nn.ConstantPad2d
        elif dim == 3:
            conv_fn = nn.Conv3d
            pad_fn = nn.ConstantPad3d
        else:
            raise Exception('NEBULAE ERROR ⨷ %d-d convolution is not supported.' % dim)

        if isinstance(stride, int):
            stride = dim * [stride]
        if isinstance(dilation, int):
            dilation = dim * [dilation]
        if isinstance(padding, int):
            padding = 2*dim * [padding]

        self.pad = pad_fn(padding, 0)
        self.conv = conv_fn(in_chs, out_chs, kernel, stride=stride, dilation=dilation,
                            groups=group, bias=False if b_init is None else True)
        w_init(self.conv.weight)
        b_init(self.conv.bias)

    def run(self, x):
        y = self.conv(self.pad(x))
        return y



class TransConv(Craft):
    def __init__(self, in_chs, out_chs, out_size, kernel: tuple, stride=1, padding=0, dilation=1, group=1,
                 w_init=XavierNorm(), b_init=Zeros(), scope='TRANSCONV'):
        '''
        Args:
        - in_chs: input channel
        - out_chs: output channel
        - out_size: output size
        - kernel: kernel size (must be a tuple)
        - stride: moving stride
        - padding: padding size
        - dilation: stride in atrous convolution
        - group: number of groups to be divided
        - w_init: weight initializer
        - w_param: options for initializing weight
        - b_init: bias initializer
        - b_param: options for initializing bias
        - scope: name scope
        '''
        super(TransConv, self).__init__(scope)
        dim = len(kernel)
        if dim == 1:
            conv_fn = nn.ConvTranspose1d
        elif dim == 2:
            conv_fn = nn.ConvTranspose2d
        elif dim == 3:
            conv_fn = nn.ConvTranspose3d
        else:
            raise Exception('NEBULAE ERROR ⨷ %d-d convolution is not supported.' % dim)

        if isinstance(stride, int):
            stride = dim * [stride]
        if isinstance(dilation, int):
            dilation = dim * [dilation]
        if isinstance(padding, int):
            padding = dim * [padding]
            # compensation = dim * [0]
        else:
            pad = padding
            padding = []
            # compensation = []
            for d in range(dim-1, -1, -1):
                n_elm = pad[2*d] + pad[2*d+1]
                half_elm = ceil(n_elm / 2)
                padding.append(half_elm)
                # compensation.append(n_elm%2)

        self.target_shape = (out_chs,) + out_size
        self.conv = conv_fn(in_chs, out_chs, kernel, stride=stride, padding=padding,
                            dilation=dilation, groups=group, bias=False if b_init is None else True)
        w_init(self.conv.weight)
        b_init(self.conv.bias)

    def run(self, x):
        target_shape = (x.shape[0],) + self.target_shape
        y = self.conv(x, output_size=target_shape)
        return y



class Dense(Craft):
    def __init__(self, in_chs, out_chs, axis=-1,
                 w_init=XavierNorm(), b_init=Zeros(), scope='DENSE'):
        super(Dense, self).__init__(scope)
        if axis == 0:
            raise Exception('NEBULAE ERROR ⨷ you cannot apply dense layer along batch axis.')
        else:
            self.axis = axis

        if not b_init is None:
            use_bias = True
        else:
            use_bias = False

        self.fc = nn.Linear(in_chs, out_chs, bias=use_bias)
        w_init(self.fc.weight)
        b_init(self.fc.bias)

    def run(self, x):
        if self.axis == -1:
            y = self.fc(x)
        else:
            dim = x.ndim()
            permuted = [i for i in range(dim)]
            permuted = permuted[:self.axis] + permuted[self.axis + 1:] + [self.axis]
            x = x.transpose(*permuted)
            y = self.fc(x)
            permuted = [i for i in range(dim)]
            permuted = permuted[:self.axis] + [dim - 1] + permuted[self.axis:-1]
            y = y.transpose(*permuted)
        return y



class Embed(Craft):
    def __init__(self, ntoken, token_dim, scope='EMBED'):
        super(Embed, self).__init__(scope)
        self.embd = nn.Embedding(ntoken, token_dim)

    def run(self, x):
        y = self.embd(x)
        return y



class Identity(Craft):
    def __init__(self, scope='IDENTITY'):
        super(Identity, self).__init__(scope)

    def run(self, x):
        return x



# ---------------------------------- Manipulation ------------------------------------ #

class EMA(Craft):
    def __init__(self, hull, mmnt, scope='EMA'):
        super(EMA, self).__init__(scope)
        self.counter = 0
        self.mmnt = mmnt
        self.hull = hull
        # self.var_keys = [k for k, _ in self.hull.named_parameters()]
        # self.buf_keys = [k for k, _ in self.hull.named_buffers()]

        # initialize shadow as hull itself
        self._backup()

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
        if hasattr(self, 'hull'):
            if hasattr(self.hull, name):
                return getattr(self.hull, name)
        raise AttributeError("'{}' object has no attribute '{}'".format(type(self).__name__, name))

    def _backup(self):
        self.shadow = {}
        hull_params = self.hull.state_dict()
        for k, v in hull_params.items():
            self.shadow[k] = v.clone().detach()

    def update(self):
        self.counter += 1 # count calling times
        decay = self.mmnt
        with torch.no_grad():
            hull_params = self.hull.state_dict()
            for key in self.shadow.keys():
                hull_params[key].data.copy_(hull_params[key].data * (1 - decay) + self.shadow[key].data * decay)
        self._backup()

    def run(self, *args, **kwargs):
        return self.hull(*args, **kwargs)



# ------------------------------------ Polyadic -------------------------------------- #

class Concat(Craft):
    def __init__(self, scope='CONCAT'):
        super(Concat, self).__init__(scope)

    def run(self, t, axis=-1):
        y = torch.cat(t, dim=axis)
        return y



# ----------------------------------- Statistics ------------------------------------- #

class Clip(Craft):
    def __init__(self, intrinsic=False, scope='CLIP'):
        super(Clip, self).__init__(scope)
        self.intrinsic = intrinsic

    def run(self, x, ranges):
        if isinstance(ranges, tuple):
            assert len(ranges)==2
        else:
            ranges = (-ranges, ranges)
        if self.intrinsic:
            x.data = x.clamp(ranges[0], ranges[1])
            return
        else:
            return torch.clamp(x, ranges[0], ranges[1])



class Mean(Craft):
    def __init__(self, scope='MEAN'):
        super(Mean, self).__init__(scope)

    def run(self, x, axis=None):
        if axis is None:
            y = torch.mean(x)
        else:
            y = torch.mean(x, dim=axis)
        return y



class Max(Craft):
    def __init__(self, scope='MAX'):
        super(Max, self).__init__(scope)

    def run(self, x, axis=None):
        if axis is None:
            y = torch.max(x)
        else:
            y = torch.max(x, dim=axis)
        return y



class Min(Craft):
    def __init__(self, scope='MIN'):
        super(Min, self).__init__(scope)

    def run(self, x, axis=None):
        if axis is None:
            y = torch.min(x)
        else:
            y = torch.min(x, dim=axis)
        return y



class Sum(Craft):
    def __init__(self, scope='SUM'):
        super(Sum, self).__init__(scope)

    def run(self, x, axis=None):
        if axis is None:
            y = torch.sum(x)
        else:
            y = torch.sum(x, dim=axis)
        return y



class MatMul(Craft):
    def __init__(self, scope='MATMUL'):
        super(MatMul, self).__init__(scope)

    def run(self, x, y, in_batch=False):
        if in_batch:
            z = torch.bmm(x, y)
        else:
            z = torch.mm(x, y)
        return z



class Grad(Craft):
    def __init__(self, scope='GRAD'):
        super(Grad, self).__init__(scope)

    def run(self, i, o):
        grad_out_weight = torch.ones((i.shape[0], 1), device=i.device)
        g = torch.autograd.grad(o, i, grad_outputs=grad_out_weight,
                                retain_graph=True, create_graph=True, only_inputs=True)
        return g



# ------------------------------------- Resizer -------------------------------------- #

class Reshape(Craft):
    def __init__(self, scope='RESHAPE'):
        super(Reshape, self).__init__(scope)

    def run(self, x, shape):
        y = torch.reshape(x, shape)
        return y



class Permute(Craft):
    def __init__(self, scope='PERMUTE'):
        super(Permute, self).__init__(scope)

    def run(self, x, shape):
        y = x.permute(shape)
        return y



class Upscale(Craft):
    def __init__(self, scale, interp=NEAREST, scope='UPS'):
        super(Upscale, self).__init__(scope)
        self.fn = nn.Upsample(scale_factor=scale, mode=PT_INTERP[interp])

    def run(self, x):
        y = self.fn(x)
        return y



class MaxPool(Craft):
    def __init__(self, kernel: tuple, stride=2, padding=0, scope='MPOOL'):
        super(MaxPool, self).__init__(scope)
        dim = len(kernel)
        is_global = True if kernel[-1] < 0 else False
        if dim == 1:
            if is_global:
                pool_fn = nn.AdaptiveMaxPool1d
            else:
                pool_fn = nn.MaxPool1d
            pad_fn = nn.ConstantPad1d
        elif dim == 2:
            if is_global:
                pool_fn = nn.AdaptiveMaxPool2d
            else:
                pool_fn = nn.MaxPool2d
            pad_fn = nn.ConstantPad2d
        elif dim == 3:
            if is_global:
                pool_fn = nn.AdaptiveMaxPool3d
            else:
                pool_fn = nn.MaxPool3d
            pad_fn = nn.ConstantPad3d
        else:
            raise Exception('NEBULAE ERROR ⨷ %d-d pooling is not supported.' % dim)

        if isinstance(stride, int):
            stride = dim * [stride]

        self.pad = pad_fn(padding, 0)
        if is_global:
            assert padding == 0
            self.pool = pool_fn(tuple(dim * [1]))
        else:
            self.pool = pool_fn(kernel_size=kernel, stride=stride)

    def run(self, x):
        y = self.pool(self.pad(x))
        return y



class AvgPool(Craft):
    def __init__(self, kernel: tuple, stride=2, padding=0, scope='APOOL'):
        super(AvgPool, self).__init__(scope)
        dim = len(kernel)
        is_global = True if kernel[-1]<0 else False
        if dim == 1:
            if is_global:
                pool_fn = nn.AdaptiveAvgPool1d
            else:
                pool_fn = nn.AvgPool1d
            pad_fn = nn.ConstantPad1d
        elif dim == 2:
            if is_global:
                pool_fn = nn.AdaptiveAvgPool2d
            else:
                pool_fn = nn.AvgPool2d
            pad_fn = nn.ConstantPad2d
        elif dim == 3:
            if is_global:
                pool_fn = nn.AdaptiveAvgPool3d
            else:
                pool_fn = nn.AvgPool3d
            pad_fn = nn.ConstantPad3d
        else:
            raise Exception('NEBULAE ERROR ⨷ %d-d pooling is not supported.' % dim)

        if isinstance(stride, int):
            stride = dim * [stride]

        self.pad = pad_fn(padding, 0)
        if is_global:
            assert padding == 0
            self.pool = pool_fn(tuple(dim * [1]))
        else:
            self.pool = pool_fn(kernel_size=kernel, stride=stride)

    def run(self, x):
        y = self.pool(self.pad(x))
        return y



# ------------------------------------ Activation ------------------------------------ #

class Relu(Craft):
    def __init__(self, scope='RELU'):
        super(Relu, self).__init__(scope)
        self.actv = nn.ReLU()

    def run(self, x):
        y = self.actv(x)
        return y



class LRelu(Craft):
    def __init__(self, alpha=0.2, scope='LRELU'):
        super(LRelu, self).__init__(scope)
        self.actv = nn.LeakyReLU(alpha)

    def run(self, x):
        y = self.actv(x)
        return y



class Tanh(Craft):
    def __init__(self, scope='TANH'):
        super(Tanh, self).__init__(scope)
        self.actv = nn.Tanh()

    def run(self, x):
        y = self.actv(x)
        return y



class Sigm(Craft):
    def __init__(self, scope='SIGM'):
        super(Sigm, self).__init__(scope)
        self.actv = nn.Sigmoid()

    def run(self, x):
        y = self.actv(x)
        return y



class Sftm(Craft):
    def __init__(self, axis=-1, scope='SFTM'):
        super(Sftm, self).__init__(scope)
        self.actv = nn.Softmax(dim=axis)

    def run(self, x):
        y = self.actv(x)
        return y



class Sftp(Craft):
    def __init__(self, beta=1, scope='SFTP'):
        super(Sftp, self).__init__(scope)
        self.actv = nn.Softplus(beta)

    def run(self, x):
        y = self.actv(x)
        return y



# ------------------------------------ Distributing ------------------------------------ #

class Dropout(Craft):
    def __init__(self, p_drop, dim, scope='DROPOUT'):
        super(Dropout, self).__init__(scope)
        if dim == 1:
            dp_fn = nn.Dropout
        elif dim == 2:
            dp_fn = nn.Dropout2d
        elif dim == 3:
            dp_fn = nn.Dropout3d
        else:
            raise Exception('NEBULAE ERROR ⨷ %d-d BN is not supported.' % dim)
        self.dp = dp_fn(p=p_drop)

    def run(self, x):
        y = self.dp(x)
        return y



class BN(Craft):
    def __init__(self, out_chs, dim, mmnt=0.9, resilient=True, scope='BN'):
        super(BN, self).__init__(scope)
        if dim == 1:
            norm_fn = nn.BatchNorm1d
        elif dim == 2:
            norm_fn = nn.BatchNorm2d
        elif dim == 3:
            norm_fn = nn.BatchNorm3d
        else:
            raise Exception('NEBULAE ERROR ⨷ %d-d BN is not supported.' % dim)
        self.norm = norm_fn(out_chs, momentum=1 - mmnt, affine=resilient, eps=1e-5)

    def run(self, x):
        y = self.norm(x)
        return y



class CBN(Craft):
    def __init__(self, in_chs, out_chs, dim, mmnt=0.9, scope='CBN'):
        super(CBN, self).__init__(scope)
        if dim == 1:
            norm_fn = nn.BatchNorm1d
        elif dim == 2:
            norm_fn = nn.BatchNorm2d
        elif dim == 3:
            norm_fn = nn.BatchNorm3d
        else:
            raise Exception('NEBULAE ERROR ⨷ %d-d CN is not supported.' % dim)
        self.norm = norm_fn(out_chs, momentum=1 - mmnt, affine=False, eps=1e-5)
        self.relu = nn.ReLU()
        self.gamma_1 = nn.Linear(in_chs, in_chs // 2)
        self.gamma_2 = nn.Linear(in_chs // 2, out_chs)
        self.beta_1 = nn.Linear(in_chs, in_chs // 2)
        self.beta_2 = nn.Linear(in_chs // 2, out_chs)

    def run(self, x, z):
        y = self.norm(x)

        g = self.gamma_1(z)
        g = self.relu(g)
        g = self.gamma_2(g)

        b = self.beta_1(z)
        b = self.relu(b)
        b = self.beta_2(b)

        for _ in range(x.ndim - 2):
            g = g.unsqueeze(-1)
            b = b.unsqueeze(-1)

        self.weight = g
        self.bias = b
        y = self.weight * y + self.bias

        return y



class IN(Craft):
    def __init__(self, out_chs, dim, mmnt=0.9, resilient=True, scope='IN'):
        super(IN, self).__init__(scope)
        if dim == 1:
            norm_fn = nn.InstanceNorm1d
        elif dim == 2:
            norm_fn = nn.InstanceNorm2d
        elif dim == 3:
            norm_fn = nn.InstanceNorm3d
        else:
            raise Exception('NEBULAE ERROR ⨷ %d-d IN is not supported.' % dim)
        self.norm = norm_fn(out_chs, momentum=1 - mmnt, affine=resilient, eps=1e-5)

    def run(self, x):
        y = self.norm(x)
        return y



class CIN(Craft):
    def __init__(self, in_chs, out_chs, dim, mmnt=0.9, scope='CIN'):
        super(CIN, self).__init__(scope)
        if dim == 1:
            norm_fn = nn.InstanceNorm1d
        elif dim == 2:
            norm_fn = nn.InstanceNorm2d
        elif dim == 3:
            norm_fn = nn.InstanceNorm3d
        else:
            raise Exception('NEBULAE ERROR ⨷ %d-d CN is not supported.' % dim)
        self.norm = norm_fn(out_chs, momentum=1 - mmnt, affine=False, eps=1e-5)
        self.relu = nn.ReLU()
        self.gamma_1 = nn.Linear(in_chs, in_chs // 2)
        self.gamma_2 = nn.Linear(in_chs // 2, out_chs)
        self.beta_1 = nn.Linear(in_chs, in_chs // 2)
        self.beta_2 = nn.Linear(in_chs // 2, out_chs)

    def run(self, x, z):
        y = self.norm(x)

        g = self.gamma_1(z)
        g = self.relu(g)
        g = self.gamma_2(g)

        b = self.beta_1(z)
        b = self.relu(b)
        b = self.beta_2(b)

        for _ in range(x.ndim - 2):
            g = g.unsqueeze(-1)
            b = b.unsqueeze(-1)

        self.weight = g
        self.bias = b
        y = self.weight * y + self.bias

        return y



class LN(Craft):
    def __init__(self, norm_shape, resilient=True, scope='LN'):
        super(LN, self).__init__(scope)
        norm_shape = tuple([norm_shape[-1]] + [ns for ns in norm_shape[:-1]])
        self.norm = nn.LayerNorm(norm_shape, elementwise_affine=resilient, eps=1e-5)

    def run(self, x):
        y = self.norm(x)
        return y



class SN(Craft):
    def __init__(self, craft, niter=3, eps=1e-12, scope='SN'):
        super(SN, self).__init__(scope)
        self.name = 'weight'
        if isinstance(craft, (Conv, TransConv)):
            self.key = 'conv/'
        elif isinstance(craft, Dense):
            self.key = 'fc/'
        elif isinstance(craft, Embed):
            self.key = 'embd/'
        elif isinstance(craft, (BN, IN, LN)):
            self.key = 'norm/'
        elif isinstance(craft, (CBN, CIN)):
            self.key = ''
        else:
            raise Exception('NEBULAE ERROR ⨷ SN does not support %s layer.' % type(craft))
        self.craft = craft
        self.hull = craft[self.key]
        self.niter = niter
        self.eps = eps
        if not self._made_params():
            self._make_params()

    def l2normalize(self, v):
        return v / (v.norm() + self.eps)

    def _update_u_v(self):
        if not self._made_params():
            self._make_params()
        w = getattr(self.hull, self.name)
        u = getattr(self.hull, self.name + "_u")

        height = w.data.shape[0]
        for _ in range(self.niter):
            v = self.l2normalize(torch.mv(torch.t(w.view(height, -1).data), u))
            u = self.l2normalize(torch.mv(w.view(height, -1).data, v))

        setattr(self.hull, self.name + "_u", u)
        w.data = w.data / torch.dot(u, torch.mv(w.view(height, -1).data, v))

    def _made_params(self):
        try:
            u = getattr(self.hull, self.name + "_u")
            return True
        except AttributeError:
            return False

    def _make_params(self):
        w = getattr(self.hull, self.name)

        height = w.data.shape[0]
        width = w.view(height, -1).data.shape[1]

        u = self.l2normalize(w.data.new(height).normal_(0, 1))

        self.hull.register_buffer(self.name + "_u", u)

    def run(self, *args, **kwargs):
        self._update_u_v()
        return self.craft.run(*args, **kwargs)



# ------------------------------------ Loss ------------------------------------ #

class MAE(Craft):
    def __init__(self, scope='MAE'):
        super(MAE, self).__init__(scope)
        self.cost = nn.L1Loss()

    def run(self, x, y):
        z = self.cost(x, y)
        return z



class MSE(Craft):
    def __init__(self, scope='MAE'):
        super(MSE, self).__init__(scope)
        self.cost = nn.MSELoss()

    def run(self, x, y):
        z = self.cost(x, y)
        return z



class SigmXE(Craft):
    def __init__(self, is_one_hot, scope='SFTMXE'):
        super(SigmXE, self).__init__(scope)
        self.ioh = is_one_hot
        self.cost = nn.BCEWithLogitsLoss()

    def run(self, x, y):
        if self.ioh:
            y = torch.argmax(y, dim=-1)
        z = self.cost(x, y)
        return z



class SftmXE(Craft):
    def __init__(self, is_one_hot, scope='SFTMXE'):
        super(SftmXE, self).__init__(scope)
        self.ioh = is_one_hot
        self.cost = nn.CrossEntropyLoss()

    def run(self, x, y):
        if self.ioh:
            y = torch.argmax(y, dim=-1)
        z = self.cost(x, y)
        return z



# ------------------------------------ Metric ------------------------------------ #

class AccCls(Craft):
    def __init__(self, multi_class, is_one_hot, scope='ACCCLS'):
        super(AccCls, self).__init__(scope)
        if multi_class:
            assert not is_one_hot
        self.mulcls = multi_class
        self.ioh = is_one_hot

    def run(self, x, y):
        if self.mulcls:
            x = torch.round(x)
            correct = torch.mean((x == y).float(), dim=-1)
            z = torch.mean((correct == 1).float())
        else:
            if self.ioh:
                y = torch.argmax(y, dim=-1)
            if x.shape[-1] == 1: # binary classification
                x = torch.round(x)
            else:
                x = torch.argmax(x, dim=-1)
            z = torch.mean((x == y).float())
        return z


# ------------------------------------ Optimizer ------------------------------------ #

class StepLR(object):
    def __init__(self, period, factor):
        self.period = period
        self.factor = factor

    def __call__(self, optimizer):
        return torch.optim.lr_scheduler.StepLR(optimizer, self.period, gamma=self.factor)



class PolyLR(object):
    def __init__(self, cutoff, power):
        self.cutoff = cutoff
        self.power = power

    def __call__(self, optimizer):
        lr_update = lambda mile: (1.001 - min(mile / self.cutoff, 1)) ** self.power
        return torch.optim.lr_scheduler.LambdaLR(optimizer, lr_update)



class CosLR(object):
    def __init__(self, period):
        self.period = period

    def __call__(self, optimizer):
        return torch.optim.lr_scheduler.CosineAnnealingLR(optimizer, T_max=self.period,
                                                          eta_min=optimizer.defaults['lr']*0.001)



class ExpLR(object):
    def __init__(self, period, base):
        self.period = period
        self.base = base

    def __call__(self, optimizer):
        lr_update = lambda mile: self.base ** (mile / self.period)
        return torch.optim.lr_scheduler.LambdaLR(optimizer, lr_update)



class WavyLR(object):
    def __init__(self, period, dampen):
        self.period = period
        self.dampen = dampen

    def __call__(self, optimizer):
        lr_update = lambda x: self.dampen ** (x - 1)
        return torch.optim.lr_scheduler.CyclicLR(optimizer, optimizer.defaults['lr'] / 2, optimizer.defaults['lr'],
                                                 step_size_up=self.period // 2, scale_fn=lr_update, scale_mode='cycle')



class Momentum(Craft):
    def __init__(self, hull, lr, mmnt=0.9, wd=0, lr_decay=None,
                 grad_limit=-1, update_scope=None, scope='MOMENTUM'):
        super(Momentum, self).__init__(scope)
        # select parameters await updating
        if update_scope is None:
            update_var = hull.parameters()
        else:
            if isinstance(update_scope, str):
                update_scope = [update_scope]
            update_var = []
            for us in update_scope:
                paths = us.split('/')
                craft = hull
                for p in paths:
                    craft = getattr(craft, p)
                update_var.append(craft.parameters())

        if grad_limit>0:
            nn.utils.clip_grad_value_(update_var, grad_limit)
        self.optz = torch.optim.SGD(update_var, lr=lr, momentum=mmnt, weight_decay=wd)
        if lr_decay is None:
            self.lr_decay = None
        else:
            self.lr_decay = lr_decay(self.optz)

    def run(self, target):
        self.optz.zero_grad()
        target.backward()
        self.optz.step()
        if self.lr_decay is not None:
            self.lr_decay.step()



class Nesterov(Craft):
    def __init__(self, hull, lr, mmnt=0.9, wd=0,
                 lr_decay=None, lr_params=None, grad_limit=-1,
                 update_scope=None, scope='NESTEROV'):
        super(Nesterov, self).__init__(scope)
        # select parameters await updating
        if update_scope is None:
            update_var = hull.parameters()
        else:
            if isinstance(update_scope, str):
                update_scope = [update_scope]
            update_var = []
            for us in update_scope:
                paths = us.split('/')
                craft = hull
                for p in paths:
                    craft = getattr(craft, p)
                update_var.append(craft.parameters())

        if grad_limit > 0:
            nn.utils.clip_grad_value_(update_var, grad_limit)
        self.optz = torch.optim.SGD(update_var, lr=lr, momentum=mmnt, weight_decay=wd, nesterov=True)
        if lr_decay is None:
            self.lr_decay = None
        else:
            self.lr_decay = lr_decay(self.optz)

    def run(self, target):
        self.optz.zero_grad()
        target.backward()
        self.optz.step()
        if self.lr_decay is not None:
            self.lr_decay.step()



class RMSProp(Craft):
    def __init__(self, hull, lr, mmnt=0., wd=0,
                 lr_decay=None, lr_params=None, grad_limit=-1,
                 update_scope=None, scope='RMSPROP'):
        super(RMSProp, self).__init__(scope)
        # select parameters await updating
        if update_scope is None:
            update_var = hull.parameters()
        else:
            if isinstance(update_scope, str):
                update_scope = [update_scope]
            update_var = []
            for us in update_scope:
                paths = us.split('/')
                craft = hull
                for p in paths:
                    craft = getattr(craft, p)
                update_var.append(craft.parameters())

        if grad_limit > 0:
            nn.utils.clip_grad_value_(update_var, grad_limit)
        self.optz = torch.optim.RMSprop(update_var, lr=lr, momentum=mmnt, weight_decay=wd)
        if lr_decay is None:
            self.lr_decay = None
        else:
            self.lr_decay = lr_decay(self.optz)

    def run(self, target):
        self.optz.zero_grad()
        target.backward()
        self.optz.step()
        if self.lr_decay is not None:
            self.lr_decay.step()



class Adam(Craft):
    def __init__(self, hull, lr, mmnt1=0.9, mmnt2=0.999, wd=0,
                 lr_decay=None, lr_params=None, grad_limit=-1,
                 update_scope=None, scope='ADAM'):
        super(Adam, self).__init__(scope)
        # select parameters await updating
        if update_scope is None:
            update_var = hull.parameters()
        else:
            if isinstance(update_scope, str):
                update_scope = [update_scope]
            update_var = []
            for us in update_scope:
                paths = us.split('/')
                craft = hull
                for p in paths:
                    craft = getattr(craft, p)
                update_var.append(craft.parameters())

        if grad_limit > 0:
            nn.utils.clip_grad_value_(update_var, grad_limit)
        self.optz = torch.optim.Adam(update_var, lr=lr, betas=(mmnt1, mmnt2), weight_decay=wd)
        if lr_decay is None:
            self.lr_decay = None
        else:
            self.lr_decay = lr_decay(self.optz)

    def run(self, target):
        self.optz.zero_grad()
        target.backward()
        self.optz.step()
        if self.lr_decay is not None:
            self.lr_decay.step()



class _AdaBelief(torch.optim.Optimizer):
    r"""Implements Adam algorithm.

    It has been proposed in `Adam: A Method for Stochastic Optimization`_.

    Arguments:
        params (iterable): iterable of parameters to optimize or dicts defining
            parameter groups
        lr (float, optional): learning rate (default: 1e-3)
        betas (Tuple[float, float], optional): coefficients used for computing
            running averages of gradient and its square (default: (0.9, 0.999))
        eps (float, optional): term added to the denominator to improve
            numerical stability (default: 1e-8)
        weight_decay (float, optional): weight decay (L2 penalty) (default: 0)
        amsgrad (boolean, optional): whether to use the AMSGrad variant of this
            algorithm from the paper `On the Convergence of Adam and Beyond`_
            (default: False)

    .. _Adam\: A Method for Stochastic Optimization:
        https://arxiv.org/abs/1412.6980
    .. _On the Convergence of Adam and Beyond:
        https://openreview.net/forum?id=ryQu7f-RZ
    """

    def __init__(self, params, lr=1e-3, betas=(0.9, 0.999), eps=1e-8,
                 weight_decay=0, amsgrad=False):
        if not 0.0 <= lr:
            raise ValueError("Invalid learning rate: {}".format(lr))
        if not 0.0 <= eps:
            raise ValueError("Invalid epsilon value: {}".format(eps))
        if not 0.0 <= betas[0] < 1.0:
            raise ValueError("Invalid beta parameter at index 0: {}".format(betas[0]))
        if not 0.0 <= betas[1] < 1.0:
            raise ValueError("Invalid beta parameter at index 1: {}".format(betas[1]))
        if not 0.0 <= weight_decay:
            raise ValueError("Invalid weight_decay value: {}".format(weight_decay))
        defaults = dict(lr=lr, betas=betas, eps=eps,
                        weight_decay=weight_decay, amsgrad=amsgrad)
        super(_AdaBelief, self).__init__(params, defaults)

    def __setstate__(self, state):
        super(_AdaBelief, self).__setstate__(state)
        for group in self.param_groups:
            group.setdefault('amsgrad', False)

    @torch.no_grad()
    def step(self, closure=None):
        """Performs a single optimization step.

        Arguments:
            closure (callable, optional): A closure that reevaluates the model
                and returns the loss.
        """
        loss = None
        if closure is not None:
            with torch.enable_grad():
                loss = closure()

        for group in self.param_groups:
            for p in group['params']:
                if p.grad is None:
                    continue
                grad = p.grad
                if grad.is_sparse:
                    raise RuntimeError(
                        'AdaBelief does not support sparse gradients, please consider SparseAdam instead')
                amsgrad = group['amsgrad']

                state = self.state[p]

                # State initialization
                if len(state) == 0:
                    state['step'] = 0
                    # Exponential moving average of gradient values
                    state['exp_avg'] = torch.zeros_like(p, memory_format=torch.preserve_format)
                    # Exponential moving average of squared gradient values
                    state['exp_avg_sq'] = torch.zeros_like(p, memory_format=torch.preserve_format)
                    if amsgrad:
                        # Maintains max of all exp. moving avg. of sq. grad. values
                        state['max_exp_avg_sq'] = torch.zeros_like(p, memory_format=torch.preserve_format)

                exp_avg, exp_avg_sq = state['exp_avg'], state['exp_avg_sq']
                if amsgrad:
                    max_exp_avg_sq = state['max_exp_avg_sq']
                beta1, beta2 = group['betas']

                state['step'] += 1
                bias_correction1 = 1 - beta1 ** state['step']
                bias_correction2 = 1 - beta2 ** state['step']

                if group['weight_decay'] != 0:
                    grad = grad.add(p, alpha=group['weight_decay'])

                # Decay the first and second moment running average coefficient
                exp_avg.mul_(beta1).add_(grad, alpha=1 - beta1)
                exp_avg_sq.mul_(beta2).addcmul_(grad - exp_avg, grad - exp_avg, value=1 - beta2)
                if amsgrad:
                    # Maintains the maximum of all 2nd moment running avg. till now
                    torch.max(max_exp_avg_sq, exp_avg_sq, out=max_exp_avg_sq)
                    # Use the max. for normalizing running avg. of gradient
                    denom = (max_exp_avg_sq.sqrt() / sqrt(bias_correction2)).add_(group['eps'])
                else:
                    denom = (exp_avg_sq.sqrt() / sqrt(bias_correction2)).add_(group['eps'])

                step_size = group['lr'] / bias_correction1

                p.addcdiv_(exp_avg, denom, value=-step_size)

        return loss



class AdaBelief(Craft):
    def __init__(self, hull, lr, mmnt1=0.9, mmnt2=0.999, wd=0,
                 lr_decay=None, lr_params=None, grad_limit=-1,
                 update_scope=None, scope='ADABELIEF'):
        super(AdaBelief, self).__init__(scope)
        # select parameters await updating
        if update_scope is None:
            update_var = hull.parameters()
        else:
            if isinstance(update_scope, str):
                update_scope = [update_scope]
            update_var = []
            for us in update_scope:
                paths = us.split('/')
                craft = hull
                for p in paths:
                    craft = getattr(craft, p)
                update_var.append(craft.parameters())

        if grad_limit > 0:
            nn.utils.clip_grad_value_(update_var, grad_limit)
        self.optz = _AdaBelief(update_var, lr=lr, betas=(mmnt1, mmnt2), weight_decay=wd)
        if lr_decay is None:
            self.lr_decay = None
        else:
            self.lr_decay = lr_decay(self.optz)

    def run(self, target):
        self.optz.zero_grad()
        target.backward()
        self.optz.step()
        if self.lr_decay is not None:
            self.lr_decay.step()

