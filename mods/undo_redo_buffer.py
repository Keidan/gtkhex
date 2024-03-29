###################################################################################
# @file undo_redo_buffer.py
# @author Keidan (Kevin Billonneau)
# @par Copyright GNU GENERAL PUBLIC LICENSE Version 3
###################################################################################

from gi.repository import Gtk
from gi.repository import GObject
from consts import CONST
from queue import LifoQueue


class UndoRedoBuffer(Gtk.TextBuffer):
    __gsignals__ = {
        'buffer-update': (GObject.SIGNAL_RUN_FIRST, GObject.TYPE_NONE, ()),
        'buffer-undo': (GObject.SIGNAL_RUN_FIRST, GObject.TYPE_NONE, ()),
        'buffer-redo': (GObject.SIGNAL_RUN_FIRST, GObject.TYPE_NONE, ()),
    }

    def __init__(self, iter_on_screen, statusbar):
        Gtk.TextBuffer.__init__(self)
        self.iter_on_screen = iter_on_screen
        self.tag_found = self.create_tag('found', background='yellow', weight=700)
        # connect the buff with the status bar
        self.connect(
            'notify::cursor-position', self.on_cursor_position_changed, statusbar
        )
        # Add undo/redo callbacks
        self.connect('changed', self.buffer_changed)
        self.connect('insert_text', self.buffer_insert_text)
        self.connect('delete_range', self.buffer_delete_range)
        self.connect('begin_user_action', self.buffer_begin_user_action)
        self.connect('end_user_action', self.buffer_end_user_action)
        self.undopool = LifoQueue(CONST.max_undo())
        self.redopool = LifoQueue(CONST.max_redo())
        self.user_action = False
        self.user_ptr = None
        self.changed = False

    def set_changed(self, changed):
        self.changed = changed

    def is_changed(self):
        return self.changed

    def get_undo_size(self):
        return self.undopool.qsize()

    def get_redo_size(self):
        return self.redopool.qsize()

    def get_user_ptr(self):
        return self.user_ptr

    def set_user_ptr(self, user_ptr):
        self.user_ptr = user_ptr

    def get_full_text(self):
        return self.get_text(self.get_start_iter(), self.get_end_iter(), True)

    def get_tag_found(self):
        return self.tag_found

    def select_all(self):
        match_start = self.get_start_iter()
        match_end = self.get_end_iter()
        self.select_range(match_start, match_end)

    def get_selected_text(self):
        it = self.get_iter_at_mark(self.get_mark('insert'))
        sel_bound = self.get_iter_at_mark(self.get_mark('selection_bound'))
        text = ''
        if it != sel_bound:
            text = self.get_text(it, sel_bound, True)
        return text

    def on_cursor_position_changed(self, buffer, param, sb):
        idx = CONST.statusbar_text_idx()
        # clear the statusbar
        sb.pop(idx)
        # get the words number
        words = buffer.get_char_count()
        if not words:
            words = 1
        # get the current position
        word = buffer.props.cursor_position
        # get the current iter
        it = buffer.get_iter_at_mark(buffer.get_insert())
        # get the current line
        line = it.get_line()
        # get the cursor position into the current line
        #col = buffer.get_iter_at_line_offset(line, 0)
        sb.push(
            idx,
            f'Ln {line + 1}, Col: {it.get_line_offset()}, {(word * 100 / words):.02f}%'
        )

    def buffer_changed(self, buffer):
        self.changed = True
        self.emit('buffer-update')

    def buffer_insert_text(self, buffer, iter, text, length):
        if self.user_action:
            self.undopool.put(
                ['insert_text', iter.get_offset(), iter.get_offset() + len(text), text]
            )
            with self.redopool.mutex:
                self.redopool.queue[:] = []

    def buffer_delete_range(self, buffer, start_iter, end_iter):
        if self.user_action:
            text = buffer.get_text(start_iter, end_iter, True)
            self.undopool.put(
                ['delete_range', start_iter.get_offset(), end_iter.get_offset(), text]
            )

    def buffer_begin_user_action(self, buffer):
        self.user_action = True

    def buffer_end_user_action(self, buffer):
        self.user_action = False

    def set_undo(self):
        if not self.undopool.qsize():
            return
        action = self.undopool.get()
        if action[0] == 'insert_text':
            start_iter = self.get_iter_at_offset(action[1])
            end_iter = self.get_iter_at_offset(action[2])
            self.delete(start_iter, end_iter)
        elif action[0] == 'delete_range':
            start_iter = self.get_iter_at_offset(action[1])
            self.insert(start_iter, action[3])
        self.iter_on_screen(start_iter, 'insert')
        self.redopool.put(action)
        self.emit('buffer-undo')

    def set_redo(self):
        if not self.redopool.qsize():
            return
        action = self.redopool.get()
        if action[0] == 'insert_text':
            start_iter = self.get_iter_at_offset(action[1])
            self.insert(start_iter, action[3])
        elif action[0] == 'delete_range':
            start_iter = self.get_iter_at_offset(action[1])
            end_iter = self.get_iter_at_offset(action[2])
            self.delete(start_iter, end_iter)
        self.iter_on_screen(start_iter, 'insert')
        self.undopool.put(action)
        self.emit('buffer-undo')

    def set_find(self, find, tags, parent, all):
        self.clear_search()
        if all:
            cursor_mark = self.get_insert()
            start = self.get_iter_at_mark(cursor_mark)
            if start.get_offset() == self.get_char_count():
                start = self.get_start_iter()
            self.search_and_mark(find, start)
        else:
            self.find_and_select(find, tags, parent)

    def clear_search(self):
        start = self.get_start_iter()
        end = self.get_end_iter()
        self.remove_all_tags(start, end)

    def search_and_mark(self, find, start):
        text = find.get_text()
        end = self.get_end_iter()
        match = start.forward_search(text, 0, end)
        if match != None:
            match_start, match_end = match
            self.apply_tag(self.tag_found, match_start, match_end)
            self.search_and_mark(find, match_end)

    def find_and_select(self, find, tags, parent):
        text = find.get_text()
        cursor_mark = self.get_insert()
        start = self.get_iter_at_mark(cursor_mark)
        if start.get_offset() == self.get_char_count():
            start = self.get_start_iter()
        search_flags = Gtk.TextSearchFlags.TEXT_ONLY
        match_iters = start.forward_search(text, search_flags)

        if match_iters != None:
            next_iter = [match_iters[1], match_iters[0]]
            self.iter_on_screen(next_iter[0], 'insert')
            self.move_mark(self.get_mark('selection_bound'), next_iter[1])
            if tags:
                self.apply_tag(self.tag_found, next_iter[0], next_iter[1])
            return True
        else:
            d = Gtk.MessageDialog(
                parent,
                Gtk.DialogFlags.MODAL | Gtk.DialogFlags.DESTROY_WITH_PARENT,
                Gtk.MessageType.INFO,
                Gtk.ButtonsType.OK,
                None,
            )
            d.set_markup('The string ' + text + ' has not been found.')
            d.run()
            d.destroy()
            return False

    def set_replace(self, replacefind, tags, parent, replace_text):
        self.clear_search()
        if self.find_and_select(replacefind, False, parent):
            it = self.get_iter_at_mark(self.get_mark('insert'))
            sel_bound = self.get_iter_at_mark(self.get_mark('selection_bound'))
            if it != sel_bound:
                self.replace_selected_text(replace_text, it, sel_bound)

    def replace_selected_text(self, str, start_iter, end_iter):
        self.begin_user_action
        self.delete(start_iter, end_iter)
        self.insert(start_iter, str)
        self.end_user_action
        self.iter_on_screen(start_iter, 'insert')

    def iter_on_screen(self, iter, mark_str):
        buffer = self.tv.get_buffer()
        buffer.place_cursor(iter)
        self.tv.scroll_mark_onscreen(buffer.get_mark(mark_str))
