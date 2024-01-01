#!/usr/bin/env python

###################################################################################
# @file gtkhex.py
# @author Keidan (Kevin Billonneau)
# @par Copyright GNU GENERAL PUBLIC LICENSE Version 3
###################################################################################


import sys, os, inspect, datetime

# get the current folder
current_folder = os.path.realpath(
    os.path.abspath(os.path.split(inspect.getfile(inspect.currentframe()))[0])
)
# include modules from a subforder
cmd_subfolder = os.path.join(current_folder, 'mods')
if cmd_subfolder not in sys.path:
    sys.path.append(cmd_subfolder)

import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from gi.repository import GdkPixbuf
from consts import CONST
from handlers import Handlers
from icon_tray import IconTray

APPLICATION_VERSION = '1.0.1'

class gtkhex:
    def __init__(self):
        self.icon_path = os.path.join(current_folder, 'icon.png')
        # Set the Glade file
        gladefile = os.path.join(current_folder, 'gtkhex.glade')
        builder = Gtk.Builder()
        builder.add_from_file(gladefile)
        # get objects
        window = builder.get_object(CONST.window_name())
        window.set_icon_from_file(self.icon_path)
        sb = builder.get_object(CONST.statusbar_name())
        # init
        sb.push(CONST.statusbar_text_idx(), 'Ln 1, Col: 0, 0%')
        # system tray
        tray = IconTray(window.get_title(), 'document-edit')
        tray.add_menu_item(lambda x: self.handlers.show_hide_window(x), 'Hide')
        tray.add_menu_item(lambda x: self.handlers.on_about(x), 'About')
        tray.add_seperator()
        tray.add_menu_item(lambda x: self.handlers.on_quit(x), 'Quit')

        # connect handlers
        self.handlers = Handlers(builder)
        window.add_accel_group(self.handlers.get_accel_group())
        builder.connect_signals(self.handlers)
        self.install_about_info()

        # Show the window
        window.show_all()

    def load_file(self, filename):
        self.handlers.open_file(filename)

    def main(self):
        Gtk.main()

    def install_about_info(self):
        today = datetime.date.today()
        about = self.handlers.get_dialog_about()
        about.set_copyright(f'Copyright © 2014 - {today.year}')
        about.set_comments('GtkHex is a simple hexadecimal editor.')
        about.set_website_label('GitHub')
        about.set_website('https://github.com/Keidan/gtkhex')
        about.set_license(
            'This program is provided without warranty of any kind.\nFor more information, visit GNU General Public License, version 3 or later.\nhttps://www.gnu.org/licenses/gpl-3.0.html'
        )
        about.set_authors(['Keidan'])
        pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_size(self.icon_path, 48, 48)
        about.set_logo(pixbuf)
        about.set_version(APPLICATION_VERSION)


def main(argv):
    win = gtkhex()
    if len(sys.argv) == 2:
        win.load_file(argv[0])
    win.main()


if __name__ == '__main__':
    main(sys.argv[1:])
