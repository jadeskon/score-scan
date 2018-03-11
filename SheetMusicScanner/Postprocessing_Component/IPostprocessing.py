#!/usr/bin/env python

"""
IPostprocessing bietet das Interface für ein Postprocessing, der zur Steuerung eines bestimmten Ablaufs des
Postprocessing einer Klassifizierung dient.
"""

from abc import ABCMeta, abstractmethod

__author__  = "Bonifaz Stuhr"
__version__ = "0.0.0"
__status__ = "Production"


class IPostprocessing(metaclass=ABCMeta):


    @abstractmethod
    def execute(self, classification):
        """
        Interface Methode: Jedes Postprocessing muss diese realisieren.
        Führt Postprocessingschritte auf die Klassifizierung aus und gibt die bearbeitet Klassifizierung zurück.

        Parameters
        ----------
        classification : Die Klassifizierung auf welche Postprocessingschritte angewendet werden sollen.

        Returns
        -------
        classification : IClassification
        Die "postprocesste" Klassifizierung.
        """
        pass
		
		
