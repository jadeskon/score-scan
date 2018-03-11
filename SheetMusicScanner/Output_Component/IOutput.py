#!/usr/bin/env python

"""
IOutput bietet das Interface für einen Output, der zur Steuerung eines bestimmten Ablaufs des Ausgebens
einer Klassifizierung dient.
"""

from abc import ABCMeta, abstractmethod

__author__  = "Bonifaz Stuhr"
__version__ = "0.0.0"
__status__ = "Production"


class IOutput(metaclass=ABCMeta):


    @abstractmethod
    def execute(self, classification):
        """
        Interface Methode: Jeder Output muss diese realisieren.
        Führt den entsprechenden Outputvorgang über einen Parser oder ähnliches durch.

        :param classification : Die Klassifizierung auf, welche ausgegeben werden sollen.
        :return: successful : boolean War die Ausgabe erfolgreich?
        """
        pass

    @abstractmethod
    def writeNextTraindata(self, trainMats, trainLable):
        """
        Interface Methode: Jeder Output muss diese realisieren.
        Schreibt die gegebenen Trainingsdaten.

        :param trainMats : Die Trainingsbilder die geschreiben werden sollen.
        :param trainLable : Die zu den Bildern gehörenden Lable die geschreiben werden sollen.
        :return: successful : boolean War die Ausgabe erfolgreich?
        """
        pass



		
		