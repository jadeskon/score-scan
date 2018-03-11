#!/usr/bin/env python

"""
IPreprocessing bietet das Interface für ein Preprocessing, der zur Steuerung eines bestimmten Ablaufs des Preprocessing
einer Bildmatrix dient, welche diese für die Klassifizierung vorbereitet.
"""

from abc import ABCMeta, abstractmethod

__author__  = "Bonifaz Stuhr"
__version__ = "0.0.0"
__status__ = "Production"


class IPreprocessing(metaclass=ABCMeta):


    @abstractmethod
    def execute(self, mat):
        """
        Interface Methode: Jedes Preprocessing muss diese realisieren.
        Führt Preprocessingschritte auf die BildMatrix aus und gibt die bearbeitet Matrix zurück.

        Parameters
        ----------
        mat : Die Bildmatrix auf welche Preprocessingschritte angewendet werden sollen.

        Returns
        -------
        imgMatrix : Mat
        Die "preprocesste" Matrix.
        """
        pass

		
		