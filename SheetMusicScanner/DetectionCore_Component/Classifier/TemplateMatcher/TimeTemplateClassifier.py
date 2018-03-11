__author__ = "Christian Dufter"
__version__ = "0.0.0"
__status__ = "Production"

from DetectionCore_Component.Classifier.ATemplateMatcher import ATempalteMatcher
from DetectionCore_Component.ClassificationUnit.TimeSignature import TimeSignature
from State_Component.State.State import State
import cv2


class TimeTemplateClassifier(ATempalteMatcher):
    """
    Klasse zur Klassifizierung von Rythmusangaben in einem Takt.
    Erkennt 2/4, 3/4, 4/4, 5/4, 6/4, 3/8, 6/8, 9/8, 12/8.
    """

    def __init__(self, config):
        """
        Konstruktor der BeatTemplateClassifier Klasse.

        Initialisiert alle Membervariablen.

        :param config:          Die Config für diesen TemplateMatcher
        """
        self.__logger = State().getLogger("DetectionCore_Component_Logger")

        self.__templateFolder = config["templateFolder"]
        self.__templateMethod = config["templateMethod"]
        self.__removeIfFound = config["removeIfFound"]

        self.__timeTemplates = []
        self.__timeTemplates.append(self.__loadTemplate(2, 4))
        self.__timeTemplates.append(self.__loadTemplate(3, 4))
        self.__timeTemplates.append(self.__loadTemplate(4, 4))
        self.__timeTemplates.append(self.__loadTemplate(5, 4))
        self.__timeTemplates.append(self.__loadTemplate(6, 4))
        self.__timeTemplates.append(self.__loadTemplate(3, 8))
        self.__timeTemplates.append(self.__loadTemplate(6, 8))
        self.__timeTemplates.append(self.__loadTemplate(9, 8))
        self.__timeTemplates.append(self.__loadTemplate(12, 8))

        self.__timeRatio = 47 / 97
        self.__timeThreshold = 0.57  # max: 0.70 min: 0.44 mid: 0.57

        for template in self.__timeTemplates:
            self.__logger.info("Loaded Time Signature " + str(template[1]) + "/" + str(template[2]) + " Template",
                               "TimeTemplateClassifier::__init__", template[0])

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
        [True] wenn Taktangabe erkannt wurde, [False] falls nicht
        """
        maxMatch = -1
        maxLoc = (0, 0)

        for i in range(0, len(self.__timeTemplates)):
            match, loc = self.__hasTime(matArray, self.__timeTemplates[i][0], self.__timeRatio, self.__timeThreshold)
            if match > classUnit.recognitionPercentage:
                classUnit.recognitionPercentage = match
                classUnit.beats = self.__timeTemplates[i][1]
                classUnit.beatType = self.__timeTemplates[i][2]
                maxMatch = i
                maxLoc = loc

        if maxMatch == -1:
            return False

        self.__logger.info(
            "Time Signature found " + str(classUnit.beats) + "/" + str(classUnit.beatType) + " " +
            str(classUnit.recognitionPercentage),
            "TimeTemplateClassifier::classify",
            matArray[0])

        if self.__removeIfFound:
            self._removeHit(matArray, self.__timeTemplates[maxMatch][0], self.__timeRatio, maxLoc)

        return True

    def __hasTime(self, mats, template, templateMatRatio, threshold):
        """
        Führt den eigentlichen Templatematch aus.

        :param mats:                Takt als Bildmatrix ([0] ohne Linien, [1] mit Linien, [2] nur skaliert).
        :param template:            Template, welches zum Templatematching verwendet wird.
        :param templateMatRatio:    Höhenverhältnis von Template zum Bildausschnitt.
        :param threshold:           Grenzwert, welcher erreicht werden muss, damit das Template als gefunden gilt.
        :return:                    Maximal erreichten Matchwert.

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

            # Hole den maximalen Wert und die zugehörige Position
            __, maxVal, __, maxLoc = cv2.minMaxLoc(match)

            # Wenn Threshold erreicht wurde
            if maxVal >= threshold:
                return maxVal, maxLoc

        return 0, (0, 0)

    def __loadTemplate(self, beat, beatType):
        return [cv2.imread(self.__templateFolder + "beat_" + str(beat) + "_" + str(beatType) + ".jpg", 0),
                beat,
                beatType]
