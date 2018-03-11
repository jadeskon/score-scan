#!/usr/bin/env python

"""
Der BitwiseNotPreprocessor ist ein Blatt des Kompositum-Patterns im Preprozessor.
Diese Klasse ist für die Bitwise Inversierung in dem Eingabebild verantwortlich.
Sie wendet zur Inversierung ein bit-weises not an filter an.
"""

from Preprocessing_Component.IPreprocessingUnit import IPreprocessingUnit
from State_Component.State.State import State
import cv2

__author__  = "Juergen Maier"
__version__ = "0.0.0"
__status__ = "Production"


class BitwiseNotPreprocessor(IPreprocessingUnit):

    def __init__(self,
                 showImagesInWindow=False):
        """
        To-Do:
        Bitte Kommentar bzw. Dokumentaion erstellen!
        """
        self.__logger = State().getLogger("Preprocessing_Component_Logger")
        self.__logger.info("Starting __init__()", "BitwiseNotPreprocessor:__init__")

        self.__showImagesInWindow = showImagesInWindow

        self.__logger.info("Finished __init__()", "BitwiseNotPreprocessor:__init__")

    def preProcess(self, mat):
        """
        Führt eine Inversierung (bit-weises not) auf eine Bildmatrix aus.

        Parameters
        ----------
        mat : Mat
        Die Matrix auf welche die Operation ausgeführt werden soll.

        Returns
        -------
        bitwiseNot : Mat
        Die Ergebniss-Matrix auf die die Operation ausgeführt wurde.

        Example
        -------
        >>> bitwiseNotPreprocessor.preProcess()
        """
        self.__logger.info("Starting preProcess()", "BitwiseNotPreprocessor:preProcess")

        bitwiseNot = cv2.bitwise_not(mat)

        # Anzeigen des Ergebnisses Note
        if (self.__showImagesInWindow):
            cv2.imshow("BitwiseNotPreprocessor", bitwiseNot)
            cv2.waitKey(0)

        self.__logger.info("Finished preProcess() with following Image: ", "GaussianBlurNoiseFilterPreprocessor:preProcess", bitwiseNot)
        return bitwiseNot
		
		
