#!/usr/bin/env python

"""
IMatParser bietet das Interface für einen MatParser, der zum Einlesen eines bestimmten Datei dient und diese in eine
Bildmatrix für die Klassifizierung umwandelt.
"""
from Input_Component.IMatParser import IMatParser

import cv2

__author__  = "Dominik Rauch"
__version__ = "0.1.0"
__status__ = "Ready"


class PngToMatParser(IMatParser):

    def __init__(self, pathToPNG):
        self.__pathToPNG = pathToPNG


    def parseToMat(self):
        """
        Führt den entsprechenden Einlesevorgang durch und erstellt die Bildmatrix.

        Parameters
        ----------

        Returns
        -------
        imgMatrix : Mat
        Die eingelesene Matrix.
        """

        mat = cv2.imread(self.__pathToPNG, 0)

        return mat

		
		