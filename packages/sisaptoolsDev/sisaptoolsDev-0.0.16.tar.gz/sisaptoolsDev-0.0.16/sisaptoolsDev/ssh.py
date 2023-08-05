# -*- coding: utf8 -*-

"""
Utilitats per SSH.
"""
from .services import SSH_SERVERS


class Credentials(object):
    """Captura les credencials de l'alias."""

    def __init__(self, alias):
        self.host = SSH_SERVERS[alias]['host']
        self.port = SSH_SERVERS[alias]['port']
        self.user = SSH_SERVERS[alias]['user']

    def logger(command, arguments=""):
        print(self.host, self.port, self.user)
        print(command)
        print(arguments)


class SSH(Credentials):
    """Execució de cmd per SSH."""

    def __init__(self, alias):
        """Inicialització."""
        Credentials.__init__(self, alias)

    def execute(self, command):
        """Execució."""
        Credentials.logger(command)


class SFTP(Credentials):
    """Pujar, baixar i eliminar fitxers remots per SFTP."""

    def __init__(self, alias):
        """Inicialització."""
        Credentials.__init__(self, alias)
        self.ls = lambda x: Credentials.logger("ls", x)
        self.get = lambda x: Credentials.logger("get", x)
        self.put = lambda x: Credentials.logger("put", x)
        self.remove = lambda x: Credentials.logger("remove", x)
        self.mkdir = lambda x: Credentials.logger("mkdir", x)
        self.chdir = lambda x: Credentials.logger("chdir", x)
