#!/usr/bin/env python

"""
IMatParser bietet das Interface für einen MatParser, der zum Einlesen eines bestimmten Datei dient und diese in eine
Bildmatrix für die Klassifizierung umwandelt.
"""
from Input_Component.IMatParser import IMatParser
from wand.image import Image
import wand

import cv2

__author__  = "Dominik Rauch"
__version__ = "0.1.0"
__status__ = "Ready"


class PdfToMatParser(IMatParser):

    def __init__(self, pathToPDF):
        self.__pathToPDF = pathToPDF


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
        img = wand.image.Image(filename=self.__pathToPDF + "[0]", resolution=225)
        img.format = "png"
        # img.resize(500,500)
        img.save(filename="convertedpdf.png")
        mat = cv2.imread("convertedpdf.png", 0)

        return mat

		
		