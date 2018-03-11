#!/usr/bin/env python

"""
IState bietet das Interface für einen State, der zur Initialisierung der Stateklassen dient.
"""

from abc import ABCMeta, abstractmethod

__author__  = "Bonifaz Stuhr"
__version__ = "0.0.0"
__status__ = "Production"


class IState(metaclass=ABCMeta):

    @abstractmethod
    def init(self, config):
        """
        Interface Methode: Jeder State muss diese realisieren.
        Initialisiert die State Klassen, welche von Pipe und Controller verwendet werden.

        Parameters
        ----------
        config : Config
        Die Konfiguration.

        Returns
        -------
        successful : boolean
        Initialisierung erfolgreich?
        """
        pass

    @abstractmethod
    def getLogger(self, name, append = False):
        """
        Interface Methode: Jeder State muss diese realisieren.
        State Interface to get a Logger from the SLogController.
        Gibt den Logger mit gegebenen Namen zurück oder erstellt einen neuen, falls noch nicht vorhanden.

        :param name: Der Name des Loggers.
        :param append: Bestimmt ob Logmeldungen an ein bereits bestehendes Logfile angehängt werden, oder das alte Logfile überschrieben wird. Gilt nur beim ersten Aufruf des Loggers. [False] by default.
        :return: Der Logger.
        """
        pass

		
		
