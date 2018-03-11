#!/usr/bin/env python

"""
Der State ist eine Realisierung des Interfaces IState der zur Initialisierung der Stateklassen dient.
"""

from State_Component.IState import IState
from State_Component.Logger.SLogController import SLogController

__author__  = "Bonifaz Stuhr"
__version__ = "0.0.0"
__status__ = "Production"


class State(IState):

    def __init__(self):
        """
        Constructor, initialisiert Membervariablen.

        Parameters
        ----------

        Example
        -------
        >>> Sate()
        """
        self.__logger = SLogController().getLogger("State_Component_Logger")

    def init(self, config):
        """
        Initialisiert die State Klassen, welche von Pipe und Controller verwendet werden.

        Parameters
        ----------
        config : Config
        Die Konfiguration.

        Returns
        -------
        successful : boolean
        Initialisierung erfolgreich?

        Example
        -------
        >>> state.init()
        """
        self.__logger.info("Starting init()", "State:init")
        """
        Todo: try stateClasses.init(self.__config) 
        """
        self.__logger.info("Finished init()", "State:init")
        return True

    def getLogger(self, name, append = False):
        """
        State Interface to get a Logger from the SLogController.
        Gibt den Logger mit gegebenen Namen zurück oder erstellt einen neuen, falls noch nicht vorhanden.

        :param name: Der Name des Loggers.
        :param append: Bestimmt ob Logmeldungen an ein bereits bestehendes Logfile angehängt werden, oder das alte Logfile überschrieben wird. Gilt nur beim ersten Aufruf des Loggers. [False] by default.
        :return: Der Logger.
        """
        return SLogController().getLogger(name, append)
		
		