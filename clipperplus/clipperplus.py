# -*- coding: utf-8 -*-
# ex:set ts=4 et sw=4 ai:

##
# clipperplus.py
# This plugin integrates with the Clipper+ Android Application
# https://play.google.com/store/apps/details?id=fi.rojekti.clipper
#
# Plugin (C) 2014 Austin Riba <root@austinriba.com>
#
# Diodon - GTK+ clipboard manager.
# Copyright (C) 2011 Diodon Team <diodon-team@lists.launchpad.net>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published
# by the Free Software Foundation, either version 2 of the License, or (at
# your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY
# or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public
# License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
##

from gi.repository import GObject, Gtk, Peas, PeasGtk, Diodon
import os
import ConfigParser


class ClipperPlusPlugin(GObject.Object, Peas.Activatable, PeasGtk.Configurable):
    __gtype_name__ = 'ClipperPlusPlugin'

    object = GObject.property(type=GObject.Object)

    def __init__(self):
        self.config = ConfigParser.ConfigParser()
        self.config.read([os.environ['HOME'] + '/.local/share/diodon/plugins/clipperplus/config.cfg'])
        self.username = self.config.get('DEFAULT', 'username')
        self.password = self.config.get('DEFAULT', 'password')

    def do_create_configure_widget(self):
        grid = Gtk.Grid()

        title = Gtk.Label("Clipper+ Login")
        username_label = Gtk.Label("Username: ")
        self.username_entry = Gtk.Entry()
        self.username_entry.set_text(self.username)

        password_label = Gtk.Label("Password: ")
        self.password_entry = Gtk.Entry()
        self.password_entry.set_visibility(False)
        self.password_entry.set_text(self.password)

        button = Gtk.Button("Save")
        button.connect("clicked", self.do_save_configure)

        grid.attach(title, 0, 0, 2, 1)
        grid.attach(username_label, 0, 1, 1, 1)
        grid.attach_next_to(self.username_entry, username_label, Gtk.PositionType.RIGHT, 1, 1)
        grid.attach(password_label, 0, 2, 1, 1)
        grid.attach_next_to(self.password_entry, password_label, Gtk.PositionType.RIGHT, 1, 1)
        grid.attach(button, 0, 3, 2, 1)

        return grid

    def do_save_configure(self, arg):
        self.username = self.username_entry.get_text()
        self.password = self.password_entry.get_text()

        self.config.set('DEFAULT', 'username', self.username)
        self.config.set('DEFAULT', 'password', self.password)
        with open(os.environ['HOME'] + '/.local/share/diodon/plugins/clipperplus/config.cfg', 'wb') as configfile:
            self.config.write(configfile)

    def do_activate(self):
        controller = self.object
        controller.add_as_text_item(Diodon.ClipboardType.PRIMARY,
            "Clipper+ Integration")

        self.add_menu_items()

    def do_deactivate(self):
        controller = self.object

    def do_update_state(self):
        pass

    def add_menu_items(self):
        controller = self.object
        menu = controller.get_menu()

        sep = Gtk.SeparatorMenuItem.new()
        select_from_clipper = Gtk.MenuItem.new_with_label("Select last from Clipper")
        upload_to_clipper = Gtk.MenuItem.new_with_label("Upload Selected to Clipper")

        select_from_clipper.connect("activate", self.do_select_from_clipper)
        upload_to_clipper.connect("activate", self.do_upload_to_clipper)

        menu.append(sep)
        menu.append(select_from_clipper)
        menu.append(upload_to_clipper)

        menu.show_all()

    def do_select_from_clipper(self, arg):
        print ("selecting from clipper")

    def do_upload_to_clipper(self, arg):
        print ("uploading to clipper")
