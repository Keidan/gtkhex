###################################################################################
# @file ScrolledTextView.py
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

from DropTextView import *

class ScrolledTextView(gtk.ScrolledWindow):
    def __init__(self, statusbar):
        gtk.ScrolledWindow.__init__(self)
        self.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_ALWAYS)
        self.tv = DropTextView(statusbar)
        self.add_with_viewport(self.tv)
        self.show_all()

    def get_textview(self):
        return self.tv
