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

class Ui_DebugBar(ui.FormBaseClass):
    def setupUi(self, DebugBar):
        ui.FormBaseClass.__init__(self)

        DebugBar.setObjectName("DebugBar")
        DebugBar.resize(379, 293)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(DebugBar.sizePolicy().hasHeightForWidth())
        DebugBar.setSizePolicy(sizePolicy)
        self.verticalLayoutWidget = QtGui.QWidget(DebugBar)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(0, 0, 341, 251))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.layout = QtGui.QVBoxLayout(self.verticalLayoutWidget)
        self.layout.setSizeConstraint(QtGui.QLayout.SetNoConstraint)
        self.layout.setObjectName("layout")
        self.label = QtGui.QLabel(self.verticalLayoutWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.layout.addWidget(self.label)
        self.messagesList = QtGui.QListWidget(self.verticalLayoutWidget)
        self.messagesList.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.messagesList.setObjectName("messagesList")
        self.layout.addWidget(self.messagesList)

        self.retranslateUi(DebugBar)
        QtCore.QMetaObject.connectSlotsByName(DebugBar)

    def retranslateUi(self, DebugBar):
        DebugBar.setWindowTitle(QtGui.QApplication.translate("DebugBar", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("DebugBar", "debug output", None, QtGui.QApplication.UnicodeUTF8))


class DebugBar(QtGui.QWidget, Ui_DebugBar):
    def __init__(self, path, parent=None, f=QtCore.Qt.WindowFlags()):
        QtGui.QWidget.__init__(self, parent, f)

        self.setupUi(self)
        return


    def setLayoutGeometry( self, width, height ):
        """ updates the whole form layout size """

        self.verticalLayoutWidget.setGeometry( QtCore.QRect( 0, 0, width, height ) )
        return


    def appendMessage( self, message ):
        """ Appends a message to the debug window list """

        if self.messagesList.count() > 300:
            self.messagesList.takeItem( 0 )
        self.messagesList.addItem( message )
        self.messagesList.scrollToBottom()
        return
