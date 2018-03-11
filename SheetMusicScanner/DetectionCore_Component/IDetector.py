#!/usr/bin/env python

"""
IDetector bietet das Interface für ein Detector, der zur Erkennung bestimmer "Merkmale" in Bildmatrizen dient.
Ein IDetector unterscheidet sich von einem IClassifier wie folgt: Ein IDetector führt Operationen im Bildraum durch und
gibt als Erbegniss dieser Operationen Bildmatrizen zurück, auf welche -über einen IClassifier- Klassifizierungen
durchgeführt werden können.
Ein IClassifier führt eine Klassifizierung auf Bildmatrizen aus und gibt das erkannte Objetc zurück. Also die
eigendliche Klassifizierung
"""

from abc import ABCMeta, abstractmethod

__author__  = "Bonifaz Stuhr"
__version__ = "0.0.0"
__status__ = "Production"


class IDetector(metaclass=ABCMeta):


    @abstractmethod
    def detect(self, matArray):
        """
        Interface Methode: Jeder Detector muss diese realisieren.
        Führt die Detektierung auf ein Array von Bildmatrizen aus und gibt das Detektierte zurück.

        Parameters
        ----------
        matArray : Die Bildmatrizen auf welche die Detektierung ausgeführt werden soll.

        Returns
        -------
        detections : matArray
        Aus dem Eingabe-matArray Detektiertes als mat (z.B. Notelinien).
        """
        pass

		
		