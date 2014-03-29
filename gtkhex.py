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
    def STATUSBAR_FILE_IDX(): return 0
    @constant
    def STATUSBAR_TEXT_IDX(): return 1
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
    return content

# translate text hex to data representation
def hex_to_data(content):
    return content

class Handler:
    def __init__(self, builder, tag_found):
        self.win = builder.get_object(CONST.WINDOW_NAME)
        self.sb = builder.get_object(CONST.STATUSBAR_NAME)
        self.tv = builder.get_object(CONST.TEXTVIEW_NAME)
        self.dabout = builder.get_object(CONST.ABOUTDIALOG_NAME)
        self.dfind = builder.get_object(CONST.FINDDIALOG_NAME)
        self.dreplace = builder.get_object(CONST.REPLACEDIALOG_NAME)
        self.efind = builder.get_object(CONST.FINDENTRY_NAME)
        self.ereplace = builder.get_object(CONST.REPLACEENTRY_NAME)
        self.defaultWindowTitle = self.win.get_title()
        self.tag_found = tag_found
        self.currentFile = None
        self.changed = False

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
            self.currentFile = cfile
            filename = self.currentFile
            self.sb.push(CONST.STATUSBAR_FILE_IDX, "Opened File: " + filename)
            file = open(filename, "r")
            self.tv.get_buffer().set_text(data_to_hex(file.read()))
            file.close()
            self.changed = False

    def on_save(self, button):
        if self.currentFile == None:
            self.on_save_as(button)
        else:
            filename = self.currentFile
            self.changed = False
            buffer = self.tv.get_buffer()
            self.sb.pop(CONST.STATUSBAR_FILE_IDX)
            self.sb.push(CONST.STATUSBAR_FILE_IDX, "Saved File: " + filename)
            index = filename.replace("\\","/").rfind("/") + 1
            text = buffer.get_text(buffer.get_start_iter() , buffer.get_end_iter())
            index = filename.replace("\\","/").rfind("/") + 1
            title = filename[index:] + " - " + self.defaultWindowTitle
            self.win.set_title(title)
            self.win.queue_draw()
            file = open(filename, "w+")
            file.write(hex_to_data(text))
            file.close()

    def on_save_as(self, button):
        response, cfile =  gtk_file_chooser("Save file", gtk.FILE_CHOOSER_ACTION_SAVE)
        if response:
            self.currentFile = cfile
            # generic call
            self.on_save(button)

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
        buffer = self.tv.get_buffer()
        cursor_mark = buffer.get_insert()
        start = buffer.get_iter_at_mark(cursor_mark)
        if start.get_offset() == buffer.get_char_count():
            start = buffer.get_start_iter()
        self.search_and_mark(self.efind.get_text(), start)

    #Replace dialog
    def on_replace(self, widget):
        self.dreplace.show()
    def on_replace_quit(self, widget):
        self.dreplace.hide()
    def on_replace_execute(self, widget):
        buffer = self.tv.get_buffer()
        iter = buffer.get_iter_at_mark(buffer.get_mark("insert"))
        sel_bound = buffer.get_iter_at_mark(buffer.get_mark("selection_bound"))
        if iter == sel_bound:
            rself.eplace_selected_text(self.ereplace.get_text(), iter, sel_bound)

    def on_search_clear(self, button):
        buffer = self.tv.get_buffer()
        start = buffer.get_start_iter()
        end = buffer.get_end_iter()
        buffer.remove_all_tags(start, end)

    def search_and_mark(self, text, start):
        buffer = self.tv.get_buffer()
        end = buffer.get_end_iter()
        match = start.forward_search(text, 0, end)
        if match != None:
            match_start, match_end = match
            buffer.apply_tag(self.tag_found, match_start, match_end)
            self.search_and_mark(text, match_end)
        else:
            d = gtk.MessageDialog(None,
                           gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT, 
                           gtk.MESSAGE_INFO, 
                           gtk.BUTTONS_OK, None)
            d.set_markup("The string " + text + " has not been found.")
            d.run()
            d.destroy()

    def replace_selected_text(self, str, start_iter, end_iter):
        buffer = self.tv.get_buffer()
        buffer.begin_user_action
        buffer.delete(start_iter, end_iter)
        buffer.insert(start_iter, str)
        buffer.end_user_action
        iter_on_screen(start_iter, "insert")

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
        tag_found = buffer.create_tag("found", background="yellow", weight=700)
        tv.grab_focus()
        sb.push(CONST.STATUSBAR_TEXT_IDX, "Ln 1, Col: 1, 100%")
        # connect handlers
        handlers = Handler(builder, tag_found)
        builder.connect_signals(handlers)

        # connect the buffer with the status bar
        buffer.connect("notify::cursor-position", handlers.on_cursor_position_changed, sb)
        # Show the window
        window.set_title("Untitled - " + window.get_title())
        window.show_all()

    def main(self):
        gtk.gdk.threads_enter()
        gtk.main()
        gtk.gdk.threads_leave()

def main(argv):
    win = gtkhex()
    win.main()


if __name__ == '__main__':
    main(sys.argv[1:])
