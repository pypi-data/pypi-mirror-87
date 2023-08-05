# -*- coding: utf8 -*-

"""
Utilitats per enviar mails.
"""

from email.mime.multipart import MIMEMultipart
from email.utils import COMMASPACE, formatdate
from email.header import Header
from email.mime.text import MIMEText

from .constants import APP_CHARSET


class Mail(object):
    """Classe principal a instanciar."""

    def __init__(self, server='sisap'):
        """Inicialització de paràmetres."""
        self.to = []
        self.cc = []
        self.subject = ''
        self.text = ''
        self.attachments = []

    def __construct(self):
        """Construcció del missatge, cridat per send."""
        self.message = MIMEMultipart()
        self.message['From'] = self.me
        self.message['To'] = COMMASPACE.join(self.to)
        self.message['Cc'] = COMMASPACE.join(self.cc)
        self.message['Date'] = formatdate(localtime=True)
        self.message['Subject'] = Header(self.subject, APP_CHARSET)
        self.message.attach(MIMEText(self.text, 'plain', APP_CHARSET))
        for filename, iterable in self.attachments:
            data = '\r\n'.join([';'.join(map(str, row)) for row in iterable])
            attachment = MIMEText(data, 'plain', APP_CHARSET)
            attachment.add_header(
                'Content-Disposition',
                'attachment',
                filename=filename
            )
            self.message.attach(attachment)
        self.to += self.cc

    def send(self):
        """Enviament del mail."""
        if self.to or self.cc:
            self.__construct()
            print("SENDING EMAIL FROM:" + str(self.me))
            print("SENDING EMAIL TO:" + str(self.to))
            print("EMAIL CONTENT:\n" + str(self.message.as_string()))
