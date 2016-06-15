#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
file: crud.py $Id$
version: 0.0001 $Date$

    LICENCIA PÚBLICA PARA QUE HAGA LO QUE LE DÉ LA GANA
                    Versión 2, diciembre de 2004
 
 Derechos de autor (C) 2004 Sam Hocevar
  14 rue de Plaisance, 75014 París, Francia
 Se permite la copia y distribución de forma literal o modificada
 copias de este documento de licencia, y su modificación están permitidas siempre
 que el se cambie el nombre.
 
            LICENCIA PÚBLICA PARA QUE HAGA LO QUE LE DÉ LA GANA
   TÉRMINOS Y CONDICIONES PARA LA COPIA, DISTRIBUCIÓN & MODIFICACIÓN
 
  0. Eso sí, HAGA LO QUE LE DÉ LA GANA.
"""

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
import MySQLdb as db

# Database 
db_host = "localhost"
db_user = "crud"
db_pass = "crud"
db_data = "CRUD"

class Aplicacion(Gtk.Window):
    """
    Clase Aplicacion
    """
    def __init__(self):

        b = Gtk.Builder()
        b.add_from_file('ui/crud.glade')
        
        # Ventanas
        self.ventana = b.get_object("winBBDD")
        self.acerca = b.get_object("dlgAcerca")
        self.registro = b.get_object("winRegistro")
        
        # Objetos
        self.btnCreate = b.get_object("btnCreate")
        self.btnRemove = b.get_object("btnRemove")
        self.btnUpdate = b.get_object("btnUpdate")
        self.btnDelete = b.get_object("btnDelete")
        
        self.mnuCreate = b.get_object("mnuCreate")
        self.mnuRemove = b.get_object("mnuRemove")
        self.mnuUpdate = b.get_object("mnuUpdate")
        self.mnuDelete = b.get_object("mnuDelete")

        self.status = b.get_object("staStatus")
        self._id = self.status.get_context_id("CRUD")
        
        # Datos
        self.model = b.get_object("lsCrud")
        self.list = b.get_object("treBBDD")

        # Handlers
        self._handlers = {
            "onDeleteWindow": self.deleteWindow,
            "on_btnCreate_clicked": self.createBBDD, 
            "on_btnRemove_clicked": self.removeBBDD, 
            "on_btnUpdate_clicked": self.onOpenRegistro, 
            "on_btnDelete_clicked": self.deleteRecord, 
            "on_btnAbout_clicked": self.onOpenAbout, 
            "on_btnExit_clicked": self.deleteWindow, 
            "on_mnuCreate_activate": self.createBBDD, 
            "on_mnuRemove_activate": self.removeBBDD, 
            "on_mnuUpdate_activate": self.onOpenRegistro, 
            "on_mnuDelete_activate": self.deleteRecord, 
            "on_mnuAbout_activate": self.onOpenAbout, 
            "on_mnuQuit_activate": self.deleteWindow,
            "on_dlgAcerca_response": self.onCloseAbout,
            "on_tsSelect_changed": self.changedRecord, 
            "on_treNombre_edited": self.updateRecord, 
            "on_treApellidos_edited": self.updateRecord, 
            "on_treDNI_edited": self.updateRecord, 
            "on_treVivienda_edited": self.updateRecord, 
            "on_btnCancel_clicked": self.onCloseRegistro, 
            "on_btnAdd_clicked": self.updateRecord
        }
        b.connect_signals(self._handlers)
        
        
        # Init BBDD
        self.initBBDD()
        
        self.ventana.resize(200, 300)
        self.ventana.show_all()
        return Gtk.main()
        
    def updateStatus(self, *args):
        self.status.push(self._id, *args)

    # Bases de datos
    def initBBDD(self, *args):
        self.disable(self.btnRemove)
        self.disable(self.mnuRemove)
        self.disable(self.btnUpdate)
        self.disable(self.btnDelete)
        self.disable(self.mnuUpdate)
        self.disable(self.mnuDelete)
        try:
            self.db = db.connect(db_host, db_user, db_pass, db_data)
        except:
            self.db = None
            self.updateStatus("Error MySQL: Revisa los datos de conexión")

    def createBBDD(self, *args):
        query = "CREATE TABLE IF NOT EXISTS "\
                    "Crud (id INT PRIMARY KEY AUTO_INCREMENT, "\
                    "Nombre VARCHAR(100) NOT NULL, "\
                    "Apellidos VARCHAR(100) NOT NULL, "\
                    "DNI VARCHAR(9), "\
                    "Vivienda VARCHAR(100))"
        try:
            cursor = self.db.cursor()
            cursor.execute(query)
            self.enable(self.btnRemove)
            self.enable(self.mnuRemove)
            self.disable(self.btnCreate)
            self.disable(self.mnuCreate)
            self.updateStatus("BBDD creada")
        except:
            self.updateStatus("Error: BBDD no creada")

    def removeBBDD(self, *args):
        if self.db is not None:
            query = "DROP TABLE Crud"
            cursor = self.db.cursor()
            cursor.execute(query)
            self.disable(self.btnRemove)
            self.disable(self.mnuRemove)
            self.enable(self.btnCreate)
            self.enable(self.mnuCreate)
            self.updateStatus("BBDD Eliminada")
        else:
            self.updateStatus("Error: BBDD no eliminada")

    def updateRecord(self, *args):
        self.onCloseRegistro()
        self.updateStatus("Registro actualizado")

    def deleteRecord(self, *args):
        self.disable(self.btnDelete)
        self.disable(self.mnuDelete)
        self.updateStatus("Registro eliminado")

    def changedRecord(self, *args):
        self.enable(self.btnUpdate)
        self.enable(self.mnuUpdate)
        self.enable(self.btnDelete)
        self.enable(self.mnuDelete)
        self.updateStatus("Cambiado registro")

    # Ventanas
    def disable(self, widget):
        widget.set_sensitive(False)
    def enable(self, widget):
        widget.set_sensitive(True)
        
    def onOpenAbout(self, *args):
        self.acerca.show()
    def onCloseAbout(self, *args):
        self.acerca.hide()
    def onOpenRegistro(self, *args):
        self.registro.show()
    def onCloseRegistro(self, *args):
        self.registro.hide()

    # Ventana principal
    def deleteWindow(self, *args):
        self.ventana.hide()
        Gtk.main_quit(*args)

# main
def main():
    return Aplicacion()

if __name__ == '__main__':
    main()

