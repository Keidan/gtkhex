###################################################################################
# @file scrolled_text_view.py
# @author Keidan (Kevin Billonneau)
# @par Copyright GNU GENERAL PUBLIC LICENSE Version 3
###################################################################################

from drop_text_view import *
from gi.repository import Gtk


class ScrolledTextView(Gtk.ScrolledWindow):
    def __init__(self, statusbar):
        Gtk.ScrolledWindow.__init__(self)
        self.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.ALWAYS)
        self.tv = DropTextView(statusbar)
        self.add_with_viewport(self.tv)
        self.show_all()
        self.user_ptr = None

    def get_textview(self):
        return self.tv

    def set_user_ptr(self, user_ptr):
        self.user_ptr = user_ptr

    def get_user_ptr(self):
        return self.user_ptr
