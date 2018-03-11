#!/usr/bin/env python

"""
IClassifier bietet das Interface für ein Classifier, der zur Klassifikation bestimmer Objekte in Bildmatrizen dient.
Ein IClassifier unterscheidet sich von einem IDetector wie folgt: Ein IDetector führt Operationen im Bildraum durch und
gibt als Erbegniss dieser Operationen Bildmatrizen zurück, auf welche -über einen IClassifier- Klassifizierungen
durchgeführt werden können.
Ein IClassifier führt eine Klassifizierung auf Bildmatrizen aus und gibt das erkannte Objetc zurück. Also die
eigentliche Klassifizierung.
"""

from abc import ABCMeta, abstractmethod

__author__  = "Bonifaz Stuhr"
__version__ = "0.0.0"
__status__ = "Production"


class IClassifier(metaclass=ABCMeta):


    @abstractmethod
    def classify(self, matArray):
        """
        Interface Methode: Jeder Classifier muss diese realisieren.
        Führt die Klassifizierung auf ein Array von Bildmatrizen aus und gibt die erkannten Objekte zurück.

        Parameters
        ----------
        matArray : Die Bildmatrizen auf welche die Klassifizierung ausgeführt werden soll.

        Returns
        -------
        classificationUnits : IClassificationUnitArray
        Aus dem Eingabe-matArray Erkanntes als ClassificationUnit-Array (z.B. Note, Slur, Rest).
        """
        pass

		