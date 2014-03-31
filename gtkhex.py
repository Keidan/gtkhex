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


import sys, os, inspect, string, urlparse
from Queue import *

# get the current folder
current_folder = os.path.realpath(os.path.abspath(
        os.path.split(inspect.getfile(
                inspect.currentframe()))[0]))
if current_folder not in sys.path:
    sys.path.insert(0, current_folder)

try:
    import pygtk
    pygtk.require("2.0")
except:
    pass
try:
    import gtk
    import gtk.glade
    import pango
except:
    sys.exit(1)

#Define constats utils
def constant(f):
    def fset(self, value): raise SyntaxError
    def fget(self): return f()
    return property(fget, fset)

class _Const(object):
    @constant
    def MAX_REDO(): return 255
    @constant
    def MAX_UNDO(): return 255
    @constant
    def STATUSBAR_FILE_IDX(): return 0
    @constant
    def STATUSBAR_TEXT_IDX(): return 1
    @constant
    def MAX_CHAR_BY_SEGMENT(): return 8
    @constant
    def MAX_CHAR_BY_LINE(): return 32
    @constant
    def DEFAULT_FONT(): return "Courier 10"
    @constant
    def IMINEW_NAME(): return "imiNew"
    @constant
    def IMIOPEN_NAME(): return "imiOpen"
    @constant
    def IMISAVE_NAME(): return "imiSave"
    @constant
    def IMIQUIT_NAME(): return "imiQuit"
    @constant
    def IMIUNDO_NAME(): return "imiUndo"
    @constant
    def IMIREDO_NAME(): return "imiRedo"
    @constant
    def IMICUT_NAME(): return "imiCut"
    @constant
    def IMICOPY_NAME(): return "imiCopy"
    @constant
    def IMIPASTE_NAME(): return "imiPaste"
    @constant
    def IMISELECTALL_NAME(): return "imiSelectAll"
    @constant
    def IMIFIND_NAME(): return "imiFind"
    @constant
    def IMIREPLACE_NAME(): return "imiReplace"
    @constant
    def TBUNDO_NAME(): return "tbUndo"
    @constant
    def TBREDO_NAME(): return "tbRedo"
    @constant
    def WINDOW_NAME(): return "appwindow"
    @constant
    def STATUSBAR_NAME(): return "sb"
    @constant
    def TEXTVIEW_NAME(): return "tv"
    @constant
    def ABOUTDIALOG_NAME(): return "about_dialog"
    @constant
    def FINDDIALOG_NAME(): return "find_dialog"
    @constant
    def FINDENTRY_NAME(): return "find_entry"
    @constant
    def REPLACEDIALOG_NAME(): return "replace_dialog"
    @constant
    def REPLACEENTRY_NAME(): return "replace_entry"
    @constant
    def REPLACEFINDENTRY_NAME(): return "replace_find_entry"

CONST = _Const()

# simple confirm box in pygtk
def gtk_confirm_box(text):
    md = gtk.MessageDialog(None,
                           gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT, 
                           gtk.MESSAGE_QUESTION, 
                           gtk.BUTTONS_YES_NO, None)
    md.set_markup(text)
    response = md.run()
    result = False
    if response == gtk.RESPONSE_YES:
        result = True
    md.destroy()
    return result 
# simple file chooser box in pygtk
def gtk_file_chooser(title, action):
    chooser = gtk.FileChooserDialog(
        title=title,
        action=action, 
        buttons=(gtk.STOCK_CANCEL,gtk.RESPONSE_CANCEL,
                 gtk.STOCK_OPEN,gtk.RESPONSE_OK))
    chooser.set_default_response(gtk.RESPONSE_OK)
    filter = gtk.FileFilter()
    filter.set_name("All Files")
    filter.add_pattern("*.*")
    chooser.add_filter(filter)
    response = chooser.run()
    if response == gtk.RESPONSE_OK:
        currentFile = chooser.get_filename()
        chooser.destroy()
        return True, currentFile
    chooser.destroy()
    return False, None

# translate text data to hex representation
def data_to_hex(content):
    li = list(content)
    result = ""
    i = 0
    length = len(li)
    for l in li:
        result += "{0:02x} ".format(ord(l))
        if i == CONST.MAX_CHAR_BY_LINE - 1:
            i = 0
            result += "\n"
        else: i += 1
        if not i % CONST.MAX_CHAR_BY_SEGMENT and not i == 0: result += " "
    del li[:]  
    return result.strip()
def is_hex(s):
     hex_digits = set(string.hexdigits)
     # if s is long, then it is faster to check against a set
     return all(c in hex_digits for c in s)
# translate text hex to data representation
def hex_to_data(content):
    li = content.split(" ")
    result = ""
    for l in li:
        if l == ' ': continue
        if not is_hex(l): return None
        result += l.decode('hex')
    return result

