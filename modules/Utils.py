###################################################################################
# @file Utils.py
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

import string
import gtk
from Const import *

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
    filter.add_pattern("*")
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
        l = l.strip()
        if l == ' ' or l == '\r' or l == '\n' or not len(l): continue
        if not is_hex(l): return None
        try: result += l.decode('hex')
        except: return None
    return result

def copy_from_clipbard(clipboard, buffer):
    if buffer == None: return
    content = clipboard.wait_for_text()
    if content == None: return
    li = content.split(" ")
    all_done = False
    for l in li:
        l = l.strip()
        if l == ' ' or not len(l): continue
        if not is_hex(l):
            all_done = False
            break
        all_done = True
    if not all_done: content = data_to_hex(content)
    if not content.endswith(" "): content += " "
    buffer.insert_at_cursor(content)
        
