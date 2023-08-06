#!/usr/bin/env python
'''
utility
Created by Seria at 14/11/2018 8:33 PM
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

import json
import numpy as np
import subprocess as subp
import h5py
import os
import io
from math import ceil
from PIL import Image
from copy import deepcopy
from ..law import Constant



def autoPad(in_size: tuple, kernel: tuple, stride=1, dilation=1):
    '''
    Args
    - in_size: input size e.g. (h, w) for 2d tensor
    - kernel: kernel size
    - stride: convolution stride
    - dilation: stride in atrous convolution

    Return
    padding elements on dimensions in reverse order
    e.g. (left, right, top, bottom, front, back) for 3d tensor
    '''
    dim = len(kernel)
    if isinstance(stride, int):
        stride = dim * [stride]
    if isinstance(dilation, int):
        dilation = dim * [dilation]

    padding = []
    for d in range(dim-1,-1,-1):
        margin = (ceil(in_size[d] / stride[d]) - 1) * stride[d] + kernel[d] + (dilation[d] - 1) \
                             * (kernel[d] - 1) - in_size[d]
        padding.extend([margin//2, margin-margin//2])
    return padding

def cap(key, scope):
    return scope + '/' + key

def doff(key):
    return key.split('/')[-1]

def leftOnExceptHook(exc_type, exc_value, tb, ignored=''):
    '''
    leave particular exception messages out
    '''
    msg = ' Traceback (most recent call last):\n'
    while tb:
        filename = tb.tb_frame.f_code.co_filename
        name = tb.tb_frame.f_code.co_name
        lineno = tb.tb_lineno
        if not ignored or ignored not in filename:
            msg += '   File "%.500s", line %d, in %.500s\n' % (filename, lineno, name)
        tb = tb.tb_next

    msg += ' %s: %s\n' %(exc_type.__name__, exc_value)
    print(msg)


def toDenseLabel(labels, nclasses, on_value=1, off_value=0):
    batch_size = labels.shape[0]
    # initialize dense labels
    dense = off_value * np.ones((batch_size * nclasses), dtype=np.float32)
    indices = []
    if isinstance(labels[0], str):
        for b in range(batch_size):
            indices += [int(s) + b * nclasses for s in labels[b].split(Constant.CHAR_SEP)]
    elif isinstance(labels[0], (list, np.ndarray)): # labels is a nested array
        for b in range(batch_size):
            indices += [l + b * nclasses for l in labels[b]]
        dense[indices] = on_value
    else:
        for b in range(batch_size):
            indices += [int(labels[b]) + b * nclasses]
        dense[indices] = on_value
    return np.reshape(dense, (batch_size, nclasses))


def getAvailabelGPU(ngpus, least_mem):
    p = subp.Popen('nvidia-smi', stdout=subp.PIPE)
    gpu_id = 0  # next gpu we are about to probe
    flag_gpu = False
    id_mem = []  # gpu having avialable memory greater than least requirement
    for l in p.stdout.readlines():
        line = l.decode('utf-8').split()
        if len(line) < 1:
            break
        elif len(line) < 2:
            continue
        if line[1] == str(gpu_id):
            flag_gpu = True
            continue
        if flag_gpu:
            vacancy = int(line[10].split('M')[0]) - int(line[8].split('M')[0])
            if vacancy > least_mem:
                if len(id_mem) < ngpus:
                    id_mem.append((gpu_id, vacancy)) # (id, mem) of gpu
                else:
                    id_mem.sort(key=lambda x: x[1])
                    if vacancy > id_mem[0][1]:
                        id_mem[0] = (gpu_id, vacancy)
            gpu_id += 1
            flag_gpu = False
    return [elem[0] for elem in id_mem]

def parseConfig(config_path):
    with open(config_path, 'r') as config_file:
        return json.load(config_file)

def recordConfig(config_path, config, overwrite=True):
    while not overwrite and os.path.exists(config_path):
        config_path = config_path[:-5]+'_.json'
    with open(config_path, 'w') as config_file:
        json.dump(config, config_file, indent=4)

def _mergeFuel(src_dir, src, dst, dtype, keep_src=True):
    data = {}
    info_keys = []
    shards = len(src)
    print('+' + (23 + 2 * shards + len(dst)) * '-' + '+')
    # read
    ending_char = '\r'
    for i, f in enumerate(src):
        hdf5 = h5py.File(os.path.join(src_dir, f), 'r')
        if i == 0:
            for key in hdf5.keys():
                info_keys.append(key)
            for key in info_keys:
                if key == Constant.FRAME_KEY:
                    data[key] = 0
                else:
                    data[key] = []
        for key in info_keys:
            if key == Constant.FRAME_KEY:
                frames = hdf5[key]
                data[key] = frames if frames>data[key] else data[key]
            else:
                data[key].extend(hdf5[key][()].tolist())
        hdf5.close()
        if not keep_src:
            os.remove(os.path.join(src_dir, f))

        progress = i+1
        yellow_bar = progress * '❖-'
        space_bar = (shards - progress) * '◇-'
        if progress == shards:
            ending_char = '\n'
        print('| Merging data  \033[1;35m%s\033[0m  ⊰⟦-%s%s⟧⊱ |'
              % (dst, yellow_bar, space_bar), end=ending_char)
    # write
    hdf5 = h5py.File(os.path.join(src_dir, dst), 'w')
    for key in info_keys:
        if dtype[key].startswith('v'):  # dealing with encoded / varied data
            dt = h5py.special_dtype(vlen=dtype[key])
            hdf5.create_dataset(key, dtype=dt, data=np.array(data[key]))
        elif key == Constant.FRAME_KEY:
            hdf5[key] = data[key]
        else:
            hdf5[key] = np.array(data[key]).astype(dtype[key])
    hdf5.close()
    print('+' + (23 + 2 * shards + len(dst)) * '-' + '+')

def _fillFuel(src, key, data):
    hdf5 = h5py.File(src, 'a')
    if isinstance(data, (int, float, str)):
        data = [data]
    if isinstance(data, list):
        data = np.array(data)
    if data.dtype.kind == 'U': # convert unicode to string
        nbyte = data.dtype.descr[0][1].split('U')[-1]
        data_copy = data.copy()
        data = np.empty(data_copy.shape, dtype='|S'+nbyte)
        for idx, elm in np.ndenumerate(data_copy):
            data[idx] = elm.encode()
    if data.dtype.kind == 'S':
        sdt = h5py.special_dtype(vlen=str)
        hdf5.create_dataset(key, dtype=sdt, data=data)
    else:
        hdf5[key] = data
    hdf5.close()

def _deductFuel(src, key):
    hdf5 = h5py.File(src, 'a')
    del hdf5[key]
    hdf5.close()

def byte2arr(data_src, as_np=True):
    data_bytes = data_src.tobytes()
    data_pil = Image.open(io.BytesIO(data_bytes))
    if as_np:
        data_np = np.array(data_pil)  # pixels range between [0, 255]
        data_np = (data_np / 255).astype(np.float32)  # pixels range between [0, 1]
        return data_np
    else:
        return data_pil

def curve2str(curve, divisor, span, is_global, x_title='x', y_title='y'):
    assert curve.ndim == 1 and span > 9 # must be a vector
    assert os.get_terminal_size().columns > span + 10 + 5 # ensure that curve is not too long to display

    line_type = {'ascent': '/', 'descent': '\\', 'vertical': '|', 'horizontal': '_'}
    if span < curve.size:
        if is_global:
            indices = [round(i * curve.size / span) for i in range(span)]
            curve = curve[indices]
            indices = [idx+1 for idx in indices]
        else:
            indices = [curve.size - i for i in range(span, 0, -1)]
            curve = curve[-span:]
    else:
        indices = [i for i in range(1, span+1)]
    y_max = curve.max()
    y_min = curve.min()
    delta = (y_max - y_min) / divisor
    if delta == 0.:
        grid = [[10*' ' + ' ┃ ', span * ' ', '\n'] for i in range(1, divisor + 1)]
        grid.append([10 * ' ' + ' ▲ ', span * ' ', '\n'])
    else:
        quant = np.round((curve - y_min) / delta).astype(np.int8)

        grid = [[f'{y_min + i*delta:>10.3f} ┃ ', span * ' ', '\n'] for i in range(1, divisor + 1)]
        grid.append([10 * ' ' + ' ▲︎ ', span * ' ', '\n'])
        # draw the curve
        for i in range(curve.size-1):
            prev = quant[i]
            curr = quant[i + 1]
            if prev > curr:
                grid[prev - 1][1] = grid[prev - 1][1][:i] + line_type['descent'] + grid[prev - 1][1][i + 1:]
                for j in range(1, prev - curr):
                    grid[prev - 1 - j][1] = grid[prev - 1 - j][1][:i] + line_type['vertical'] + grid[prev - 1 - j][1][
                                                                                                i + 1:]
            elif prev < curr:
                grid[prev][1] = grid[prev][1][:i] + line_type['ascent'] + grid[prev][1][i + 1:]
                for j in range(1, curr - prev):
                    grid[prev + j][1] = grid[prev + j][1][:i] + line_type['vertical'] + grid[prev + j][1][i + 1:]
            else:
                grid[prev][1] = grid[prev][1][:i] + line_type['horizontal'] + grid[prev][1][i + 1:]

    # initialize axis
    cstr = ''
    cstr += 10 * ' ' + ' %s\n'%y_title
    for i in range(divisor, -1, -1):
        cstr += ''.join(grid[i])
    cstr += f'{y_min:>10.3f} ┗━' + span * '━' + ' ► %s\n'%x_title
    x_domain = (10+3) * ' '
    for i in range(0, len(indices), 5):
        idx = indices[i]
        if idx<1e3:
                x_domain += f'{idx:<4d} '
        elif idx<1e4:
                x_domain += f'{idx/1e3:<3.1f}K '
        elif idx<1e6:
                x_domain += f'{round(idx/1e3):<3d}K '
        elif idx<1e7:
                x_domain += f'{idx/1e6:<3.1f}M '
        elif idx<1e9:
                x_domain += f'{round(idx/1e6):<3d}M '
    cstr += x_domain+'\n'

    return cstr



def joinImg(imgs, nrow, ncol):
    N, H, W, C = imgs.shape
    assert N == nrow*ncol, 'NEBULAE ERROR ⨷ the number of images does not match cells.'
    assert N > 1, 'NEBULAE ERROR ⨷ one image does not need to be pieced together.'
    margin_h = max(1, H//20)
    margin_w = max(1, W//20)
    canvas = np.zeros((margin_h*(nrow+1) + H*nrow, margin_w*(ncol+1) + W*ncol, C))
    for c in range(ncol):
        for r in range(nrow):
            y = margin_h*(r+1) + H*r
            x = margin_w*(c+1) + W*c
            canvas[y:y+H, x:x+W] = imgs[r*ncol + c]
    return canvas