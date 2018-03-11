#!/usr/bin/env python

"""
IPreporcessingUnit bietet das Interface für eine PreprocessingUnit, die auf einem Eingabebild einen konkreten
Preprocessing-Schritt (wie das umwandeln in ein Binärbild) ausführt.
"""

from abc import ABCMeta, abstractmethod

__author__  = "Bonifaz Stuhr"
__version__ = "0.0.0"
__status__ = "Production"


class IPreprocessingUnit(metaclass=ABCMeta):


    @abstractmethod
    def preProcess(self, mat):
        """
        Interface Methode: Jede PreprocessingUnit muss diese realisieren.
        Führt den entsprechenden Preprocessing-Schritt auf eine Bildmatrix aus.

        Parameters
        ----------
        imgMatrix : Mat
        Die Matrix auf welcher der Preprocessing-Schritt ausgeführt werden soll.

        Returns
        -------
        imgMatrix : Mat
        Die Ergebniss-Matrix auf welcher der Preprocessing-Schritt ausgeführt wurde.
        """
        pass

		