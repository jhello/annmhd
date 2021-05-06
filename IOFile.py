#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec 15 20:47:14 2020

@author: jhello
"""
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter
import matplotlib.pyplot as plt
from sortedcontainers import SortedSet
import configparser
import linecache
import pandas as pd


def plot_solution(dfs, time_count, space_count, var_name):
    """
    Plot 3D for specified variable.
    :param dfs:
    :param time_count:
    :param space_count:
    :param var_name:
    :return:
    """
    x = dfs['x'].values.reshape([time_count, space_count])
    y = dfs['t'].values.reshape([time_count, space_count])
    z = dfs[var_name].values.reshape([time_count, space_count])
    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')
    # Note: Constant value cause warning when plot contourf.
    ax.contourf(x, y, z, zdir='z', offset=-1, cmap=cm.coolwarm)
    ax.contourf(x, y, z, zdir='y', offset=0.5, cmap=cm.coolwarm)
    surf = ax.plot_surface(x, y, z, cmap=cm.coolwarm, rstride=1, cstride=1, alpha=0.8)
    ax.set_xlabel('x')
    ax.set_ylabel('t')
    ax.set_zlabel(var_name)
    ax.set_ylim(0, 0.5)
    ax.set_zlim(-1, 1)
    fig.colorbar(surf, shrink=0.5, aspect=5, ax=ax)

    plt.show()


class IniFile:
    def __init__(self):
        self._config = configparser.ConfigParser(delimiters=' ')
        self._config.optionxform = str

        self._config['Grid'] = {}
        self._config['Chombo Refinement'] = {}
        self._config['Time'] = {}
        self._config['Solver'] = {}
        self._config['Boundary'] = {}
        self._config['Static Grid Output'] = {}
        self._config['Chombo HDF5 output'] = {}
        self._config['Parameters'] = {}

        self._config['Grid'][''] = ''
        self._config['Grid']['X1-grid'] = '1    0.0    400    u    1.0'
        self._config['Grid']['X2-grid'] = '1    0.0    1    u    1.0'
        self._config['Grid']['X3-grid'] = '1    0.0    1    u    1.0'

        self._config['Chombo Refinement'][''] = ''
        self._config['Chombo Refinement']['Levels'] = '4'
        self._config['Chombo Refinement']['Ref_ratio'] = '2 2 2 2 2'
        self._config['Chombo Refinement']['Regrid_interval'] = '2 2 2 2'
        self._config['Chombo Refinement']['Refine_thresh'] = '0.3'
        self._config['Chombo Refinement']['Tag_buffer_size'] = '3'
        self._config['Chombo Refinement']['Block_factor'] = '4'
        self._config['Chombo Refinement']['Max_grid_size'] = '32'
        self._config['Chombo Refinement']['Fill_ratio'] = '0.75'

        self._config['Time'][''] = ''
        self._config['Time']['CFL'] = '0.8'
        self._config['Time']['CFL_max_var'] = '1.1'
        self._config['Time']['tstop'] = '0.3'
        self._config['Time']['first_dt'] = '1.e-6'

        self._config['Solver'][''] = ''
        self._config['Solver']['Solver'] = 'hllc'

        self._config['Boundary'][''] = ''
        self._config['Boundary']['X1-beg'] = 'outflow'
        self._config['Boundary']['X1-end'] = 'outflow'
        self._config['Boundary']['X2-beg'] = 'outflow'
        self._config['Boundary']['X2-end'] = 'outflow'
        self._config['Boundary']['X3-beg'] = 'outflow'
        self._config['Boundary']['X3-end'] = 'outflow'

        self._config['Static Grid Output'][''] = ''
        self._config['Static Grid Output']['uservar'] = '0'
        self._config['Static Grid Output']['output_dir'] = 'output_dir'
        self._config['Static Grid Output']['dbl'] = '-1.0  -1   single_file'
        self._config['Static Grid Output']['flt'] = '-1.0  -1   single_file'
        self._config['Static Grid Output']['vtk'] = '-1.0  -1   single_file'
        self._config['Static Grid Output']['tab'] = '0.01  -1'
        self._config['Static Grid Output']['ppm'] = '-1.0  -1'
        self._config['Static Grid Output']['png'] = '-1.0  -1'
        self._config['Static Grid Output']['log'] = '100'
        self._config['Static Grid Output']['analysis'] = '-1.0  -1'

        self._config['Chombo HDF5 output'][''] = ''
        self._config['Chombo HDF5 output']['Checkpoint_interval'] = '-1.0  0'
        self._config['Chombo HDF5 output']['Plot_interval'] = '1.0  0'

        self._config['Parameters'][''] = ''
        self._config['Parameters']['RHO_LEFT'] = '1.0'
        self._config['Parameters']['VX_LEFT'] = '0.0'
        self._config['Parameters']['VY_LEFT'] = '0.0'
        self._config['Parameters']['VZ_LEFT'] = '0.0'
        self._config['Parameters']['BY_LEFT'] = '1.0'
        self._config['Parameters']['BZ_LEFT'] = '0.0'
        self._config['Parameters']['PR_LEFT'] = '1.0'
        self._config['Parameters']['RHO_RIGHT'] = '0.125'
        self._config['Parameters']['VX_RIGHT'] = '0.0'
        self._config['Parameters']['VY_RIGHT'] = '0.0'
        self._config['Parameters']['VZ_RIGHT'] = '0.0'
        self._config['Parameters']['BY_RIGHT'] = '-1.0'
        self._config['Parameters']['BZ_RIGHT'] = '0.0'
        self._config['Parameters']['PR_RIGHT'] = '0.1'
        self._config['Parameters']['BX_CONST'] = '0.75'
        self._config['Parameters']['GAMMA_EOS'] = '2.0'
        self._config['Parameters']['DIVIDE_BY_4PI'] = '0.0'

    def write(self, filename):
        self._name = filename
        with open(self._name, 'w') as configfile:
            self._config.write(configfile)

    def set_space_mesh_count(self, count):
        value_string = '1    0.0    ' + str(count) + '    u    1.0'
        self._config['Grid']['X1-grid'] = value_string

    def set_time_mesh_count(self, count):
        tstop = float(self._config['Time']['tstop'])
        tab = tstop / count
        self._config['Static Grid Output']['tab'] = '  '.join([str(tab), '-1'])

    def set_output_dir(self, output_dir):
        self._config['Static Grid Output']['output_dir'] = output_dir


class DataTabFile:
    def __init__(self, name):
        self._name = name

    def dataframe(self):
        # dataframe headers
        df_names = 'x t rho vx1 vx2 vx3 Bx1 Bx2 Bx3 prs'.split()
        return pd.read_table(self._name, delim_whitespace=True, names=df_names)


class DataTabFiles:
    def __init__(self, result_tmp_dir, time_steps):
        self._result_tmp_dir = result_tmp_dir
        self._time_steps = time_steps
        self._solution = pd.DataFrame()

    def solution(self):
        df_list = []
        for time_index, time_step in enumerate(self._time_steps):
            tab_file_name = self._result_tmp_dir + 'data.{:04d}.tab'.format(time_index)
            df = DataTabFile(tab_file_name).dataframe()
            # assign time step to 'y' column
            df['t'] = time_step
            df_list += [df]

        # concatenate all dataframes to a long big one
        self._solution = pd.concat(df_list, ignore_index=True)
        return self._solution

    def a_style_dataframe(self):
        """
        Returns solution dataframe as
                                t_1 t_2 ... t_n
        node_1 para_1
               para_2
               para_3
               ...
               para_x

        node_2 para_1
               para_2
               para_3
               ...
               para_x

        ...

        node_m para_1
               para_2
               para_3
               ...
               para_x

        :return:
        """
        para_names = 'rho vx1 vx2 vx3 Bx1 Bx2 Bx3 prs'.split()
        if self._solution.empty:
            self._solution = self.solution()
        time_steps = list(SortedSet(self._solution['t']))
        space_steps = list(SortedSet(self._solution['x']))

        a_style_dfs = []
        for space_step in space_steps:
            src_df = self._solution.loc[self._solution['x'] == space_step]
            new_index_df = src_df.set_index('t')
            transposed_df = new_index_df.transpose()
            tgt = transposed_df.loc[transposed_df.index.isin(para_names)]
            tgt_without_all_0_rows = tgt.loc[(tgt.T != 0).any()]
            a_style_dfs += [tgt_without_all_0_rows]

        return pd.concat(a_style_dfs)

    def b_style_dataframe(self):
        pass


class TabOutFile:
    """The tab.out file.
    """

    def __init__(self, name):
        self._name = name

    def time_steps(self):
        # read time step from 'tab.out' file
        return pd.read_table(self._name, delim_whitespace=True, usecols=[1], header=None)[1]


class GridOutFile:
    """The grid.out file.
    """

    def __init__(self, name):
        self._name = name

    def space_count(self):
        # read space step count from 'grid.out' file (No. 9 line)
        return int(linecache.getline(self._name, 9))
