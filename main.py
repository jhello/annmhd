#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec 15 12:05:48 2020

@author: jhello
"""

from IOFile import IniFile, TabFile
import os, shutil, subprocess

def clear_output_dir(result_dir, temp_dir):
    if os.path.isdir(result_dir):
        shutil.rmtree(result_dir)
    os.mkdir(result_dir)
    os.chdir(result_dir)
    os.mkdir(temp_dir)
    os.chdir('..')

def create_ini_file(space_mesh_count, output_dir, ini_file_name):
    ini_file = IniFile()
    ini_file.set_space_mesh_count(space_mesh_count)
    ini_file.set_output_dir(output_dir)
    ini_file.write(ini_file_name)

def store_output():
    # Read the output files,
    # compress them and store in one file.
    pass

def main():
    pluto_exec = './pluto'
    ini_file_name = 'pluto.ini'
    result_dir = 'result'
    temp_dir = 'tmp'
    output_dir = result_dir + '/' + temp_dir
    space_mesh_count = 800
    time_mesh_count = 800 # not used

    clear_output_dir(result_dir, temp_dir)

    create_ini_file(ini_file_name = ini_file_name,
                    output_dir = output_dir,
                    space_mesh_count = space_mesh_count)

    #output = \
    subprocess.check_output([pluto_exec])
    #print(output.decode())

if __name__ == '__main__':
    main()