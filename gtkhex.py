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

    def update_statusbar(self, buffer, statusbar):
        print "New event"
	#gchar *msg;
	#gint lines;
	#gint words = 0;
	#GtkTextIter iter;
	#gtk_statusbar_pop(statusbar, 0);
	#bool isPlain = (statusbar == GTK_STATUSBAR(pStatusbarPlain));
	#words = gtk_text_buffer_get_char_count(buffer);
	#gtk_text_buffer_get_end_iter(buffer, &iter);
	#lines = gtk_text_iter_get_line(&iter);
	#if(isPlain) {
	#	msg = g_strdup_printf("Plain area lines : %d, words : %d", lines, words);
	#} else
	#	msg = g_strdup_printf("Hexa area lines : %d, words : %d", lines, words);
	#gtk_statusbar_push(statusbar, 0, msg);
	#g_free(msg);
	#if(isPlain && !lock_by_file) {
	#	gtk_clear_text(bufferHexa);
	#	String text = computeToHexChars(buffer);
        #	if(!text.empty()) {
	#		gtk_append_text(pScrollbarHexa, bufferHexa, text);
	#		text.clear();
	#	} else gtk_clear_text(bufferHexa);
	#}



class gtkhex:
    def __init__(self):
        #Set the Glade file
        handlers = Handler()
        gladefile = os.path.join(current_folder, "gtkhex.glade")
        self.builder = gtk.Builder()
        self.builder.add_from_file(gladefile)
        self.builder.connect_signals(handlers)
        # get objects
	self.window = self.builder.get_object("appwindow")
        sb = self.builder.get_object("sb")
        tv = self.builder.get_object("tv")
        buffer = tv.get_buffer()
        # connect the buffer with the status bar
        buffer.connect("changed", handlers.update_statusbar, sb)
        # Show the window
        self.window.show_all()

    def main(self):
        gtk.gdk.threads_enter()
        gtk.main()
        gtk.gdk.threads_leave()

def main(argv):
    win = gtkhex()
    win.main()


if __name__ == '__main__':
    main(sys.argv[1:])
