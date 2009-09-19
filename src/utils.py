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

""" utility functions """

import sys, os, os.path, tempfile, ConfigParser
from subprocess import Popen, PIPE
from traceback import format_tb



# Configuration files in the order of search
configFile = [ "/ttkiosk/etc/ttkiosk.ini", "/etc/ttkiosk/ttkiosk.ini",
               "~/ttkiosk.ini" ]


def safeRun( commandArgs ):
    """ Runs the given command and reads the output """

    errTmp = tempfile.mkstemp()
    errStream = os.fdopen( errTmp[0] )
    process = Popen( commandArgs, stdin = PIPE,
                     stdout = PIPE, stderr = errStream )
    process.stdin.close()
    processStdout = process.stdout.read()
    process.stdout.close()
    errStream.seek( 0 )
    err = errStream.read()
    errStream.close()
    os.unlink( errTmp[1] )
    process.wait()
    if process.returncode != 0:
        raise Exception( "Error in '%s' invocation: %s" % \
                         (commandArgs[0], err) )
    return processStdout



def getExceptionInfo():
    """
    The function formats the exception and returns the string which
    could be then printed or logged
    """

    excType, value, tback = sys.exc_info()
    msg = str( value )

    if len( msg ) == 0:
        msg = "There is no message associated with the exception."
    if msg.startswith( '(' ) and msg.endswith( ')' ):
        msg = msg[1:-1]

    try:
        tbInfo = format_tb( tback )
        tracebackInfoMsg = "Traceback information:\n" + "".join( tbInfo )
    except:
        tracebackInfoMsg = "No traceback information available"

    return "Exception is cought. " + msg + "\n" + tracebackInfoMsg


def getExceptionMessage():
    """ The function returns the exception associated string """

    excType, value, tback = sys.exc_info()
    msg = str( value )

    if len( msg ) == 0:
        msg = "There is no message associated with the exception."
    if msg.startswith( '(' ) and msg.endswith( ')' ):
        msg = msg[1:-1]

    return msg


class Settings( object ):
    """
    Read only singleton settings
    Implementation idea is taken from here:
    http://wiki.forum.nokia.com/index.php/How_to_make_a_singleton_in_Python
    """

    _iInstance = None
    class Singleton:
        """ Provides settings singleton facility """

        def __init__( self ):
            # Settings members
            configFileName = ""
            for name in configFile:
                if "~" in name:
                    name = name.replace( "~", os.environ["HOME"] )
                if os.path.exists( name ):
                    configFileName = name
                    break
            if configFileName == "":
                raise Exception( "Config file is not found. Checked: " + \
                                 " ".join( configFile ) )


            # Read the settings
            config = ConfigParser.ConfigParser()
            config.read( [ configFileName ] )

            self.mailSmtpUser       = get_string( config, "mail",
                                                          "smtpUser" )
            self.mailSmtpPassword   = get_string( config, "mail",
                                                          "smtpPassword" )
            self.mailSmtpServer     = get_string( config, "mail",
                                                          "smtpServer" )
            self.mailSmtpPort       = get_string( config, "mail",
                                                          "smtpPort" )
            self.mailFrom           = get_string( config, "mail",
                                                          "from" )
            self.mailErrorRecipient = get_string( config, "mail",
                                                          "errorRecipient" )

            path = get_string( config, "path", "logs" )
            self.pathLogs = normalizeDir( "Logs", path )

            path = get_string( config, "path", "videos" )
            self.pathVideos = normalizeDir( "Videos", path )

            path = get_string( config, "path", "slides" )
            self.pathSlides = normalizeDir( "Slides", path )

            path = get_string( config, "path", "templates" )
            self.pathTemplates = normalizeDir( "Templates", path )


            # Build the skin path
            self.generalSkin = get_string( config, "general", "skin" )

            path = get_string( config, "path", "skins" )
            pathSkins = normalizeDir( "Skins", path )

            self.pathSkin = pathSkins + self.generalSkin
            if not self.pathSkin.endswith( '/' ):
                self.pathSkin = self.pathSkin + '/'
            if not os.path.exists( self.pathSkin ):
                raise Exception( "The '" + self.generalSkin + \
                                 "' skin directory (" + \
                                 self.pathSkin + ") has not been found" )

            # Check timeout
            self.timeoutIdle = int( get_string( config, "timeout", "idle" ) )
            if self.timeoutIdle < 0:
                raise Exception( "Idle timeout has to be >= 0. 0 means never." )

            config = None
            return

    def __init__( self ):

        if Settings._iInstance is None:
            Settings._iInstance = Settings.Singleton()

        self.__dict__[ '_Settings__iInstance' ] = Settings._iInstance
        return

    def __getattr__( self, aAttr ):
        return getattr( self._iInstance, aAttr )


def get_string( config, section, value ):
    """ Reads string value and strips quotas if there are """

    value = config.get( section, value )
    if value.startswith( '"' ) and value.endswith( '"' ):
        return value[ 1:-1 ]
    elif value.startswith( "'" ) and value.endswith( "'" ):
        return value[ 1:-1 ]
    return value


def normalizeDir( pathName, path ):
    """ Forms an absolute path and adds / if it is not there """

    path = os.path.abspath( path )
    if not path.endswith( '/' ):
        path = path + "/"

    if not os.path.exists( path ):
        raise Exception( pathName + " path (" + path + ") has not been found" )

    return path


def resolveSymbolicLink( path ):
    """ resolves the symbolic link and
        provides the resolution path and the final path
        Expects a full path
    """

    if not os.path.exists( path ):
        raise Exception( "Cannot find file: '" + path + "'" )

    resolutionPath = path
    currentPath = path

    while os.path.islink( currentPath ):
        sLink = os.readlink( currentPath )
        if sLink.startswith( '/' ):
            currentPath = sLink
        else:
            currentPath = os.path.abspath( os.path.dirname( currentPath ) + \
                                           '/' + sLink )
        resolutionPath += " -> " + currentPath
        if not os.path.exists( currentPath ):
            raise Exception( "Cannot find file: '" + currentPath + \
                             "' while resolving " + resolutionPath )

    return resolutionPath, currentPath



def splitThousands( value, sep="'"):
    """ provides thousands separated value """
    if len( value ) <= 3:
        return value
    return splitThousands( value[:-3], sep) + sep + value[-3:]

