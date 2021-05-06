#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec 15 12:05:48 2020

@author: jhello
"""

import os
import shutil
import subprocess

from IOFile import IniFile


def clear_output_dir(result_dir, temp_dir):
    if os.path.isdir(result_dir):
        shutil.rmtree(result_dir)
    os.mkdir(result_dir)
    os.chdir(result_dir)
    os.mkdir(temp_dir)
    os.chdir('..')


def create_ini_file(space_mesh_count, output_dir, ini_file_name, time_mesh_count):
    ini_file = IniFile()
    ini_file.set_space_mesh_count(space_mesh_count)
    ini_file.set_time_mesh_count(time_mesh_count)
    ini_file.set_output_dir(output_dir)
    ini_file.write(ini_file_name)


def store_output():
    # Read the output files,
    # compress them and store in one file.
    pass


def main():
    # path of pluto executive file
    pluto_exec = './pluto'
    # path of pluto input file, with init edge condition, mesh count and
    # other config in it
    ini_file_name = 'pluto.ini'
    # path of folder to store pluto output files and our post-process files
    result_dir = 'result'
    # sub-folder in result_dir to store pluto output files
    temp_dir = 'tmp'
    # temp_dir is in result_dir
    output_dir = result_dir + '/' + temp_dir
    # element count meshed on x-axis,
    # physical variables result given at the middle of each element
    space_mesh_count = 800
    # time mesh count, not time step, a result file is output at the mesh point
    time_mesh_count = 40
    # reset problem by remove the output folder
    clear_output_dir(result_dir, temp_dir)
    # create pluto input file of pluto with certain params
    create_ini_file(ini_file_name=ini_file_name,
                    output_dir=output_dir,
                    space_mesh_count=space_mesh_count,
                    time_mesh_count=time_mesh_count)
    # call pluto to compute
    # output = \
    subprocess.check_output([pluto_exec])
    # print(output.decode())


if __name__ == '__main__':
    # story starts here
    main()
