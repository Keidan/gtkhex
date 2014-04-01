###################################################################################
# @file const.py
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
    def STATUSBAR_TEXT_IDX(): return 0
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
    def NOTEBOOK_NAME(): return "nbFiles"
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
