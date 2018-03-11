"""
Detector-Klasse zum detektieren von Notenschlüsseln.
"""

from DetectionCore_Component.IDetector import IDetector
from State_Component.State.State import State
from operator import itemgetter
import cv2

__author__  = "Christian Dufter"
__version__ = "0.0.0"
__status__ = "Production"

class ClefDetector(IDetector):
    def __init__(self,
                 delimitWidthMax = 30,
                 delimitWidthMin = 20,
                 delimitHeightMin = 20,
                 templateThreshold = 0.55,
                 templateMethod = cv2.TM_CCOEFF_NORMED,
                 findCountersMode = cv2.RETR_LIST,
                 findCountersMethode = cv2.CHAIN_APPROX_NONE
                 ):
        """
        Konstruktor für den ClefDetector.

        :param delimitWidthMax:     Maximale Breite eines Notenschlüssels.
        :param delimitWidthMin:     Minimale Breite eines Notenschlüssels.
        :param delimitHeightMin:    Minimale Höhe eines Notenschlüssels.
        :param templateThreshold:   Der Wert den das Template-Matching mindestens erreichen muss, damit ein Bildauschnitt als der jeweilige Notenschlüssel erkannt wird
        :param templateMethod:      Methode des Template-Matchers
        :param findCountersMode:    Modus des Konturfindungs-Algorithmus
        :param findCountersMethode: Methode des Konturfindungs-Algorithmus
        """

        self.__logger = State().getLogger("DetectionCore_Component_Logger")
        self.__logger.info("Starting __init__()", "ClefDetector:__init__")

        self.__delimitWidthMax = delimitWidthMax
        self.__delimitWidthMin = delimitWidthMin
        self.__delimitHeightMin = delimitHeightMin
        self.__templateThreshold = templateThreshold
        self.__templateMethod = templateMethod
        self.__findCountersMode = findCountersMode
        self.__findCountersMethode = findCountersMethode

        self.__logger.info("Finished __init__()", "ClefDetector:__init__")

    def detect(self, matArray):
        """
        Detection Funktion. Geerbt von IDetector.

        :param matArray:        Liste von Bilder, welche die Takte enthalten
        :return:                Liste alles gefundenen Notenschlüssel mit und ohne Notenlinien
        """
        self.__logger.info("Starting detect()", "ClefDetector:detect")

        # Initialierung der Taktlisten:
        # 1. List ohne und die 2. Liste mit Notenlinien
        clefMatsNoLines= []
        clefMatsLines = []

        # Variablen zum Zeichnen
        lineThickness = 1
        rectangleColor = (0, 255, 0)

        for j in range(0, len(matArray[0])):
            mat = matArray[0][j].copy() # Takt ohne Linien
            matLine = matArray[1][j].copy()

            xCoordinates = []
            xCoordinates.append([0 , 0])

            self.__logger.debug("Starting detect Clefs for image", "ClefDetector:detect", mat)

            # Finde alle Konturen im Takt
            _, contours, _ = cv2.findContours(image=mat,
                                              mode=self.__findCountersMode,
                                              method=self.__findCountersMethode)

            found = False
            for i in range(0, len(contours)):
                # Erstelle aus einem Konturelement ein Rechteck
                # und speichere die benoetigten parameter
                x, y, w, h = cv2.boundingRect(contours[i])

                if (self.__delimitWidthMin <= w and w < self.__delimitWidthMax and h >= self.__delimitHeightMin):
                    found = True

                    # Falls es sich um einen Violinschlüssel handelt, im Bild markieren und koordinaten merken
                    if self.__isViolin(mat[:, x:x + w]):
                        xCoordinates.append([x, x + w])

                        cv2.rectangle(img=mat,
                              pt1=(x, y),
                              pt2=(x + w, y + h),
                              color=rectangleColor,
                              thickness=lineThickness)

                    # TODO an dieser Stelle die gefundenen prüfen ob vll ein Bassschlüssel

            if found:
                self.__logger.info("Detect following rectangle: ", "ClefDetector:detect", mat)

            # Sortieren der gefundenen Elemente von links nach rechts
            xCoordinates.sort(key=itemgetter(0))

            # Ueberpruefe alle gefundenen Noten auf ihre Mindestbreite
            for i in range(1, len(xCoordinates)):
                x0 = xCoordinates[i][0]
                x1 = xCoordinates[i][1]
                clefMatsNoLines.append(mat[:, x0:x1])
                clefMatsLines.append(matArray[1][j][:, x0:x1])

        for i in range(0, len(clefMatsNoLines)):
            self.__logger.info("Detected following clef: ", "ClefDetector:detect", clefMatsNoLines[i])

        self.__logger.info("Finished detect()", "ClefDetector:detect")

        return clefMatsNoLines, clefMatsLines

    def __isViolin(self, image):
        """
        Funktion, welche feststellt ob es sich bei einem gegebenen Bildauschnitt um einen Violinschlüssel handelt oder nicht.

        :param image: Bildauschnitt, welcher untersucht wird.
        :return: [True] wenn ein Violinschlüssel, [False] falls nicht.
        """

        # Lade Template als Graustufenbild
        #template = cv2.cvtColor(cv2.imread("DetectionCore_Component/Detector/templates/clef_violin.jpg"), cv2.COLOR_BGR2GRAY)
        template = cv2.imread("DetectionCore_Component/Detector/templates/clef_violin.jpg", 0)

        # Wenn Bild kleiner als Template ist, brich ab mit False
        if image.shape[0] >= template.shape[0] and image.shape[1] >= template.shape[1]:
            match = cv2.matchTemplate(image, template, self.__templateMethod)
        else:
            self.__logger.warning("Template to small", "ClefDetector:__isViolin")
            return False

        # Wenn einer der Werte im Match größer als der vordefinierte Threshold ist, handelt es sich um einen Violinschlüssel
        if(match >= self.__templateThreshold).any():
           return True
        else:
           return False
		   
		   