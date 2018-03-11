#!/usr/bin/env python

"""
To-Do:
Bitte Kommentar bzw. Dokumentaion erstellen!
"""

from State_Component.State.State import State
import cv2

__author__  = "Juergen Maier / Bonifaz Stuhr"
__version__ = "0.0.0"
__status__ = "Production"


class ImageResizer:

    def __init__(self,
                 targetNumberOfRows=110,
                 targetNumberOfColumns=32,
                 interpolation=cv2.INTER_LINEAR,
                 showImagesInWindow=False):
        """
        To-Do:
        Bitte Kommentar bzw. Dokumentaion erstellen!
        """
        self.__logger = State().getLogger("DetectionCore_Component_Logger")
        self.__logger.info("Starting __init__()", "ImageResizer:__init__")

        self.__targetNumberOfRows = targetNumberOfRows
        self.__targetNumberOfColumns = targetNumberOfColumns
        self.__interpolation = interpolation
        self.__showImagesInWindow = showImagesInWindow

        self.__logger.info("Finsihed __init__()", "ImageResizer:__init__")

    def coreProcess(self, mats):
        """
        To-Do:
        Bitte Kommentar bzw. Dokumentaion erstellen!
        """
        self.__logger.info("Starting coreProcess()", "ImageResizer:coreProcess")

        # Erstelle eine Liste mit i leeren Listen.
        # Jede leere Liste i wird fuer einen Matrix-Typen angelegt
        newMats = []
        for i in range(0, len(mats)):
            newMats.append([])

        # Iteriere ueber jeden Matrix-Typen
        for i in range(0, len(mats)):

            # Iteriere ueber jedes Objekt der Matrix-Typen-Liste
            for matObject in mats[i]:

                # Skaliere das Mat-Objekt mit der angegeben Interpolations-Methode
                newMatObject = cv2.resize(src=matObject,
                                          dsize=(self.__targetNumberOfColumns, self.__targetNumberOfRows),
                                          interpolation=self.__interpolation)

                # Fuege die Matrix der
                newMats[i].append(newMatObject)

                # Anzeigen des Mat-Objektes dem Zeilen bzw. Spalten
                # abgezogen bzw. hinzugefuegt wurden.
                if (self.__showImagesInWindow):
                    cv2.imshow("ImageFiller_Object: " + str(newMatObject.shape), newMatObject)
                    cv2.waitKey(0)

        # Abspeichern aller Noten von jedem Matrix-Typ
        for matType in newMats:
            for note in matType:
                self.__logger.info("Resized following Object to:  " + str(note.shape), "ImageResizer:coreProcess", note)

        self.__logger.info("Finished coreProcess()", "ImageResizer:coreProcess")

        return newMats