#!/usr/bin/env python

"""
Der Input ist eine Realisierung des Interfaces IPreprocessing und dient zur Steuerung eines bestimmten Ablaufs des
Preprocessing einer Bildmatrix , welche diese für die Klassifizierung vorbereitet.
"""

from Preprocessing_Component.IPreprocessing import IPreprocessing
from Preprocessing_Component.PreprocessingUnit.Preprocessor import Preprocessor
from Preprocessing_Component.PreprocessingUnit.AdaptiveThresholdBinarizationPreProcessor import AdaptiveThresholdBinarizationPreprocessor
from Preprocessing_Component.PreprocessingUnit.GaussianBlurNoiseFilterPreprocessor import GaussianBlurNoiseFilterPreprocessor
from Preprocessing_Component.PreprocessingUnit.BitwiseNotPreprocessor import BitwiseNotPreprocessor
from Preprocessing_Component.PreprocessingUnit.ScaleNoteSheetPreprocessor import ScaleNoteSheetPreprocessor
from Preprocessing_Component.Preprocessing.NoteSheetScaleConstCalculator import NoteSheetScaleConstCalculator
from State_Component.State.State import State

import cv2
import numpy as np

__author__  = "Bonifaz Stuhr / Juergen Maier"
__version__ = "0.0.0"
__status__ = "Production"


