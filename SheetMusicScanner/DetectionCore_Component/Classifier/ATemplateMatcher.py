#!/usr/bin/env python

"""
ATempalteMatcher ist eine abstracte Klasse für ein TempalteMatcher, der zur Klassifikation bestimmer Objekte in
Bildmatrizen über TemplateMAtching dient.
"""

from abc import abstractmethod
from DetectionCore_Component.IClassifier import IClassifier
import cv2

__author__  = "Bonifaz Stuhr"
__version__ = "0.0.0"
__status__ = "Production"


class ATempalteMatcher(IClassifier):


    @abstractmethod
    def classify(self, matArray):
        """
        Interface Methode: Jeder TempalteMatcher muss diese realisieren.
        Führt die Klassifizierung auf ein Array von Bildmatrizen anhand TemplateMatching aus und gibt die
        erkannten Objekte zurück.

        Parameters
        ----------
        matArray : Die Bildmatrizen auf welche die Klassifizierung ausgeführt werden soll.

        Returns
        -------
        classificationUnits : IClassificationUnitArray
        Aus dem Eingabe-matArray Erkanntes als ClassificationUnit-Array (z.B. Note, Slur, Rest).
        """
        pass

    def _resizeTemplate(self, image, template, ratio):
        """
        Sakliert ein Template auf die höhe des gegebenen Bildes.

        :param image:               Das Bild auf dessen Höhe skaliert wird.
        :param template:            Das zu skalierende Template.
        :param ratio:               Das Größenverhältnis, das das Template zum gesamtbild haben soll.
        :return:                    Das skalierte Template.
        """
        height, __ = image.shape  # Bildhöhe
        templateHeight, __ = template.shape  # Templatehöhe
        resizeFactor = (height * ratio) / templateHeight  # Höhenverhätlis
        return cv2.resize(template, (0, 0), fx=resizeFactor, fy=resizeFactor)  # Skaliertes Template

    def _removeHit(self, mats, template, ratio, topLeft):
        """
        Entfernt das gefundene Template aus den gegebenen Bildern.

        :param mats:                Die Bilder aus denen das gefundene Template entfernt wird.
        :param template:            Das Template das entfernt wird.
        :param ratio:               Das Größenverhältnis, das das Template zum gesamtbild haben soll.
        :param topLeft:             Die obere linke position des gefundenen templates.
        """
        # Template auf Bildgröße skalieren
        resizedTemplate = self._resizeTemplate(mats[0], template, ratio)

        height, width = resizedTemplate.shape
        posX, posY = topLeft

        for mat in mats:
            cv2.rectangle(mat, topLeft, (posX + width, posY + height), 255, -1)