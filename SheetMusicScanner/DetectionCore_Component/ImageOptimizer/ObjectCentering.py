#!/usr/bin/env python

"""
To-Do:
Bitte Kommentar bzw. Dokumentaion erstellen!
"""

from State_Component.State.State import State
import numpy as np
import cv2

__author__  = "Juergen Maier"
__version__ = "0.0.0"
__status__ = "Production"


class ObjectCentering:

    def __init__(self,
                 indexOfProcessMat=0,
                 targetNumberOfRows=110,
                 targetNumberOfColumns=32,
                 useDeletingVerticalSpaces=True,
                 useDeletingHorizontalSpaces=True,
                 findCountersMode=cv2.RETR_LIST,
                 findCountersMethode=cv2.CHAIN_APPROX_NONE,
                 colorOfBorder=0,
                 showImagesInWindow=False):
        """
        To-Do:
        Bitte Kommentar bzw. Dokumentaion erstellen!
        """
        self.__logger = State().getLogger("DetectionCore_Component_Logger")
        self.__logger.info("Starting __init__()", "ObjectCentering:__init__")

        self.__indexOfProcessMat = indexOfProcessMat
        self.__targetNumberOfRows = targetNumberOfRows
        self.__targetNumberOfColumns = targetNumberOfColumns
        self.__useDeletingVerticalSpaces = useDeletingVerticalSpaces
        self.__useDeletingHorizontalSpaces = useDeletingHorizontalSpaces
        self.__findCountersMode = findCountersMode
        self.__findCountersMethode = findCountersMethode
        self.__colorOfBorder = colorOfBorder
        self.__showImagesInWindow = showImagesInWindow

        self.__logger.info("Finsihed __init__()", "ObjectCentering:__init__")

    def coreProcess(self, mats):
        """
        To-Do:
        Bitte Kommentar bzw. Dokumentaion erstellen!
        """
        self.__logger.info("Starting coreProcess()", "ObjectCentering:coreProcess")

        # Variablen zum Zeichnen
        lineThickness = 1
        rectangleColorGreen = (0, 255, 0)
        rectangleColorRed = (0, 0, 255)

        # Erstelle eine Liste mit i leeren Listen.
        # Jede leere Liste i wird fuer einen Matrix-Typen angelegt
        newMats = []
        for i in range(0, len(mats)):
            newMats.append([])

        # Speichern der Liste, die die Objekte ohne Notenlinien enthaelt
        matsOfObjectsWithoutLines = mats[self.__indexOfProcessMat]

        # Iteriere ueber jeden Matrix-Typen
        for i in range(0, len(matsOfObjectsWithoutLines)):

            # Extrahiere die i-te Objekt-Matrix
            matObject = matsOfObjectsWithoutLines[i]

            # Abholung der Breite und Höhe einer Notenzeile
            xRight = matObject.shape[1]
            yBottom = matObject.shape[0]


            # Erstellen einer weißen Spalte
            additionalColumn = np.full((yBottom), 255, dtype=matObject.dtype)

            # Die Methode findContours findet keine Objekte, die sich in der ersten oder/und letzten Zeile
            # oder/und in der ersten oder/und letzten Zeile befinden.
            # Daher werden diese für die findCountours Methode temporäre auf den Wert 255 (weiß) gesetzt.
            matObject[:, 0] = additionalColumn
            matObject[:, xRight - 1] = additionalColumn


            # Finde alle Konturen (Elemente) in der Objekt-Matrix
            _, contours, _ = cv2.findContours(image=matObject,
                                              mode=self.__findCountersMode,
                                              method=self.__findCountersMethode)

            # Erstelle eine Darstellungsbild indem die
            # gefundenen Elemente eingezeichnet werden
            imgShowObject = cv2.cvtColor(matObject, cv2.COLOR_GRAY2RGB)

            # Finde das kleinste Rechteck, welches alle Elemente binhaltet.
            # Hierzu werden die Minimalwerte zu Beginn mit den hoechst moeglichen
            # Werten initialisiert und umbekehrt.
            minX = matObject.shape[1]
            minY = matObject.shape[0]
            maxX = 0
            maxY = 0

            # Entferne das letzte Element.
            # Das letzte Element ist die Kontur, welche das gesamte Feld einschliesst.
            contours.pop()

            # Iteriere ueber alle gefundenen Elemente des Matrix-Objektes
            for j in range(0, len(contours)):

                # Erstelle aus einem Konturelement ein Rechteck
                # und speichere die benoetigten Parameter
                xLeft, yTop, w, h = cv2.boundingRect(points=contours[j])
                xRight = xLeft + w
                yBottom = yTop + h

                # Zeichnen der Rechtecke um die gefundenen Elemente
                cv2.rectangle(img=imgShowObject,
                              pt1=(xLeft, yTop),
                              pt2=(xRight, yBottom),
                              color=rectangleColorRed,
                              thickness=lineThickness)

                # Ueberpruefe, ob das aktuelle Rechteck, das gefundene Element beinhaltet,
                # wenn nicht, dann passe die Koordinaten des alles umschließenden Rechtecks an.
                if xLeft < minX:
                    minX = xLeft

                if yTop < minY:
                    minY = yTop

                if maxX < xRight:
                    maxX = xRight

                if maxY < yBottom:
                    maxY = yBottom

            # Zeichnen des kleinst moeglichen Rechtecks,
            # welches alle gefundenen Elemente beinhaltet.
            cv2.rectangle(img=imgShowObject,
                          pt1=(minX, minY),
                          pt2=(maxX, maxY),
                          color=rectangleColorGreen,
                          thickness=lineThickness)

            # Anzeigen des Bildes in dem die gefundenen
            # Rechtecke eingezeichnet werden.
            if (self.__showImagesInWindow):
                cv2.imshow("ObjectCentering_FoundedContours", imgShowObject)
                cv2.waitKey(0)

            # Initialisiere die Werte der zu herausnehmenden Teilmatrix auf die gesamte Bildgroesse.
            xLeft = 0
            xRight = matObject.shape[1]
            yTop = 0
            yBottom = matObject.shape[0]

            # Falls ueber und unter den gefundenen Elementen die urspruenglichen Bildzeilen
            # zerstoert werden sollen, muessen die y-Koordinaten der zu herausnehmenden Teilmatrix
            # auf die y-Werte des Rahmens gesetzt werden.
            if(self.__useDeletingVerticalSpaces):
                yTop = minY
                yBottom = maxY

            # Falls neben den gefundenen Elementen die urspruenglichen Bildspalten
            # zerstoert werden sollen, muessen die x-Koordinaten der zu herausnehmenden Teilmatrix
            # auf die x-Werte des Rahmens gesetzt werden.
            if (self.__useDeletingHorizontalSpaces):
                xLeft = minX
                xRight = maxX

            # Schneide aus allen Eingangslisten, welche jeweils einen anderen Bildtypen enthaelt
            # die Teilmatrix mit den gefundenen Objekten aus und fuege sie in eine neue groessen-normierte Matrix ein.
            # Itteriere hierzu ueber alle Listen.
            for k in range(0, len(mats)):

                # Erstelle eine neue leere Matrix, in der die neue Matrix eingefuegt werden soll.
                newMatObject = np.full((self.__targetNumberOfRows, self.__targetNumberOfColumns),
                                        fill_value=self.__colorOfBorder,
                                        dtype=matObject.dtype)

                # Schneide aus der urspruenglichen Matrix, die Teilmatrix aus,
                # die alle enthaltenen Objekte enthaelt.
                newCroppedMatObject = mats[k][i][yTop:yBottom, xLeft:xRight]

                # Anzeige der ausgeschnittenen Teilmatrix
                if (self.__showImagesInWindow):
                    cv2.imshow("ObjectCentering_CropedMatrix", newCroppedMatObject)
                    cv2.waitKey(0)

                # Speichern der Zeilen- und Spaltenzahl der Teilmatrix
                # und der Matrix in der diese eingefuegt werden soll.
                shapeCroppedMatObject_rows = newCroppedMatObject.shape[0]
                shapeCroppedMatObject_columns = newCroppedMatObject.shape[1]
                shapeNewMatObject_rows = newMatObject.shape[0]
                shapeNewMatObject_columns = newMatObject.shape[1]

                # Berechnung der Koordinaten in der die Teilmatrix in die neue Matrix eingefuegt werden soll.
                xLeft_insertion = int((shapeNewMatObject_columns / 2) - (shapeCroppedMatObject_columns / 2))
                xRight_insertion = int((shapeNewMatObject_columns / 2) + (shapeCroppedMatObject_columns / 2))
                yTop_insertion = int((shapeNewMatObject_rows / 2) - (shapeCroppedMatObject_rows / 2))
                yBottom_insertion = int((shapeNewMatObject_rows / 2) + (shapeCroppedMatObject_rows / 2))

                # Fuege die Teilmatrix in die Mitte der neuen Matrix hinzu,
                # um fuer alle Matrizen die selbe Groesse zu erhalten.
                newMatObject[yTop_insertion:yBottom_insertion, xLeft_insertion:xRight_insertion] = newCroppedMatObject

                # Fuege die Matrix der k-ten Liste hinzu
                newMats[k].append(newMatObject)

                # Anzeige der Ergebnismatrix mit der normierten Groesse
                if (self.__showImagesInWindow):
                    cv2.imshow("ObjectCentering_ResultMatrix", newMatObject)
                    cv2.waitKey(0)

        # Abspeichern aller Objekte von jedem Matrix-Typ
        for matType in newMats:
            for object in matType:
                self.__logger.info("Centered/Resized following Object: ", "ObjectCentering:coreProcess", object)

        self.__logger.info("Finished coreProcess()", "ObjectCentering:coreProcess")

        return mats