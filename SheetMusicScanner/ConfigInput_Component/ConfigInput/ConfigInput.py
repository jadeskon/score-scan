#!/usr/bin/env python

"""
Der ConfigInput ist eine Realisierung des Interfaces IConfigInput und dient zur Steuerung eines bestimmten
Ablaufs, welcher eine Config für die gesammte Pipe einliest.
"""

from ConfigInput_Component.IConfigInput import IConfigInput
from State_Component.State.State import State
from ConfigInput_Component.ConfigParser.JsonParser import JsonParser

__author__  = "Bonifaz Stuhr"
__version__ = "0.0.0"
__status__ = "Production"


class ConfigInput(IConfigInput):

    def __init__(self, configPath):
        """
        Constructor, initialisiert Membervariablen

        Parameters
        ----------
        configPath : string
        Path to config file.

        Example
        -------
        >>> ConfigInput("/path/to/config")
        """
        self.__logger = State().getLogger("ConfigInput_Component_Logger")
        self.__logger.info("Starting __init__() with ConfigPath: " + configPath, "Input:__init__")
        self.__configParser = JsonParser(configPath)
        self.__logger.info("Finished __init__() with ConfigPath: " + configPath, "Input:__init__")

    def execute(self):
        """
        Führt den entsprechenden Einlesevorgang über einen Parser durch und erstellt die Config.

        Parameters
        ----------

        Returns
        -------
        config : Config
        Die erstellte Konfiguration.

        Example
        -------
        >>> configInput.execute()
        """
        self.__logger.info("Starting execute()", "Input:execute")

        config = self.__configParser.parse()

        self.__logger.info("Finished execute()", "Input:execute")
        return config

		
		