class Handler:
    def __init__(self, builder, tag_found):
        self.builder = builder
        self.win = builder.get_object(CONST.WINDOW_NAME)
        self.sb = builder.get_object(CONST.STATUSBAR_NAME)
        self.tv = builder.get_object(CONST.TEXTVIEW_NAME)
        self.dabout = builder.get_object(CONST.ABOUTDIALOG_NAME)
        self.dfind = builder.get_object(CONST.FINDDIALOG_NAME)
        self.dreplace = builder.get_object(CONST.REPLACEDIALOG_NAME)
        self.efind = builder.get_object(CONST.FINDENTRY_NAME)
        self.ereplace = builder.get_object(CONST.REPLACEENTRY_NAME)
        self.ereplacefine = builder.get_object(CONST.REPLACEFINDENTRY_NAME)
        self.defaultWindowTitle = self.win.get_title()
        self.tag_found = tag_found
        self.currentFile = None
        self.changed = False
        self.undopool = LifoQueue(CONST.MAX_UNDO)
        self.redopool = LifoQueue(CONST.MAX_REDO)
        self.user_action = False

    def on_quit(self, button):
        self.on_appwindow_delete_event(None)

    def on_appwindow_delete_event(self, *args):
        if self.changed:
            text = "Do you really want to leave this program without save ?"
            if gtk_confirm_box(text):
                gtk.main_quit()
                return False
            return True
        else:
            gtk.main_quit()
            return False

    def on_drop(self, widget, drag_context, x, y, selection_data, info, timestamp, user_param1):
        p = urlparse.urlparse(selection_data.get_uris()[0]).path
        self.open_file(p)

    def on_new(self, button):
        if self.currentFile != None and self.changed:
            if not gtk_confirm_box("Do you want to create a new file without saving your changes?"):
                return
        self.sb.pop(CONST.STATUSBAR_FILE_IDX)
        self.currentFile = None
        self.win.set_title("Untitled - " + self.defaultWindowTitle)
        self.tv.get_buffer().set_text("")
        self.changed = False

    def on_open(self, button):
        response, cfile =  gtk_file_chooser("Open a file", gtk.FILE_CHOOSER_ACTION_OPEN)
        self.sb.pop(CONST.STATUSBAR_FILE_IDX)
        if response:
            self.open_file(cfile)

    def open_file(self, cfile):
        self.currentFile = cfile
        filename = self.currentFile
        self.sb.push(CONST.STATUSBAR_FILE_IDX, "Opened File: " + filename)
        file = open(filename, "r")
        self.tv.get_buffer().set_text(data_to_hex(file.read()))
        file.close()
        self.changed = False

    def write_file(self, data):
        filename = self.currentFile
        self.changed = False
        self.sb.pop(CONST.STATUSBAR_FILE_IDX)
        self.sb.push(CONST.STATUSBAR_FILE_IDX, "Saved File: " + filename)
        index = filename.replace("\\","/").rfind("/") + 1
        title = filename[index:] + " - " + self.defaultWindowTitle
        self.win.set_title(title)
        self.win.queue_draw()
        file = open(filename, "w+")
        file.write(data)
        file.close()

    def test_data_buffer(self):
        buffer = self.tv.get_buffer()
        text = buffer.get_text(buffer.get_start_iter() , buffer.get_end_iter())
        data = hex_to_data(text)
        if data == None:
            d = gtk.MessageDialog(self.win,
                                  gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT, 
                                  gtk.MESSAGE_ERROR, 
                                  gtk.BUTTONS_OK, None)
            d.set_markup("The text entry contain one or more invalid characters.")
            d.run()
            d.destroy()
            return None
        return data


    def on_save(self, button):
        data = self.test_data_buffer()
        if data == None: return
        if self.currentFile == None: self.on_save_as(button)
        else: self.write_file(data)

    def on_save_as(self, button):
        data = self.test_data_buffer()
        if data == None: return
        response, cfile = gtk_file_chooser("Save file", gtk.FILE_CHOOSER_ACTION_SAVE)
        if response:
            self.currentFile = cfile
            # generic call
            self.write_file(data)

    def on_cut(self, button):
        buff = self.tv.get_buffer()
        buff.cut_clipboard(gtk.clipboard_get(), True)

    def on_copy(self, button):
        buff = self.tv.get_buffer()
        buff.copy_clipboard (gtk.clipboard_get())

    def on_paste(self, button):
        buff = self.tv.get_buffer()
        buff.paste_clipboard (gtk.clipboard_get(), None, True)

    def on_delete(self, button):
        buff = self.tv.get_buffer()
        buff.delete_selection(False, True)

    def on_select_all(self, button):
        buff = self.tv.get_buffer()
        match_start = buff.get_start_iter() 
        match_end = buff.get_end_iter() 
        buff.select_range(match_start, match_end)

    # undo/redo 
    def undo_redo_state(self):
        if not self.undopool.qsize():
            self.set_sensitive(CONST.IMIUNDO_NAME, False)
            self.set_sensitive(CONST.TBUNDO_NAME, False)
        else:
            self.set_sensitive(CONST.IMIUNDO_NAME, True)
            self.set_sensitive(CONST.TBUNDO_NAME, True)
        if not self.redopool.qsize():
            self.set_sensitive(CONST.IMIREDO_NAME, False)
            self.set_sensitive(CONST.TBREDO_NAME, False)
        else:
            self.set_sensitive(CONST.IMIREDO_NAME, True)
            self.set_sensitive(CONST.TBREDO_NAME, True)

    def buffer_insert_text(self, buffer, iter, text, length):
        if self.user_action:
            self.undopool.put(["insert_text", iter.get_offset(), iter.get_offset() + len(text), text])
            with self.redopool.mutex:
                self.redopool.queue[:] = []

    def buffer_delete_range(self, buffer, start_iter, end_iter):
        if self.user_action:
            text = buffer.get_text(start_iter, end_iter)
            self.undopool.put(["delete_range", start_iter.get_offset(), end_iter.get_offset(), text])

    def buffer_begin_user_action(self, buffer):
        self.user_action = True

    def buffer_end_user_action(self, buffer):
        self.user_action = False

    def on_undo(self, button):
        buffer = self.tv.get_buffer()
        if not self.undopool.qsize(): return
        action = self.undopool.get()
        if action[0] == "insert_text":
            start_iter = buffer.get_iter_at_offset(action[1])
            end_iter = buffer.get_iter_at_offset(action[2])
            buffer.delete(start_iter, end_iter)
        elif action[0] == "delete_range":
            start_iter = buffer.get_iter_at_offset(action[1])
            buffer.insert(start_iter, action[3])
        self.iter_on_screen(start_iter, "insert")
        self.redopool.put(action)
        self.undo_redo_state()

    def on_redo(self, button):
        buffer = self.tv.get_buffer()
        if not self.redopool.qsize(): return
        action = self.redopool.get() 
        if action[0] == "insert_text":
            start_iter = buffer.get_iter_at_offset(action[1])
            end_iter = buffer.get_iter_at_offset(action[2])
            buffer.insert(start_iter, action[3])
        elif action[0] == "delete_range":
            start_iter = buffer.get_iter_at_offset(action[1])
            end_iter = buffer.get_iter_at_offset(action[2])
            buffer.delete(start_iter, end_iter)
        self.iter_on_screen(start_iter, "insert")
        self.undopool.put(action)
        self.undo_redo_state()


    def on_about(self, button):
        self.dabout.run()
        self.dabout.destroy()

    # Find dialog
    def on_find_quit(self, button):
        self.dfind.hide()
    def on_search(self, button):
        self.dfind.show()
    def on_find_execute(self, button):
        self.on_search_clear(None)
        self.find_and_select(self.efind, True, self.dfind)

    def on_search_clear(self, button):
        buffer = self.tv.get_buffer()
        start = buffer.get_start_iter()
        end = buffer.get_end_iter()
        buffer.remove_all_tags(start, end)

    def find_and_select(self, find, tags, parent):
        text = find.get_text()
        buffer = self.tv.get_buffer()
        cursor_mark = buffer.get_insert()
        start = buffer.get_iter_at_mark(cursor_mark)
        if start.get_offset() == buffer.get_char_count():
            start = buffer.get_start_iter()
        search_flags = gtk.TEXT_SEARCH_TEXT_ONLY
        match_iters = start.forward_search(text, search_flags)

        if match_iters != None:
            next_iter = [match_iters[1], match_iters[0]]
            self.iter_on_screen(next_iter[0], "insert")
            buffer.move_mark(buffer.get_mark("selection_bound"), next_iter[1])
            if tags: buffer.apply_tag(self.tag_found, next_iter[0], next_iter[1])
            return True
        else:
            d = gtk.MessageDialog(parent,
                           gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT, 
                           gtk.MESSAGE_INFO, 
                           gtk.BUTTONS_OK, None)
            d.set_markup("The string " + text + " has not been found.")
            d.run()
            d.destroy()
            return False

    #Replace dialog
    def on_replace(self, widget):
        self.dreplace.show()
    def on_replace_quit(self, widget):
        self.dreplace.hide()
    def on_replace_execute(self, widget):
        self.on_search_clear(None)
        buffer = self.tv.get_buffer()
        if self.find_and_select(self.ereplacefine, False, self.dreplace):
            iter = buffer.get_iter_at_mark(buffer.get_mark("insert"))
            sel_bound = buffer.get_iter_at_mark(buffer.get_mark("selection_bound"))
            if not iter == sel_bound:
                self.replace_selected_text(self.ereplace.get_text(), iter, sel_bound)

    def replace_selected_text(self, str, start_iter, end_iter):
        buffer = self.tv.get_buffer()
        buffer.begin_user_action
        buffer.delete(start_iter, end_iter)
        buffer.insert(start_iter, str)
        buffer.end_user_action
        self.iter_on_screen(start_iter, "insert")

    def iter_on_screen(self, iter, mark_str):
        buffer = self.tv.get_buffer()
        buffer.place_cursor(iter) 
        self.tv.scroll_mark_onscreen(buffer.get_mark(mark_str))

    def set_sensitive(self, name, state):
        widget = self.builder.get_object(name)
        if not widget.get_sensitive() == state:
            widget.set_sensitive(state)
    

    def on_cursor_position_changed(self, buffer, param, sb):
        self.undo_redo_state()
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
        if self.currentFile == None:
            title = "Untitled - " + self.defaultWindowTitle
        else:
            index = self.currentFile.replace("\\","/").rfind("/") + 1
            title = self.currentFile[index:] + " - " + self.defaultWindowTitle
        if self.changed: self.win.set_title(title + " *")
        else: self.win.set_title(title)
        self.changed = True
        self.win.queue_draw()

