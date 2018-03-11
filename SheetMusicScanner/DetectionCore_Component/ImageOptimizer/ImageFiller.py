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


class ImageFiller:

    def __init__(self,
                 fillRows=True,
                 fillColumns=True,
                 targetNumberOfRows=110,
                 targetNumberOfColumns=32,
                 appendRowsTop=False,
                 appendColumnsRight=True,
                 showImagesInWindow=False):
        """
        To-Do:
        Bitte Kommentar bzw. Dokumentaion erstellen!
        """
        self.__logger = State().getLogger("DetectionCore_Component_Logger")
        self.__logger.info("Starting __init__()", "ImageFiller:__init__")

        self.__fillRows = fillRows
        self.__fillColumns = fillColumns
        self.__targetNumberOfRows = targetNumberOfRows
        self.__targetNumberOfColumns = targetNumberOfColumns
        self.__appendRowsTop = appendRowsTop
        self.__appendColumnsRight = appendColumnsRight
        self.__showImagesInWindow = showImagesInWindow

        self.__logger.info("Finsihed __init__()", "ImageFiller:__init__")

    def coreProcess(self, mats):
        """
        To-Do:
        Bitte Kommentar bzw. Dokumentaion erstellen!
        """
        self.__logger.info("Starting coreProcess()", "ImageFiller:coreProcess")

        # Erstelle eine Liste mit i leeren Listen.
        # Jede leere Liste i wird fuer einen Matrix-Typen angelegt
        newMats = []
        for i in range(0, len(mats)):
            newMats.append([])

        # Iteriere ueber jeden Matrix-Typen
        for i in range(0, len(mats)):

            # Iteriere ueber jedes Objekt der Matrix-Typen-Liste
            for matObject in mats[i]:

                # Speichere die Matrix als neues Objekt ab
                newMatObject = matObject.copy()

                # Zwischenspeichern der Zeilen und Spaltenanzahl
                rows, columns = newMatObject.shape

                # Wenn die Anzahl der Zeilen angepasst werden sollen ...
                if(self.__fillRows):

                    # dann ueberpruefe, ob die urspruengliche Matrix
                    # zu wenig Zeilen besitzt.
                    if(rows < self.__targetNumberOfRows):

                        # Berechne die Anzahl der zusaetzlich benoetigten Zeilen.
                        numberOfAdditionalRows = self.__targetNumberOfRows - rows

                        # Erstellen der Zeilen die zusaetzlich hinzugefuegt werden sollen
                        additionalRows = np.full((numberOfAdditionalRows, columns), 255, dtype=newMatObject.dtype)

                        # Fuege die zusaetzlichen Zeilen oben an, wenn True
                        if(self.__appendRowsTop):
                            newMatObject = np.append(additionalRows, newMatObject, axis=0)

                        # ansonsten fuege die Zeilen unten an.
                        else:
                            newMatObject = np.append(newMatObject, additionalRows, axis=0)

                    # Wenn nicht, dann ueberpruefe, ob die urspruengliche
                    # Matrix zu viele Zeilen besitzt.
                    elif(self.__targetNumberOfRows < rows):

                        # Loesche die Zeilen von der obersten Zeile beginnend
                        # nach unten, wenn True
                        if(self.__appendRowsTop):

                            # Berechne von oben her die Indices der zu loeschenden Zeilen
                            # und loesche diese Zeilen
                            indicesToDeleteRows = range(0, rows - self.__targetNumberOfRows)
                            newMatObject = np.delete(newMatObject, indicesToDeleteRows, axis=0)

                        # ansonsten loesche die Zeilen von der
                        # untersten Zeile beginnend nach oben.
                        else:
                            # Berechne von unten her die Indices der zu loeschenden Zeilen
                            # und loesche diese Zeilen
                            indicesToDeleteRows = range(self.__targetNumberOfRows, rows)
                            newMatObject = np.delete(newMatObject, indicesToDeleteRows, axis=0)


                # Aktualisieren der Zeilen und Spaltengroesse
                rows, columns = newMatObject.shape

                # Wenn die Anzahl der Spalten angepasst werden sollen ...
                if (self.__fillColumns):

                    # dann ueberpruefe, ob die urspruengliche Matrix
                    # zu wenig Spalten besitzt.
                    if (columns < self.__targetNumberOfColumns):

                        # Berechne die Anzahl der zusaetzlich benoetigten Spalten.
                        numberOfAdditionalColumns = self.__targetNumberOfColumns - columns

                        # Erstellen der Spalten die zusaetzlich hinzugefuegt werden sollen.
                        additionalColumns = np.full((rows, numberOfAdditionalColumns), 255, dtype=newMatObject.dtype)

                        # Fuege die zusaetzlichen Spalten rechts an, wenn True
                        if(self.__appendColumnsRight):
                            newMatObject = np.append(newMatObject, additionalColumns, axis=1)

                        # ansonsten fuege die Spalten links an.
                        else:
                            newMatObject = np.append(additionalColumns, newMatObject, axis=1)

                    # Wenn nicht, dann ueberpruefe, ob die urspruengliche
                    # Matrix zu viele Spalten besitzt.
                    elif (self.__targetNumberOfColumns < columns):

                        # Loesche die Spalten von der rechtesten Spalte beginnend
                        # nach links, wenn True
                        if(self.__appendColumnsRight):

                            # Berechne von rechts her die Indices der zu loeschenden Spalten
                            # und loesche diese Spalten
                            indicesToDeleteColumns = range(self.__targetNumberOfColumns, columns)
                            newMatObject = np.delete(newMatObject, indicesToDeleteColumns, axis=1)

                        # ansonsten loesche die Spalten von der linkesten Spalte beginnend
                        # nach rechts.
                        else:
                            # Berechne von links her die Indices der zu loeschenden Spalten
                            # und loesche diese Spalten
                            indicesToDeleteColumns = range(0, columns - self.__targetNumberOfColumns)
                            newMatObject = np.delete(newMatObject, indicesToDeleteColumns, axis=1)

                # Fuege die Matrix der
                newMats[i].append(newMatObject)

                # Anzeigen des Mat-Objektes dem Zeilen bzw. Spalten
                # abgezogen bzw. hinzugefuegt wurden.
                if (self.__showImagesInWindow):
                    cv2.imshow("ImageFiller_Object", newMatObject)
                    cv2.waitKey(0)

        # Abspeichern aller Noten von jedem Matrix-Typ
        for matType in newMats:
            for note in matType:
                self.__logger.info("Filled following Object: ", "ImageFiller:coreProcess", note)

        self.__logger.info("Finished coreProcess()", "ImageFiller:coreProcess")

        return mats