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

import sys, os, time, getpass, os.path, tempfile, ConfigParser
import socket, fcntl, struct

from subprocess import Popen, PIPE



# Configuration files in the order of search
configFile = [ "/ttkiosk/etc/ttkiosk.ini", "/etc/ttkiosk/ttkiosk.ini",
               "~/ttkiosk.ini" ]


debug = False           # Updated from ttkiosk.py
debugWindow = None      # Updated from ui.py

def debugMsg( message ):
    """ Writes a message to a debug file """

    if not debug:
        return

    # Debug message file is always here
    fileName = '/var/log/ttkiosk/ttkiosk.debug'
    message = time.ctime( time.time() ) + ' ' + message
    try:
        f = open( fileName, "a+" )
        f.write( message + '\n' )
        f.close()
    except:
        pass

    if not debugWindow is None:
        debugWindow.appendMessage( message )

    return


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


def getConfigFileName():
    """ Returns the settings file name """

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
    return configFileName


class GlobalData( object ):
    """ Global data singleton """
    _iInstance = None
    class Singleton:
        """ Provides singleton facility """

        def __init__( self ):
            self.isAdmin = False
            self.screenWidth = 0
            self.screenHeight = 0
            self.startupForms = []
            self.application = None
            self.uuid = ""
            self.isConnected = False
            return

    def __init__( self ):
        if GlobalData._iInstance is None:
            GlobalData._iInstance = GlobalData.Singleton()
        self.__dict__[ '_GlobalData__iInstance' ] = GlobalData._iInstance
        return

    def __getattr__( self, aAttr ):
        return getattr( self._iInstance, aAttr )

    def __setattr__( self, aAttr, aValue ):
        setattr( self._iInstance, aAttr, aValue )
        return


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
            configFileName = getConfigFileName()
            debugMsg( "Configuration file: " + configFileName )

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
            debugMsg( "[mail]" )
            debugMsg( "smtpUser: " + self.mailSmtpUser )
            debugMsg( "smtpPassword: " + self.mailSmtpPassword )
            debugMsg( "smtpServer: " + self.mailSmtpServer )
            debugMsg( "smtpPort: " + self.mailSmtpPort )
            debugMsg( "from: " + self.mailFrom )
            debugMsg( "errorRecipient: " + self.mailErrorRecipient )

            path = get_string( config, "path", "logs" )
            self.pathLogs = normalizeDir( "Logs", path )

            path = get_string( config, "path", "videos" )
            self.pathVideos = normalizeDir( "Videos", path )

            path = get_string( config, "path", "slides" )
            self.pathSlides = normalizeDir( "Slides", path )

            path = get_string( config, "path", "templates" )
            self.pathTemplates = normalizeDir( "Templates", path )

            debugMsg( "[path]" )
            debugMsg( "logs: " + self.pathLogs )
            debugMsg( "videos: " + self.pathVideos )
            debugMsg( "slides: " + self.pathSlides )
            debugMsg( "templates: " + self.pathTemplates )

            # Build the skin path
            self.generalSkin = get_string( config, "general", "skin" )
            debugMsg( "skin: " + self.generalSkin )

            path = get_string( config, "path", "skins" )
            pathSkins = normalizeDir( "Skins", path )
            debugMsg( "skins: " + pathSkins )

            self.pathSkin = pathSkins + self.generalSkin
            if not self.pathSkin.endswith( '/' ):
                self.pathSkin = self.pathSkin + '/'
            if not os.path.exists( self.pathSkin ):
                raise Exception( "The '" + self.generalSkin + \
                                 "' skin directory (" + \
                                 self.pathSkin + ") has not been found" )
            debugMsg( "skin path: " + self.pathSkin )

            # Read DB section
            self.dbHost = get_string( config, "db", "host" )
            debugMsg( "DB host: " + self.dbHost )

            # Get notification port
            self.notificationPort = int( get_string( config,
                                                     "general",
                                                     "notificationPort" ) )
            debugMsg( "notification port: " + str( self.notificationPort ) )

            self.adminPassword = get_string( config, "general",
                                             "adminPassword" )
            debugMsg( "Administrator password: " + self.adminPassword )

            self.venue = get_string( config, "general", "venue" )
            debugMsg( "Venue: " + self.venue )

            # Check timeout
            self.timeoutIdle = int( get_string( config, "timeout", "idle" ) )
            if self.timeoutIdle < 0:
                raise Exception( "Idle timeout has to be >= 0. 0 means never." )
            debugMsg( "idle timeout: " + str( self.timeoutIdle ) )
            debugMsg( "Configuration has been read" )

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


def getIPAddress( ifname ):
    """ Provides the given interface IP address """

    soc = socket.socket( socket.AF_INET, socket.SOCK_DGRAM )
    return socket.inet_ntoa( fcntl.ioctl( soc.fileno(),
                                          0x8915,  # SIOCGIFADDR
                                          struct.pack( '256s', ifname[:15] )
                                        )[20:24]
                           )


def getInterfaceAddresses():
    """ Tries to get IP addresses of some interfaces """

    addresses = []
    ifaces = [ 'eth0', 'eth1', 'wlan0', 'wlan1' ]
    for iface in ifaces:
        try:
            addresses.append( iface + ": " + getIPAddress( iface ) )
        except:
            pass
    return addresses


def getStrippedSettingsFileContent():
    """ Returns the settings file content without remarks and empty lines """

    content = ""
    try:
        fileName = getConfigFileName()
        f = open( fileName, "r" )
        for line in f:
            line = line.strip()
            if line != "" and not line.startswith( '#' ):
                if len( content ) > 0:
                    content += "\n"
                content += line
        f.close()
    except:
        pass
    return content


def collectHostInfo():
    """ Returns a string with the whole host info """

    ifaces = getInterfaceAddresses()
    iniFileContent = getStrippedSettingsFileContent()

    hostInfo = "Date: " + time.ctime( time.time() ) + "\n" \
               "---------------------------------------\n" \
               "Python version: " + sys.version + "\n" \
               "OS version: " + "; ".join( os.uname() ) + "\n" \
               "User: " + getpass.getuser() + \
                          " (" + str( os.getuid() ) + ")\n" \
               "Current directory: " + os.getcwd() + "\n"

    for iface in ifaces:
        hostInfo += iface + "\n"

    hostInfo += "---------------------------------------\n"

    if len( iniFileContent ) > 0:
        hostInfo += "Configuration file content:\n" + iniFileContent + "\n" \
                    "---------------------------------------\n"

    hostInfo += "Environment variables:\n"
    for param in os.environ.keys():
        hostInfo += param + " = " + os.environ[param] + "\n"

    return hostInfo


def writeToLog( message ):
    """ Writes the given message to the log file """

    if not message.endswith( '\n' ):
        message += '\n'

    try:
        settings = Settings()
        logFileName = settings.pathLogs + "ttkiosk.log"
        f = open( logFileName, "a" )
        if message.count( '\n' ) == 1:
            # Single line message
            f.write( time.ctime( time.time() ) + ": " + message )
        else:
            # Many lines message
            timestamp = time.ctime( time.time() )
            f.write( timestamp + " ------ begin ------\n" )
            f.write( message )
            f.write( timestamp + " ------ end ------\n" )
        f.close()
    except:
        pass
    return

