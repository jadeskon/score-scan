#!/usr/bin/env python

"""
Der Input ist eine Realisierung des Interfaces IPostprocessing und dient zur Steuerung eines bestimmten Ablaufs des
Postrocessing einer Klassifizierung.
"""

from Postprocessing_Component.IPostprocessing import IPostprocessing
from State_Component.State.State import State

__author__  = "Bonifaz Stuhr"
__version__ = "0.0.0"
__status__ = "Production"


class Postprocessing(IPostprocessing):

    def __init__(self, config):
        """
        Constructor, initialisiert Membervariablen.

        Parameters
        ----------
        config : Config
        Die Konfiguration.

        Example
        -------
        >>> Postprocessing(config)
        """
        self.__logger = State().getLogger("Postprocessing_Component_Logger")
        self.__logger.info("Starting __init__()", "Postprocessing:__init__")
        """
        Todo: create some Postprocessing Classes 
        """
        self.__logger.info("Finished __init__()", "Postprocessing:__init__")

    def execute(self, classification):
        """
        Führt Postprocessingschritte auf die Klassifizierung aus und gibt die bearbeitet Klassifizierung zurück.

        Parameters
        ----------
        classification : Die Klassifizierung auf welche Postprocessingschritte angewendet werden sollen.

        Returns
        -------
        classification : IClassification
        Die "postprocesste" Klassifizierung.

        Example
        -------
        >>> postprocessing.execute(classification)
        """
        self.__logger.info("Starting execute()", "Postprocessing:execute")
        """
        Todo: execute some postprocessing classes
        """
        self.__logger.info("Finished execute()", "Postprocessing:execute")

        return classification

		
		