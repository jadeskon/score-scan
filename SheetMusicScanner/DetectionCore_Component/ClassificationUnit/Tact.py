# !/usr/bin/env python

from DetectionCore_Component.IClassificationUnit import IClassificationUnit
from DetectionCore_Component.ClassificationUnit.KeySignatur import KeySignatur
from DetectionCore_Component.ClassificationUnit.TimeSignature import TimeSignature
from DetectionCore_Component.ClassificationUnit.Clef import Clef
from DetectionCore_Component.ClassificationUnit.DurationUnit.Chord import Chord
from DetectionCore_Component.ClassificationUnit.DurationUnit.Rest import Rest

__author__ = "Tobias Eigler"
__version__ = "0.0.0"
__status__ = "Production"


class Tact(IClassificationUnit):
    """
    Datenstruktur fuer Takte

    """

    def __init__(self):
        self.__elementNumber = 0  # Nummer im gesamten SheetMusic
        self.__recognitionPercentage = 0
        self.__tactNumber = 0  # Nummer des Taktes
        self.__tactElements = []  # Elemente IClassificationUnits die sich in diesem Takt befinden.
        self.__width = 0.0  # Taktbreite

    # region Eigenschaften

    @property
    def elementNumber(self):
        return self.__elementNumber

    @elementNumber.setter
    def elementNumber(self, elementNumber):
        self.__elementNumber = elementNumber

    @property
    def recognitionPercentage(self):
        return self.__recognitionPercentage

    @recognitionPercentage.setter
    def recognitionPercentage(self, recognitionPercentage):
        self.__recognitionPercentage = recognitionPercentage

    @property
    def tactNumber(self):
        return self.__tactNumber

    @tactNumber.setter
    def tactNumber(self, tactNumber):
        self.__tactNumber = tactNumber

    @property
    def tactElements(self):
        return self.__tactElements

    @property
    def width(self):
        return self.__width

    @width.setter
    def width(self, width):
        self.__width = width

    # endregion


    def creatKeySignature(self, tactInternalNumber, elementNumber):
        """
        Erstellt eine Tonart und gibt diese zurück.
        :return: Die erstellte Tonart.
        """
        keySig = KeySignatur()
        keySig.elementNumber = elementNumber
        keySig.tactInternalNumber = tactInternalNumber
        return keySig

    def creatKeySig(self):
        """
        Erstellt eine Tonart und gibt diese zurück.
        Besser wäre:  creatKeySignature(self, tactInternalNumber, elementNumber) zu verwenden!
        -> Da Tonart ohne diese Nummern schwer zu händeln ist.
        :return: Die erstellte Tonart.
        """
        return KeySignatur()

    def creatTimeSignature(self, tactInternalNumber, elementNumber):
        """
        Erstellt eine Taktart und gibt diese zurück.
        :return: Die erstellte Taktart.
        """
        timeSig = TimeSignature()
        timeSig.elementNumber = elementNumber
        timeSig.tactInternalNumber = tactInternalNumber
        return timeSig

    def creatTimeSig(self):
        """
        Erstellt eine Taktart und gibt diese zurück.
        Besser wäre:  creatKeySignature(self, tactInternalNumber, elementNumber) zu verwenden!
        -> Da Taktart ohne diese Nummern schwer zu händeln ist.
        :return: Die erstellte Taktart.
        """
        return TimeSignature()

    def creatClef(self, tactInternalNumber, elementNumber):
        """
        Erstellt einen Notenschlüssel und gibt diese zurück.
        :return: Der erstellte Notenschlüssel.
        """
        cl = Clef()
        cl.elementNumber = elementNumber
        cl.tactInternalNumber = tactInternalNumber
        return cl

    def creatCl(self):
        """
        Erstellt einen Notenschlüssel und gibt diese zurück.
        Besser wäre:  creatClef(self,tactInternalNumber, elementNumber) zu verwenden!
        -> Da Notenschlüssel ohne diese Nummern schwer zu händeln ist.
        :return: Der erstellte Notenschlüssel.
        """
        return Clef()

    def creatChord(self, tactInternalNumber, elementNumber):
        """
        Erstellt einen Akkord und gibt diese zurück.
        :return: Der erstellte Akkord.
        """
        chord = Chord()
        chord.elementNumber = elementNumber
        chord.tactInternalNumber = tactInternalNumber
        return chord

    def creatCh(self):
        """
        Erstellt einen Akkord und gibt diese zurück.
        Besser wäre:  creatChord(self, tactInternalNumber, elementNumber) zu verwenden!
        -> Da Akkord ohne diese Nummern schwer zu händeln ist.
        :return: Der erstellte Akkord.
        """
        return Chord()

    def creatRest(self, tactInternalNumber, elementNumber):
        """
        Erstellt eine Pause und gibt diese zurück.
        :return: Die erstellte Pause.
        """
        rest = Rest()
        rest.elementNumber = elementNumber
        rest.tactInternalNumber = tactInternalNumber
        return rest

    def creatRe(self):
        """
        Erstellt eine Pause und gibt diese zurück.
        Besser wäre:  creatRest(self, tactInternalNumber, elementNumber zu verwenden!
        -> Da Pause ohne diese Nummern schwer zu händeln ist.
        :return: Die erstellte Pause.
        """
        return Rest()

    def addKeySignatur(self, keySignatur):
        self.__tactElements.append(keySignatur)

    def addTimeSignatur(self, timeSignatur):
        self.__tactElements.append((timeSignatur))

    def addClef(self, clef):
        self.__tactElements.append(clef)

    def addChord(self, chord):
        self.__tactElements.append(chord)

    def addRest(self, rest):
        self.__tactElements.append(rest)
