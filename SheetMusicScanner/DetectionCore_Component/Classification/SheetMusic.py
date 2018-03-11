#!/usr/bin/env python

from DetectionCore_Component.IClassification import IClassification
from DetectionCore_Component.ClassificationUnit.Tact import Tact

__author__  = "Tobias Eigler"
__version__ = "0.0.0"
__status__ = "Production"



class SheetMusic(IClassification):
    """
    Datenstruktur fuer ein Musikblatt
    """

    def __init__(self):
        self.__sheetMusicClassificationUnits = []

    @property
    def sheetMusicClassificationUnits(self):
        return self.__sheetMusicClassificationUnits

    @sheetMusicClassificationUnits.setter
    def sheetMusicClassificationUnits(self, sheetMusicClassificationUnits):
        self.__sheetMusicClassificationUnits = sheetMusicClassificationUnits


    def creatTact(self, tactNumber, elementNumber):
        """
        Erstellt einen Takt und gibt diesen zurück.
        Besser wäre diese Methode, da Tact ohne Nummer nicht von Vorteil ist.!!
        :param tactNumber: Taktnummer des zu erstellenden Taktes.
        :param elementNumber: Elementnummer des zu erstellenden Taktes.
        :return: Der erstellte Takt.
        """
        tact = Tact()
        tact.tactNumber = tactNumber
        tact.elementNumber = elementNumber
        return tact

    def creatT(self):
        """
        Erstellt einen Takt und gibt diesen zurück.
        Besser wäre creatTact mit tactNumber und elementNumber zu verwenden!
        Kann aber fälle geben bei denen diese Nummern noch nicht bekannt sind der Takt aber schon erstellt werden muss.
        Dies sollte aber die Ausnahme sein.
        :return: Der erstellte Takt.
        """
        tact = Tact()
        return tact


    def addTact(self, tact):
        self.sheetMusicClassificationUnits.append(tact)

    @property
    def tacts(self):
        return self.sheetMusicClassificationUnits
		