class gtkhex:
    def __init__(self):
        #Set the Glade file
        gladefile = os.path.join(current_folder, "gtkhex.glade")
        builder = gtk.Builder()
        builder.add_from_file(gladefile)
        # get objects
	window = builder.get_object(CONST.WINDOW_NAME)
        sb = builder.get_object(CONST.STATUSBAR_NAME)
        tv = builder.get_object(CONST.TEXTVIEW_NAME)
        buffer = tv.get_buffer()
        # init
        agr = gtk.AccelGroup()
        window.add_accel_group(agr)
        tag_found = buffer.create_tag("found", background="yellow", weight=700)
        tv.grab_focus()
        tv.modify_font(pango.FontDescription(CONST.DEFAULT_FONT))
        sb.push(CONST.STATUSBAR_TEXT_IDX, "Ln 1, Col: 1, 100%")
        # init accels
        self.load_accels(agr, builder, CONST.IMIOPEN_NAME, "<Control>O")
        self.load_accels(agr, builder, CONST.IMINEW_NAME, "<Control>N")
        self.load_accels(agr, builder, CONST.IMISAVE_NAME, "<Control>S")
        self.load_accels(agr, builder, CONST.IMIQUIT_NAME, "<Control>Q")
        self.load_accels(agr, builder, CONST.IMIUNDO_NAME, "<Control>Z")
        self.load_accels(agr, builder, CONST.IMIREDO_NAME, "<Control>Y")
        self.load_accels(agr, builder, CONST.IMICUT_NAME, "<Control>X")
        self.load_accels(agr, builder, CONST.IMICOPY_NAME, "<Control>C")
        self.load_accels(agr, builder, CONST.IMIPASTE_NAME, "<Control>V")
        self.load_accels(agr, builder, CONST.IMISELECTALL_NAME, "<Control>A")
        self.load_accels(agr, builder, CONST.IMIFIND_NAME, "<Control>F")
        self.load_accels(agr, builder, CONST.IMIREPLACE_NAME, "<Control>H")
        # connect handlers
        self.handlers = Handler(builder, tag_found)
        builder.connect_signals(self.handlers)
        # init sensitive
        self.handlers.set_sensitive(CONST.IMIUNDO_NAME, False)
        self.handlers.set_sensitive(CONST.IMIREDO_NAME, False)
        self.handlers.set_sensitive(CONST.TBUNDO_NAME, False)
        self.handlers.set_sensitive(CONST.TBREDO_NAME, False)
        # connect the buffer with the status bar
        buffer.connect("notify::cursor-position", self.handlers.on_cursor_position_changed, sb)
        # Add undo/redo callbacks
        buffer.connect("insert_text", self.handlers.buffer_insert_text)
        buffer.connect("delete_range", self.handlers.buffer_delete_range)
        buffer.connect("begin_user_action", self.handlers.buffer_begin_user_action)
        buffer.connect("end_user_action", self.handlers.buffer_end_user_action)
        # connect drag and drop
        tv.drag_dest_set(gtk.DEST_DEFAULT_ALL, 
                         [('text/uri-list', 0, 0)], gtk.gdk.ACTION_COPY); 
        tv.connect('drag-data-received', self.handlers.on_drop, tv);
        # Show the window
        window.set_title("Untitled - " + window.get_title())
        window.show_all()

    def loadFile(self, filename):
        self.handlers.open_file(filename)

    def load_accels(self, agr, builder, name, shortcut):
        key, mod = gtk.accelerator_parse(shortcut)
        builder.get_object(name).add_accelerator("activate", agr, key, 
            mod, gtk.ACCEL_VISIBLE)

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
