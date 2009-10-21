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
from PyQt4.QtCore import SIGNAL, SLOT
import ui
from utils import debugMsg, GlobalData


class Ui_DigitKeyboard(ui.FormBaseClass):
    def setupUi(self, DigitKeyboard, path):
        ui.FormBaseClass.__init__(self)

        DigitKeyboard.setObjectName("DigitKeyboard")
        DigitKeyboard.resize(190, 367)
        self.userInputLabel = QtGui.QLabel(DigitKeyboard)
        self.userInputLabel.setGeometry(QtCore.QRect(10, 10, 171, 50))
        font = QtGui.QFont()
        font.setFamily("Monospace")
        font.setPointSize(24)
        font.setWeight(50)
        font.setBold(False)
        self.userInputLabel.setFont(font)
        self.userInputLabel.setAutoFillBackground(False)
        self.userInputLabel.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.userInputLabel.setObjectName("userInputLabel")
        self.button7 = QtGui.QPushButton(DigitKeyboard)
        self.button7.setGeometry(QtCore.QRect(10, 130, 50, 50))
        font = QtGui.QFont()
        font.setPointSize(24)
        self.button7.setFont(font)
        self.button7.setFocusPolicy(QtCore.Qt.NoFocus)
        self.button7.setObjectName("button7")
        self.button8 = QtGui.QPushButton(DigitKeyboard)
        self.button8.setGeometry(QtCore.QRect(70, 130, 50, 50))
        font = QtGui.QFont()
        font.setPointSize(24)
        self.button8.setFont(font)
        self.button8.setFocusPolicy(QtCore.Qt.NoFocus)
        self.button8.setObjectName("button8")
        self.button9 = QtGui.QPushButton(DigitKeyboard)
        self.button9.setGeometry(QtCore.QRect(130, 130, 50, 50))
        font = QtGui.QFont()
        font.setPointSize(24)
        self.button9.setFont(font)
        self.button9.setFocusPolicy(QtCore.Qt.NoFocus)
        self.button9.setObjectName("button9")
        self.button4 = QtGui.QPushButton(DigitKeyboard)
        self.button4.setGeometry(QtCore.QRect(10, 190, 50, 50))
        font = QtGui.QFont()
        font.setPointSize(24)
        self.button4.setFont(font)
        self.button4.setFocusPolicy(QtCore.Qt.NoFocus)
        self.button4.setObjectName("button4")
        self.button5 = QtGui.QPushButton(DigitKeyboard)
        self.button5.setGeometry(QtCore.QRect(70, 190, 50, 50))
        font = QtGui.QFont()
        font.setPointSize(24)
        self.button5.setFont(font)
        self.button5.setFocusPolicy(QtCore.Qt.NoFocus)
        self.button5.setObjectName("button5")
        self.button6 = QtGui.QPushButton(DigitKeyboard)
        self.button6.setGeometry(QtCore.QRect(130, 190, 50, 50))
        font = QtGui.QFont()
        font.setPointSize(24)
        self.button6.setFont(font)
        self.button6.setFocusPolicy(QtCore.Qt.NoFocus)
        self.button6.setObjectName("button6")
        self.button1 = QtGui.QPushButton(DigitKeyboard)
        self.button1.setGeometry(QtCore.QRect(10, 250, 50, 50))
        font = QtGui.QFont()
        font.setPointSize(24)
        self.button1.setFont(font)
        self.button1.setFocusPolicy(QtCore.Qt.NoFocus)
        self.button1.setObjectName("button1")
        self.button2 = QtGui.QPushButton(DigitKeyboard)
        self.button2.setGeometry(QtCore.QRect(70, 250, 50, 50))
        font = QtGui.QFont()
        font.setPointSize(24)
        self.button2.setFont(font)
        self.button2.setFocusPolicy(QtCore.Qt.NoFocus)
        self.button2.setObjectName("button2")
        self.button3 = QtGui.QPushButton(DigitKeyboard)
        self.button3.setGeometry(QtCore.QRect(130, 250, 50, 50))
        font = QtGui.QFont()
        font.setPointSize(24)
        self.button3.setFont(font)
        self.button3.setFocusPolicy(QtCore.Qt.NoFocus)
        self.button3.setObjectName("button3")
        self.deleteButton = QtGui.QPushButton(DigitKeyboard)
        self.deleteButton.setGeometry(QtCore.QRect(130, 70, 50, 50))
        self.deleteButton.setFocusPolicy(QtCore.Qt.NoFocus)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(path + "clear_left.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.deleteButton.setIcon(icon)
        self.deleteButton.setIconSize(QtCore.QSize(48, 48))
        self.deleteButton.setObjectName("deleteButton")
        self.button0 = QtGui.QPushButton(DigitKeyboard)
        self.button0.setGeometry(QtCore.QRect(10, 310, 50, 50))
        font = QtGui.QFont()
        font.setPointSize(24)
        self.button0.setFont(font)
        self.button0.setFocusPolicy(QtCore.Qt.NoFocus)
        self.button0.setObjectName("button0")
        self.okButton = QtGui.QPushButton(DigitKeyboard)
        self.okButton.setGeometry(QtCore.QRect(70, 310, 111, 50))
        self.okButton.setFocusPolicy(QtCore.Qt.NoFocus)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(path + "apply.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.okButton.setIcon(icon1)
        self.okButton.setIconSize(QtCore.QSize(48, 48))
        self.okButton.setObjectName("okButton")
        self.cancelButton = QtGui.QPushButton(DigitKeyboard)
        self.cancelButton.setGeometry(QtCore.QRect(10, 70, 111, 50))
        self.cancelButton.setFocusPolicy(QtCore.Qt.NoFocus)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(path + "close.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.cancelButton.setIcon(icon2)
        self.cancelButton.setIconSize(QtCore.QSize(48, 48))
        self.cancelButton.setObjectName("cancelButton")

        self.retranslateUi(DigitKeyboard)
        QtCore.QMetaObject.connectSlotsByName(DigitKeyboard)

    def retranslateUi(self, DigitKeyboard):
        DigitKeyboard.setWindowTitle(QtGui.QApplication.translate("DigitKeyboard", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.button7.setText(QtGui.QApplication.translate("DigitKeyboard", "7", None, QtGui.QApplication.UnicodeUTF8))
        self.button8.setText(QtGui.QApplication.translate("DigitKeyboard", "8", None, QtGui.QApplication.UnicodeUTF8))
        self.button9.setText(QtGui.QApplication.translate("DigitKeyboard", "9", None, QtGui.QApplication.UnicodeUTF8))
        self.button4.setText(QtGui.QApplication.translate("DigitKeyboard", "4", None, QtGui.QApplication.UnicodeUTF8))
        self.button5.setText(QtGui.QApplication.translate("DigitKeyboard", "5", None, QtGui.QApplication.UnicodeUTF8))
        self.button6.setText(QtGui.QApplication.translate("DigitKeyboard", "6", None, QtGui.QApplication.UnicodeUTF8))
        self.button1.setText(QtGui.QApplication.translate("DigitKeyboard", "1", None, QtGui.QApplication.UnicodeUTF8))
        self.button2.setText(QtGui.QApplication.translate("DigitKeyboard", "2", None, QtGui.QApplication.UnicodeUTF8))
        self.button3.setText(QtGui.QApplication.translate("DigitKeyboard", "3", None, QtGui.QApplication.UnicodeUTF8))
        self.button0.setText(QtGui.QApplication.translate("DigitKeyboard", "0", None, QtGui.QApplication.UnicodeUTF8))


#class DigitKeyboard(QtGui.QWidget, Ui_DigitKeyboard):
class DigitKeyboard(QtGui.QDialog, Ui_DigitKeyboard):
    def __init__(self, path, parent=None, f=QtCore.Qt.WindowFlags()):
        #QtGui.QWidget.__init__(self, parent, f)
        #QtGui.QDialog.__init__(self, parent, f)
        QtGui.QDialog.__init__(self, parent, f | QtCore.Qt.WindowStaysOnTopHint)
        #self.setModal( True )
        #self.setWindowModality( QtCore.Qt.ApplicationModal )

        self.setupUi(self, path)

        self.hideInput = True
        self.userInput = ""
        self.userInputLabel.setText( "" )
        self.cancelled = False

        self.makeConnections()
        return


    def showEvent( self, event ):
        """ reset the label """
        self.userInput = ""
        self.cancelled = False
        self.userInputLabel.setText( "" )
        return


    def makeConnections( self ):
        """ A collection of SIGNAL - SLOT connections """

        self.connect( self.button0, SIGNAL("clicked()"), self.button0Clicked )
        self.connect( self.button1, SIGNAL("clicked()"), self.button1Clicked )
        self.connect( self.button2, SIGNAL("clicked()"), self.button2Clicked )
        self.connect( self.button3, SIGNAL("clicked()"), self.button3Clicked )
        self.connect( self.button4, SIGNAL("clicked()"), self.button4Clicked )
        self.connect( self.button5, SIGNAL("clicked()"), self.button5Clicked )
        self.connect( self.button6, SIGNAL("clicked()"), self.button6Clicked )
        self.connect( self.button7, SIGNAL("clicked()"), self.button7Clicked )
        self.connect( self.button8, SIGNAL("clicked()"), self.button8Clicked )
        self.connect( self.button9, SIGNAL("clicked()"), self.button9Clicked )

        self.connect( self.okButton, SIGNAL("clicked()"), self.okButtonClicked )
        self.connect( self.cancelButton, SIGNAL("clicked()"), self.cancelButtonClicked )
        self.connect( self.deleteButton, SIGNAL("clicked()"), self.deleteButtonClicked )
        return

    def button0Clicked( self ):
        self.buttonPressed( 0 )
    def button1Clicked( self ):
        self.buttonPressed( 1 )
    def button2Clicked( self ):
        self.buttonPressed( 2 )
    def button3Clicked( self ):
        self.buttonPressed( 3 )
    def button4Clicked( self ):
        self.buttonPressed( 4 )
    def button5Clicked( self ):
        self.buttonPressed( 5 )
    def button6Clicked( self ):
        self.buttonPressed( 6 )
    def button7Clicked( self ):
        self.buttonPressed( 7 )
    def button8Clicked( self ):
        self.buttonPressed( 8 )
    def button9Clicked( self ):
        self.buttonPressed( 9 )

    def buttonPressed( self, value ):
        self.userInput = self.userInput + str( value )
        self.updateText()
        return

    def okButtonClicked( self ):
        self.close()
        return

    def cancelButtonClicked( self ):
        self.cancelled = True
        self.close()
        return

    def deleteButtonClicked( self ):
        if len( self.userInput ) == 0:
            return
        self.userInput = self.userInput[ :-1 ]
        self.updateText()
        return

    def updateText( self ):
        debugMsg( "Current user input: " + self.userInput )
        if not self.hideInput:
            self.userInputLabel.setText( self.userInput )
        else:
            self.userInputLabel.setText( len( self.userInput ) * "*" )
        return

    def setLayoutGeometry( self, width, height ):
        """ updates the whole form layout size """
        return

