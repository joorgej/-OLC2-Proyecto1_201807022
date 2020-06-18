# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Form.ui'
#
# Created by: PyQt5 UI code generator 5.14.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets
'''from PyQt5.QtCore import QFile, QRegExp, Qt
from PyQt5.QtGui import QFont, QSyntaxHighlighter, QTextCharFormat'''
import threading
import ascendente as ascendente
import descendente as descendente
from AST_Graph import GraphAST
from graphviz import Graph
from Interprete import interpretar


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setWindowModality(QtCore.Qt.NonModal)
        MainWindow.resize(1920, 1000)
        QtWidgets.QLineEdit
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(88, 88, 88))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(63, 63, 63))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(88, 88, 88))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255, 128))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.PlaceholderText, brush)
        brush = QtGui.QBrush(QtGui.QColor(88, 88, 88))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(63, 63, 63))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(88, 88, 88))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255, 128))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.PlaceholderText, brush)
        brush = QtGui.QBrush(QtGui.QColor(88, 88, 88))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(120, 120, 120))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(88, 88, 88))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(88, 88, 88))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0, 128))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.PlaceholderText, brush)
        MainWindow.setPalette(palette)
        font = QtGui.QFont()
        font.setFamily("Calibri Light")
        MainWindow.setFont(font)
        MainWindow.setFocusPolicy(QtCore.Qt.StrongFocus)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("./resourses/icons8-a-64.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        MainWindow.setAutoFillBackground(True)

        self.ast = None
        self.gramatica = None
        self.simbolos = None

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.openedFile = ''
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(10, 10, 621, 51))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")

        """Boton nuevo archivo"""
        self.pushButton = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.pushButton.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("./resourses/icons8-archivo-64 (1).png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton.setIcon(icon1)
        self.pushButton.setIconSize(QtCore.QSize(30, 30))
        self.pushButton.setFlat(True)
        self.pushButton.setObjectName("pushButton")
        self.pushButton.clicked.connect(self.newFile)
        self.horizontalLayout.addWidget(self.pushButton)

        """Boton abrir archivo"""
        self.pushButton_5 = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.pushButton_5.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.pushButton_5.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.pushButton_5.setText("")
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap("./resourses/icons8-abrir-carpeta-64.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_5.setIcon(icon2)
        self.pushButton_5.setIconSize(QtCore.QSize(30, 30))
        self.pushButton_5.setFlat(True)
        self.pushButton_5.setObjectName("pushButton_5")
        self.pushButton_5.clicked.connect(self.openFile)
        self.horizontalLayout.addWidget(self.pushButton_5)

        """Boton guardar archivo"""
        self.pushButton_4 = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.pushButton_4.setText("")
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap("./resourses/icons8-guardar-64.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_4.setIcon(icon3)
        self.pushButton_4.setIconSize(QtCore.QSize(30, 30))
        self.pushButton_4.setFlat(True)
        self.pushButton_4.setObjectName("pushButton_4")
        self.pushButton_4.clicked.connect(self.saveFile)
        self.horizontalLayout.addWidget(self.pushButton_4)

        """Boton guardar como"""
        self.pushButton_3 = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.pushButton_3.setText("")
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap("./resourses/icons8-guardar-como-64.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_3.setIcon(icon4)
        self.pushButton_3.setIconSize(QtCore.QSize(30, 30))
        self.pushButton_3.setFlat(True)
        self.pushButton_3.setObjectName("pushButton_3")
        self.pushButton_3.clicked.connect(self.saveAsFile)
        self.horizontalLayout.addWidget(self.pushButton_3)
        spacerItem = QtWidgets.QSpacerItem(50, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)

        """Boton parar ejecucion"""
        self.pushButton_2 = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.pushButton_2.setText("")
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap("./resourses/icons8-señal-de-stop-64.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_2.setIcon(icon5)
        self.pushButton_2.setIconSize(QtCore.QSize(30, 30))
        self.pushButton_2.setFlat(True)
        self.pushButton_2.setObjectName("pushButton_2")
        self.horizontalLayout.addWidget(self.pushButton_2)

        """Boton analisis descendente"""
        self.pushButton_7 = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.pushButton_7.setText("")
        icon6 = QtGui.QIcon()
        icon6.addPixmap(QtGui.QPixmap("./resourses/icons8-abajo-64.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_7.setIcon(icon6)
        self.pushButton_7.setIconSize(QtCore.QSize(30, 30))
        self.pushButton_7.setFlat(True)
        self.pushButton_7.setObjectName("pushButton_7")
        self.pushButton_7.clicked.connect(self.analisisDescendente)
        self.horizontalLayout.addWidget(self.pushButton_7)

        """Boton analisis ascendente"""
        self.pushButton_6 = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.pushButton_6.setText("")
        icon7 = QtGui.QIcon()
        icon7.addPixmap(QtGui.QPixmap("./resourses/icons8-arriba-64.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_6.setIcon(icon7)
        self.pushButton_6.setIconSize(QtCore.QSize(30, 30))
        self.pushButton_6.setFlat(True)
        self.pushButton_6.setObjectName("pushButton_6")
        self.pushButton_6.clicked.connect(self.analisisAscendente)
        self.horizontalLayout.addWidget(self.pushButton_6)

        """Boton debugger"""
        self.pushButton_8 = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.pushButton_8.setText("")
        icon8 = QtGui.QIcon()
        icon8.addPixmap(QtGui.QPixmap("./resourses/icons8-play-64.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_8.setIcon(icon8)
        self.pushButton_8.setIconSize(QtCore.QSize(30, 30))
        self.pushButton_8.setAutoDefault(False)
        self.pushButton_8.setFlat(True)
        self.pushButton_8.setObjectName("pushButton_8")
        self.horizontalLayout.addWidget(self.pushButton_8)


        """Barra separacion"""
        spacerItem1 = QtWidgets.QSpacerItem(50, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)

        """Boton ayuda"""
        self.pushButton_9 = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.pushButton_9.setText("")
        icon9 = QtGui.QIcon()
        icon9.addPixmap(QtGui.QPixmap("./resourses/icons8-ayuda-64.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_9.setIcon(icon9)
        self.pushButton_9.setIconSize(QtCore.QSize(30, 30))
        self.pushButton_9.setFlat(True)
        self.pushButton_9.setObjectName("pushButton_9")
        self.horizontalLayout.addWidget(self.pushButton_9)

        """Boton acerca de"""
        self.pushButton_10 = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.pushButton_10.setText("")
        icon10 = QtGui.QIcon()
        icon10.addPixmap(QtGui.QPixmap("./resourses/icons8-acerca-de-64.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_10.setIcon(icon10)
        self.pushButton_10.setIconSize(QtCore.QSize(30, 30))
        self.pushButton_10.setFlat(True)
        self.pushButton_10.setObjectName("pushButton_10")
        self.horizontalLayout.addWidget(self.pushButton_10)

        """Consola"""
        self.textEdit_2 = QtWidgets.QTextEdit(self.centralwidget)
        self.textEdit_2.setGeometry(QtCore.QRect(80, 710, 1181, 211))
        font = self.textEdit_2.font()
        font.setPointSize(11)
        self.textEdit_2.setFont(font)
        self.textEdit_2.setTextColor(QtGui.QColor(254,245,100))
        self.textEdit_2.setObjectName("textEdit_2")
        

        """Editor de codigo"""
        self.textEdit = QtWidgets.QTextEdit(self.centralwidget)
        self.textEdit.setGeometry(QtCore.QRect(80, 130, 1751, 501))
        self.textEdit.setObjectName("textEdit")
        font = self.textEdit.font()
        font.setPointSize(12)
        self.textEdit.setFont(font)
        self.highlighter = Highlighter(self.textEdit.document())


        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(90, 665, 221, 31))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.ButtonText, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.ButtonText, brush)
        brush = QtGui.QBrush(QtGui.QColor(120, 120, 120))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(120, 120, 120))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.ButtonText, brush)
        self.label.setPalette(palette)
        font = QtGui.QFont()
        font.setPointSize(16)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(90, 90, 221, 31))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy)
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.ButtonText, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.ButtonText, brush)
        brush = QtGui.QBrush(QtGui.QColor(120, 120, 120))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(120, 120, 120))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.ButtonText, brush)
        self.label_2.setPalette(palette)
        font = QtGui.QFont()
        font.setPointSize(16)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.textEdit_3 = QtWidgets.QTextEdit(self.centralwidget)
        self.textEdit_3.setGeometry(QtCore.QRect(1310, 710, 521, 211))
        self.textEdit_3.setObjectName("textEdit_3")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(1320, 660, 221, 31))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_3.sizePolicy().hasHeightForWidth())
        self.label_3.setSizePolicy(sizePolicy)
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.ButtonText, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.ButtonText, brush)
        brush = QtGui.QBrush(QtGui.QColor(120, 120, 120))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(120, 120, 120))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.ButtonText, brush)
        self.label_3.setPalette(palette)
        font = QtGui.QFont()
        font.setPointSize(16)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1920, 25))
        self.menubar.setObjectName("menubar")
        self.menuArchivo = QtWidgets.QMenu(self.menubar)
        self.menuArchivo.setObjectName("menuArchivo")
        self.menuEditar = QtWidgets.QMenu(self.menubar)
        self.menuEditar.setObjectName("menuEditar")
        self.menuEjecutar = QtWidgets.QMenu(self.menubar)
        self.menuEjecutar.setObjectName("menuEjecutar")
        self.menuOpciones = QtWidgets.QMenu(self.menubar)
        self.menuOpciones.setObjectName("menuOpciones")
        self.menuAyuda = QtWidgets.QMenu(self.menubar)
        self.menuAyuda.setObjectName("menuAyuda")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionNuevo = QtWidgets.QAction(MainWindow)
        self.actionNuevo.setObjectName("actionNuevo")
        self.actionAbrir = QtWidgets.QAction(MainWindow)
        self.actionAbrir.setObjectName("actionAbrir")
        self.actionAyuda = QtWidgets.QAction(MainWindow)
        self.actionAyuda.setObjectName("actionAyuda")
        self.actionAcerca_de = QtWidgets.QAction(MainWindow)
        self.actionAcerca_de.setObjectName("actionAcerca_de")
        self.actionCopiar = QtWidgets.QAction(MainWindow)
        self.actionCopiar.setObjectName("actionCopiar")
        self.actionPegar = QtWidgets.QAction(MainWindow)
        self.actionPegar.setObjectName("actionPegar")
        self.actionCortar = QtWidgets.QAction(MainWindow)
        self.actionCortar.setObjectName("actionCortar")
        self.actionBuscar = QtWidgets.QAction(MainWindow)
        self.actionBuscar.setObjectName("actionBuscar")
        self.actionReemplazar = QtWidgets.QAction(MainWindow)
        self.actionReemplazar.setObjectName("actionReemplazar")
        self.actionAnalicis_ascendente = QtWidgets.QAction(MainWindow)
        self.actionAnalicis_ascendente.setObjectName("actionAnalicis_ascendente")
        self.actionAnalicis_descendente = QtWidgets.QAction(MainWindow)
        self.actionAnalicis_descendente.setObjectName("actionAnalicis_descendente")
        self.actionReporte_Gramatical = QtWidgets.QAction(MainWindow)
        self.actionReporte_Gramatical.setObjectName("actionReporte_Gramatical")
        self.actionReporte_Gramatical.triggered.connect(self.graphGrammar)
        self.actionReporte_AST = QtWidgets.QAction(MainWindow)
        self.actionReporte_AST.setObjectName("actionReporte_AST")
        self.actionReporte_AST.triggered.connect(self.graphAST)
        self.actionGuardar = QtWidgets.QAction(MainWindow)
        self.actionGuardar.setObjectName("actionGuardar")
        self.actionGuardar_como = QtWidgets.QAction(MainWindow)
        self.actionGuardar_como.setObjectName("actionGuardar_como")
        self.menuArchivo.addAction(self.actionNuevo)
        self.menuArchivo.addAction(self.actionAbrir)
        self.menuArchivo.addAction(self.actionGuardar)
        self.menuArchivo.addAction(self.actionGuardar_como)
        self.menuEditar.addSeparator()
        self.menuEditar.addAction(self.actionCopiar)
        self.menuEditar.addAction(self.actionPegar)
        self.menuEditar.addAction(self.actionCortar)
        self.menuEditar.addAction(self.actionBuscar)
        self.menuEditar.addAction(self.actionReemplazar)
        self.menuEjecutar.addAction(self.actionAnalicis_ascendente)
        self.menuEjecutar.addAction(self.actionAnalicis_descendente)
        self.menuOpciones.addAction(self.actionReporte_Gramatical)
        self.menuOpciones.addAction(self.actionReporte_AST)
        self.menuAyuda.addAction(self.actionAyuda)
        self.menuAyuda.addAction(self.actionAcerca_de)
        self.menubar.addAction(self.menuArchivo.menuAction())
        self.menubar.addAction(self.menuEditar.menuAction())
        self.menubar.addAction(self.menuEjecutar.menuAction())
        self.menubar.addAction(self.menuOpciones.menuAction())
        self.menubar.addAction(self.menuAyuda.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "ugus"))
        self.textEdit_2.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Calibri Light\'; font-size:7.8pt; font-weight:400; font-style:normal;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>"))
        self.label.setText(_translate("MainWindow", "Consola:"))
        self.label_2.setText(_translate("MainWindow", "Archivo:"))
        self.textEdit_3.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Calibri Light\'; font-size:7.8pt; font-weight:400; font-style:normal;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>"))
        self.label_3.setText(_translate("MainWindow", "Tabla de Simbolos:"))
        self.menuArchivo.setTitle(_translate("MainWindow", "Archivo"))
        self.menuEditar.setTitle(_translate("MainWindow", "Editar"))
        self.menuEjecutar.setTitle(_translate("MainWindow", "Ejecutar"))
        self.menuOpciones.setTitle(_translate("MainWindow", "Reportes"))
        self.menuAyuda.setTitle(_translate("MainWindow", "Ayuda"))
        self.actionNuevo.setText(_translate("MainWindow", "Nuevo"))
        self.actionAbrir.setText(_translate("MainWindow", "Abrir"))
        self.actionAyuda.setText(_translate("MainWindow", "Ayuda"))
        self.actionAcerca_de.setText(_translate("MainWindow", "Acerca de"))
        self.actionCopiar.setText(_translate("MainWindow", "Copiar"))
        self.actionPegar.setText(_translate("MainWindow", "Pegar"))
        self.actionCortar.setText(_translate("MainWindow", "Cortar"))
        self.actionBuscar.setText(_translate("MainWindow", "Buscar"))
        self.actionReemplazar.setText(_translate("MainWindow", "Reemplazar"))
        self.actionAnalicis_ascendente.setText(_translate("MainWindow", "Analicis ascendente"))
        self.actionAnalicis_descendente.setText(_translate("MainWindow", "Analicis descendente"))
        self.actionReporte_Gramatical.setText(_translate("MainWindow", "Reporte Gramatical"))
        self.actionReporte_AST.setText(_translate("MainWindow", "Reporte AST"))
        self.actionGuardar.setText(_translate("MainWindow", "Guardar"))
        self.actionGuardar_como.setText(_translate("MainWindow", "Guardar como"))

    def openFile(self):
        try:
            fileName = QtWidgets.QFileDialog.getOpenFileName(None, 'brir archivos', 'C:\\',"Augus files (*.aug)")
            _file = open(fileName[0],"r")
            content = _file.read()
            self.textEdit.setText(content)
            self.openedFile = fileName[0]
            _file.close()
        except:
            print("Advertencia")
            

    def newFile(self):
        if self.textEdit.toPlainText()!='':
            self.saveFile()
            self.textEdit.setText('')
            self.openedFile = ''


    def saveFile(self):
        if self.openedFile == '':
            self.saveAsFile()
        else:
            _file = open(self.openedFile,"w")
            content = self.textEdit.toPlainText()
            _file.write(content)
            _file.close()
        

    def saveAsFile(self):
        try:
            fileName = QtWidgets.QFileDialog.getSaveFileName(None, 'Guardar archivos','C:\\',"Augus files (*.aug)")
            _file = open(fileName[0],"w")
            content = self.textEdit.toPlainText()
            _file.write(content)
            self.openedFile = fileName[0]
            _file.close()
        except:
            print("Advertencia")
            
    def analisisAscendente(self):
        texto = self.textEdit.toPlainText()
        arr = ascendente.analizar(texto, self.textEdit_2)
        self.ast = arr[0]
        self.gramatica = arr[1]
        texto = self.textEdit_2.toPlainText()
        if arr[0] != None:
            try:
                interpretar(arr[0], self.textEdit_2, self.textEdit_3)
            except:
                self.textEdit_2.setText(texto + 'ERROR NO CONTROLADO: A ocurrido un problema en la ejecucion del codigo. \n                   Para recivir soporte pongase en contacto con siguiente correo: jorgejuarezdal@gmail.com')




    def analisisDescendente(self):
        texto = self.textEdit.toPlainText()
        arr = descendente.analizar(texto, self.textEdit_2)
        self.ast = arr[0]
        self.gramatica = arr[1]
        texto = self.textEdit_2.toPlainText()
        if arr[0] != None:
            try:
                interpretar(arr[0], self.textEdit_2, self.textEdit_3)
            except:
                self.textEdit_2.setText(texto + 'ERROR NO CONTROLADO: A ocurrido un problema en la ejecucion del codigo. \n                   Para recivir soporte pongase en contacto con siguiente correo: jorgejuarezdal@gmail.com')

        

    def graphAST(self):
        if self.ast != None:
            GraphAST(self.ast, self.textEdit_2)


    def graphGrammar(self):
        if self.gramatica != None:
            dot = Graph()
            dot.attr(splines = 'false')
            dot.node_attr.update(shape = 'record')
            dot.node_attr.update(center = 'false')
            dot.node(str(0), '{'+ self.gramatica.replace('\n', '\\l |')[:-1] +'}')
            try:
                dot.view()
            except:
                self.textEdit_2.setText('ERROR: No fue posible realizar el reporte gramatical por algun error desconocido.')

