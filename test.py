#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec 17 10:19:16 2020

@author: jhello
"""

import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf

from IOFile import TabOutFile, GridOutFile, DataTabFiles

# time step file
result_dir = 'result/'
result_tmp_dir = result_dir + 'tmp/'
tab_out_file_name = result_tmp_dir + 'tab.out'
grid_out_file_name = result_tmp_dir + 'grid.out'
# dataframe headers
df_names = 'x t rho vx1 vx2 vx3 Bx1 Bx2 Bx3 prs'.split()

# read time step from 'tab.out' file
time_steps = TabOutFile(tab_out_file_name).time_steps()
# time step count
time_count = len(time_steps)
# init space count to 0
space_count = GridOutFile(grid_out_file_name).space_count()

data_tab_files = DataTabFiles(result_tmp_dir, time_steps)
dfs = data_tab_files.solution()

a_style_dataframe = data_tab_files.a_style_dataframe()
print('a_style_dataframe')
print(a_style_dataframe)
s, u, v = tf.linalg.svd(a_style_dataframe)

us, uu, uv = tf.linalg.svd(u)

last_time_point_sol = a_style_dataframe.iloc[:, -1]
coord = last_time_point_sol.dot(uu)
print('coord')
print(coord)

error = []
for i in range(1, len(coord) + 1):
    last_time_point_predict = np.dot(uu[:, :i], coord[:i])

    last_time_point_sol_ndarray = last_time_point_sol.values
    error += [sum(abs(last_time_point_predict - last_time_point_sol_ndarray) / last_time_point_sol_ndarray)]
    rho_predict = last_time_point_predict[::6]
    rho_sol = last_time_point_sol_ndarray[::6]

    fig, ax = plt.subplots()
    ax.set_title('Coord Count = ' + str(i))
    ax.plot(rho_predict, '.-')
    ax.plot(rho_sol)
    plt.savefig('imgs/'+'Coord Count = ' + str(i))
    plt.close()

fig, ax_err = plt.subplots()
ax_err.plot(error, '.-')
ax_err.grid(True)
plt.savefig('imgs/'+'error')
plt.close()
