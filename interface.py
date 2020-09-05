# -*- coding: utf-8 -*-
import view_interface
from PyQt5.QtWidgets import QMainWindow, QApplication, QLineEdit, QDialog, QLabel,\
                             QMessageBox, QTableWidget,QTableWidgetItem, QHeaderView, QPushButton
from PyQt5.QtGui import QPixmap, QStandardItemModel
from PyQt5.QtPrintSupport import QPrinter
from PyQt5 import QtCore, QtGui
import sys
import os
import gestion_appli

'''Défintion du comportement de l'application graphique'''
class Updater(QMainWindow):
    """Classe qui gère le super marche"""
    def __init__(self):
        super().__init__()
        self.infos = ['SAGEES Report', 'SAGEES Schooling', 'SAGEES Passage' , 'SAGEES Informer', 'SAGEES TimeTable', 'SAGEES BnR', 'Database']
        self.path = ['C:\\Program Files (x86)\\INFOLAB Technologies', 'C:\\Program Files \\INFOLAB Technologies']
        self.ui = view_interface.Ui_MainWindow()
        self.online_version = gestion_appli.get_online_version('https://infolab-technologies.com/setup/')
        self.ui.setupUi(self)
        self.set_actions()

    def set_actions(self):
        self.rempli_table_view()

    def rempli_online_version(self):
        for i in range(self.ui.tableWidget.rowCount() - 1):
            name = self.infos[i].split(' ')[1]
            self.ui.tableWidget.setItem(i, 2, QTableWidgetItem(self.online_version[name] ))

    def mis_a_jour(self):
        indice = self.ui.tableWidget.currentRow()
        QMessageBox.warning(self, 'ILT','indice : {}'.format(indice))
        if self.ui.tableWidget.item(indice, 2).text == 'Non connecté':
            QMessageBox.warning(self, 'ILT',"Veuillez vous connecter !")
        else:
            if self.ui.tableWidget.item(indice, 2).text != self.ui.tableWidget.item(indice, 1).text :
                self.ui.tableWidget.setCellWidget(indice, 3, QLabel("Version à jour"))
                self.ui.tableWidget.cellWidget(indice, 3).setStyleSheet("font: 75 20pt \"Footlight MT Light\";\n" 
                "color : #00CCFF;\n""border: 1px solid white;\n""background-color :#0D3DA3;border-radius : 20px")
            else :
                print("Non à jour")
                self.ui.tableWidget.setCellWidget(indice, 3, QLabel("Version non à jour"))


    def rempli_table_view(self):
        self.ui.tableWidget.setRowCount(len(self.infos))
        self.ui.tableWidget.setColumnCount(4)
        self.ui.tableWidget.setHorizontalHeaderLabels(["Logiciels", "Version installée", "Version en ligne", ''])
        self.ui.tableWidget.verticalHeader().hide()
        for i in range(self.ui.tableWidget.rowCount()):
            self.ui.tableWidget.setItem(i, 0, QTableWidgetItem(self.infos[i]))
            self.ui.tableWidget.setCellWidget(i, 3, QPushButton("Mettre à Jour"))
            self.ui.tableWidget.cellWidget(i, 3).setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
            self.ui.tableWidget.cellWidget(i, 3).clicked.connect(lambda  : self.mis_a_jour())
            self.ui.tableWidget.cellWidget(i, 3).setStyleSheet("font: 75 20pt \"Footlight MT Light\";\n" 
                "color : #00CCFF;\n""border: 1px solid white;\n""background-color :#0D3DA3;border-radius : 20px")
            for path in self.path :
                file_name = path + '\\' + self.infos[i]
                if os.path.exists(file_name):
                    file_name += '\\' + self.infos[i].split(' ')[-1] + '.exe'
                    self.ui.tableWidget.setItem(i,1, QTableWidgetItem(gestion_appli.get_version_number(file_name)))
                    break
        self.rempli_online_version()
        for i in range(self.ui.tableWidget.rowCount()):
            for j in range (self.ui.tableWidget.columnCount()):
                if not self.ui.tableWidget.item(i,j) :
                    self.ui.tableWidget.setItem(i,j, QTableWidgetItem(""))
                self.ui.tableWidget.item(i,j).setFlags(QtCore.Qt.ItemIsSelectable|QtCore.Qt.ItemIsEnabled )
        self.ui.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.ui.tableWidget.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.ui.tableWidget.resizeRowsToContents()
        print(self.ui.tableWidget.item(3,1).text() < self.ui.tableWidget.item(3,2).text())
        print(self.ui.tableWidget.item(3,2).text())


def main():
    appli = QApplication(sys.argv)
    window =Updater()
    window.show()
    sys.exit(appli.exec_())

if __name__ == '__main__':
    main()