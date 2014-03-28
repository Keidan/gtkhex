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

#Define constats utils
def constant(f):
    def fset(self, value): raise SyntaxError
    def fget(self): return f()
    return property(fget, fset)

class _Const(object):
    @constant
    def STATUSBAR_TEXT_IDX(): return 0

CONST = _Const()


class Handler:
    def __init__(self, window):
        self.window = window
        self.defaultWindowTitle = self.window.get_title()


    def on_appwindow_delete_event(self, *args):
        gtk.main_quit(*args)

    def on_cursor_position_changed(self, buffer, param, sb):
        idx = CONST.STATUSBAR_TEXT_IDX
        # clear the statusbar
        sb.pop(idx)
        # get the words number
        words = buffer.get_char_count()
        if not words: words = 1
        # get the current position
        word = buffer.props.cursor_position
        # get the current iter
        iter = buffer.get_iter_at_mark(buffer.get_insert())
        # get the current line
        line = iter.get_line()
        # get the cursor position into the current line
        col = buffer.get_iter_at_line_offset(line, 0)
        sb.push(idx, "Ln {0}, Col: {1}, {2}%".format(line + 1, iter.get_line_offset(), word * 100 / words))
        # update the title
        if buffer.get_modified():
            self.window.set_title(self.defaultWindowTitle + "*")
        else: self.window.set_title(self.defaultWindowTitle)
        self.window.queue_draw()

class gtkhex:
    def __init__(self):
        #Set the Glade file
        gladefile = os.path.join(current_folder, "gtkhex.glade")
        self.builder = gtk.Builder()
        self.builder.add_from_file(gladefile)
        # get objects
	self.window = self.builder.get_object("appwindow")
        sb = self.builder.get_object("sb")
        tv = self.builder.get_object("tv")
        buffer = tv.get_buffer()
        # connect handlers
        handlers = Handler(self.window)
        self.builder.connect_signals(handlers)
        # init
        tv.grab_focus()
        sb.push(0, "Ln 1, Col: 1, 100%")
        # connect the buffer with the status bar
        buffer.connect("notify::cursor-position", handlers.on_cursor_position_changed, sb)
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
