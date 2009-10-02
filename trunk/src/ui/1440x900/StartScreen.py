#
# ttkiosk - table tennis club touch screen based kiosk.
# Copyright (C) 2009  Sergey Satskiy
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor,
# Boston, MA  02110-1301, USA.
#
# $Id$
#
# Generated by PyQt4 UI code generator 4.5.4 and then customized
#


from PyQt4 import QtCore, QtGui
import ui

class Ui_StartScreen(ui.FormBaseClass):
    def setupUi(self, StartScreen):
        StartScreen.setObjectName("StartScreen")
        StartScreen.resize(668, 517)
        self.graphicsView = QtGui.QGraphicsView(StartScreen)
        self.graphicsView.setGeometry(QtCore.QRect(10, 10, 341, 131))
        self.graphicsView.setObjectName("graphicsView")
        self.scrollArea = QtGui.QScrollArea(StartScreen)
        self.scrollArea.setGeometry(QtCore.QRect(360, 10, 281, 261))
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtGui.QWidget(self.scrollArea)
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 277, 257))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.toolButton = QtGui.QToolButton(StartScreen)
        self.toolButton.setGeometry(QtCore.QRect(90, 290, 191, 23))
        self.toolButton.setObjectName("toolButton")
        self.buttonBox = QtGui.QDialogButtonBox(StartScreen)
        self.buttonBox.setGeometry(QtCore.QRect(390, 290, 160, 24))
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.listWidget = QtGui.QListWidget(StartScreen)
        self.listWidget.setGeometry(QtCore.QRect(10, 150, 341, 121))
        self.listWidget.setObjectName("listWidget")
        self.calendarWidget = QtGui.QCalendarWidget(StartScreen)
        self.calendarWidget.setGeometry(QtCore.QRect(150, 340, 240, 144))
        self.calendarWidget.setObjectName("calendarWidget")

        self.retranslateUi(StartScreen)
        QtCore.QMetaObject.connectSlotsByName(StartScreen)

    def retranslateUi(self, StartScreen):
        StartScreen.setWindowTitle(QtGui.QApplication.translate("StartScreen", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.toolButton.setText(QtGui.QApplication.translate("StartScreen", "...", None, QtGui.QApplication.UnicodeUTF8))


class StartScreen(QtGui.QWidget, Ui_StartScreen):
    def __init__(self, parent=None, f=QtCore.Qt.WindowFlags()):
        QtGui.QWidget.__init__(self, parent, f)
        ui.FormBaseClass.__init__(self)

        self.setupUi(self)


    def setLayoutGeometry( self, width, height ):
        """ updates the whole form layout size """

        # self.verticalLayoutWidget.setGeometry( QtCore.QRect( 0, 0, width, height ) )
        return

