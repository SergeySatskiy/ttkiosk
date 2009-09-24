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

""" mail related functions """

import smtplib
import utils
from email.mime.text import MIMEText


def sendMail( smtpUser, smtpPassword, smtpServer, smtpPort,
              fromAddress, toAddress, subject, message ):
    """ sends an e-mail """

    msg = MIMEText( message )
    msg[ 'Subject' ] = subject
    msg[ 'From' ]    = fromAddress
    msg[ 'To' ]      = toAddress
 
    server = smtplib.SMTP( smtpServer, smtpPort )
    server.ehlo()
    server.starttls()
    server.ehlo()
    server.login( smtpUser, smtpPassword )
    server.sendmail( fromAddress, toAddress, msg.as_string() )
    server.close()
    return


def sendErrorReport( subject, message ):
    """ sends a message with the given subject
        taking the rest of parameters from settings """

    settings = utils.Settings()
    sendMail( settings.mailSmtpUser, settings.mailSmtpPassword,
              settings.mailSmtpServer, settings.mailSmtpPort,
              settings.mailFrom, settings.mailErrorRecipient,
              subject, message )
    return



