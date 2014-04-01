###################################################################################
# @file TabLabel.py
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

class TabLabel(gtk.Box):
    __gsignals__ = {
        "close-clicked": (gobject.SIGNAL_RUN_FIRST, gobject.TYPE_NONE, ()),
    }
    def __init__(self, label_text):
        gtk.Box.__init__(self)
        self.set_orientation(gtk.ORIENTATION_HORIZONTAL)
        self.set_spacing(5) # spacing: [icon|5px|label|5px|close]  
        
        # icon
        icon = gtk.Image()
        icon.set_from_stock(gtk.STOCK_FILE, gtk.ICON_SIZE_MENU)
        self.pack_start(icon, False, False, 0)
        
        # label 
        self.label = gtk.Label(label_text)
        self.pack_start(self.label, True, True, 0)
        
        # close button
        button = gtk.Button()
        button.set_relief(gtk.RELIEF_NONE)
        button.set_focus_on_click(False)
        im = gtk.Image()
        im.set_from_stock(gtk.STOCK_CLOSE, gtk.ICON_SIZE_MENU)
        button.add(im)
        button.connect("clicked", self.button_clicked)
        #data =  ".button {\n" \
        #        "-GtkButton-default-border : 0px;\n" \
        #        "-GtkButton-default-outside-border : 0px;\n" \
        #        "-GtkButton-inner-border: 0px;\n" \
        #        "-GtkWidget-focus-line-width : 0px;\n" \
        #        "-GtkWidget-focus-padding : 0px;\n" \
        #        "padding: 0px;\n" \
        #        "}"
        #provider = gtk.CssProvider()
        #provider.load_from_data(data)
        # 600 = GTK_STYLE_PROVIDER_PRIORITY_APPLICATION
        #button.get_style_context().add_provider(provider, 600) 
        self.pack_start(button, False, False, 0)
        self.show_all()

    def set_tab_text(self, label_text):
        self.label.set_text(label_text)

    def button_clicked(self, button, data=None):
        self.emit("close-clicked")


