#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
file: crud.py $Date$
version: $Id$

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

        self.b = Gtk.Builder()
        self.b.add_from_file('ui/crud.glade')
        
        # Ventanas
        self.ventana = self.b.get_object("winBBDD")
        self.acerca = self.b.get_object("dlgAcerca")
        self.registro = self.b.get_object("winRegistro")
        
        # Objetos
        self.btnCreate = self.b.get_object("btnCreate")
        self.btnRead = self.b.get_object("btnRead")
        self.btnUpdate = self.b.get_object("btnUpdate")
        self.btnDelete = self.b.get_object("btnDelete")
        
        self.mnuCreate = self.b.get_object("mnuCreate")
        self.mnuRead = self.b.get_object("mnuRead")
        self.mnuUpdate = self.b.get_object("mnuUpdate")
        self.mnuDelete = self.b.get_object("mnuDelete")

        self.status = self.b.get_object("staStatus")
        self._cid = self.status.get_context_id("CRUD")
        
        # Datos
        self.model = self.b.get_object("lsCrud")
        self.list = self.b.get_object("treBBDD")
        self.model.clear()
        self.select = self.list.get_selection()
        self.select.connect("changed", self.changedSelect)
        
        # Handlers
        self._handlers = {
            "onDeleteWindow": self.deleteWindow,
            "on_btnCreate_clicked": self.onNewRecord, 
            "on_btnRead_clicked": self.refreshDB, 
            "on_btnUpdate_clicked": self.onEditRecord, 
            "on_btnDelete_clicked": self.deleteRecord, 
            "on_btnExit_clicked": self.deleteWindow, 
            "on_mnuCreateDB_activate": self.createDB, 
            "on_mnuDropDB_activate": self.removeDB, 
            "on_mnuCreate_activate": self.onNewRecord, 
            "on_mnuRead_activate": self.refreshDB, 
            "on_mnuUpdate_activate": self.onEditRecord, 
            "on_mnuDelete_activate": self.deleteRecord, 
            "on_mnuAbout_activate": self.onOpenAbout, 
            "on_mnuQuit_activate": self.deleteWindow,
            "on_dlgAcerca_response": self.onCloseAbout,
            "on_btnCancel_clicked": self.onCloseRegistro, 
            "on_btnAdd_clicked": self.addRecord,
            "on_btnUpt_clicked": self.updateRecord
        }
        self.b.connect_signals(self._handlers)
        
        # Init BBDD
        self.initDB()
        # DEBUG
        #self.removeDB()
        # DEBUG
        #self.createDB()
        # DEBUG
        #self.populateDB()
        self.refreshDB()
        
        # Init
        self.setId(None)
        self.setRow(None)
        self.ventana.resize(200, 300)
        self.ventana.show_all()
        return Gtk.main()
        
    def updateStatus(self, *args):
        self.status.push(self._cid, *args)
    
    # Bases de datos
    def setDB(self, db, *args):
        self._db = db
    
    def getDB(self, *args):
        return self._db

    def commitDB(self, *args):
        return self._db.commit()
    
    def cursorDB(self, *args):
        return self._db.cursor()
    
    def initDB(self, *args):
        self.disable(self.btnUpdate)
        self.disable(self.mnuUpdate)
        self.disable(self.btnDelete)
        self.disable(self.mnuDelete)
        try:
            self.setDB(db.connect(db_host, db_user, db_pass, db_data))
        except:
            self.disable(self.btnCreate)
            self.disable(self.mnuCreate)
            self.disable(self.btnRead)
            self.disable(self.mnuRead)
            self.setDB(None)
            self.updateStatus("Error MySQL: Revisa los datos de conexión")

    def talkDB(self, query, many=False):
        cursor = self.cursorDB()
        try:
            cursor.execute(query)
            if many:
                data = cursor.fetchall()
            else:
                data = cursor.fetchone()
            cursor.close()
            self.commitDB()
            return data
        except:
            self.updateStatus("Error: %s" % query)
    
    def populateDB(self, *args):
        if self.getDB() is not None:
            for a in range(50):
                self.talkDB("INSERT INTO Crud (Nombre, Apellidos, DNI, Vivienda) " \
                    "VALUES ('%s', '%s', '%s', '%s')" % 
                    (a, a, a, a))
        else:
            self.updateStatus("Error: BBDD no populada")
            
    def createDB(self, *args):
        query = "CREATE TABLE IF NOT EXISTS "\
                    "Crud (id INT PRIMARY KEY AUTO_INCREMENT NOT NULL, "\
                    "Nombre VARCHAR(100) NOT NULL, "\
                    "Apellidos VARCHAR(100) NOT NULL, "\
                    "DNI VARCHAR(9), "\
                    "Vivienda VARCHAR(100))"
        try:
            self.talkDB(query)
            self.enable(self.btnCreate)
            self.enable(self.mnuCreate)
            self.enable(self.btnRead)
            self.enable(self.mnuRead)            
            self.updateStatus("BBDD creada")
        except:
            self.updateStatus("Error: BBDD no creada")

    def removeDB(self, *args):
        if self.getDB() is not None:
            query = "DROP TABLE Crud"
            self.talkDB(query)
            self.disable(self.btnCreate)
            self.disable(self.mnuCreate)
            self.disable(self.btnRead)
            self.disable(self.mnuRead)

            self.refreshDB()
            self.updateStatus("BBDD eliminada")
        else:
            self.updateStatus("Error: BBDD no eliminada")
    
    def refreshDB(self, *args):
        if self.getDB() is not None:
            query = "SELECT id, Nombre, Apellidos, DNI, Vivienda FROM Crud WHERE 1"
            data = self.talkDB(query, True)
            self.model.clear()
            if data:
                for row in data:
                    self.model.append([ row[0], row[1], row[2], row[3], row[4] ])
            else:
                self.disable(self.btnUpdate)
                self.disable(self.mnuUpdate)
                self.disable(self.btnDelete)
                self.disable(self.mnuDelete)
                self.updateStatus("Base de datos vacía")
        else:
            self.disable(self.btnUpdate)
            self.disable(self.mnuUpdate)
            self.disable(self.btnDelete)
            self.disable(self.mnuDelete)
            self.model.clear()
            self.updateStatus("No hay base de datos. Comprueba la conexion.")
            
    def getId(self, *args):
        return self._id
    
    def setId(self, id, *args):
        self._id = id
    
    def getRow(self, *args):
        return self._row
    
    def setRow(self, row, *args):
        self._Row = row
    
    def addRecord(self, *args):
        nombre = self.b.get_object("txtNombre").get_text()
        apellidos = self.b.get_object("txtApellidos").get_text()
        dni = self.b.get_object("txtDNI").get_text()
        vivienda = self.b.get_object("txtVivienda").get_text()
        if len(nombre) and \
            len(apellidos) and \
            len(dni) and \
            len(vivienda):
            self.talkDB("INSERT INTO Crud (Nombre, Apellidos, DNI, Vivienda) " \
                    "VALUES ('%s', '%s', '%s', '%s')" % 
                    (nombre, apellidos, dni, vivienda))
            self.onCloseRegistro()
            self.refreshDB()
        else:
            self.updateStatus("Registro incompleto")

    def updateRecord(self, *args):
        self.disable(self.b.get_object("txtId"))
        id = self.b.get_object("txtId").get_text()
        nombre = self.b.get_object("txtNombre").get_text()
        apellidos = self.b.get_object("txtApellidos").get_text()
        dni = self.b.get_object("txtDNI").get_text()
        vivienda = self.b.get_object("txtVivienda").get_text()
        if len(nombre) and \
            len(apellidos) and \
            len(dni) and \
            len(vivienda):
            self.talkDB("UPDATE Crud SET Nombre='%s', " \
                    "Apellidos='%s', DNI='%s', Vivienda='%s' " \
                    "WHERE id=%s" % (nombre, apellidos, dni, vivienda, id))
            self.onCloseRegistro()
            self.refreshDB()
        else:
            self.updateStatus("Registro incompleto")

    def deleteRecord(self, *args):
        self.disable(self.btnUpdate)
        self.disable(self.mnuUpdate)
        self.disable(self.btnDelete)
        self.disable(self.mnuDelete)
        id = self.getId()
        if id is not None:
            self.talkDB("DELETE FROM Crud WHERE id=%s" % id)
            self.refreshDB()
            self.setId(None)
            self.updateStatus("Registro eliminado")
        else:
            self.updateStatus("Selecciona un registro")
    
    def changedSelect(self, tree):
        self.enable(self.btnUpdate)
        self.enable(self.mnuUpdate)
        self.enable(self.btnDelete)
        self.enable(self.mnuDelete)
        model, path = tree.get_selected_rows()
        for p in path:
            t = model.get_iter(p)
            v = model.get_value(t, 0)
            #print v, t, p
            self.setRow(p)
            self.setId(v)
    
    # Ventanas
    def disable(self, widget):
        widget.set_sensitive(False)
    def enable(self, widget):
        widget.set_sensitive(True)
        
    def onOpenAbout(self, *args):
        self.acerca.show()
    def onCloseAbout(self, *args):
        self.acerca.hide()

    def onEditRecord(self, *args):
        # Editar registro
        id = self.getId()
        if id is not None:
            self.b.get_object("txtId").set_visible(True)
            self.b.get_object("lblId").set_visible(True)
            self.b.get_object("btnAdd").set_visible(False)
            self.b.get_object("btnUpd").set_visible(True)
            
            query = "SELECT Nombre, Apellidos, DNI, Vivienda FROM Crud WHERE id=%s" % id
            nombre, apellidos, dni, vivienda = self.talkDB(query)
            self.b.get_object("txtId").set_text(str(id))
            self.b.get_object("txtNombre").set_text(nombre)
            self.b.get_object("txtApellidos").set_text(apellidos)
            self.b.get_object("txtDNI").set_text(dni)
            self.b.get_object("txtVivienda").set_text(vivienda)
            self.registro.show()
        else:
            self.updateStatus("Selecciona un registro")
        
    def onNewRecord(self, *args):
        # Agregar un registro nuevo
        self.b.get_object("txtId").set_visible(False)
        self.b.get_object("lblId").set_visible(False)
        self.b.get_object("btnAdd").set_visible(True)
        self.b.get_object("btnUpd").set_visible(False)
        
        self.b.get_object("txtId").set_text('')
        self.b.get_object("txtNombre").set_text('')
        self.b.get_object("txtApellidos").set_text('')
        self.b.get_object("txtDNI").set_text('')
        self.b.get_object("txtVivienda").set_text('')
        self.registro.show()
        
    def onCloseRegistro(self, *args):
        # self.updateStatus('')
        # Ocultar
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