class Highlighter(QtGui.QSyntaxHighlighter):
    def __init__(self, parent=None):
        super(Highlighter, self).__init__(parent)

        signFormat = QtGui.QTextCharFormat()
        signFormat.setForeground(QtGui.QColor(206,61,81))

        singPatterns = ["[=]", "[+]", "[>]"
                ,"[<]", "[-]", "[*]", "[/]"
                ,"[&]", "[|]", "[;]", "[:]"
                , "[[]", "[]]", "[(]", "[)]"
                , "[\\^]", "[%]", "[~]", "[,]"]

        self.highlightingRules = [(QtCore.QRegExp(pattern), signFormat)
                for pattern in singPatterns]


        registerFormat = QtGui.QTextCharFormat()
        registerFormat.setForeground(QtGui.QColor(140,192,176))
        self.highlightingRules.append((QtCore.QRegExp("[$].([0-9]+|.)\\b"),
                registerFormat))

        singleLineCommentFormat = QtGui.QTextCharFormat()
        singleLineCommentFormat.setForeground(QtGui.QColor(240, 184, 184))
        self.highlightingRules.append((QtCore.QRegExp("[#](.|\\d)*"),
                singleLineCommentFormat))


        quotationFormat = QtGui.QTextCharFormat()
        quotationFormat.setForeground(QtGui.QColor(230,127,131))
        self.highlightingRules.append((QtCore.QRegExp("\".*\"|\'.*\'"), quotationFormat))

        numberFormat = QtGui.QTextCharFormat()
        numberFormat.setForeground(QtGui.QColor(203,242,229))
        self.highlightingRules.append((QtCore.QRegExp("\\b\\d+(?:\\.\\d{0,20})?"),
                numberFormat))

        keywordFormat = QtGui.QTextCharFormat()
        keywordFormat.setForeground(QtGui.QColor(0, 135, 108))

        keywordPatterns = ["\\bchar\\b", "\\bfloat\\b", "\\bint\\b",
                "\\bif\\b", "\\bgoto\\b", "\\bunset\\b", "\\bset\\b",
                "\\bprint\\b", "\\bread\\b", "\\bexit\\b", "\\bxor\\b"
                , "\\babs\\b", "\\barray\\b"]
        for pattern in keywordPatterns:
            self.highlightingRules.append((QtCore.QRegExp(pattern), keywordFormat))
                
        '''classFormat = QtGui.QTextCharFormat()
        classFormat.setFontWeight(QtGui.QFont.Bold)
        classFormat.setForeground(QtCore.Qt.darkMagenta)
        self.highlightingRules.append((QtCore.QRegExp("\\b[A-Za-z9-0_]+\\b"),
                classFormat))'''


    def highlightBlock(self, text):
        for pattern, format in self.highlightingRules:
            expression = QtCore.QRegExp(pattern)
            index = expression.indexIn(text)
            while index >= 0:
                length = expression.matchedLength()
                self.setFormat(index, length, format)
                index = expression.indexIn(text, index + length)


