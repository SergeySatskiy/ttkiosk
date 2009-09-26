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
Functions that define a framework for ttkiosk forms
"""

from utils import debugMsg, GlobalData, writeToLog
import os, os.path, sys


# Global map FormName -> Widget instance
kioskForms = {}



class FormBaseClass( object ):
    """ All the forms should derive from this class """

    def __init__( self ):
        self.arguments = {}

    def setArguments( self, args ):
        """ Stores the passed arguments """
        self.arguments = args




def buildFormsList( path ):
    """ Populates the kioskForms map """

    global kioskForms

    debugMsg( "buildFormsList(): processing " + path + "..." )
    if not os.path.exists( path ) or not os.path.isdir( path ):
        raise Exception( "buildFormsList() expects a path. The '" + \
                         path + "' does not exist or is not a directory" )
    if not path.endswith( '/' ):
        path += '/'

    # Alter the list of pathes where modules are searched
    if not path in sys.path:
        sys.path.append( path )

    for item in os.listdir( path ):
        if os.path.isdir( path + item ):
            buildFormsList( path + item + '/' )
            continue

        if item.endswith( '.py' ):
            debugMsg( "Form file found: " + path + item )
            formName = item.replace( '.py', '' )

            if kioskForms.has_key( formName ):
                raise Exception( "Form names clash detected. Name: " + \
                                 formName )

            # import the module and get the form class
            module = __import__( formName, globals(), locals(), ['*'] )
            formClass = getattr( module, formName )

            kioskForms[ formName ] = formClass()
            debugMsg( "Form '" + formName + "' has been registered." )

    return


def applyLayout( path ):
    """ processes the given layout file and applies the geometry to
        the forms. Returns the list of startup forms. """

    startupForms = []
    geometry = {}
    applySingleLayout( path, startupForms, geometry )

    # Apply geometry
    for formName in geometry:
        kioskForms[formName].move( geometry[formName][1],
                                   geometry[formName][2] )
        kioskForms[formName].resize( geometry[formName][3],
                                     geometry[formName][4] )

    return startupForms


def applySingleLayout( path, startupForms, geometry ):
    """ recursive function which parses a layout file """

    if not os.path.exists( path ):
        raise Exception( "Layout file '" + path + "' has not been found" )

    f = open( path )
    for line in f:
        line = line.strip()
        if len( line ) == 0:
            continue
        if line.startswith( '#' ):
            continue

        if line.upper().startswith( 'STARTUP' ):
            parts = line.split()
            if len( parts ) != 2:
                raise Exception( "Unexpected line format: '" + line + \
                                 "' in file '" + path + "'" )
            formName = parts[1].strip()
            if not kioskForms.has_key( formName ):
                raise Exception( "Unknown startup form '" + formName + \
                                 "' in file '" + path + "'" )

            if not formName in startupForms:
                startupForms.append( formName )
                debugMsg( "Found STARTUP form '" + formName + "'" )
            continue

        if line.upper().startswith( 'INCLUDE' ):
            parts = line.split()
            if len( parts ) != 2:
                raise Exception( "Unexpected line format: '" + line + \
                                 "' in file '" + path + "'" )

            fileName = parts[1].strip()
            if fileName.startswith( '/' ):
                # absolute path
                if not os.path.exists( fileName ):
                    raise Exception( "INCLUDE file '" + fileName + "' in '" + \
                                     path + "' has not been found" )
                applySingleLayout( fileName, startupForms, geometry )
                continue

            # relative path
            includedFileName = os.path.dirname( path ) + '/' + fileName
            includedFileName = os.path.normpath( includedFileName )
            if not os.path.exists( includedFileName ):
                raise Exception( "INCLUDE file '" + fileName + "' (" + \
                                 includedFileName + ") in '" + path + \
                                 "' has not been found" )
            applySingleLayout( includedFileName, startupForms, geometry )
            continue

        if line.upper().startswith( 'GEOMETRY' ):
            arguments = line[ len( 'GEOMETRY' ) : ].strip()
            if len( arguments ) == 0:
                raise Exception( "Unexpected line format: '" + line + \
                                 "' in file '" + path + "'" )
            formName = arguments.split()[0]
            if not kioskForms.has_key( formName ):
                raise Exception( "Unknown form '" + formName + \
                                 "' geometry in file '" + path + "'" )
            if geometry.has_key( formName ):
                raise Exception( "GEOMETRY for '" + formName + \
                                 "' has been defined twice.\nFirst: " + \
                                 geometry[formName][0] + "\nSecond: " + \
                                 path )

            arguments = arguments[ len( formName ) : ].strip()
            parts = arguments.split( ',' )
            if len( parts ) != 4:
                raise Exception( "Unexpected line format: '" + line + \
                                 "' in file '" + path + "'" )

            globalData = GlobalData()
            for index in range( 0, 4 ):
                parts[index] = parts[index].upper()
                parts[index] = parts[index].replace( '$WIDTH',
                                    str( globalData.screenWidth ) )
                parts[index] = parts[index].replace( '$HEIGHT',
                                    str( globalData.screenHeight ) )
                parts[index] = eval( parts[index] )

            geometry[ formName ] = [ path, parts[0], parts[1],
                                           parts[2], parts[3] ]
            debugMsg( "Found GEOMETRY for '" + formName + "'" )
            continue

        raise Exception( "Unexpected line '" + line + "' in " + path )

    f.close()
    return


def applySkin( path, application ):
    """ Searches for the skin files, processes them and applies them to the
        forms """

    if not os.path.exists( path ) or not os.path.isdir( path ):
        raise Exception( "applySkin() expects a path. The '" + \
                         path + "' does not exist or is not a directory" )
    if not path.endswith( '/' ):
        path += '/'

    cssFiles = []
    buildCSSFilesList( path, cssFiles )

    # The Application.css file must be applied first
    for fileName in cssFiles:
        if os.path.basename( fileName ) == 'Application.css':
            # Apply the application CSS
            content = getCSSContent( fileName ).strip()
            if len( content ) != 0:
                application.setStyleSheet( content )
                debugMsg( "Setting APPLICATION level CSS" )
                break

    # Apply all the other CSS files
    for fullFileName in cssFiles:
        fileName = os.path.basename( fullFileName )
        if fileName == 'Application.css':
            continue

        formName = fileName.replace( ".css", "" )
        if not kioskForms.has_key( formName ):
            message = "WARNING. Style sheet file " + fullFileName + \
                      " is skipped because the '" + formName + "'" \
                      " form is not registered"
            debugMsg( message )
            writeToLog( message )
            continue

        content = getCSSContent( fullFileName ).strip()
        if len( content ) != 0:
            kioskForms[formName].setStyleSheet( content )
            debugMsg( "Setting CSS for '" + formName + "' form" )

    return


def getCSSContent( fileName ):
    """ Returns the css file content with resolved INCLUDEs and
        without remarks """

    content = []
    parseSingleCSS( fileName, content )
    return "".join( content )


def parseSingleCSS( path, content ):
    """ Recursive function to get a single CSS content
        with removed comment lines and resolved INCLUDEs """

    f = open( path )
    for line in f:
        if line.strip().startswith( '//' ):
            continue
        if line.strip().upper().startswith( 'INCLUDE' ):
            parts = line.strip().split()
            if len( parts ) != 2:
                raise Exception( "Unexpected line format: '" + line + \
                                 "' in file '" + path + "'" )

            fileName = parts[1].strip()
            if fileName.startswith( '/' ):
                # absolute path
                if not os.path.exists( fileName ):
                    raise Exception( "INCLUDE file '" + fileName + "' in '" + \
                                     path + "' has not been found" )
                parseSingleCSS( fileName, content )
                continue

            # relative path
            includedFileName = os.path.dirname( path ) + '/' + fileName
            includedFileName = os.path.normpath( includedFileName )
            if not os.path.exists( includedFileName ):
                raise Exception( "INCLUDE file '" + fileName + "' (" + \
                                 includedFileName + ") in '" + path + \
                                 "' has not been found" )
            parseSingleCSS( includedFileName, content )
            continue
        # Some line
        if len( line.strip() ) > 0:
            content.append( line )

    f.close()
    return


def buildCSSFilesList( path, cssFiles ):
    """ builds a list of the .css files to be processed """

    debugMsg( "buildCSSFilesList(): processing " + path )
    for item in os.listdir( path ):
        if os.path.isdir( path + item ):
            buildCSSFilesList( path + item + '/', cssFiles )
            continue
        if item.endswith( '.css' ):
            cssFiles.append( path + item )
            debugMsg( "Found CSS: " + path + item )
            continue
    return


def showForm( formName ):
    """ shows the required form """

    if not kioskForms.has_key( formName ):
        raise Exception( "Try to show not registered form '" + formName + "'" )

    kioskForms[ formName ].show()
    debugMsg( "Showing form '" + formName + "'" )
    return


def setFormArguments( formName, arguments ):
    """ passes arguments to the required form """

    if not kioskForms.has_key( formName ):
        raise Exception( "Try to set arguments for not registered form '" + \
                         formName + "'" )

    kioskForms[ formName ].setArguments( arguments )
    debugMsg( "Setting arguments for '" + formName + "' form" )
    return


def findForm( formName ):
    """ Searches for the form """

    if not kioskForms.has_key( formName ):
        raise Exception( "Form '" + formName + "' is not registered." )

    return kioskForms[ formName ]

