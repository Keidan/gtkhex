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

# get the current folder
current_folder = os.path.realpath(os.path.abspath(
        os.path.split(inspect.getfile(
                inspect.currentframe()))[0]))
if current_folder not in sys.path:
    sys.path.insert(0, current_folder)
# include modules from a subforder
cmd_subfolder = os.path.join(current_folder, "modules")
if cmd_subfolder not in sys.path:
    sys.path.insert(0, cmd_subfolder)

from Handlers import *

class gtkhex:
    def __init__(self):
        #Set the Glade file
        gladefile = os.path.join(current_folder, "gtkhex.glade")
        builder = gtk.Builder()
        builder.add_from_file(gladefile)
        # get objects
	window = builder.get_object(CONST.WINDOW_NAME)
        sb = builder.get_object(CONST.STATUSBAR_NAME)
        nb = builder.get_object(CONST.NOTEBOOK_NAME)
        # init
        sb.push(CONST.STATUSBAR_TEXT_IDX, "Ln 1, Col: 1, 100%")
        # connect handlers
        self.handlers = Handlers(builder)
        window.add_accel_group(self.handlers.get_AccelGroup())
        builder.connect_signals(self.handlers)

        # Show the window
        window.set_title(window.get_title())
        window.show_all()

    def loadFile(self, filename):
        self.handlers.open_file(filename)

    def main(self):
        gtk.gdk.threads_enter()
        gtk.main()
        gtk.gdk.threads_leave()

def main(argv):
    win = gtkhex()
    if len(sys.argv) == 2: win.loadFile(argv[0])
    win.main()


if __name__ == '__main__':
    main(sys.argv[1:])
