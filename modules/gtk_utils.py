#!/usr/bin/env python

###################################################################################
# @file gtk_win.py
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

import pygtk
import gobject
pygtk.require('2.0')
import gtk


def create_stock_button(stock):
    image = gtk.Image()
    image.set_from_stock(stock, gtk.ICON_SIZE_BUTTON)
    button = gtk.Button()
    button.add(image)
    image.show()
    return button

def create_label(text):
    label = gtk.Label(text)
    label.set_justify(gtk.JUSTIFY_LEFT)
    label.set_alignment(0, 0.5)
    return label

def show_error_box(error):
    message = gtk.MessageDialog(type=gtk.MESSAGE_ERROR, buttons=gtk.BUTTONS_OK)
    message.set_markup(error)
    message.run()
    message.destroy()

def show_confirm_box(text):
    message = gtk.MessageDialog(None,
                                gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT, 
                                gtk.MESSAGE_QUESTION, 
                                gtk.BUTTONS_YES_NO,
                                None)
    message.set_markup(text)
    message.run()
    response = message.run()
    result = False
    if response == gtk.RESPONSE_YES: result = True
    message.destroy()
    return result

