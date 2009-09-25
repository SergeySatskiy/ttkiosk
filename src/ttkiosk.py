#!/bin/env python
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

"""
ttkiosk main Python script.
It performs necessery initialization and starts the Qt main loop.
"""

__version__ = "0.0.1"

import utils, mail, sys, os.path
from PyQt4 import QtGui
from optparse import OptionParser

# Make it possible to import from the ./ui directory
sys.path.append( os.path.dirname( os.path.abspath( sys.argv[0] ) ) + '/ui/' )
import ui


def ttkioskMain():
    """ The ttkiosk driver """

    parser = OptionParser(
    """
    %prog [options]
    Runs table tennis club touch screen kiosk UI
    """ )

    parser.add_option( "-g", "--debug",
                       action="store_true", dest="debug", default=False,
                       help="debug mode (default: False)" )

    options, args = parser.parse_args()
    if len( args ) != 0:
        print >> sys.stderr, "Warning: all the arguments are ignored."
        parser.print_help()

    utils.debug = options.debug

    # Load settings
    settings = None
    try:
        settings = utils.Settings()
    except:
        message = utils.getExceptionInfo()
        print >> sys.stderr, "Error loading settings. " \
                             "Fix the error and run again."
        sys.exit( 1 )

    # Settings have been loaded successfully.
    # Now the default exception handler can be replaced
    # sys.excepthook = exceptionHook

    globalData = utils.GlobalData()
    ttkioskApp = QtGui.QApplication( sys.argv )

    screenSize = ttkioskApp.desktop().screenGeometry()
    globalData.screenWidth = screenSize.width()
    globalData.screenHeight = screenSize.height()

    formsPath = os.path.dirname( os.path.abspath( sys.argv[0] ) ) + '/ui/' + \
                str( screenSize.width() ) + 'x' + str( screenSize.height() ) + \
                '/'

    # Build a list of forms, apply layout, apply CSS
    ui.buildFormsList( formsPath )
    startupForms = ui.applyLayout( formsPath + 'layout.ini' )
    ui.applySkin( settings.pathSkin, ttkioskApp )

    if len( startupForms ) == 0:
        raise Exception( "No startup forms found. Exiting." )

    # Show startup forms; the startup forms may not have arguments
    for formName in startupForms:
        ui.showForm( formName )

    # Run the application main cycle
    ttkioskApp.exec_()


def exceptionHook( excType, excValue, tracebackobj ):
    """ Catches unhandled exceptions """

    # Write a message to a log file
    utils.writeToLog( "Unhandled exception is caught\n" + \
                      utils.getExceptionInfo() )

    print >> sys.stderr, "Unhandled exception is caught\n" + \
                         utils.getExceptionInfo()

    # Display the message as a QT modal dialog box if the 


    # TODO: e-mail sending is better done as asynch process because it
    #       causes delays especially if the connection is broken
    # Send an e-mail
    try:
        mail.sendErrorReport( "ttkiosk: unhandled exception",
                              "Unhandled exception is caught\n" + \
                              utils.getExceptionInfo() + "\n" + \
                              utils.collectHostInfo() )
    except:
        utils.writeToLog( "Cannot send e-mail error report: " + \
                          utils.getExceptionInfo() )

if __name__ == '__main__':
    ttkioskMain()

