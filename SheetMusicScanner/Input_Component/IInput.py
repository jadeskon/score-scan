#!/usr/bin/env python

"""
IInput bietet das Interface für einen Input, der zur Steuerung eines bestimmten Ablaufs des Einlesens
einer Bildmatrix für die Klassifizierung dient.
"""

from abc import ABCMeta, abstractmethod

__author__  = "Bonifaz Stuhr"
__version__ = "0.0.0"
__status__ = "Production"


class IInput(metaclass=ABCMeta):


    @abstractmethod
    def execute(self):
        """
        Interface Methode: Jeder Input muss diese realisieren.
        Führt den entsprechenden Einlesevorgang über einen Parser durch und erstellt die Bildmatrix.
        :return: mat Die Matrix des eingelesenen Bildes
        """
        pass

    @abstractmethod
    def readNextImgXMLPair(self):
        """
        Interface Methode: Jeder Input muss diese realisieren.
        Führt den entsprechenden Einlesevorgang für die nächsten Files im Ordner
        über einen Parser durch und erstellt die Bildmatrix sowie das Lable.
        :return: mat Die Matrix des eingelesenen Bildes.
        :return: lable Das Lable zur Bildmatrix.
        """
        pass

    @abstractmethod
    def readNoteTrainData(self):
        """
        Interface Methode: Jeder Input muss diese realisieren.
        Führt den entsprechenden Einlesevorgang für einen Ordner über einen Parser durch und gibt die
        Notentrainingsdaten mit ihrem Label zurück.
        :return: matArray Die MAtrizen des eingelesenen Bildes.
        :return: lableArray Die Lable zu den Bildmatrizen.
        """
        pass
		
		