###################################################################################
# @file UndoRedoBuffer.py
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

from Imports import *
from ScrolledTextView import *
from TabLabel import *

class Handlers:
    def __init__(self, builder):
        self.builder = builder
        self.win = builder.get_object(CONST.WINDOW_NAME)
        self.sb = builder.get_object(CONST.STATUSBAR_NAME)
        self.pb = builder.get_object(CONST.PROGRESSBAR_NAME)
        self.nb = builder.get_object(CONST.NOTEBOOK_NAME)
        self.dabout = builder.get_object(CONST.ABOUTDIALOG_NAME)
        self.dfind = builder.get_object(CONST.FINDDIALOG_NAME)
        self.dreplace = builder.get_object(CONST.REPLACEDIALOG_NAME)
        self.efind = builder.get_object(CONST.FINDENTRY_NAME)
        self.ereplace = builder.get_object(CONST.REPLACEENTRY_NAME)
        self.ereplacefind = builder.get_object(CONST.REPLACEFINDENTRY_NAME)
        self.defaultWindowTitle = self.win.get_title()
        self.buffer = None
        self.timer = 0
        self.changed = False
        # some inits
        self.nb.connect("switch-page", self.on_notebook_page_selected)
        self.add_new_tab_text(File())
        # init sensitive
        self.undo_redo_state()
        # init accels
        self.accelGroup = None
        self.load_accels(self.builder, CONST.IMIOPEN_NAME, "<Control>O")
        self.load_accels(self.builder, CONST.IMINEW_NAME, "<Control>N")
        self.load_accels(self.builder, CONST.IMISAVE_NAME, "<Control>S")
        self.load_accels(self.builder, CONST.IMIQUIT_NAME, "<Control>Q")
        self.load_accels(self.builder, CONST.IMIUNDO_NAME, "<Control>Z")
        self.load_accels(self.builder, CONST.IMIREDO_NAME, "<Control>Y")
        self.load_accels(self.builder, CONST.IMICUT_NAME, "<Control>X")
        self.load_accels(self.builder, CONST.IMICOPY_NAME, "<Control>C")
        self.load_accels(self.builder, CONST.IMIPASTE_NAME, "<Control>V")
        self.load_accels(self.builder, CONST.IMISELECTALL_NAME, "<Control>A")
        self.load_accels(self.builder, CONST.IMIFIND_NAME, "<Control>F")
        self.load_accels(self.builder, CONST.IMIREPLACE_NAME, "<Control>H")

    def get_AccelGroup(self):
        if self.accelGroup == None:
            self.accelGroup = gtk.AccelGroup()
        return self.accelGroup

    def load_accels(self, builder, name, shortcut):
        key, mod = gtk.accelerator_parse(shortcut)
        builder.get_object(name).add_accelerator("activate", self.get_AccelGroup(), key, 
            mod, gtk.ACCEL_VISIBLE)
        
    def stop_timer(self):
        if not self.timer: return
        gobject.source_remove(self.timer)
        self.timer = 0
            
    def progress_timeout(self, me):
        me.pb.pulse()
        # As this is a timeout function, return TRUE so that it
        # continues to get called
        return True
        
    def on_quit(self, button):
        self.on_appwindow_delete_event(None)

    def on_appwindow_delete_event(self, *args):
        if self.buffer != None and self.changed:
            text = "Do you really want to leave this program without save ?"
            if gtk_confirm_box(text):
                self.stop_timer()
                gtk.main_quit()
                return False
            return True
        else:
            self.stop_timer()
            gtk.main_quit()
            return False

    def on_drop_file(self, widget, path):
        self.open_file(path)

    def on_new(self, button):
        if self.buffer != None and self.buffer.get_user_ptr() != None and self.buffer.get_user_ptr().get_filename() != None and self.changed:
            if not gtk_confirm_box("Do you want to create a new file without saving your changes?"):
                return
        self.add_new_tab_text(File())
        
    def on_open(self, button):
        response, cfile = gtk_file_chooser("Open a file", gtk.FILE_CHOOSER_ACTION_OPEN)
        if response: self.open_file(cfile)

    def open_file(self, cfile):
        gtk.gdk.threads_enter()
        self.stop_timer()
        self.timer = gobject.timeout_add(100, self.progress_timeout, self)
        f = File(cfile)
        f.read()
        if not self.buffer or len(self.buffer.get_full_text()):
            self.add_new_tab_text(f)
        else:
            self.nb.get_nth_page(self.nb.get_current_page()).get_user_ptr().set_tab_text(f.get_simple_name())
        tv = self.nb.get_nth_page(self.nb.get_current_page()).get_textview()
        tv.set_sensitive(False)
        self.buffer.set_text(data_to_hex(f.get_data()))
        tv.set_sensitive(True)
        self.changed = False
        self.stop_timer()
        gtk.gdk.threads_leave()

    def test_data_buffer(self):
        if self.buffer == None: return None
        data = hex_to_data(self.buffer.get_full_text())
        if data == None:
            d = gtk.MessageDialog(self.win,
                                  gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT, 
                                  gtk.MESSAGE_ERROR, 
                                  gtk.BUTTONS_OK, None)
            d.set_markup("The text entry contain one or more invalid characters.\nOr an Odd-length.")
            d.run()
            d.destroy()
            return None
        return data

    def on_save(self, button):
        data = self.test_data_buffer()
        if data == None: return
        if self.buffer.get_user_ptr() == None or self.buffer.get_user_ptr().get_filename() == None: self.on_save_as(button)
        else: 
            self.buffer.get_user_ptr().set_data(data)
            self.buffer.get_user_ptr().write()
            self.check_tab_title()

    def check_tab_title(self):
        if self.buffer == None: return
        tablabel = self.nb.get_nth_page(self.nb.get_current_page()).get_user_ptr()
        if tablabel.get_tab_text().endswith(" *"):
            tablabel.set_tab_text(tablabel.get_tab_text()[:-2])
            self.changed = False

    def on_save_as(self, button):
        if self.buffer == None: return
        data = self.test_data_buffer()
        if data == None: return
        response, cfile = gtk_file_chooser("Save file", gtk.FILE_CHOOSER_ACTION_SAVE)
        if response:
            f = File(cfile)
            f.set_data(data)
            self.buffer.set_user_ptr(f)
            # generic call
            f.write() 
            self.check_tab_title()       

    def on_cut(self, button):
        if self.buffer == None: return
        self.buffer.cut_clipboard(gtk.clipboard_get(), True)

    def on_copy(self, button):
        if self.buffer == None: return
        self.buffer.copy_clipboard (gtk.clipboard_get())

    def on_paste(self, button):
        if self.buffer == None: return
        self.buffer.paste_clipboard (gtk.clipboard_get(), None, True)

    def on_delete(self, button):
        if self.buffer == None: return
        self.buffer.delete_selection(False, True)

    def on_select_all(self, button):
        if self.buffer == None: return
        self.buffer.select_all()

    # undo/redo 
    def undo_redo_state(self):
        if self.buffer == None: 
            self.set_sensitive(CONST.IMIUNDO_NAME, False)
            self.set_sensitive(CONST.TBUNDO_NAME, False)
            self.set_sensitive(CONST.IMIREDO_NAME, False)
            self.set_sensitive(CONST.TBREDO_NAME, False)
            return
        if not self.buffer.get_undo_size():
            self.set_sensitive(CONST.IMIUNDO_NAME, False)
            self.set_sensitive(CONST.TBUNDO_NAME, False)
        else:
            self.set_sensitive(CONST.IMIUNDO_NAME, True)
            self.set_sensitive(CONST.TBUNDO_NAME, True)
        if not self.buffer.get_redo_size():
            self.set_sensitive(CONST.IMIREDO_NAME, False)
            self.set_sensitive(CONST.TBREDO_NAME, False)
        else:
            self.set_sensitive(CONST.IMIREDO_NAME, True)
            self.set_sensitive(CONST.TBREDO_NAME, True)

    def buffer_update(self, buffer):
        self.undo_redo_state()
        if len(self.buffer.get_full_text()): 
            self.changed = True
            tablabel = self.nb.get_nth_page(self.nb.get_current_page()).get_user_ptr()
            if not tablabel.get_tab_text().endswith(" *"):
                tablabel.set_tab_text(tablabel.get_tab_text() + " *")

    def on_undo(self, button):
        if self.buffer == None: return
        self.buffer.set_undo()
        self.undo_redo_state()

    def on_redo(self, button):
        if self.buffer == None: return
        self.buffer.set_redo()
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
        if self.buffer == None: return
        self.buffer.set_find(self.efind, True, self.dfind)
    def on_search_clear(self, button):
        if self.buffer == None: return
        self.buffer.clear_search()

    #Replace dialog
    def on_replace(self, widget):
        self.dreplace.show()
    def on_replace_quit(self, widget):
        self.dreplace.hide()
    def on_replace_execute(self, widget):
        if self.buffer == None: return
        self.buffer.set_replace(self.ereplacefind, False, self.dreplace, self.ereplace.get_text())

    def set_sensitive(self, name, state):
        widget = self.builder.get_object(name)
        if not widget.get_sensitive() == state:
            widget.set_sensitive(state)

    def add_new_tab_text(self, cfile):
        stv = ScrolledTextView(self.sb)
        stv.get_textview().get_buffer().set_user_ptr(cfile)
        stv.get_textview().get_buffer().connect("buffer-update", self.buffer_update)
        stv.get_textview().connect("drop-file", self.on_drop_file)
        tab_label = TabLabel(cfile.get_simple_name())
        stv.set_user_ptr(tab_label)
        tab_label.connect("close-clicked", self.on_close_clicked, self.nb, stv)
        self.nb.append_page(stv, tab_label)
        self.buffer = stv.get_textview().get_buffer()
        stv.get_textview().grab_focus()

    def on_close_clicked(self, tab_label, notebook, tab_widget): 
        if self.changed:
            if not gtk_confirm_box("Do you want to close this tab without saving your changes?"):
                return
        self.buffer = None
        notebook.remove_page(notebook.page_num(tab_widget))
        if not notebook.get_n_pages():
            self.on_appwindow_delete_event(None)

    def on_notebook_page_selected(self, notebook, page, pagenum):
        self.buffer = notebook.get_nth_page(pagenum).get_textview().get_buffer()
        notebook.get_nth_page(pagenum).get_textview().grab_focus()
