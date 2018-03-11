"""
Detector-Klasse zum detektieren von Notenschlüsseln.
"""

from DetectionCore_Component.IDetector import IDetector
from State_Component.State.State import State
import cv2
import numpy as np

__author__  = "Christian Dufter"
__version__ = "0.0.0"
__status__ = "Production"

class KeyDetector(IDetector):
    def __init__(self,
                 templateThreshold=0.75,
                 templateMethod=cv2.TM_CCOEFF_NORMED,
                 findCountersMode=cv2.RETR_LIST,
                 findCountersMethode=cv2.CHAIN_APPROX_NONE
                 ):
        """
        Konstruktor für den KeyDetector.

        :param templateThreshold:   Der Wert den das Template-Matching mindestens erreichen muss, damit ein Bildauschnitt als der jeweilige Key erkannt wird
        :param templateMethod:      Methode des Template-Matchers
        :param findCountersMode:    Modus des Konturfindungs-Algorithmus
        :param findCountersMethode: Methode des Konturfindungs-Algorithmus
        """

        self.__logger = State().getLogger("DetectionCore_Component_Logger")
        self.__logger.info("Starting __init__()", "KeyDetector:__init__")

        self.__templateThreshold = templateThreshold
        self.__templateMethod = templateMethod
        self.__findCountersMode = findCountersMode
        self.__findCountersMethode = findCountersMethode

        self.__logger.info("Finished __init__()", "KeyDetector:__init__")

    def detect(self, matArray):
        """
        Detection Funktion. Geerbt von IDetector.

        :param matArray:        Liste von Bilder, welche die Takte enthalten
        :return:                Liste alles gefundenen Keys mit und ohne Notenlinien
        """
        self.__logger.info("Starting detect()", "KeyDetector:detect")

        # Initialierung der Taktlisten:
        # 1. List ohne und die 2. Liste mit Notenlinien
        clefMatsNoLines= []
        clefMatsLines = []

        # Variablen zum Zeichnen
        lineThickness = 1
        rectangleColor = (0, 255, 0)

        for j in range(0, len(matArray[0])):
            mat = matArray[0][j].copy() # Takt ohne Linien
            matLine = matArray[1][j].copy() # Takt mit Linien

            self.__logger.debug("Starting detect Keys for image", "KeyDetector:detect", mat)

            found = False
            template = cv2.imread("DetectionCore_Component/Detector/templates/key_b.jpg", 0)
            w, h = template.shape[::-1]

            res = cv2.matchTemplate(mat, template, cv2.TM_CCOEFF_NORMED)
            loc = np.where(res >= self.__templateThreshold)

            for pt in zip(*loc[::-1]):
                found = True
                cv2.rectangle(mat, pt, (pt[0] + w, pt[1] + h), rectangleColor, lineThickness)
                cv2.rectangle(matLine, pt, (pt[0] + w, pt[1] + h), rectangleColor, lineThickness)
                clefMatsNoLines.append(mat[:, pt[0]: pt[0] + w])
                clefMatsLines.append(matLine[:, pt[0]: pt[0] + w])

            if found:
                self.__logger.info("Detect following rectangle: ", "KeyDetector:detect", mat)

        for i in range(0, len(clefMatsNoLines)):
            self.__logger.info("Detected following clef: ", "KeyDetector:detect", clefMatsNoLines[i])

        self.__logger.info("Finished detect()", "KeyDetector:detect")

        return clefMatsNoLines, clefMatsLines

		
		