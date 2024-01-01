###################################################################################
# @file tab_label.py
# @author Keidan (Kevin Billonneau)
# @par Copyright GNU GENERAL PUBLIC LICENSE Version 3
###################################################################################


from gi.repository import Gtk
from gi.repository import GObject


class TabLabel(Gtk.Box):
    __gsignals__ = {
        'close-clicked': (GObject.SIGNAL_RUN_FIRST, GObject.TYPE_NONE, ()),
    }

    def __init__(self, label_text):
        Gtk.Box.__init__(self)
        self.set_orientation(Gtk.Orientation.HORIZONTAL)
        self.set_spacing(5)  # spacing: [icon|5px|label|5px|close]

        # icon
        icon = Gtk.Image()
        icon.set_from_stock(Gtk.STOCK_FILE, Gtk.IconSize.MENU)
        self.pack_start(icon, False, False, 0)

        # label
        self.label = Gtk.Label(label_text)
        self.pack_start(self.label, True, True, 0)

        # close button
        button = Gtk.Button()
        button.set_relief(Gtk.ReliefStyle.NONE)
        button.set_focus_on_click(False)
        im = Gtk.Image()
        im.set_from_stock(Gtk.STOCK_CLOSE, Gtk.IconSize.MENU)
        button.add(im)
        button.connect('clicked', self.button_clicked)
        self.pack_start(button, False, False, 0)
        self.show_all()

    def set_tab_text(self, label_text):
        self.label.set_text(label_text)

    def get_tab_text(self):
        return self.label.get_text()

    def button_clicked(self, button, data=None):
        self.emit('close-clicked')
