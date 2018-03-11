#!/usr/bin/env python

"""
Der AdaptiveThresholdBinarizationPreprocessor ist ein Blatt des Kompositum-Patterns im Preprozessor.
Diese Klasse ist für die Umwandlung des Eingabebildes in ein Binärbild verantwortlich.
Sie wendet zur Umwandlung die adaptive threshold binarization an.
"""

from Preprocessing_Component.IPreprocessingUnit import IPreprocessingUnit
from State_Component.State.State import State
import cv2

__author__  = "Juergen Maier"
__version__ = "0.0.0"
__status__ = "Production"


class AdaptiveThresholdBinarizationPreprocessor(IPreprocessingUnit):

    def __init__(self,
                 maxValue,
                 adaptiveMethode,
                 thresholdType,
                 blockSize,
                 C,
                 showImagesInWindow=False):
        """
        To-Do:
        Bitte Kommentar bzw. Dokumentaion erstellen!
        """
        self.__logger = State().getLogger("Preprocessing_Component_Logger")
        self.__logger.info("Starting __init__()", "AdaptiveThresholdBinarizationPreprocessor:__init__")

        self.__maxValue = maxValue
        self.__adaptiveMethode = adaptiveMethode
        self.__thresholdType = thresholdType
        self.__blockSize = blockSize
        self.__C = C
        self.__showImagesInWindow = showImagesInWindow


        self.__logger.info("Finished __init__()", "AdaptiveThresholdBinarizationPreprocessor:__init__")

    def preProcess(self, mat):
        """
        Führt die adaptive threshold binarization auf eine Bildmatrix aus.

        Parameters
        ----------
        mat : Mat
        Die Matrix auf welcher die adaptive threshold binarization ausgeführt werden soll

        Returns
        -------
        adaptiveThresholdMat : Mat
        Die Ergebniss-Matrix auf die die adaptive threshold binarization ausgeführt wurde.

        Example
        -------
        >>> adaptiveThresholdBinarizationPreProcessor.preProcess()
        """
        self.__logger.info("Starting preProcess()", "AdaptiveThresholdBinarizationPreprocessor:preProcess")

        adaptiveThresholdMat = cv2.adaptiveThreshold(src=mat,
                                                     maxValue=self.__maxValue,
                                                     adaptiveMethod=self.__adaptiveMethode,
                                                     thresholdType=self.__thresholdType,
                                                     blockSize=self.__blockSize,
                                                     C=self.__C)

        # Anzeigen des Ergebnisses Note
        if (self.__showImagesInWindow):
            cv2.imshow("AdaptiveThresholdBinarizationPreprocessor_Note", adaptiveThresholdMat)
            cv2.waitKey(0)

        self.__logger.info("Finished preProcess() with following Image: ", "AdaptiveThresholdBinarizationPreprocessor:preProcess",
                    adaptiveThresholdMat)
        return adaptiveThresholdMat

		
		