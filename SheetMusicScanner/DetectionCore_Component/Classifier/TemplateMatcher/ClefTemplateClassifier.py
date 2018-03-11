__author__ = "Christian Dufter"
__version__ = "0.0.0"
__status__ = "Production"

from DetectionCore_Component.Classifier.ATemplateMatcher import ATempalteMatcher
from DetectionCore_Component.ClassificationUnit.Clef import Clef
from State_Component.State.State import State
import cv2


class ClefTemplateClassifier(ATempalteMatcher):
    """
    Klasse zur Klassifizierung von Notenschlüsseln in einem Takt.
    Erkennt Violin-, Bass- und Altschlüssel.

    Höhe der Schlüssel wird nicht erkannt!!!!!
    """

    def __init__(self, config):
        """
        Konstruktor der ClefTemplateClassifier Klasse.

        Initialisiert alle Membervariablen.

        :param config:          Die Config für diesen TemplateMatcher
        """
        self.__logger = State().getLogger("DetectionCore_Component_Logger")

        self.__templateFolder = config["templateFolder"]
        self.__templateMethod = config["templateMethod"]
        self.__removeIfFound = config["removeIfFound"]

        self.__clefTemplates = []
        self.__clefRatios = []
        self.__clefThresholds = []

        # Violin
        self.__clefTemplates.append(self.__loadTemplate("G", 2))
        self.__clefRatios.append(83 / 97)
        self.__clefThresholds.append(0.52)  # max: 0.77  min: 0.27  mid: 0.52

        # Bass
        self.__clefTemplates.append(self.__loadTemplate("F", 4))
        self.__clefRatios.append(36 / 97)
        self.__clefThresholds.append(0.64)  # max: 0.76  min: 0.52  mid: 0.64

        # Alt
        self.__clefTemplates.append(self.__loadTemplate("C", 3))
        self.__clefRatios.append(50 / 97)
        self.__clefThresholds.append(0.535)  # max: 0.58  min: 0.49  mid: 0.535

        for template in self.__clefTemplates:
            self.__logger.info("Loaded Clef " + template[1] + str(template[2]) + " Template",
                               "ClefTemplateClassifier::__init__", template[0])

    def classify(self, classUnit, matArray):
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
        maxMatch = -1
        maxLoc = (0, 0)

        for i in range(0, len(self.__clefTemplates)):
            match, loc = self.__hasClef(matArray, self.__clefTemplates[i][0], self.__clefRatios[i],
                                        self.__clefThresholds[i])
            if match > classUnit.recognitionPercentage:
                classUnit.recognitionPercentage = match
                classUnit.sign = self.__clefTemplates[i][1]
                classUnit.line = self.__clefTemplates[i][2]
                maxMatch = i
                maxLoc = loc

        if maxMatch == -1:
            return False

        self.__logger.info(
            "Clef found " + classUnit.sign + str(classUnit.line) + " " + str(classUnit.recognitionPercentage),
            "ClefTemplateClassifier::classify",
            matArray[0])

        if self.__removeIfFound:
            self._removeHit(matArray, self.__clefTemplates[maxMatch][0], self.__clefRatios[maxMatch], maxLoc)

        return True

    def __hasClef(self, mats, template, templateMatRatio, threshold):
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

            # Verwende das Maximum von allen Matches
            match = cv2.max(matchLine, matchNoLine, matchSkal)

            # Hole den maximalen Wert und die zugehörige Position
            __, maxVal, __, maxLoc = cv2.minMaxLoc(match)

            # Wenn Threshold erreicht wurde
            if maxVal >= threshold:
                return maxVal, maxLoc

        return 0, (0, 0)

    def __loadTemplate(self, sign, line):
        return [cv2.imread(self.__templateFolder + "clef_" + sign + "_" + str(line) + ".jpg", 0), sign, line]
