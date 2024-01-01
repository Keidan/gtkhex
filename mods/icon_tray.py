###################################################################################
# @file icon_tray.py
# @author Keidan (Kevin Billonneau)
# @par Copyright GNU GENERAL PUBLIC LICENSE Version 3
###################################################################################

from gi.repository import Gtk


class IconTray:
    def __init__(self, appname, iconname):
        self.menu = Gtk.Menu()
        self.status_icon = Gtk.StatusIcon()
        self.status_icon.set_from_icon_name(iconname)
        self.status_icon.connect('popup-menu', self.right_click_event_statusicon)

    def add_menu_item(self, command, title):
        menu_item = Gtk.MenuItem()
        menu_item.set_label(title)
        menu_item.connect('activate', command)

        self.menu.append(menu_item)
        self.menu.show_all()

    def add_seperator(self):
        menu_item = Gtk.SeparatorMenuItem()
        self.menu.append(menu_item)
        self.menu.show_all()

    def get_tray_menu(self):
        return self.menu

    def right_click_event_statusicon(self, icon, button, time):
        menu = self.get_tray_menu()
        menu.popup(None, None, None, self.status_icon, button, time)

