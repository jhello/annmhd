#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec 15 20:47:14 2020

@author: jhello
"""

import configparser

class IniFile:
    def __init__(self):
        self._config = configparser.ConfigParser(delimiters=' ')
        self._config.optionxform=str

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
        tab = tstop/count
        self._config['Static Grid Output']['tab'] = '  '.join([str(tab), '-1'])

    def set_output_dir(self, output_dir):
        self._config['Static Grid Output']['output_dir'] = output_dir


class TabFile:
    def __init__(self):
        pass