#!/usr/bin/env python

"""
IConfigParser bietet das Interface für einen ConfigParser, welcher zum Einlesens eines Config-Files dient.
"""

from abc import ABCMeta, abstractmethod

__author__  = "Bonifaz Stuhr"
__version__ = "0.0.0"
__status__ = "Production"


class IConfigParser(metaclass=ABCMeta):


    @abstractmethod
    def parse(self):
        """
        Interface Methode: Jeder ConfigParser muss diese realisieren.
        Parst das entsprechende File und erstellt die Config.

        Parameters
        ----------

        Returns
        -------
        config : Config
        Die erstellte Config.
        """
        pass

		