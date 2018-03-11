#!/usr/bin/env python

"""
Der GaussianBlurNoiseFilterPreprocessor ist ein Blatt des Kompositum-Patterns im Preprozessor.
Diese Klasse ist für die Rauschfilterung in dem Eingabebild verantwortlich.
Sie wendet zur Rauschfilterung den gausian blur filter an.
"""

from Preprocessing_Component.IPreprocessingUnit import IPreprocessingUnit
from State_Component.State.State import State
import cv2

__author__  = "Juergen Maier"
__version__ = "0.0.0"
__status__ = "Production"


class GaussianBlurNoiseFilterPreprocessor(IPreprocessingUnit):

    def __init__(self,
                 ksize,
                 sigmaX,
                 sigmaY=0,
                 borderType=cv2.BORDER_DEFAULT,
                 showImagesInWindow=False):
        """
        To-Do:
        Bitte Kommentar bzw. Dokumentaion erstellen!
        """
        self.__logger = State().getLogger("Preprocessing_Component_Logger")
        self.__logger.info("Starting __init__()", "GaussianBlurNoiseFilterPreprocessor:__init__")

        self.__ksize = ksize
        self.__sigmaX = sigmaX
        self.__sigmaY = sigmaY
        self.__borderType = borderType
        self.__showImagesInWindow = showImagesInWindow

        self.__logger.info("Finished __init__()", "GaussianBlurNoiseFilterPreprocessor:__init__")

    def preProcess(self, mat):
        """
        Führt den Rauschfilter gaussian blur auf eine Bildmatrix aus.

        Parameters
        ----------
        mat : Mat
        Die Matrix auf welche der Rauschfilter gaussian blur ausgeführt werden soll.

        Returns
        -------
        gaussianBlurMat : Mat
        Die Ergebniss-Matrix auf die der Rauschfilter gaussian blur ausgeführt wurde.

        Example
        -------
        >>> gaussianBlurNoiseFilterPreprocessor.preProcess()

        """
        self.__logger.info("Starting preProcess()", "GaussianBlurNoiseFilterPreprocessor:preProcess")
        gaussianBlurMat = cv2.GaussianBlur(src=mat,
                                           ksize=self.__ksize,
                                           sigmaX=self.__sigmaX,
                                           sigmaY=self.__sigmaY,
                                           borderType=self.__borderType)

        # Anzeigen des Ergebnisses Note
        if (self.__showImagesInWindow):
            cv2.imshow("GaussianBlurNoiseFilterPreprocessor", gaussianBlurMat)
            cv2.waitKey(0)

        self.__logger.info("Finished preProcess() with following Image: ", "GaussianBlurNoiseFilterPreprocessor:preProcess", gaussianBlurMat)
        return gaussianBlurMat
		
		
