#!/usr/bin/env python

###################################################################################
# @file gtk_win.py
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

from gtk_utils import *


class GWindow:
    def __init__(self):
        # create a new window
        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.window.set_title('GtkHex')
        self.window.set_border_width(5)
        self.window.set_size_request(600, 500)
        self.window.set_position(gtk.WIN_POS_CENTER)
        self.window.connect("delete-event", self.quit)
        self.window.add(self.create_textview())
        self.window.show_all()
        
    def quit(self, widget, data):
        gtk.main_quit()

    def main(self):
        # All PyGTK applications must have a gtk.main(). Control ends here
        # and waits for an event to occur (like a key press or mouse event).
        gtk.main()

    def create_textview(self):
        vbox = gtk.VBox()
        scrolledwindow = gtk.ScrolledWindow()
        scrolledwindow.set_border_width(10)
        vbox.add(scrolledwindow)
        
        self.txtView = gtk.TextView()
        self.txtBuffer = self.txtView.get_buffer()
        self.txtView.set_wrap_mode(gtk.WRAP_WORD)
        #self.txtView.set_editable(False)
        self.txtBuffer.set_text("")
        scrolledwindow.add_with_viewport(self.txtView)
        self.tag_found = self.txtBuffer.create_tag("found", background="yellow", weight=700)
        return vbox
