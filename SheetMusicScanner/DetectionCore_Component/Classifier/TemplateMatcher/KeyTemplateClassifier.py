__author__ = "Christian Dufter"
__version__ = "0.0.0"
__status__ = "Production"

from DetectionCore_Component.Classifier.ATemplateMatcher import ATempalteMatcher
from DetectionCore_Component.ClassificationUnit.KeySignatur import KeySignatur
from State_Component.State.State import State
import cv2
import numpy as np



class KeyTemplateClassifier(ATempalteMatcher):
    """
    Klasse zur Klassifizierung von Tonhöhen in einem Takt.
    Erkennt b un #.
    """

    def __init__(self, config):
        """
        Konstruktor der KeyTemplateClassifier Klasse.

        Initialisiert alle Membervariablen.

        :param config:          Die Config für diesen TemplateMatcher
        """
        self.__logger = State().getLogger("DetectionCore_Component_Logger")

        self.__templateFolder = config["templateFolder"]
        self.__templateMethod = config["templateMethod"]

        self.__bTemplate = self.__loadTemplate(-1)
        self.__bRatio = 29 / 97
        self.__bThreshold = 0.61  # Max: 0.65  Min: 0.57  Mid: 0.61

        self.__CrossTemplate = self.__loadTemplate(1)
        self.__CrossRatio = 36 / 97
        self.__CrossThreshold = 0.635  # Max: 0.68  Min: 0.59  Mid: 0.635

        self.__logger.info("Loaded Key " + str(self.__bTemplate[1]) + " Template",
                           "KeyTemplateClassifier::__init__", self.__bTemplate[0])

        self.__logger.info("Loaded Key " + str(self.__CrossTemplate[1]) + " Template",
                           "KeyTemplateClassifier::__init__", self.__CrossTemplate[0])

    def classify(self, clasUnit, matArray):
        """
        Interface Methode: Jeder TempalteMatcher muss diese realisieren.
        Führt die Klassifizierung auf ein Array von Bildmatrizen anhand TemplateMatching aus und gibt die
        erkannten Objekte zurück.

        Parameters
        ----------
        classUnit : Die Klassifikation als Out-Parameter
        matArray : Die Bildmatrizen auf welche die Klassifizierung ausgeführt werden soll.

        Returns
        -------
        [True] wenn Notenschlüssel erkannt wurde, [False] falls nicht
        """

        # b Vorzeichen
        match, count = self.__hasKey(matArray, self.__bTemplate[0], self.__bRatio, self.__bThreshold)

        if match > clasUnit.recognitionPercentage:
            clasUnit.recognitionPercentage = match
            clasUnit.fifths = self.__bTemplate[1] * count

        # Kreuz Vorzeichen
        match, count = self.__hasKey(matArray, self.__CrossTemplate[0], self.__CrossRatio, self.__CrossThreshold)

        if match > clasUnit.recognitionPercentage:
            clasUnit.recognitionPercentage = match
            clasUnit.fifths = self.__CrossTemplate[1] * count

        if clasUnit.recognitionPercentage == 0:
            return False

        self.__logger.info(
            "Key found " + str(clasUnit.fifths) + " " + str(clasUnit.recognitionPercentage),
            "KeyTemplateClassifier::classify",
            matArray[0])

        return True

    def __hasKey(self, mats, template, templateMatRatio, threshold):
        """
        Führt den eigentlichen Templatematch aus.

        :param mats:                Takt als Bildmatrix ([0] ohne Linien, [1] mit Linien, [2] nur skaliert).
        :param template:            Template, welches zum Templatematching verwendet wird.
        :param templateMatRatio:    Höhenverhältnis von Template zum Bildausschnitt.
        :param threshold:           Grenzwert, welcher erreicht werden muss, damit das Template als gefunden gilt.
        :return:                    [True] wenn Threshold erreicht, [False] wenn nicht.
        """
        # Template auf Bildgröße skalieren
        resizedTemplate = ATempalteMatcher._resizeTemplate(self, mats[0], template, templateMatRatio)

        if (mats[0].shape[1] >= resizedTemplate.shape[1]):
            # Templatematching mit Bild OHNE Linen
            matchNoLine = cv2.matchTemplate(mats[0], resizedTemplate, self.__templateMethod)

            # Templatematching mit Bild MIT Linen
            matchLine = cv2.matchTemplate(mats[1], resizedTemplate, self.__templateMethod)

            # Templatematching mit nur skaliertem Bild
            matchSkal = cv2.matchTemplate(mats[2], resizedTemplate, self.__templateMethod)

            # Verwende das Maximum von beiden Matches
            match = cv2.max(matchLine, matchNoLine, matchSkal)

            # Erzeuge ein binarisiertes Bild anhand eines Thresholds
            __, bin = cv2.threshold(match, threshold, 255, cv2.THRESH_BINARY)

            # Zähle die Konturen im Binarisierten Bild
            im2, contours, hierarchy = cv2.findContours(np.uint8(bin), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

            # Wenn Threshold mindestens einmal erreicht wurde
            if (bin > 0).any():
                return match.max(), len(contours)

        return 0, 0

    def __loadTemplate(self, fiths):
        return [cv2.imread(self.__templateFolder + "key_" + str(fiths) + ".jpg", 0), fiths]
