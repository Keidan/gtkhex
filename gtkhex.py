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


import sys
try:
    import pygtk
    pygtk.require("2.0")
except:
    pass
try:
    import gtk
    import gtk.glade
except:
    sys.exit(1)

class Handler:
    def on_appwindow_delete_event(self, *args):
        gtk.main_quit(*args)

    def onButtonPressed(self, button):
        print("Hello World!")

class gtkhex:
    def __init__(self):
        #Set the Glade file
        gladefile = os.path.join(current_folder, "gtkhex.glade")
        self.builder = gtk.Builder()
        self.builder.add_from_file(gladefile)
        self.builder.connect_signals(Handler())
        #Get the Main Window, and connect the "destroy" event
	self.window = self.builder.get_object("appwindow")
        self.window.show_all()

    def main(self):
        gtk.main()

def main(argv):
    win = gtkhex()
    win.main()


if __name__ == '__main__':
    main(sys.argv[1:])
