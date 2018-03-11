#!/usr/bin/env python

"""
To-Do:
Bitte Kommentar bzw. Dokumentaion erstellen!
"""

from Preprocessing_Component.IPreprocessingUnit import IPreprocessingUnit
from State_Component.State.State import State
import cv2

__author__  = "Juergen Maier / Bonifaz Stuhr"
__version__ = "0.0.0"
__status__ = "Production"


class ScaleNoteSheetPreprocessor(IPreprocessingUnit):

    def __init__(self,
                 averageHeight,
                 targetLineHeight=100,
                 interpolation=cv2.INTER_CUBIC,
                 showImagesInWindow=False):
        """
        To-Do:
        Bitte Kommentar bzw. Dokumentaion erstellen!
        """
        self.__logger = State().getLogger("Preprocessing_Component_Logger")
        self.__logger.info("Starting __init__()", "ScaleNoteSheetPreprocessor:__init__")

        self.__averageHeight = averageHeight
        self.__targetLineHeight = targetLineHeight
        self.__interpolation = interpolation
        self.__showImagesInWindow = showImagesInWindow

        self.__logger.info("Finished __init__()", "ScaleNoteSheetPreprocessor:__init__")

    def preProcess(self, mat):
        """
        To-Do:
        Bitte Kommentar bzw. Dokumentaion erstellen!

        Example
        -------
        >>> ScaleNoteSheetPreprocessor.preProcess(mat)

        """
        self.__logger.info("Starting preProcess()", "ScaleNoteSheetPreprocessor:preProcess")

        # Berechnung der neuen Bildgroesse
        currentImageHeight = mat.shape[0]
        currentImageWidth = mat.shape[1]
        newImageHeight = int(currentImageHeight / (-self.__averageHeight) * self.__targetLineHeight)
        newImageWidth = int(currentImageWidth / (-self.__averageHeight) * self.__targetLineHeight)

        # Fuehrt eine Skalierung auf die angegeben Groesse aus
        resizeMat = cv2.resize(mat,
                               (newImageWidth, newImageHeight),
                               interpolation=self.__interpolation)

        # Binarisieren des Bildes, da durch die Skalierung und das damit
        # stattfindende Interpolieren zwischen Schwarz und Weiß verschiedene Graustufen entstehen
        _, resultMat = cv2.threshold(resizeMat, 127, 255, cv2.THRESH_BINARY)

        # Anzeigen des Ergebnisses Note
        if (self.__showImagesInWindow):
            cv2.imshow("ScaleNoteSheetPreprocessor", resultMat)
            cv2.waitKey(0)

        self.__logger.info("Finished preProcess() with following Image: ", "ScaleNoteSheetPreprocessor:preProcess", resultMat)

        return resultMat