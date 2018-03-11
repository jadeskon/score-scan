#!/usr/bin/env python

"""
IFullClassifier bietet das Interface für ein FullClassifier, der zur Erstellung eine vollständigen Klassifikation
aus der Eingabematrix dient.
Ein FullClassifier kann aus mehreren IDetector und IClassifier bestehen und deren Aus- und Eingaben geschickt
kombinieren. Dabei verwendet dieser IDetectors um das Eingabebild für die IClassifier zurecht zu machen.
Beispielsweiße könnte ein IDetector verwendet werden, der das Eingabebild anhand der Musiklinien in mehrere Bilder
aufteilt. Diese Musiklinienbilder werden dann von einem IDetector-IClassifier Hybrid in Taktbilder zerlegt, wobei
gleichzeitig die Takte als IClassificationUnit erkannt werden. Danach werden die Taktbilder weiteren IClassifier
gebeben, welche Noten, Pausen, usw. als IClassificationUnit erkennen.
"""


from abc import ABCMeta, abstractmethod

__author__  = "Bonifaz Stuhr"
__version__ = "0.0.0"
__status__ = "Production"


class IFullClassifier(metaclass=ABCMeta):


    @abstractmethod
    def executeClassification(self, mat):
        """
        Interface Methode: Jeder FullClassifier muss diese realisieren.
        Führt die Klassifizierung auf einer Bildmatrix aus und gibt die erkannte IClassification zurück.

        :param Bildmatrix : mat Die Bildmatrix auf welche die Klassifizierung ausgeführt werden soll.
        :return: classification : IClassification Aus dem Eingabematrix erkannte IClassification (z.B. Note, Slur, Rest).
        """
        pass

    @abstractmethod
    def buildTraindata(self, mat):
        """
        Interface Methode: Jeder FullClassifier muss diese realisieren.
        Erstellt Trainingdaten für das Trainieren seiner Classifier

        :param Bildmatrix : mat Die Bildmatrix aus welcher die Trainingdaten erstellt werden soll.
        :return: trainData : matArray Aus dem Eingabematrix erstellte Trainingdaten.
        """
        pass

    @abstractmethod
    def train(self, inputMatArray, lableArray):
        """
        Trainiert alle trainierbaren Classifier mit den gegebenen Trainingsdaten

        :param Bildmatrizen: inputMatArray Die Bildmatrizen für das Training.
        :param Lable: lableArray Die Lable zu den Bildmatrizen für das Training.
        :return: successful : boolean War das Training erfolgreich?
        """
        pass
		
		
