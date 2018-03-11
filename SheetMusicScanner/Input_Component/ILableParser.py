#!/usr/bin/env python

"""
ILableParser bietet das Interface für einen lableParser, der zum Einlesen eines bestimmten Datei dient und diese in ein
Lable für das Training oder das Erstellen eines Testdatensatzes umwandelt.
"""

from abc import ABCMeta, abstractmethod

__author__  = "Bonifaz Stuhr"
__version__ = "0.1.0"
__status__ = "Ready"


class ILableParser(metaclass=ABCMeta):


    @abstractmethod
    def parseToLable(self):
        """
        Interface Methode: Jeder LableParser muss diese realisieren.
        Führt den entsprechenden Einlesevorgang durch und erstellt das Lable.

        :return: lable : Array of Dictionarys Das eingelesene Lable.
        """
        pass

		
		