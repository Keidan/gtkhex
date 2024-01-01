###################################################################################
# @file Consts.py
# @author Keidan (Kevin Billonneau)
# @par Copyright GNU GENERAL PUBLIC LICENSE Version 3
###################################################################################


class _Const(object):
    def max_redo(self):
        return 255

    def max_undo(self):
        return 255

    def statusbar_text_idx(self):
        return 0

    def max_char_by_segment(self):
        return 8

    def max_char_by_line(self):
        return 32

    def default_font(self):
        return 'Courier 10'

    def imi_new_name(self):
        return 'imiNew'

    def imi_open_name(self):
        return 'imiOpen'

    def imi_save_name(self):
        return 'imiSave'

    def imi_quit_name(self):
        return 'imiQuit'

    def imi_undo_name(self):
        return 'imiUndo'

    def imi_redo_name(self):
        return 'imiRedo'

    def imi_cut_name(self):
        return 'imiCut'

    def imi_copy_name(self):
        return 'imiCopy'

    def imi_copy_raw_name(self):
        return 'imiCopyRaw'

    def imi_paste_name(self):
        return 'imiPaste'

    def imi_select_all_name(self):
        return 'imiSelectAll'

    def imi_format_name(self):
        return 'imiFormat'

    def imi_find_name(self):
        return 'imiFind'

    def imi_replace_name(self):
        return 'imiReplace'

    def tb_undo_name(self):
        return 'tbUndo'

    def tb_redo_name(self):
        return 'tbRedo'

    def window_name(self):
        return 'appwindow'

    def statusbar_name(self):
        return 'sb'

    def progressbar_name(self):
        return 'pb'

    def notebook_name(self):
        return 'nbFiles'

    def about_dialog_name(self):
        return 'about_dialog'
    
    def find_dialog_name(self):
        return 'find_dialog'

    def find_entry_name(self):
        return 'find_entry'

    def find_all_name(self):
        return 'find_all'

    def replace_dialog_name(self):
        return 'replace_dialog'

    def replace_entry_name(self):
        return 'replace_entry'

    def replace_find_entry_name(self):
        return 'replace_find_entry'


CONST = _Const()
