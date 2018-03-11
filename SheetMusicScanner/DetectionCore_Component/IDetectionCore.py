#!/usr/bin/env python

"""
IDetectionCore bietet das Interface für ein DetectionCore, der zur Steuerung eines bestimmten Klassifiezerung
einer Bildmatrix dient.
"""

from abc import ABCMeta, abstractmethod

__author__  = "Bonifaz Stuhr"
__version__ = "0.0.0"
__status__ = "Production"


class IDetectionCore(metaclass=ABCMeta):


    @abstractmethod
    def execute(self, mat):
        """
        Interface Methode: Jeder DetectionCore muss diese realisieren.
        Führt die Klassifiezierung auf die BildMatrix aus und gibt die Klassifiezierung zurück.

        :param Bildmatrix: mat Die Bildmatrix auf welcher die Klassifiezierung stattfinden soll.
        :return: IClassification : classification Die Klassifizierung
        """
        pass


    @abstractmethod
    def buildNextTraindata(self, mat):
        """
        Interface Methode: Jeder DetectionCore muss diese realisieren.
        Erstellt Trainingsdaten und fügt diese einem Ordner hinzu.

        :param Bildmatrix: mat Die Bildmatrix aus welcher die Trainingsdaten erstell werden sollen.
        :return: nextTrainData : Trainingsdaten zu gegebenem Bild und Lable.
        """
        pass


    @abstractmethod
    def executeTrain(self, inputMatArray, lableArray):
        """
        Interface Methode: Jeder DetectionCore muss diese realisieren.
        Trainiert alle FullClassifier und deren Classifier mit den gegebenen Trainingsdaten

        :param Bildmatrizen: inputMatArray Die Bildmatrizen für das Training.
        :param Lable: lableArray Die Lable zu den Bildmatrizen für das Training.
        :return: successful : boolean War das Training erfolgreich?
        """
        pass

		
		