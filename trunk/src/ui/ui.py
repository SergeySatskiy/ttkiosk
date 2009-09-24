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

from utils import debugMsg


kioskForms = {}

def buildFormsList( path ):
    """ Populates the kioskForms map """


    pass


def applyLayout( path ):
    """ processes the given layout file and applies the geometry to
        the forms. Returns the list of startup forms. """

    return []


def parseLayoutFile( path ):
    """ Parses the given layout file and returns two lists:
        startup forms identifiers and
        geometry entries
    """

    pass


def applySkin( path, application ):
    """ Searches for the skin files, processes them and applies them to the
        forms """


    pass


def showForm( formName ):
    """ shows the required form """

    if not kioskForms.has_key( formName ):
        raise Exception( "Try to show not registered form '" + formName + "'" )

    kioskForms[ formName ].show()
    return


def setFormArguments( formName, arguments ):
    """ passes arguments to the required form """

    if not kioskForms.has_key( formName ):
        raise Exception( "Try to set arguments for not registered form '" + \
                         formName + "'" )

    kioskForms[ formName ].setArguments( arguments )
    return

