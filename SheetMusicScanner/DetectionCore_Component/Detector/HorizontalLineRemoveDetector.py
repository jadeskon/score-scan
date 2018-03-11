#!/usr/bin/env python

"""
To-Do:
Bitte Kommentar bzw. Dokumentaion erstellen!
"""

from DetectionCore_Component.IDetector import IDetector
from State_Component.State.State import State
import cv2

__author__  = "Bonifaz Stuhr / Juergen Maier"
__version__ = "0.0.0"
__status__ = "Production"


class HorizontalLineRemoveDetector(IDetector):

    def __init__(self,
                 indexOfProcessMat=0,
                 anchorPoint=(-1,-1),
                 kernelWidth=1,
                 kernelHeight=3,
                 morphOfKernel=cv2.MORPH_RECT,
                 showImagesInWindow=True):
        """
        To-Do:
        Bitte Kommentar bzw. Dokumentaion erstellen!
        """
        self.__logger = State().getLogger("DetectionCore_Component_Logger")
        self.__logger.info("Starting __init__()", "HorizontalLineRemoveDetector:__init__")
        self.__indexOfProcessMat = indexOfProcessMat
        self.__anchorPoint = anchorPoint
        self.__kernelWidth = kernelWidth
        self.__kernelHeight = kernelHeight
        self.__morphOfKernel = morphOfKernel
        self.__logger.info("Starting __init__()", "HorizontalLineRemoveDetector:__init__")
        self.__showImagesInWindow = showImagesInWindow

    def detect(self, mats):
        """
        To-Do:
        Bitte Kommentar bzw. Dokumentaion erstellen!
        """
        self.__logger.info("Starting detect()", "HorizontalLineRemoveDetector:detect")

        # Auswahl der Matrix, die vom Detektor bearbeitet werden soll
        mat = mats[self.__indexOfProcessMat]

        # Erstelle eine Kopie der zu bearbeitenden Matrix
        vertical = mat.copy()
        if (self.__showImagesInWindow):
            cv2.imshow("Input_HorizontalLineRemoveDetector", vertical)
            cv2.waitKey(0)

        # Es wird ein verticaler Kernel erstellt,
        # d. h. viele Zeilen und wenig Spalten
        verticalStructure = cv2.getStructuringElement(self.__morphOfKernel,
                                                      (self.__kernelWidth, self.__kernelHeight))

        # Beim Erodieren wird fuer jede Kernelposition der kleinste Wert zurueckgegeben
        # Auf diese Weise werden Features wie horizontale Linien zerstoert, da eine langer
        # vertikaler Kernel verwendet wird und invertiertes Bild erwartet wird.
        # Es werden also flache Objekte verworfen.
        vertical = cv2.erode(vertical, verticalStructure, self.__anchorPoint)
        self.__logger.info("Vertical_erode:", "HorizontalLineRemoveDetector:detect", vertical)
        if (self.__showImagesInWindow):
            cv2.imshow("Input_HorizontalLineRemoveDetector", vertical)
            cv2.waitKey(0)

        # Beim Delatieren wird fuer jede Kernelposition der groesste Wert zurueckgegeben
        # Auf diese Weise werden die beim Erodieren flach gedrueckte Objekte wieder ausgedeht,
        # da der selbe Kernel verwendet und das selbe invertierte Bild erwartet wird.
        # Es werden also flache Objekte nach unten und oben ausgedeht.
        vertical = cv2.dilate(vertical, verticalStructure, self.__anchorPoint)
        if (self.__showImagesInWindow):
            cv2.imshow("Input_HorizontalLineRemoveDetector", vertical)
            cv2.waitKey(0)
        self.__logger.info("Vertical_dialte:", "HorizontalLineRemoveDetector:detect", vertical)

        # Da der Linienentferner ein invertiertes Bild erwartet,
        # muss dieses nach der Verarbeitung wieder zurueck invertiert werden
        vertical = cv2.bitwise_not(vertical)

        # Ueberschreibe die Urspruengliche Input Matrix
        # mit der Ergebnis Matrix
        mats[self.__indexOfProcessMat] = vertical

        self.__logger.info("Finished detect() with following image:", "HorizontalLineRemoveDetector:detect", vertical)

        return mats