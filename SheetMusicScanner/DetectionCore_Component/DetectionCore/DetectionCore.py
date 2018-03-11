#!/usr/bin/env python

"""
Der DetectionCore ist eine Realisierung des Interfaces DetectionCore und dient zur Steuerung eines bestimmten
Klassifiezerung einer Bildmatrix.
"""

from DetectionCore_Component.IDetectionCore import IDetectionCore
from DetectionCore_Component.FullClassifier.SheetMusicTemplateClassifier import SheetMusicTemplateClassifier
from State_Component.State.State import State

__author__ = "Bonifaz Stuhr"
__version__ = "0.0.0"
__status__ = "Production"


class DetectionCore(IDetectionCore):

    def __init__(self, config):
        """
        Constructor, initialisiert Membervariablen

        :param Config: config Die Konfiguration.
        :example:
            DetectionCore(config)
        """
        self.__logger = State().getLogger("DetectionCore_Component_Logger")
        self.__logger.info("Starting __init__()", "DetectionCore:__init__")

        self.__fullClassifier = SheetMusicTemplateClassifier(config["SheetMusicClassifier"])
        """
        Todo:     
        self.__classificationCombiner = some ClassificationCombiner
        Mehr fullClassifier können hier erstellt werden
        """
        self.__logger.info("Finished __init__()", "DetectionCore:__init__")

    def execute(self, mat):
        """
        Führt die Klassifiezierung auf die BildMatrix aus und gibt die Klassifiezierung zurück.

        :param Bildmatrix: mat Die Bildmatrix auf welcher die Klassifiezierung stattfinden soll.
        :return: IClassification : classification Die Klassifizierung
        :example:
            detectionCore.execute(mat)
        """
        self.__logger.info("Starting execute()", "DetectionCore:execute")

        classification = self.__fullClassifier.executeClassification(mat)
        """
        Todo: 
        Dann könnten noch weitere fullClassifier klassifizieren und ein Combiner die Klassifizierungen bewerten 
        und kombinieren.
        """

        self.__logger.info("Finished execute()", "DetectionCore:execute")
        return classification

    def buildNextTraindata(self, mat):
        """
        Interface Methode: Jeder DetectionCore muss diese realisieren.
        Erstellt Trainingsdaten und fügt diese einem Ordner hinzu.

        :param Bildmatrix: mat Die Bildmatrix aus welcher die Trainingsdaten erstell werden sollen.
        :return: nextTrainData : Trainingsdaten zu gegebenem Bild und Lable.
        """
        self.__logger.info("Starting buildNextTraindata()", "DetectionCore:buildNextTraindata")
        trainDataArray = self.__fullClassifier.buildTraindata(mat)
        self.__logger.info("Finished buildNextTraindata()", "DetectionCore:buildNextTraindata")
        return trainDataArray

    def executeTrain(self, inputMatArray, lableArray):
        """
        Trainiert alle FullClassifier und deren Classifier mit den gegebenen Trainingsdaten

        :param Bildmatrizen: inputMatArray Die Bildmatrizen für das Training.
        :param Lable: lableArray Die Lable zu den Bildmatrizen für das Training.
        :return: successful : boolean War das Training erfolgreich?
        """
        self.__logger.info("Starting executeTrain()", "DetectionCore:executeTrain")
        self.__fullClassifier.train(inputMatArray, lableArray)
        self.__logger.info("Finished executeTrain()", "DetectionCore:executeTrain")
        return True
