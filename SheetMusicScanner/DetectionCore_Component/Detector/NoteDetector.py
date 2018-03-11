#!/usr/bin/env python

"""
To-Do:
Bitte Kommentar bzw. Dokumentaion erstellen!
"""

from DetectionCore_Component.IDetector import IDetector
from State_Component.State.State import State
from operator import itemgetter
import numpy as np
import cv2

__author__  = "Bonifaz Stuhr / Juergen Maier"
__version__ = "0.0.0"
__status__ = "Production"


class NoteDetector(IDetector):

    def __init__(self,
                 indexOfProcessMat=0,
                 minNoteWidth_WithStem=15,
                 maxNoteWidth_WithStem=8,
                 minNoteHeight_WithStem=30,
                 maxNoteHeight_WithStem=80,
                 minNoteWidth_WithoutStem=8,
                 maxNoteWidth_WithoutStem=30,
                 minNoteHeight_WithoutStem=8,
                 maxNoteHeight_WithoutStem=23,
                 noteImageWidth=20,
                 findCountersMode=cv2.RETR_LIST,
                 findCountersMethode=cv2.CHAIN_APPROX_NONE,
                 showImagesInWindow=False):
        """
        To-Do:
        Bitte Kommentar bzw. Dokumentaion erstellen!
        """
        self.__logger = State().getLogger("DetectionCore_Component_Logger")
        self.__logger.info("Starting __init__()", "NoteDetector:__init__")

        self.__indexOfProcessMat = indexOfProcessMat
        self.__minNoteWidth_WithStem = minNoteWidth_WithStem
        self.__maxNoteWidth_WithStem = maxNoteWidth_WithStem
        self.__minNoteHeight_WithStem = minNoteHeight_WithStem
        self.__maxNoteHeight_WithStem = maxNoteHeight_WithStem
        self.__minNoteWidth_WithoutStem = minNoteWidth_WithoutStem
        self.__maxNoteWidth_WithoutStem = maxNoteWidth_WithoutStem
        self.__minNoteHeight_WithoutStem = minNoteHeight_WithoutStem
        self.__maxNoteHeight_WithoutStem = maxNoteHeight_WithoutStem
        self.__noteImageWidth = noteImageWidth
        self.__findCountersMode = findCountersMode
        self.__findCountersMethode = findCountersMethode
        self.__showImagesInWindow = showImagesInWindow

        self.__logger.info("Finsihed __init__()", "NoteDetector:__init__")

    def detect(self, mats):
        """
        To-Do:
        Bitte Kommentar bzw. Dokumentaion erstellen!
        """
        self.__logger.info("Starting detect()", "NoteDetector:detect")

        # Variablen zum Zeichnen
        lineThickness = 1
        rectangleColorGreen = (0, 255, 0)
        rectangleColorRed = (0, 0, 255)

        # Merke die Anzahl von Noten pro Takt
        noteCountPerTact = []

        # Erstelle eine Liste mit i leeren Listen.
        # Jede leere Liste i wird fuer einen Matrix-Typen angelegt
        noteMats = []
        for i in range(0, len(mats)):
            noteMats.append([])

        # Speichern der Liste, die die Takte ohne Notenlinien enthaelt
        matsOfTactsWithoutLines = mats[self.__indexOfProcessMat]



        # Itteriere ueber jeden Takt ohne Notenlinien
        for j in range(0, len(matsOfTactsWithoutLines)):

            # Setz die Notecount für diesen Takt initial auf 0
            noteCountPerTact.append(0)

            # Extrahiere den j-ten Takt
            tactWithoutLines = matsOfTactsWithoutLines[j]

            # Anlegen einer Koordinatenliste, die die x-Koordianten
            # der Noten enthaelt.
            xCoordinates = []

            if (self.__showImagesInWindow):
                cv2.imshow("NoteDetector_Tact", tactWithoutLines)
                cv2.waitKey(0)

            # Abholung der Breite und Höhe einer Notenzeile
            xRight = tactWithoutLines.shape[1]
            yBottom = tactWithoutLines.shape[0]

            # Erstellen einer weißen Zeile
            additionalRow = np.full((1, xRight), 255, dtype=tactWithoutLines.dtype)

            # Die Methode findContours findet keine Objekte, die sich in der ersten oder/und letzten Zeile
            # oder/und in der ersten oder/und letzten Zeile befinden.
            # Daher werden diese für die findCountours Methode temporäre auf den Wert 255 (weiß) gesetzt.
            tactWithoutLines[0, :] = additionalRow
            tactWithoutLines[yBottom - 1, :] = additionalRow

            # Erodiere horizontal um Loecher in unausgefuellte Noten zu zerstoeren
            tactWithoutLines_erode_dilate = cv2.erode(tactWithoutLines, np.ones((1, 9)))
            if (self.__showImagesInWindow):
                cv2.imshow("NoteDetector_Tact", tactWithoutLines_erode_dilate)
                cv2.waitKey(0)

            # Dilatiere auf die urspruengliche Groesse zurueck
            tactWithoutLines_erode_dilate = cv2.dilate(tactWithoutLines_erode_dilate, np.ones((1, 9)))
            if (self.__showImagesInWindow):
                cv2.imshow("NoteDetector_Tact", tactWithoutLines_erode_dilate)
                cv2.waitKey(0)

            # Dilatiere vertical um Verbindungen zwischen verbundene Noten zu zerstoeren
            tactWithoutLines_erode_dilate = cv2.dilate(tactWithoutLines_erode_dilate, np.ones((9, 1)))
            if (self.__showImagesInWindow):
                cv2.imshow("NoteDetector_Tact", tactWithoutLines_erode_dilate)
                cv2.waitKey(0)

            # Erodiere auf die urstpruengliche Groesse zurueck
            tactWithoutLines_erode_dilate = cv2.erode(tactWithoutLines_erode_dilate, np.ones((9, 1)))
            if (self.__showImagesInWindow):
                cv2.imshow("NoteDetector_Tact", tactWithoutLines_erode_dilate)
                cv2.waitKey(0)

            # An dieser Stelle trennen sich manchmal der Notenkopf und der Notenhals voneinander.
            # Mit diesem Erode werden sie wieder zusammengefügt.
            tactWithoutLines_erode_dilate = cv2.erode(tactWithoutLines_erode_dilate, np.ones((1, 4)))
            if (self.__showImagesInWindow):
                cv2.imshow("NoteDetector_Tact", tactWithoutLines_erode_dilate)
                cv2.waitKey(0)


            # Finde alle Konturen im Takt
            _, contours, _ = cv2.findContours(image=tactWithoutLines_erode_dilate,
                                              mode=self.__findCountersMode,
                                              method=self.__findCountersMethode)

            # Erstelle eine Darstellungsbild indem die
            # gefundenen Elemente eingezeichnet werden
            imgShowTact = cv2.cvtColor(tactWithoutLines, cv2.COLOR_GRAY2RGB)

            # Iteriere ueber allen gefundenen Elemente eines Taktes
            for i in range(0, len(contours)):

                # Erstelle aus einem Konturelement ein Rechteck
                # und speichere die benoetigten parameter
                x, y, w, h = cv2.boundingRect(contours[i])

                # Der Rahmen der gefundenen Elemente muss eine Mindesthoehe
                # und eine Minimal- und Mintestbreite besitzen
                if (((self.__minNoteWidth_WithStem < w and w < self.__maxNoteWidth_WithStem)
                    and (self.__minNoteHeight_WithStem < h and h < self.__maxNoteHeight_WithStem))
                    or ((self.__minNoteWidth_WithoutStem < w and w < self.__maxNoteWidth_WithoutStem)
                    and (self.__minNoteHeight_WithoutStem < h and h < self.__maxNoteHeight_WithoutStem)) ):

                    # Zeichnen der Rechtecke um die gefundenen Noten
                    cv2.rectangle(img=imgShowTact,
                                  pt1=(x, y),
                                  pt2=(x + w, y + h),
                                  color=rectangleColorGreen,
                                  thickness=lineThickness)

                    # Fuege die Rahmen-Koordinaten der gefundenen Noten der Liste hinzu
                    xCoordinates.append([x, x + w])

                    #Erhöhe die Notenanzahl dieses Taktes um eins
                    noteCountPerTact[j] += 1
                else:
                    # Zeichnen der Rechtecke um die restlichen gefundenen Elemente
                    cv2.rectangle(img=imgShowTact,
                                  pt1=(x, y),
                                  pt2=(x + w, y + h),
                                  color=rectangleColorRed,
                                  thickness=lineThickness)

            # Anzeigen der Notenzeilen indem die gefunden Taktstriche
            # gruen und alle anderen Elemente rot umrahmt sind.
            if (self.__showImagesInWindow):
                cv2.imshow("NoteDetector_NoteRow", imgShowTact)
                cv2.waitKey(0)


            # self.__logger.info("Detect following rectangle: ", "NoteDetector:detect", tactWithoutLines)

            # Sortieren der gefundenen Elemente von links nach rechts
            xCoordinates.sort(key=itemgetter(0))

            # Ueberpruefe alle gefundenen Noten auf ihre Mindestbreite
            for i in range(0, len(xCoordinates)):

                # Extrahieren der rechten Koordinate einer gefunden Note
                x0 = xCoordinates[i][0]
                # Extrahieren der linken Koordinate einer gefunden Note
                x1 = xCoordinates[i][1]

                # Berechnung des Zentrums der Note bzgl. x-Koordinate
                center = int((x0 + x1 ) * 0.5)

                # Berechnung der neuen x-Koordinaten, um die Sollgroesse zu erhalten
                x0 = center - int(self.__noteImageWidth * 0.5)
                x1 = center + int(self.__noteImageWidth * 0.5) + ((self.__noteImageWidth) % 2)

                # Gehe jeden eingegangene Matrix-Typen des j-ten Taktes durch
                for k in range(0, len(mats)):

                    # Extrahiere den j-ten Takt aus der Liste des k-ten Matrix-Typen
                    tact = mats[k][j]

                    # Ueberpruefe ob die linke x-Koordinate
                    # außerhalb des linken Randes ragt
                    if(x0 < 0):

                        # Berechnen der Anzahl der zusaetzlich benoetigten Spalten
                        numberOfAdditionalColumns = abs(x0)

                        # Erstellen einer Kopie der ersten Spalte
                        firstColumn = tact[:,0]

                        # Erstellen der Spalten die am Anfang hinzugefuegt werden sollen,
                        # indem die erste Spalte des Taktes mehrfach kopiert wird.
                        additionalColumns = np.repeat(firstColumn[:,np.newaxis],
                                                      repeats=numberOfAdditionalColumns,
                                                      axis=1)

                        # Setze die zusaetzlichen Spalten vor den Takt
                        tact = np.append(additionalColumns, tact, axis=1)

                        # Erweitere die x-Koordinaten um die Anzahl
                        # der zusaetzlich hinzugefuegten Spalten
                        x0 += numberOfAdditionalColumns
                        x1 += numberOfAdditionalColumns

                    # Extrahiere die Anzahl der Spalten des aktuellen Taktes
                    numberOfColumnsOfTact = tact.shape[1]

                    # Ueberpruefe ob die rechte x-Koordinate
                    # außerhalb des rechten Randes ragt
                    if(numberOfColumnsOfTact < x1):

                        # Berechnen der Anzahl der zusaetzlich benoetigten Spalten
                        numberOfAdditionalColumns = abs(x1 - numberOfColumnsOfTact)

                        # Erstellen einer Kopie der letzten Spalte
                        lastColumn = tact[:, numberOfColumnsOfTact-1]

                        # Erstellen der Spalten die am Ende zusaetzlich hinzugefuegt werden sollen,
                        # indem die letzte Spalte des Taktes mehrfach kopiert wird.
                        additionalColumns = np.repeat(lastColumn[:,np.newaxis],
                                                      repeats=numberOfAdditionalColumns,
                                                      axis=1)

                        # Setze die zusaetzlichen Spalten hinter den Takt
                        tact = np.append(tact, additionalColumns, axis=1)

                    # Extrahieren einer Note mit den x-Koordinaten x0 und x1
                    # aus dem j-ten Takt des k-ten Matrix-Typen
                    note = tact[:,x0:x1]

                    # Fuege die Note der k-ten Liste des k-ten Matrix-Typen an
                    noteMats[k].append(note)

                    # Anzeigen der hinzugefuegten Note
                    if (self.__showImagesInWindow):
                        cv2.imshow("NoteDetector_Note", note)
                        cv2.waitKey(0)

        # Abspeichern aller Noten von jedem Matrix-Typ
        for matType in noteMats:
            for note in matType:
                self.__logger.info("Detect following Note: ", "NoteDetector:detect", note)

        self.__logger.info("Finished detect()", "NoteDetector:detect")

        return noteMats, noteCountPerTact