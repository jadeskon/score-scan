#!/usr/bin/env python

"""
Preprocessor besteht aus mehreren IPreprocessingUnit und ist selbst eine.
Daher ist er das Kompositum des Kompositum-Patterns. Auf einem Eingabebild werden alle konkreten
Preprocessing-Schritte über IPreprocessingUnit -aus welchen er "besteht"- ausführt.
"""

from Preprocessing_Component.IPreprocessingUnit import IPreprocessingUnit
from State_Component.State.State import State

__author__  = "Bonifaz Stuhr"
__version__ = "0.0.0"
__status__ = "Production"


class Preprocessor(IPreprocessingUnit):

    def __init__(self, orderedPreprocessingUnits):
        """
        Constructor, initialisiert Membervariablen

        Parameters
        ----------
        orderedPreprocessingUnits: list
        Eine geordnete Liste von PreprrcessingUnits in Ausführungsreihenfolge.
        """
        self.__logger = State().getLogger("Preprocessing_Component_Logger")
        self.__logger.info("Starting __init__()", "Preprocessor:__init__()")

        self.__orderedPrePorcessingUnits = orderedPreprocessingUnits

        self.__logger.info("Finished __init__()", "Preprocessor:__init__()")

    def preProcess(self, mat):
        """
        Führt die entpsrechene Preprocessing-Schritte auf eine Bildmatrix aus.

        Parameters
        ----------
        imgMatrix : Mat
        Die Matrix auf welcher die Preprocessing-Schritte ausgeführt werden soll

        Returns
        -------
        imgMatrix : Mat
        Die Ergebniss-Matrix auf welcher alle Preprocessing-Schritte ausgeführt wurde.

        Example
        -------
        >>> preprocessor.preProcess(mat)
        """
        self.__logger.info("Starting preProcess()", "Preprocessor:preProcess")

        currentMat = mat

        for unit in self.__orderedPrePorcessingUnits:
            newMat = unit.preProcess(currentMat)
            currentMat = newMat

        self.__logger.info("Finished preProcess()", "Preprocessor:preProcess")
        return currentMat


		