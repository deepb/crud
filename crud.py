#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk


class Manejadores:
    def __init__(self):
        self.__valor = True

    def onDeleteWindow(self, *args):
        Gtk.main_quit(*args)

    def onButtonPressed(self, button):
        print("Hello World!")

    def onButtonClick(self, button):
        if self.__valor:
            self.__btnLabel = button.get_label()
            button.set_label("Contenido nuevo")
            self.__valor = False
        else:
            self.__btnLabel = button.get_label()
            button.set_label("button2")
            self.__valor = True
        print self.__btnLabel

    def ventana_quit(self, *args):
        Gtk.main_quit(*args)


class Ventana(Gtk.Window):

    def __init__(self):
        Gtk.Window.__init__(self, title="Hola Mundo!")

        self.button = Gtk.Button(label="Hazme click")
        self.button.connect("clicked", self.on_button_clicked)
        self.add(self.button)

    def on_button_clicked(self, widget):
        print("Hola Mundo!")


def main():
    b = Gtk.Builder()
    b.add_from_file('ui/crud.glade')
    # builder.add_objects_from_file(“interfaz.glade”, (“ventana1”,”boton1”, “boton2”))
    b.connect_signals(Manejadores())

    win = Ventana()
    win.connect('delete-event', Gtk.main_quit)
    win.show_all()
    Gtk.main()

main()

