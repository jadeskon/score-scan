#!/usr/bin/env python

"""
IMatParser bietet das Interface für einen MatParser, der zum Einlesen eines bestimmten Datei dient und diese in eine
Bildmatrix für die Klassifizierung umwandelt.
"""

from abc import ABCMeta, abstractmethod

__author__  = "Dominik Rauch, Bonifaz Stuhr"
__version__ = "0.1.0"
__status__ = "Ready"


class IMatParser(metaclass=ABCMeta):


    @abstractmethod
    def parseToMat(self):
        """
        Interface Methode: Jeder MatParser muss diese realisieren.
        Führt den entsprechenden Einlesevorgang durch und erstellt die Bildmatrix.

        :return: imgMatrix : MatDie eingelesene Matrix.
        """
        pass

		
		