#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
import MySQLdb

class Aplicacion:
    def __init__(self):

        self.b = Gtk.Builder()
        self.b.add_from_file('ui/crud.glade')

        self._handlers = {
            "onDeleteWindow": self.deleteWindow,
            "on_btnCreate_clicked": self.createBBDD, 
            "on_btnRemove_clicked": self.removeBBDD, 
            "on_btnUpdate_clicked": self.updateRecord, 
            "on_btnDelete_clicked": self.deleteRecord, 
            "on_btnAbout_clicked": self.onOpenAbout, 
            "on_btnExit_clicked": self.deleteWindow, 
            "on_create_item_activate": self.createBBDD, 
            "on_remove_item_activate": self.removeBBDD, 
            "on_update_item_activate": self.updateRecord, 
            "on_delete_item_activate": self.deleteRecord, 
            "on_mnuAbout_activate": self.onOpenAbout, 
            "on_mnuQuit_activate": self.deleteWindow
        }
        self.b.connect_signals(self._handlers)

        self.ventana = self.b.get_object("winBBDD")
        self.acerca = self.b.get_object("dlgAcerca")
        self.status = self.b.get_object("staStatus")
        self._id = self.status.get_context_id("CRUD")
        self.record = self.b.get_object("lsCRUD")

        self.ventana.resize(200, 300)
        self.ventana.show_all()

    def updateStatus(self, *args):
        self.status.push(self._id, *args)

    def deleteWindow(self, *args):
        Gtk.main_quit(*args)

    def createBBDD(self, *args):
        self.updateStatus("Creada BBDD")

    def removeBBDD(self, *args):
        self.updateStatus("Eliminada BBDD")

    def updateRecord(self, *args):
        self.updateStatus("Registro actualizado")

    def deleteRecord(self, *args):
        self.updateStatus("Registro eliminado")

    def onOpenAbout(self, *args):
        self.acerca.show()

    def onCloseAbout(self, *args):
        self.acerca.hide()

        
def main():
    Aplicacion()
    Gtk.main()
    return 0

if __name__ == '__main__':
    main()

