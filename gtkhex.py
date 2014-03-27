#!/usr/bin/env python

###################################################################################
# @file gtkhex.py
# @author Keidan
# @date 27/03/2014
# @par Project
# gtkhex
# @par Copyright
# Copyright 2014 Keidan, all right reserved
# This software is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY.
# 
# Licence summary : 
#    You can modify and redistribute the sources code and binaries.
#    You can send me the bug-fix
# Term of the licence in in the file licence.txt.
#
###################################################################################


import sys, os, inspect

# add module folder
cmd_folder = os.path.realpath(os.path.abspath(
        os.path.split(inspect.getfile(
                inspect.currentframe()))[0]))
if cmd_folder not in sys.path:
    sys.path.insert(0, cmd_folder)
# include modules from a subforder
cmd_subfolder = os.path.realpath(os.path.abspath(
        os.path.join(os.path.split(inspect.getfile(
                    inspect.currentframe()))[0],"modules")))
if cmd_subfolder not in sys.path:
    sys.path.insert(0, cmd_subfolder)

from gtk_win import *


def main(argv):
    win = GWindow()
    win.main()


if __name__ == '__main__':
    main(sys.argv[1:])