class Preprocessing(IPreprocessing):

    def __init__(self, config):
        """
        Constructor, initialisiert Membervariablen

        Parameters
        ----------
        config : Config
        Die Konfiguration.

        Example
        -------
        >>> Preprocessing(config)
        """
        self.__logger = State().getLogger("Preprocessing_Component_Logger")
        self.__logger.info("Starting __init__()", "Preprocessing:__init__()")
        self.__config = config

        # Erstelle eine Liste von Preprozessoreinheiten,
        # die eine Matrix bearbeiten
        ordererPreporcessingUnitList = []

        noiseFilterConfig = self.__config["GaussianBlurNoiseFilterPreprocessor"]
        self.__gaussianBlurNoiseFilterPreprocessor = GaussianBlurNoiseFilterPreprocessor \
                                (ksize=(noiseFilterConfig["ksizeWidth"], noiseFilterConfig["ksizeHeight"]),
                                 sigmaX=noiseFilterConfig["sigmaX"],
                                 showImagesInWindow=noiseFilterConfig["showImagesInWindow"])
        ordererPreporcessingUnitList.append(self.__gaussianBlurNoiseFilterPreprocessor)

        binarizationConfig1 = self.__config["AdaptiveThresholdBinarizationPreprocessor_FirstPreprocessor"]
        self.__adaptiveThresholdBinarizationPreProcessor1 = AdaptiveThresholdBinarizationPreprocessor \
                                (maxValue=binarizationConfig1["maxValue"],
                                 adaptiveMethode=getattr(cv2, binarizationConfig1["adaptiveMethode"]),
                                 thresholdType=getattr(cv2, binarizationConfig1["thresholdType"]),
                                 blockSize=binarizationConfig1["blockSize"],
                                 C=binarizationConfig1["C"],
                                 showImagesInWindow=binarizationConfig1["showImagesInWindow"])
        ordererPreporcessingUnitList.append(self.__adaptiveThresholdBinarizationPreProcessor1)

        # Erstelle einen Preprozessor, der die unterschiedelichen Preprozessoreinheiten
        # der ersten Liste nacheineander auf eine Matrix ausfuehrt
        self.__preProcessor1 = Preprocessor(ordererPreporcessingUnitList)

        # Erstelle eine weitere Liste mit anderen Preprozessoreinheiten,
        # die eine Matrix bearbeiten
        ordererPreporcessingUnitList2 = []

        bitwiseNotConfig = self.__config["BitwiseNotPreprocessor"]
        self.__bitwiseNotPreprocessor = BitwiseNotPreprocessor \
                                (showImagesInWindow=bitwiseNotConfig["showImagesInWindow"])
        ordererPreporcessingUnitList2.append(self.__bitwiseNotPreprocessor)

        binarizationConfig2 = self.__config["AdaptiveThresholdBinarizationPreprocessor_SecondPreprocessor"]
        self.__adaptiveThresholdBinarizationPreProcessor2 = AdaptiveThresholdBinarizationPreprocessor \
                                (maxValue=binarizationConfig2["maxValue"],
                                 adaptiveMethode=getattr(cv2, binarizationConfig2["adaptiveMethode"]),
                                 thresholdType=getattr(cv2, binarizationConfig2["thresholdType"]),
                                 blockSize=binarizationConfig2["blockSize"],
                                 C=binarizationConfig2["C"],
                                 showImagesInWindow=binarizationConfig2["showImagesInWindow"])
        ordererPreporcessingUnitList2.append(self.__adaptiveThresholdBinarizationPreProcessor2)

        # Erstelle einen Preprozessor, der die unterschiedelichen Preprozessoreinheiten
        # der zweiten Liste nacheineander auf eine Matrix ausfuehrt
        self.__preProcessor2 = Preprocessor(ordererPreporcessingUnitList2)

        self.__logger.info("Finished __init__()", "Preprocessing:__init__()")

    def execute(self, mat):
        """
        Führt Preprocessingschritte auf die BildMatrix aus und gibt die bearbeitet Matrix zurück.

        Parameters
        ----------
        mat : Die Bildmatrix auf welche Preprocessingschritte angewendet werden sollen.

        Returns
        -------
        imgMatrix : mat
        Die "preprocesste" Matrix.

        Example
        -------
        >>> preprocessing.execute()
        """
        self.__logger.info("Starting execute", "Preprocessing:execute")

        # Ausfuehren der Preprozessoren
        preprocessedMat1 = self.__preProcessor1.preProcess(mat)
        preprocessedMat2 = self.__preProcessor2.preProcess(mat)

        # Erstelle einen Calculator, der einen Skalierungsfaktor
        # fuer die Notenblattskalierung berechnet
        scaleCalculatorConfig = self.__config["NoteSheetScaleConstCalculator"]
        self.__noteSheetScaleConstCalculator = NoteSheetScaleConstCalculator \
                                (maxGradeOfLinesInPx=scaleCalculatorConfig["maxGradeOfLinesInPx"],
                                 marginTop=scaleCalculatorConfig["marginTop"],
                                 marginBottom=scaleCalculatorConfig["marginBottom"],
                                 cannyThreshold1=scaleCalculatorConfig["cannyThreshold1"],
                                 cannyThreshold2=scaleCalculatorConfig["cannyThreshold2"],
                                 cannyApertureSize=scaleCalculatorConfig["cannyApertureSize"],
                                 houghLinesRho=scaleCalculatorConfig["houghLinesRho"],
                                 houghLinesTheta=np.pi / 180 * scaleCalculatorConfig["houghLinesThetaInDegree"],
                                 houghLinesThreshold=scaleCalculatorConfig["houghLinesThreshold"],
                                 minDistanceToNextNoteRow=scaleCalculatorConfig["minDistanceToNextNoteRow"],
                                 minHeightOfNoteRow=scaleCalculatorConfig["minHeightOfNoteRow"],
                                 showImagesInWindow=scaleCalculatorConfig["showImagesInWindow"])

        # Ausfuehren der Konstantenberechnung auf eine Matrix (Notenblatt)
        averageHeight = self.__noteSheetScaleConstCalculator.preProcess(preprocessedMat1)

        # Initialisierung eines Preprozessors mit der aktuellen Durchschnitthoehe der Zeilen und der Zielhoehe
        sheetScalerConfig = self.__config["ScaleNoteSheetPreprocessor"]
        self.__scaleNoteSheetPreprocessor = ScaleNoteSheetPreprocessor \
                                (averageHeight=averageHeight,
                                 targetLineHeight=sheetScalerConfig["targetLineHeight"],
                                 interpolation=getattr(cv2, sheetScalerConfig["interpolation"]))

        # Skalieren der im Preprozessor bearbeiteten Matrizen
        preprocessedMat1 = self.__scaleNoteSheetPreprocessor.preProcess(preprocessedMat1)
        preprocessedMat2 = self.__scaleNoteSheetPreprocessor.preProcess(preprocessedMat2)
        preprocessedMat3 = self.__scaleNoteSheetPreprocessor.preProcess(mat)

        self.__logger.info("Finished execute", "Preprocessing:execute")

        return [preprocessedMat1, preprocessedMat2, preprocessedMat3]

		
		