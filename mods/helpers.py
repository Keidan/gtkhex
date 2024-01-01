###################################################################################
# @file helpers.py
# @author Keidan (Kevin Billonneau)
# @par Copyright GNU GENERAL PUBLIC LICENSE Version 3
###################################################################################

import string
from gi.repository import Gtk
from consts import CONST


class UIHelper:
    # simple confirm box in pygtk
    @staticmethod
    def gtk_confirm_box(text):
        md = Gtk.MessageDialog(
            None,
            Gtk.DialogFlags.MODAL | Gtk.DialogFlags.DESTROY_WITH_PARENT,
            Gtk.MessageType.QUESTION,
            Gtk.ButtonsType.YES_NO,
            None,
        )
        md.set_markup(text)
        response = md.run()
        result = False
        if response == Gtk.ResponseType.YES:
            result = True
        md.destroy()
        return result

    # simple file chooser box in pygtk
    @staticmethod
    def gtk_file_chooser(title, action):
        chooser = Gtk.FileChooserDialog(
            title=title,
            action=action,
            buttons=(
                Gtk.STOCK_CANCEL,
                Gtk.ResponseType.CANCEL,
                Gtk.STOCK_OPEN,
                Gtk.ResponseType.OK,
            ),
        )
        chooser.set_default_response(Gtk.ResponseType.OK)
        ffilter = Gtk.FileFilter()
        ffilter.set_name("All Files")
        ffilter.add_pattern("*.*")
        ffilter.add_pattern("*")
        chooser.add_filter(ffilter)
        response = chooser.run()
        if response == Gtk.ResponseType.OK:
            current_file = chooser.get_filename()
            chooser.destroy()
            return True, current_file
        chooser.destroy()
        return False, None


class SysHelper:
    @staticmethod
    def format_data_buffer(buffer):
        li = list("".join(buffer.get_full_text().split()))
        result = ""
        i = 0
        line = 0
        length = len(li)
        while i < length:
            result += f"{li[i]}"
            i += 1
            if i < length:
                result += f"{li[i]}"
                i += 1
            result += " "
            if line == CONST.max_char_by_line() - 1:
                line = 0
                result += "\n"
            else:
                line += 1
            if not line % CONST.max_char_by_segment() and line != 0:
                result += " "
        del li[:]
        buffer.set_text(result.strip())

    # translate text data to hex representation
    @staticmethod
    def data_to_hex(content):
        li = list(content)
        result = ""
        i = 0
        for l in li:
            result += f"{l:02x} "
            if i == CONST.max_char_by_line() - 1:
                i = 0
                result += "\n"
            else:
                i += 1
            if not i % CONST.max_char_by_segment() and i != 0:
                result += " "
        del li[:]
        return result.strip()

    @staticmethod
    def is_hex(s):
        hex_digits = set(string.hexdigits)
        # if s is long, then it is faster to check against a set
        return all(c in hex_digits for c in s)

    # translate text hex to data representation
    @staticmethod
    def hex_to_data(content):
        li = content.split(" ")
        result = bytearray()
        for l in li:
            l = l.strip()
            if l == " " or l == "\r" or l == "\n" or not len(l):
                continue
            if not SysHelper.is_hex(l):
                return None
            try:
                result.extend(bytes.fromhex(l))
            except Exception:
                return None
        return result

    @staticmethod
    def copy_from_clipbard(clipboard, buffer):
        if buffer == None:
            return
        content = clipboard.wait_for_text()
        if content == None:
            return
        li = content.split(" ")
        all_done = False
        for l in li:
            l = l.strip()
            if l == " " or not len(l):
                continue
            if not SysHelper.is_hex(l):
                all_done = False
                break
            all_done = True
        if not all_done:
            content = SysHelper.data_to_hex(content)
        if not content.endswith(" "):
            content += " "
        buffer.insert_at_cursor(content)
