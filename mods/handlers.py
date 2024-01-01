###################################################################################
# @file handlers.py
# @author Keidan (Kevin Billonneau)
# @par Copyright GNU GENERAL PUBLIC LICENSE Version 3
###################################################################################

from scrolled_text_view import *
from tab_label import *
from gi.repository import Gtk
from gi.repository import Gdk
from gi.repository import GObject
from consts import CONST
from file import File
from helpers import *


class Handlers:
    def __init__(self, builder):
        self.clipboard = Gtk.Clipboard.get(Gdk.SELECTION_CLIPBOARD)
        self.builder = builder
        self.win = builder.get_object(CONST.window_name())
        self.sb = builder.get_object(CONST.statusbar_name())
        self.pb = builder.get_object(CONST.progressbar_name())
        self.nb = builder.get_object(CONST.notebook_name())
        self.dabout = builder.get_object(CONST.about_dialog_name())
        self.dfind = builder.get_object(CONST.find_dialog_name())
        self.dreplace = builder.get_object(CONST.replace_dialog_name())
        self.efind = builder.get_object(CONST.find_entry_name())
        self.afind = builder.get_object(CONST.find_all_name())
        self.ereplace = builder.get_object(CONST.replace_entry_name())
        self.ereplacefind = builder.get_object(CONST.replace_find_entry_name())
        self.default_window_title = self.win.get_title()
        self.buffer = None
        self.timer = 0
        self.title = None
        # some inits
        self.dfind.connect('delete-event', self.on_destroy_dialog)
        self.dreplace.connect('delete-event', self.on_destroy_dialog)
        self.nb.connect('switch-page', self.on_notebook_page_selected)
        self.add_new_tab_text(File())
        # init sensitive
        self.undo_redo_state()
        # init accels
        self.accel_group = None
        self.load_accels(self.builder, CONST.imi_open_name(), '<Control>O')
        self.load_accels(self.builder, CONST.imi_new_name(), '<Control>N')
        self.load_accels(self.builder, CONST.imi_save_name(), '<Control>S')
        self.load_accels(self.builder, CONST.imi_quit_name(), '<Control>Q')
        self.load_accels(self.builder, CONST.imi_undo_name(), '<Control>Z')
        self.load_accels(self.builder, CONST.imi_redo_name(), '<Control>Y')
        self.load_accels(self.builder, CONST.imi_cut_name(), '<Control>X')
        self.load_accels(self.builder, CONST.imi_copy_name(), '<Control>C')
        self.load_accels(self.builder, CONST.imi_copy_raw_name(), '<Control>R')
        self.load_accels(self.builder, CONST.imi_paste_name(), '<Control>V')
        self.load_accels(self.builder, CONST.imi_select_all_name(), '<Control>A')
        self.load_accels(self.builder, CONST.imi_find_name(), '<Control>F')
        self.load_accels(self.builder, CONST.imi_replace_name(), '<Control>H')
        self.load_accels(self.builder, CONST.imi_format_name(), '<Control>W')

    def get_dialog_about(self):
        return self.dabout

    def on_destroy_dialog(self, widget, *data):
        widget.hide()
        return True
        
    def show_hide_window(self, item):
        if self.win.props.visible:
            item.set_label('Show')
            self.win.hide()
        else:
            item.set_label('Hide')
            self.win.show()

    def get_accel_group(self):
        if self.accel_group == None:
            self.accel_group = Gtk.AccelGroup()
        return self.accel_group

    def load_accels(self, builder, name, shortcut):
        key, mod = Gtk.accelerator_parse(shortcut)
        builder.get_object(name).add_accelerator(
            'activate', self.get_accel_group(), key, mod, Gtk.AccelFlags.VISIBLE
        )

    def on_format(self, button):
        if not self.buffer:
            return
        SysHelper.format_data_buffer(self.buffer)

    def stop_timer(self):
        if not self.timer:
            return
        GObject.source_remove(self.timer)
        self.timer = 0

    def progress_timeout(self, me):
        me.pb.pulse()
        # As this is a timeout function, return TRUE so that it
        # continues to get called
        return True

    def on_quit(self, button):
        self.on_appwindow_delete_event()

    def on_appwindow_delete_event(self, *args):
        if self.buffer != None and self.buffer.is_changed():
            text = 'Do you really want to leave this program without save ?'
            if UIHelper.gtk_confirm_box(text):
                self.stop_timer()
                Gtk.main_quit()
                return False
            return True
        else:
            self.stop_timer()
            Gtk.main_quit()
            return False

    def on_drop_file(self, widget, path):
        self.open_file(path)

    def on_new(self, button):
        if (
            self.buffer != None
            and self.buffer.get_user_ptr() != None
            and self.buffer.get_user_ptr().get_filename() != None
            and self.buffer.is_changed()
            and not UIHelper.gtk_confirm_box(
                'Do you want to create a new file without saving your changes?'
            )
        ):
            return
        self.add_new_tab_text(File())

    def on_open(self, button):
        response, cfile = UIHelper.gtk_file_chooser('Open a file', Gtk.FileChooserAction.OPEN)
        if response:
            self.open_file(cfile)

    def open_file(self, cfile):
        self.stop_timer()
        self.timer = GObject.timeout_add(100, self.progress_timeout, self)
        f = File(cfile)
        f.read()
        if not self.buffer or len(self.buffer.get_full_text()):
            self.add_new_tab_text(f)
        else:
            self.nb.get_nth_page(
                self.nb.get_current_page()
            ).get_user_ptr().set_tab_text(f.get_simple_name())
        tv = self.nb.get_nth_page(self.nb.get_current_page()).get_textview()
        tv.set_sensitive(False)
        self.buffer.set_text(SysHelper.data_to_hex(f.get_data()))
        self.buffer.set_user_ptr(f)
        tv.set_sensitive(True)
        self.buffer.set_changed(False)
        self.stop_timer()
        self.check_tab_title()
        self.update_window_title()

    def test_data_buffer(self):
        if self.buffer == None:
            return None
        data = SysHelper.hex_to_data(self.buffer.get_full_text())
        if data == None:
            d = Gtk.MessageDialog(
                self.win,
                Gtk.DialogFlags.MODAL | Gtk.DialogFlags.DESTROY_WITH_PARENT,
                Gtk.MessageType.ERROR,
                Gtk.ButtonsType.OK,
                None,
            )
            d.set_markup(
                'The text entry contain one or more invalid characters.\nOr an Odd-length.'
            )
            d.run()
            d.destroy()
            return None
        return data

    def on_save(self, button):
        data = self.test_data_buffer()
        if data == None:
            return
        if (
            self.buffer.get_user_ptr() == None
            or self.buffer.get_user_ptr().get_filename() == None
        ):
            self.on_save_as()
        else:
            self.buffer.get_user_ptr().set_data(data)
            self.buffer.get_user_ptr().write()
            self.check_tab_title()

    def buffer_update(self, buffer):
        self.undo_redo_state()
        tablabel = self.nb.get_nth_page(self.nb.get_current_page()).get_user_ptr()
        if not tablabel.get_tab_text().endswith(' *'):
            tablabel.set_tab_text(tablabel.get_tab_text() + ' *')

    def check_tab_title(self):
        if self.buffer == None:
            return
        tablabel = self.nb.get_nth_page(self.nb.get_current_page()).get_user_ptr()
        if tablabel.get_tab_text().endswith(' *'):
            tablabel.set_tab_text(tablabel.get_tab_text()[:-2])
            self.buffer.set_changed(False)
        if tablabel.get_tab_text() != self.buffer.get_user_ptr().get_simple_name():
            tablabel.set_tab_text(self.buffer.get_user_ptr().get_simple_name())

    def on_save_as(self):
        if self.buffer == None:
            return
        data = self.test_data_buffer()
        if data == None:
            return
        response, cfile = UIHelper.gtk_file_chooser('Save file', Gtk.FileChooserAction.SAVE)
        if response:
            f = File(cfile)
            f.set_data(data)
            self.buffer.set_user_ptr(f)
            # generic call
            f.write()
            self.check_tab_title()

    def on_cut(self, button):
        if self.buffer == None:
            return
        self.buffer.user_action = True
        self.buffer.cut_clipboard(self.clipboard, True)
        self.buffer.user_action = False
        self.undo_redo_state()

    def on_copy(self, button):
        if self.buffer == None:
            return
        self.buffer.copy_clipboard(self.clipboard)

    def on_copy_raw(self, button):
        if self.buffer == None:
            return
        text = self.buffer.get_selected_text()
        if len(text) == 0:
          text = self.buffer.get_full_text()
        if len(text) == 0:
            return
        data = SysHelper.hex_to_data(text)
        length = len(data)
        if data and length:
            s = bytes(data).decode('utf-8')
            self.clipboard.set_text(s, length)
            self.clipboard.store()
        # self.buffer.copy_clipboard (self.clipboard)

    def on_paste(self, button):
        if self.buffer == None:
            return
        self.buffer.user_action = True
        SysHelper.copy_from_clipbard(self.clipboard, self.buffer)
        self.buffer.user_action = False
        self.undo_redo_state()
        # self.buffer.paste_clipboard (slf.clipboard, None, True)

    def on_delete(self, button):
        if self.buffer == None:
            return
        self.buffer.delete_selection(False, True)

    def on_select_all(self, button):
        if self.buffer == None:
            return
        self.buffer.select_all()

    # undo/redo
    def undo_redo_state(self):
        if self.buffer == None:
            self.set_sensitive(CONST.imi_undo_name(), False)
            self.set_sensitive(CONST.tb_undo_name(), False)
            self.set_sensitive(CONST.imi_redo_name(), False)
            self.set_sensitive(CONST.tb_redo_name(), False)
            return
        if not self.buffer.get_undo_size():
            self.set_sensitive(CONST.imi_undo_name(), False)
            self.set_sensitive(CONST.tb_undo_name(), False)
        else:
            self.set_sensitive(CONST.imi_undo_name(), True)
            self.set_sensitive(CONST.tb_undo_name(), True)
        if not self.buffer.get_redo_size():
            self.set_sensitive(CONST.imi_redo_name(), False)
            self.set_sensitive(CONST.tb_redo_name(), False)
        else:
            self.set_sensitive(CONST.imi_redo_name(), True)
            self.set_sensitive(CONST.tb_redo_name(), True)

    def on_undo(self, button):
        if self.buffer == None:
            return
        self.buffer.set_undo()
        self.undo_redo_state()

    def on_redo(self, button):
        if self.buffer == None:
            return
        self.buffer.set_redo()
        self.undo_redo_state()

    def on_about(self, button):
        self.dabout.show_all()
        self.dabout.run()
        self.dabout.hide()

    # Find dialog
    def on_find_quit(self, button):
        self.dfind.hide()

    def on_search(self, button):
        self.dfind.show()

    def on_find_execute(self, button):
        if self.buffer == None:
            return
        self.buffer.set_find(self.efind, True, self.dfind, self.afind.get_active())

    def on_search_clear(self, button):
        if self.buffer == None:
            return
        self.buffer.clear_search()

    # Replace dialog
    def on_replace(self, widget):
        self.dreplace.show()

    def on_replace_quit(self, widget):
        self.dreplace.hide()

    def on_replace_execute(self, widget):
        if self.buffer == None:
            return
        self.buffer.set_replace(
            self.ereplacefind, False, self.dreplace, self.ereplace.get_text()
        )

    def set_sensitive(self, name, state):
        widget = self.builder.get_object(name)
        try:
            if widget.get_sensitive() != state:
                widget.set_sensitive(state)
        except Exception:
            widget.set_sensitive(state)

    def add_new_tab_text(self, cfile):
        stv = ScrolledTextView(self.sb)
        stv.get_textview().get_buffer().set_user_ptr(cfile)
        stv.get_textview().get_buffer().connect('buffer-update', self.buffer_update)
        stv.get_textview().connect('drop-file', self.on_drop_file)
        tab_label = TabLabel(cfile.get_simple_name())
        stv.set_user_ptr(tab_label)
        tab_label.connect('close-clicked', self.on_close_clicked, self.nb, stv)
        self.nb.append_page(stv, tab_label)
        self.buffer = stv.get_textview().get_buffer()
        stv.get_textview().grab_focus()
        self.nb.set_current_page(self.nb.get_n_pages() - 1)
        self.update_window_title()

    def update_window_title(self, num=-1):
        n = num
        if n == -1:
            n = self.nb.get_current_page()
        tab_label = self.nb.get_nth_page(n).get_user_ptr()
        if self.title == None:
            self.title = self.win.get_title()
        self.win.set_title(self.title + ' - ' + tab_label.get_tab_text())
        self.win.queue_draw()

    def on_close_clicked(self, tab_label, notebook, tab_widget):
        if (
            self.buffer
            and self.buffer.is_changed()
            and not UIHelper.gtk_confirm_box(
                'Do you want to close this tab without saving your changes?'
            )
        ):
            return
        self.buffer = None
        notebook.remove_page(notebook.page_num(tab_widget))
        if not notebook.get_n_pages():
            self.on_appwindow_delete_event()

    def on_notebook_page_selected(self, notebook, page, pagenum):
        scroll = notebook.get_nth_page(pagenum)
        self.buffer = scroll.get_textview().get_buffer()
        scroll.get_textview().grab_focus()
        self.update_window_title(pagenum)
