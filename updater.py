# -*- coding: utf-8 -*-
import sys
import os
import time
import requests
from PyQt5.QtWidgets import QMainWindow, QApplication, QLineEdit, QDialog, QLabel, QProgressBar, \
                             QMessageBox, QTableWidget,QTableWidgetItem, QHeaderView, QPushButton
from PyQt5.QtGui import QPixmap, QStandardItemModel
from PyQt5.QtPrintSupport import QPrinter
from PyQt5 import QtCore, QtGui

import gestion_appli
import view_interface

'''Défintion du comportement de l'application graphique'''
class Updater(QMainWindow):
    def __init__(self):
        super().__init__()
        self.infos = ['SAGEES Report', 'SAGEES Schooling', 'SAGEES Passage' , 'SAGEES Informer', 'SAGEES TimeTable', 'SAGEES BnR', 'Database']
        self.path = self.chemin_existant()
        self.ui = view_interface.Ui_MainWindow()
        self.online_version = gestion_appli.get_online_version('https://infolab-technologies.com/setup/')
        self.ui.setupUi(self)
        self.set_actions()
        self.ui.reloard_button.clicked.connect(lambda : self.reload())
        self.ui.quit_button.clicked.connect(lambda : self.close())


    ''' renvoie le chemin vers les installation de ilt'''
    def chemin_existant(self):
        for i in  ['C:\\Program Files (x86)\\INFOLAB Technologies', 'C:\\Program Files \\INFOLAB Technologies']:
            if os.path.exists(i):
                return i
        return ''

    def set_actions(self):
        if not os.path.exists('Downloads') :
            os.popen('mkdir Downloads')
        self.online_version = gestion_appli.get_online_version('https://infolab-technologies.com/setup/')
        self.rempli_table_view()

    def reload(self):
        self.setCursor(QtGui.QCursor(QtCore.Qt.WaitCursor))
        self.set_actions()
        self.setCursor(QtGui.QCursor())


    '''Remplissage des case de la colonne des versions en ligne'''
    def rempli_online_version(self):
        for i in range(self.ui.tableWidget.rowCount() - 1):
            name = self.infos[i].split(' ')[1]
            self.ui.tableWidget.setItem(i, 2, QTableWidgetItem(self.online_version[name][0] ))

    def telechargeur(self, url, progress_widget):
        '''Télégarger une ressource au bout de l'url dans le chemin '''
        try :
            if gestion_appli.connexion_on() :
                reponse = requests.get(url, stream = True)
                nom_fichier =  'Downloads/' + url.split('/')[-1]
                if reponse.status_code == requests.codes.ok:
                    with open(nom_fichier,'wb') as flux:
                        taille_fichier = int(reponse.headers.get('content-length'))
                        if taille_fichier is None:
                            flux.write(reponse.content)
                        else:
                            effectuer = 0
                            for partie in reponse.iter_content(chunk_size = 1024):
                                effectuer += len(partie)
                                flux.write(partie)
                                progress_widget.setValue(int(effectuer * 100 / taille_fichier))
            else :
                QMessageBox.warning(self, "ILT", "Veuillez vous connecter !!")
        except Exception as e:
            QMessageBox.critical(self, "ILT", "Une erreur est survenue lors du téléchargement !!") 

    ''' Action qui est effectué lors du clic sur le bouton mis à jour '''
    def mis_a_jour(self, indice):
        self.setCursor(QtGui.QCursor(QtCore.Qt.WaitCursor))
        if gestion_appli.connexion_on() == False:
            QMessageBox.warning(self, 'ILT',"Veuillez vous connecter !")
        else:
            if self.ui.tableWidget.item(indice, 1).text() == "":
                 QMessageBox.critical(self, 'ILT',"Application non installée !")
            else:
                if self.ui.tableWidget.item(indice, 2).text() == self.ui.tableWidget.item(indice, 1).text() :
                    self.ui.tableWidget.setCellWidget(indice, 3, QLabel("Version à jour"))
                    self.ui.tableWidget.cellWidget(indice, 3).setStyleSheet("font: 75 15pt \"Footlight MT Light\";\n" 
                    "color : white;\n""border: 1px solid white;\n""background-color :#2ecc71;")
                else :
                    self.setCursor(QtGui.QCursor(QtCore.Qt.WaitCursor))
                    nom = self.ui.tableWidget.item(indice, 0).text().split(' ')[1]
                    self.ui.tableWidget.setCellWidget(indice, 3, QLabel())
                    self.ui.tableWidget.setCellWidget(indice, 3, QProgressBar())
                    self.telechargeur(self.online_version[nom][1], self.ui.tableWidget.cellWidget(indice, 3))
                    setup = 'Downloads/' + self.online_version[nom][1].split('/')[-1]
                    nom = self.ui.tableWidget.item(indice, 0).text()
                    gestion_appli.mis_a_jour(setup, self.path + nom + '/' + 'unins000.exe')
                    self.ui.tableWidget.setCellWidget(indice, 3, QLabel("Version à jour"))
                    self.set_actions()
        self.setCursor(QtGui.QCursor())

    def rempli_table_view(self):
        self.ui.tableWidget.setRowCount(len(self.infos))
        self.ui.tableWidget.setColumnCount(4)
        self.ui.tableWidget.setHorizontalHeaderLabels(["Logiciels", "Version installée", "Version en ligne", 'Action/Statut'])
        self.ui.tableWidget.verticalHeader().hide()
        for i in range(self.ui.tableWidget.rowCount()):
            self.ui.tableWidget.setItem(i, 0, QTableWidgetItem(self.infos[i]))
            self.ui.tableWidget.setCellWidget(i, 3, QPushButton("Mettre à Jour"))
            self.ui.tableWidget.cellWidget(i, 3).setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
            self.ui.tableWidget.cellWidget(i, 3).clicked.connect(lambda  : self.mis_a_jour(self.ui.tableWidget.currentRow()))
            self.ui.tableWidget.cellWidget(i, 3).setStyleSheet("font: 75 20pt \"Footlight MT Light\";\n" 
                "color : #00CCFF;\n""\n""background-color :#0D3DA3;")
            file_name = self.path + '\\' + self.infos[i]
            if os.path.exists(file_name):
                file_name += '\\' + self.infos[i].split(' ')[-1] + '.exe'
                self.ui.tableWidget.setItem(i, 1, QTableWidgetItem(gestion_appli.get_version_number(file_name)))
        self.rempli_online_version()
        for i in range(self.ui.tableWidget.rowCount()):
            for j in range (self.ui.tableWidget.columnCount()):
                if not self.ui.tableWidget.item(i,j) :
                    self.ui.tableWidget.setItem(i,j, QTableWidgetItem(""))
                self.ui.tableWidget.item(i,j).setFlags(QtCore.Qt.ItemIsSelectable|QtCore.Qt.ItemIsEnabled )
        self.ui.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.ui.tableWidget.horizontalHeader().setStyleSheet("font: 90 20pt")
        self.ui.tableWidget.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.ui.tableWidget.resizeRowsToContents()


def main():
    appli = QApplication(sys.argv)
    window =Updater()
    window.show()
    sys.exit(appli.exec_())

if __name__ == '__main__':
    main()
