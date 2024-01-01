###################################################################################
# @file drop_text_view.py
# @author Keidan (Kevin Billonneau)
# @par Copyright GNU GENERAL PUBLIC LICENSE Version 3
###################################################################################

import urllib
from undo_redo_buffer import *
from gi.repository import Gtk
from gi.repository import Gdk
from gi.repository import GObject
from gi.repository import Pango
from consts import CONST


class DropTextView(Gtk.TextView):
    __gsignals__ = {
        'drop-file': (GObject.SIGNAL_RUN_FIRST, None, (GObject.TYPE_PYOBJECT,)),
    }

    def __init__(self, statusbar):
        Gtk.TextView.__init__(self)
        buffer = UndoRedoBuffer(self.iter_on_screen, statusbar)
        self.set_buffer(buffer)
        self.grab_focus()
        self.modify_font(Pango.FontDescription(CONST.default_font()))
        self.connect_drop(self)

    def connect_drop(self, widget):
        widget.drag_dest_set(
            Gtk.DestDefaults.ALL, [Gtk.TargetEntry('text/uri-list', 0, 0)], Gdk.DragAction.COPY
        )
        widget.connect('drag-data-received', self.on_drop_data)
        widget.connect('drag_motion', self.motion_cb)
        widget.connect('drag_drop', self.drop_cb)

    def motion_cb(self, wid, context, x, y, time) -> bool:
        context.drag_status(Gdk.DragAction.COPY, time)
        return True

    def drop_cb(self, wid, context, x, y, time) -> bool:
        context.finish(True, False, time)
        return True

    def on_drop_data(self, widget, drag_context, x, y, selection_data, info, timestamp):
        for uri in selection_data.get_uris():
            p = urllib.urlparse(uri).path
            self.emit('drop-file', p)

    def iter_on_screen(self, iter, mark_str):
        buffer = self.get_buffer()
        buffer.place_cursor(iter)
        self.scroll_mark_onscreen(buffer.get_mark(mark_str))
