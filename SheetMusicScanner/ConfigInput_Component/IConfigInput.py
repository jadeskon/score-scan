#!/usr/bin/env python

"""
IConfigInput bietet das Interface für einen ConfigInput, der zur Steuerung eines bestimmten
Ablaufs, welcher eine Config für die gesammte Pipe einliest.
"""

from abc import ABCMeta, abstractmethod

__author__  = "Bonifaz Stuhr"
__version__ = "0.0.0"
__status__ = "Production"


class IConfigInput(metaclass=ABCMeta):


    @abstractmethod
    def execute(self):
        """
        Interface Methode: Jeder ConfigInput muss diese realisieren.
        Führt den entsprechenden Einlesevorgang über einen Parser oder ähnliches durch und erstellt die Config.

        Parameters
        ----------

        Returns
        -------
        config : Config
        Die erstellte Configuration.
        """
        pass

		