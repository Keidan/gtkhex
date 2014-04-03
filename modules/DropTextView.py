###################################################################################
# @file DropTextView.py
# @author Keidan
# @date 01/04/2014
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

from UndoRedoBuffer import *

class DropTextView(gtk.TextView):
    __gsignals__ = {
        "drop-file": (gobject.SIGNAL_RUN_FIRST, None, (gobject.TYPE_PYOBJECT,)),
    }
    def __init__(self, statusbar):
        gtk.TextView.__init__(self)
        buffer = UndoRedoBuffer(self.iter_on_screen, statusbar)
        self.set_buffer(buffer)
        self.grab_focus()
        self.modify_font(pango.FontDescription(CONST.DEFAULT_FONT))
        self.connect_drop(self)

    def connect_drop(self, widget):
        widget.drag_dest_set(gtk.DEST_DEFAULT_ALL, 
                           [('text/uri-list', 0, 0)], gtk.gdk.ACTION_COPY)
        widget.connect('drag-data-received', self.on_drop_data)
        widget.connect('drag_motion', self.motion_cb)
        widget.connect('drag_drop', self.drop_cb)
   
    def motion_cb(self, wid, context, x, y, time):
        context.drag_status(gtk.gdk.ACTION_COPY, time)
        return True
   
    def drop_cb(self, wid, context, x, y, time):
        context.finish(True, False, time)
        return True

    def on_drop_data(self, widget, drag_context, x, y, selection_data, info, timestamp):
        for uri in selection_data.get_uris():
            p = urlparse.urlparse(uri).path
            self.emit("drop-file", p)

    def iter_on_screen(self, iter, mark_str):
        buffer = self.get_buffer()
        buffer.place_cursor(iter) 
        self.scroll_mark_onscreen(buffer.get_mark(mark_str))
