#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec 17 10:19:16 2020

@author: jhello
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter
import tensorflow as tf

tab_out_file_name = 'result/tmp/tab.out'
tab_file_name3 = 'result/tmp/data.0003.tab'
tab_file_name4 = 'result/tmp/data.0004.tab'
hdf_file_name = 'result/tmp/sample1.h5'
df_names = 'x y rho vx1 vx2 vx3 Bx1 Bx2 Bx3 prs'.split()

time_steps = pd.read_table(tab_out_file_name, delim_whitespace=True, usecols=[1], header=None)
time_count = time_steps.shape[0]
space_count = 0

df_list = []
for time_index, time_step in enumerate(time_steps[1]):
    tab_file_name = 'result/tmp/data.{:04d}.tab'.format(time_index)
    df = pd.read_table(tab_file_name, delim_whitespace=True, names=df_names)
    space_count = df.shape[0]
    df['y'] = time_step
    df_list += [df]

dfs = pd.concat(df_list, ignore_index=True)

#print(dfs)

dfs.to_hdf(hdf_file_name, 'sample1')

def plot_var_2D(var_name):
    x = dfs['x'].values.reshape([time_count, space_count])
    y = dfs['y'].values.reshape([time_count, space_count])
    z = dfs[var_name].values.reshape([time_count, space_count])
    fig = plt.figure()
    ax = fig.gca(projection='3d')
    # Note: Constant value cause warning when plot contourf.
    #ax.contourf(x, y, z, zdir='z', offset=-1, cmap=cm.coolwarm)
    #ax.contourf(x, y, z, zdir='y', offset=0.5, cmap=cm.coolwarm)
    surf = ax.plot_surface(x, y, z, cmap=cm.coolwarm, rstride=1, cstride=1, alpha=0.8)
    ax.set_xlabel('x')
    ax.set_ylabel('t')
    ax.set_zlabel(var_name)
    ax.set_ylim(0, 0.5)
    ax.set_zlim(-1, 1)
    fig.colorbar(surf, shrink=0.5, aspect=5)

    plt.show()

#plot_var_2D('rho')
#plot_var_2D('prs')
#plot_var_2D('vx1')
#plot_var_2D('vx2')
#plot_var_2D('vx3')
#plot_var_2D('Bx1')
#plot_var_2D('Bx2')
#plot_var_2D('Bx3')

sample_tensor = tf.constant([dfs[var_name].values.reshape([time_count, space_count])
                           for var_name in df_names[2:]],
                          dtype=tf.float32)
#print(sample_tensor)
s, u, v = tf.linalg.svd(sample_tensor)
print('s', s)
print('u', u)
print('v', v)
print('s.shape', s.shape)
print('u.shape', u.shape)
print('v.shape', v.shape)

def plot_s(var_index):
    plt.plot(s[var_index])

plot_s(0)
plot_s(1)
plot_s(2)



