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

import urllib, urlparse, utils, socket, os
from PyQt4 import QtGui, QtNetwork, QtCore
from PyQt4.QtCore import SIGNAL, QTimer
from threading import Thread


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



class PingAgent( Thread ):
    """ Checks the connection status """
    def __init__( self, application, host ):
        Thread.__init__( self )
        self.application = application
        self.host = host
        return

    def run( self ):
        retCode = os.system( 'ping -c 1 -W 4 ' + self.host + " > /dev/null" )
        self.application.onConnectionStatus( self.host, retCode == 0 )

        # Hack - make the thread restartable
        Thread.__init__( self )
        return


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

        # Prepare the ping agent
        self.pingAgent = PingAgent( self, settings.dbHost )

        # Run the timer which checks the connection periodically
        self.connectionTimer = QTimer( self )
        self.connect( self.connectionTimer, SIGNAL( "timeout()" ),
                      self.checkConnection )
        # Check the connection every 16 seconds if the connection is lost
        # or every 5 minutes if the connection is here
        self.connectionTimer.start( 16 * 1000 )

        # Check it at the very beginning
        QtCore.QTimer.singleShot( 1000, self.checkConnection )

    def __del__( self ):
        self.connectionTimer.stop()
        self.socketTo.close()
        try:
            self.pingAgent.join()
        except:
            pass
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

    def onConnectionStatus( self, host, isAlive ):
        """ Called by ping agent.
            isAlive shows the current connection status """

        if isAlive == utils.GlobalData().isConnected:
            return

        # The status has been changed
        self.connectionTimer.stop()
        utils.GlobalData().isConnected = isAlive
        if isAlive:
            # Connection restored
            # Check the connection every 5 minutes
            self.connectionTimer.start( 5 * 60 * 1000 )
            utils.debugMsg( "Connection restored. Switch interval to 5 minutes." )
        else:
            # Connection lost
            # Check the connection every 16 seconds
            self.connectionTimer.start( 16 * 1000 )
            utils.debugMsg( "Connection lost. Switch interval to 10 seconds." )

        self.emit( SIGNAL( "connectionStatus" ), isAlive )
        return

    def checkConnection( self ):
        """ Checks the connection to the web host and generates 
            a signal if the state has been changed """

        self.pingAgent.start()
        return

