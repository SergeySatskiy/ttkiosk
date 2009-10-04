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
import ui, time
from utils import debugMsg


class Ui_Clock(ui.FormBaseClass):
    def setupUi(self, Clock):
        ui.FormBaseClass.__init__(self)

        Clock.setObjectName("Clock")
        Clock.resize(246, 146)
        self.gridLayoutWidget = QtGui.QWidget(Clock)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(0, 0, 241, 131))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayout = QtGui.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setObjectName("gridLayout")
        spacerItem = QtGui.QSpacerItem(20, 10, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        self.gridLayout.addItem(spacerItem, 0, 1, 1, 1)
        spacerItem1 = QtGui.QSpacerItem(20, 6, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem1, 2, 1, 1, 1)
        spacerItem2 = QtGui.QSpacerItem(10, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem2, 1, 0, 1, 1)
        spacerItem3 = QtGui.QSpacerItem(20, 20, QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem3, 1, 2, 1, 1)
        self.timeLabel = QtGui.QLabel(self.gridLayoutWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.timeLabel.sizePolicy().hasHeightForWidth())
        self.timeLabel.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Monospace")
        font.setPointSize(32)
        font.setWeight(75)
        font.setBold(True)
        self.timeLabel.setFont(font)
        self.timeLabel.setObjectName("timeLabel")
        self.gridLayout.addWidget(self.timeLabel, 1, 1, 1, 1)
        self.dateLabel = QtGui.QLabel(self.gridLayoutWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.dateLabel.sizePolicy().hasHeightForWidth())
        self.dateLabel.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("DejaVu Sans")
        font.setPointSize(16)
        self.dateLabel.setFont(font)
        self.dateLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.dateLabel.setObjectName("dateLabel")
        self.gridLayout.addWidget(self.dateLabel, 3, 1, 1, 1)
        spacerItem4 = QtGui.QSpacerItem(20, 10, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        self.gridLayout.addItem(spacerItem4, 4, 1, 1, 1)

        self.retranslateUi(Clock)
        QtCore.QMetaObject.connectSlotsByName(Clock)


    def retranslateUi(self, Clock):
        Clock.setWindowTitle(QtGui.QApplication.translate("Clock", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.timeLabel.setText(QtGui.QApplication.translate("Clock", "12:59:59", None, QtGui.QApplication.UnicodeUTF8))
        self.dateLabel.setText(QtGui.QApplication.translate("Clock", "Jan 10, 1971", None, QtGui.QApplication.UnicodeUTF8))


class Clock(QtGui.QWidget, Ui_Clock):
    def __init__(self, path, parent=None, f=QtCore.Qt.WindowFlags()):
        QtGui.QWidget.__init__(self, parent, f)

        self.setupUi(self)
        self.displayedDate = ""
        self.displayedTime = ""

        self.update()
        self.dateTimer = QtCore.QBasicTimer()
        self.dateTimer.start( 1000, self )


    def setLayoutGeometry( self, width, height ):
        """ updates the whole form layout size """

        self.gridLayoutWidget.setGeometry( QtCore.QRect( 0, 0, width, height ) )
        return


    def update( self ):
        """ Updates date and time labels if required """

        # newTime = time.strftime( "%H:%M:%S" )
        newTime = time.strftime( "%H:%M" )
        if newTime != self.displayedTime:
            self.displayedTime = newTime
            self.timeLabel.setText( newTime )

        newDate = time.strftime( "%a, %b %d, %Y" )
        if newDate != self.displayedDate:
            self.displayedDate = newDate
            self.dateLabel.setText( newDate )

        return


    def timerEvent( self, event ):
        """ Updates the labels if it is the expected timer """

        if event.timerId() == self.dateTimer.timerId():
            self.update()
        return

