#!/usr/bin/env python

"""
To-Do:
Bitte Kommentar bzw. Dokumentaion erstellen!
"""

from DetectionCore_Component.IDetector import IDetector
from operator import itemgetter
from State_Component.State.State import State
import cv2

__author__  = "Bonifaz Stuhr / Juergen Maier"
__version__ = "0.0.0"
__status__ = "Production"


class TactDetector(IDetector):
    def __init__(self,
                 indexOfProcessMat=0,
                 tactLineWidthMax=8,
                 tactLineHeightMin=40,
                 minWidthOfTactLine=10,
                 findCountersMode=cv2.RETR_LIST,
                 findCountersMethode=cv2.CHAIN_APPROX_NONE,
                 showImagesInWindow=False):
        """
        To-Do:
        Bitte Kommentar bzw. Dokumentaion erstellen!
        """
        self.__logger = State().getLogger("DetectionCore_Component_Logger")
        self.__logger.info("Starting __init__()", "TactDetector:__init__")

        self.__indexOfProcessMat = indexOfProcessMat
        self.__tactLineWidthMax = tactLineWidthMax
        self.__tactLineHeightMin = tactLineHeightMin
        self.__minWidthOfTactLine = minWidthOfTactLine
        self.__findCountersMode = findCountersMode
        self.__findCountersMethode = findCountersMethode
        self.__showImagesInWindow = showImagesInWindow

        self.__logger.info("Finished __init__()", "TactDetector:__init__")

    def detect(self, mats):
        """
        To-Do:
        Bitte Kommentar bzw. Dokumentaion erstellen!
        """
        self.__logger.info("Starting detect()", "TactDetector:detect")

        # Variablen zum Zeichnen
        lineThickness = 1
        rectangleColorGreen = (0, 255, 0)
        rectangleColorRed = (0, 0, 255)

        # Erstelle eine Liste mit i leeren Listen.
        # Jede leere Liste i wird fuer einen Matrix-Typen angelegt
        tactMats = []
        for i in range(0, len(mats)):
            tactMats.append([])

        # Extrahier die Liste der Notenzeilen,
        # deren Notenlinien entfernt wurde
        matsOfNoteRowsWithoutLines = mats[self.__indexOfProcessMat]

        # Iteriere ueber alle Notenzeilen
        for j in range(0, len(matsOfNoteRowsWithoutLines)):

            # Extrahiere die j-te Notenzeile
            matNoteRow = matsOfNoteRowsWithoutLines[j]

            # Anlegen einer Koordinatenliste, die die x-Koordianten
            # der Taktstriche enthaelt.
            xCoordinates = []

            # Fuege die erste Pixelspalte des Bildes der Notenzeile
            # zu den Koordinaten hinzu, um den Anfang als ersten Takt erkennen zu koennen,
            # da der Zeilenanfang of keinen Taktstrich enthaelt
            xCoordinates.append([0, 0])

            # Verbreitern der Elemente in der Notenzeile
            anchorPoint = (-1, -1)
            kernelWidth = 3
            kernelHeight = 1
            morphOfKernel = cv2.MORPH_RECT
            verticalStructure = cv2.getStructuringElement(morphOfKernel, (kernelWidth, kernelHeight))
            matNoteRow_eroded = cv2.erode(matNoteRow, verticalStructure, anchorPoint)

            # Anzeigen des Notenblattes indem die gefunden Notenzeilen
            # und Notenlinien farblich markiert sind.
            if (self.__showImagesInWindow):
                cv2.imshow("TactDetector_NoteRow", matNoteRow_eroded)
                cv2.waitKey(0)

            # Finde alle Konturen in der Notenzeile
            _, contours, _ = cv2.findContours(image=matNoteRow_eroded,
                                              mode=self.__findCountersMode,
                                              method=self.__findCountersMethode)

            # Erstelle eine Darstellungsbild indem die
            # gefundenen Elemente eingezeichnet werden
            imgShowNoteRow = cv2.cvtColor(matNoteRow, cv2.COLOR_GRAY2RGB)

            # Iteriere ueber alle gefundenen Elemente der Notenzeile
            for i in range(0, len(contours)):

                # Erstelle aus einem Konturelement ein Rechteck
                # und speichere die benoetigten parameter
                x, y, w, h = cv2.boundingRect(points=contours[i])

                # Der Rahmen der gefundenen Elemente muss eine Maximalbreite
                # und eine Mindesthoehe besitzen um als Takt klassifiziert zu werden
                if(w < self.__tactLineWidthMax) and (self.__tactLineHeightMin < h):

                    # Zeichnen der Rechtecke um die gefundenen Taktstriche
                    cv2.rectangle(img=imgShowNoteRow,
                                  pt1=(x, y),
                                  pt2=(x + w, y + h),
                                  color=rectangleColorGreen,
                                  thickness=lineThickness)

                    # Fuege die Rahmen-Koordinaten der gefundenen Taktstriche zu der Liste hinzu
                    xCoordinates.append([x, x + w])

                else:
                    # Zeichnen der Rechtecke um die restlichen gefundenen Elemente
                    cv2.rectangle(img=imgShowNoteRow,
                                  pt1=(x, y),
                                  pt2=(x + w, y + h),
                                  color=rectangleColorRed,
                                  thickness=lineThickness)

            # Fuege die letzte Pixelspalte des Bildes der Notenzeile
            # zu den Koordinaten hinzu, um das Ende als letzten Takt erkennen zu koennen,
            # da das Zeilenende of keinen Taktstrich enthaelt
            xCoordinates.append([matNoteRow.shape[1], matNoteRow.shape[1]])

            # Anzeigen der Notenzeilen indem die gefunden Taktstriche
            # gruen und alle anderen Elemente rot umrahmt sind.
            if (self.__showImagesInWindow):
                cv2.imshow("TactDetector_NoteRow", imgShowNoteRow)
                cv2.waitKey(0)

            # Sortieren der gefundenen Elemente von links nach rechts
            xCoordinates.sort(key=itemgetter(0))

            # Ueberpruefe alle gefundenen Takte auf ihre Mindestbreite mit Hilfe der Koordinaten
            # Iteriere hierzu ueber die Koordinaten
            for i in range(0, len(xCoordinates) - 1):

                # Extrahieren der rechten Koordinate eines gefunden Taktstriches
                x0 = xCoordinates[i][1]

                # Extrahieren der linken Koordinate des darauffolgenden Taktstriches
                x1 = xCoordinates[i+1][0]

                # Der Inhalt zwischen den Koordinatn x0 und x1 ist ein Tak
                newMatWithoutLines = matNoteRow[:, x0:x1]

                # Finde alle Konturen in der Notenzeile
                _, contours, _ = cv2.findContours(image=newMatWithoutLines,
                                                  mode=self.__findCountersMode,
                                                  method=self.__findCountersMethode)

                # Speichern der Anzahl der Elemente
                numberOfElementsInTact = len(contours)

                # Falls der gefundene Takt breit genug ist und mindestens zwei Elemente besitzt,
                # dann ist es ein Takt. Der gesamte Takt an sich ist auch ein Element,
                # daher muss der Takt mindestens zwei Elemente besitzen.
                if (self.__minWidthOfTactLine < x1 - x0) and (2 <= numberOfElementsInTact):

                    for k in range(0, len(mats)):
                        # Gehe jeden eingegangene Matrix-Typen der j-ten Zeile durch
                        # Extrahieren eines Taktes mit den x-Koordinaten x0 und x1
                        # aus j-ten Notenzeile des k-ten Matrix-Typen
                        tact = mats[k][j][:, x0:x1]

                        # Fuege den Takt der k-ten Liste des k-ten Matrix-Typen an
                        tactMats[k].append(tact)

                        # Anzeigen des hinzugefuegten Taktes
                        if (self.__showImagesInWindow):
                            cv2.imshow("TactDetector_Tact", tact)
                            cv2.waitKey(0)

        # Abspeichern aller Takte von jedem Matrix-Typ
        for matType in tactMats:
            for tact in matType:
                self.__logger.info("Detecting Tact:", "TactDetector:detect", tact)

        self.__logger.info("Finished detect()", "TactDetector:detect")

        return tactMats