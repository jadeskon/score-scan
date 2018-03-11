#!/usr/bin/env python

"""
Der NoteSheetScaleConstCalculator ist ein berechnet an Hand des Eingabebildes eine Konstante, der
später für die Skalierung verwendet werden kann.
"""

from State_Component.State.State import State
from operator import itemgetter
import cv2
import numpy as np

__author__  = "Juergen Maier / Bonifaz Stuhr"
__version__ = "0.0.0"
__status__ = "Production"


class NoteSheetScaleConstCalculator:

    def __init__(self,
                 maxGradeOfLinesInPx=2,
                 marginTop=0.5,
                 marginBottom=0.5,
                 cannyThreshold1=50,
                 cannyThreshold2=150,
                 cannyApertureSize=3,
                 houghLinesRho=1,
                 houghLinesTheta=np.pi / 180,
                 houghLinesThreshold=200,
                 minDistanceToNextNoteRow=30,
                 minHeightOfNoteRow=20,
                 showImagesInWindow=True):
        """
        To-Do:
        Bitte Kommentar bzw. Dokumentaion erstellen!
        """
        self.__logger = State().getLogger("Preprocessing_Component_Logger")
        self.__logger.info("Starting __init__()", "NoteSheetScaleConstCalculator:__init__")
        self.__averageHeight = 0
        self.__maxGradeOfLinesInPx = maxGradeOfLinesInPx
        self.__marginTop = marginTop
        self.__marginBottom = marginBottom
        self.__cannyThreshold1 = cannyThreshold1
        self.__cannyThreshold2 = cannyThreshold2
        self.__cannyApertureSize = cannyApertureSize
        self.__houghLinesRho = houghLinesRho
        self.__houghLinesTheta = houghLinesTheta
        self.__houghLinesThreshold = houghLinesThreshold
        self.__minDistanceToNextNoteRow = minDistanceToNextNoteRow
        self.__minHeightOfNoteRow = minHeightOfNoteRow
        self.__showImagesInWindow = showImagesInWindow
        self.__logger.info("Finished __init__()", "NoteSheetScaleConstCalculator:__init__")

    def preProcess(self, mat):

        """
        To-Do:
        Bitte Kommentar bzw. Dokumentaion erstellen!

        Example
        -------
        >>> NoteSheetScaleConstCalculator.preProcess(mat)

        """
        self.__logger.info("Starting preProcess()", "NoteSheetScaleConstCalculator:preProcess")

        # Anwendung des Canny Filters um als Kantendetektor,
        # um über den HoughLines Detektor Kanten zu detektieren
        edges = cv2.Canny(mat,
                          threshold1=self.__cannyThreshold1,
                          threshold2=self.__cannyThreshold2,
                          apertureSize=self.__cannyApertureSize)

        self.__logger.info("Detected following Canny-Edges", "NoteSheetScaleConstCalculator:detect", edges)

        # Verwendung des HoughLines Detektors um Notenlinien zu detektieren
        lines = cv2.HoughLines(edges,
                               rho=self.__houghLinesRho,
                               theta=self.__houghLinesTheta,
                               threshold=self.__houghLinesThreshold)

        # Gehe alle Linien durch, um aus rho und theta
        # die Linienkoordinaten zu berechnen
        lines_coordinates = []
        for x in range(0, len(lines)):
            for rho, theta in lines[x]:

                # Berechnung der Linienkoordinaten
                # Die X Koordinaten gehen über die komplette Seite,
                # daher 0 und mat.shape[1]
                a = np.cos(theta)
                b = np.sin(theta)
                x0 = a * rho
                y0 = b * rho
                x1 = int(x0 + 0 * (-b))
                y1 = int(y0 + 1000 * (a))
                x2 = int(x0 - mat.shape[1] * (-b))
                y2 = int(y0 - 1000 * (a))

                # Speichere die Koordinaten in eine Liste, wenn
                # eine definierte Steigung nicht überschritten wird
                if (abs(y1 - y2) <= self.__maxGradeOfLinesInPx):
                    lines_coordinates.append([x1, y1, x2, y2])

        # Sortieren die Linien von oben nach unten
        lines_coordinates.sort(key=itemgetter(1))

        # Erstelle eine Matrix, welche als Ausgabe verwendete wird
        # auf welcher die Linien farbig gezeichnet werden koennen
        showMat = cv2.cvtColor(src=mat,
                               code=cv2.COLOR_GRAY2BGR)

        # Die noteLineHeights ist ein Array, welches spaeter
        # die Hoehen der Notenzeilen enthaelt.
        # Eine Liniengruppe definiert Linien die zur selben Zeile gehoeren
        noteLineHeights = []
        line_groupe = []
        lineThickness = 2
        lineColor = (0, 255, 0)
        rectangleColor = (255, 255, 0)

        # Gehe allen Notenlinien durch
        for i in range(0, len(lines_coordinates) - 1):

            # Erhalte die Koordinaten einer Linie und Speichere sie in einer Liniengruppe
            line_coordinates = lines_coordinates[i]
            line_groupe.append(line_coordinates)

            # Zeichne die Linie auf die Debug-Matrix
            cv2.line(showMat, (line_coordinates[0], line_coordinates[1]),
                     (line_coordinates[2], line_coordinates[3]), lineColor, lineThickness)

            # Falls der Abstand zwischen zwei Notenzinien gering genug ist,
            # dann ist die Linie ein Teil einer Liniengruppe und somit Teil einer Notenzeile
            if (not(abs(line_coordinates[1] - lines_coordinates[i + 1][1]) < self.__minDistanceToNextNoteRow)): # 30

                # Berechne einen Rahmen zu der aktuellen Notenzeile
                marginTop = int(abs(line_groupe[0][1] - line_groupe[len(line_groupe) - 1][1]) * self.__marginTop)
                marginBorder = int(abs(line_groupe[0][1] - line_groupe[len(line_groupe) - 1][1]) * self.__marginBottom)

                coordinateTop = line_groupe[0][1] - marginTop
                coordinateBottom = line_groupe[len(line_groupe) - 1][1] + marginBorder

                # Zeichne einen Rahmen um die aktuelle Notenzeile
                cv2.rectangle(img=showMat,
                              pt1=(0, coordinateTop),
                              pt2=(mat.shape[1], coordinateBottom),
                              color=rectangleColor,
                              thickness=lineThickness)

                # Speichern der Hoehe der aktuellen Notenzeile
                if (abs(coordinateTop - coordinateBottom) > self.__minHeightOfNoteRow):
                    noteLineHeight = coordinateTop - coordinateBottom
                    noteLineHeights.append([noteLineHeight])

                # Loesche den Inhalt, um Platz fuer eine neue Liniengruppe zu sorgen
                line_groupe.clear()

        else:
            # Erhalte die Koordinaten einer Linie und Speichere sie in einer Liniengruppe
            line_coordinates = lines_coordinates[len(lines_coordinates) - 1]
            line_groupe.append(line_coordinates)

            # Zeichne die Linie auf die Debug-Matrix
            cv2.line(showMat, (line_coordinates[0], line_coordinates[1]), (line_coordinates[2], line_coordinates[3]), lineColor, lineThickness)

            # Berechne einen Rahmen zu der aktuellen Notenzeile
            marginTop = int(abs(line_groupe[0][1] - line_groupe[len(line_groupe) - 1][1]) * self.__marginTop)
            marginBorder = int(abs(line_groupe[0][1] - line_groupe[len(line_groupe) - 1][1]) * self.__marginBottom)

            coordinateTop = line_groupe[0][1] - marginTop
            coordinateBottom = line_groupe[len(line_groupe) - 1][1] + marginBorder

            # Zeichne einen Rahmen um die aktuelle Notenzeile
            cv2.rectangle(img=showMat,
                          pt1=(0, coordinateTop),
                          pt2=(mat.shape[1], coordinateBottom),
                          color=rectangleColor,
                          thickness=lineThickness)
            self.__logger.info("Detected following Line:", "NoteSheetScaleConstCalculator:detect", showMat)

            # Speichern der Hoehe der aktuellen Notenzeile
            if (abs(coordinateTop - coordinateBottom) > self.__minHeightOfNoteRow):
                noteLineHeight = coordinateTop - coordinateBottom
                noteLineHeights.append([noteLineHeight])

            # Loesche den Inhalt, um Platz fuer eine neue Liniengruppe zu sorgen
            line_groupe.clear()

        # Anzeigen des Notenblattes indem die gefunden Notenzeilen
        # und Notenlinien farblich markiert sind.
        if(self.__showImagesInWindow):
            cv2.imshow("NoteSheetScalConstCalculator_MusicSheet", showMat)
            cv2.waitKey(0)

        self.__averageHeight = np.mean(noteLineHeights)

        self.__logger.info("Finished preProcess() with following Image: ", "NoteSheetScaleConstCalculator:preProcess", showMat)

        return self.__averageHeight