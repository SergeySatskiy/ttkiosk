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

""" definition of the ttkiosk QT based application class """

import urllib, urlparse, utils, socket
from PyQt4 import QtGui, QtNetwork
from PyQt4.QtCore import SIGNAL


def prepareNotification( what, values ):
    """ prepares a notification string for peer kiosks
        what - identifier of what was changed
        values - map of 'name' -> 'value' """

    globalData = utils.GlobalData()
    vals = { 'kioskID' : globalData.uuid,
             'what':     what }
    for key in values.keys():
        vals[ str( key ) ] = str( values[ key ] )
    return urllib.urlencode( vals )


def parseNotification( notificationString ):
    """ parses the notification string. Returns a map of 'name' -> 'value' """

    return dict( urlparse.parse_qsl( notificationString ) )




class ttkioskApplication( QtGui.QApplication ):
    """ ttkiosk application class """

    def __init__( self, argv ):
        QtGui.QApplication.__init__( self, argv )

        settings = utils.Settings()

        # Prepare socket for sending notifications
        self.socketTo = socket.socket( socket.AF_INET, socket.SOCK_DGRAM )
        self.socketTo.setsockopt( socket.SOL_SOCKET, socket.SO_BROADCAST, 1 )
        self.socketTo.connect( ('255.255.255.255', settings.notificationPort) )

        # Prepare socket for receiving notifications
        self.socketFrom = QtNetwork.QUdpSocket()
        anyAddress = QtNetwork.QHostAddress( QtNetwork.QHostAddress.Any )
        self.socketFrom.bind( anyAddress, settings.notificationPort )
        self.connect( self.socketFrom,
                      SIGNAL( "readyRead()" ),
                      self.onNotification )


    def __del__( self ):
        self.socketTo.close()
        return


    def sendNotification( self, what, values = {} ):
        """ Sends a broadcast UDP notification message """

        self.socketTo.send( prepareNotification( what, values ) )
        return


    def onNotification( self ):
        """ Called when a notification has been received """

        while self.socketFrom.hasPendingDatagrams():
            datagramSize = self.socketFrom.pendingDatagramSize()
            datagram, host, port = self.socketFrom.readDatagram( datagramSize )

            values = parseNotification( str( datagram ) )

            # Check that it is a correct diagramm
            if not values.has_key( 'kioskID' ) or not values.has_key( 'what' ):
                # Unexpected diagramm
                utils.debugMsg( "Unexpected diagram format. Skipping." )
                continue

            if values[ 'kioskID' ] == utils.GlobalData().uuid:
                # Self sent diagram
                utils.debugMsg( "Self sent diagram. Skipping." )
                continue

            # emit a signal
            self.emit( SIGNAL( "peerNotification" ), values )

        return

