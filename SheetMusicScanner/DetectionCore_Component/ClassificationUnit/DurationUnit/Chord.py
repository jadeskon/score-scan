#!/usr/bin/env python

from DetectionCore_Component.ClassificationUnit.ADurationUnit import ADurationUnit
from DetectionCore_Component.ClassificationUnit.DurationUnit.Note import Note

__author__  = "Tobias Eigler"
__version__ = "0.0.0"
__status__ = "Production"




class Chord(ADurationUnit):
    """
    Datenstruktur fuer Akkorde
    """
    def __init__(self):
        self.__chordInternalNumber = 0 # Nummer der Note im Akkord.
        self.__duration = 0
        self.__tactInternalNumber = 0  # Nummer der Note im Takt, in der sich die Note befindet.
        self.__tactNumber = 0  # Nummer des Taktes zu der die Note gehört
        self.__type = ""
        self.__elementNumber = 0
        self.__recognitionPercentage = 0
        self.__chordElements = []



    # region Eigenschaften

    @property
    def chordInternalNumber(self):
        return self.__chordInternalNumber

    @chordInternalNumber.setter
    def chordInternalNumber(self, chordInternalNumber):
        self.__chordInternalNumber = chordInternalNumber

    @property
    def duration(self):
        return self.__duration

    @duration.setter
    def duration(self, duration):
        self.__duration = duration

    @property
    def tactInternalNumber(self):
        return self.__tactInternalNumber

    @tactInternalNumber.setter
    def tactInternalNumber(self, tactInternalNumber):
        self.__tactInternalNumber = tactInternalNumber

    @property
    def tactNumber(self):
        return self.__tactNumber

    @tactNumber.setter
    def tactNumber(self, tactNumber):
        self.__tactNumber = tactNumber

    @property
    def type(self):
        return self.__type

    @type.setter
    def type(self, type):
        self.__type = type

    @property
    def elementNumber(self):
        return self.__elementNumber

    @elementNumber.setter
    def elementNumber(self, elementNumber):
        self.__elementNumber = elementNumber

    @property
    def chordElements(self):
        return self.__chordElements

    @chordElements.setter
    def chordElements(self, chordElements):
        self.__chordElements = chordElements
    # endregion

    def creatNote(self, tactInternalNumber, elementNumber, chordInternalNumber):
        """
        Erstellt eine Note und gibt diese zurück.
        :return: Die erstellte Note.
        """
        note = Note()
        note.elementNumber = elementNumber
        note.tactInternalNumber = tactInternalNumber
        note.chordInternalNumber = chordInternalNumber
        return note

    def creatNot(self):
        """
        Erstellt eine Note und gibt diese zurück.
        Besser wäre:  creatNote(self, tactInternalNumber, elementNumber, chordInternalNumber zu verwenden!
        -> Da Note ohne diese Nummern schwer zu händeln ist.
        :return: Die erstellte Note.
        """
        return Note()

    def addNote(self, note):
        self.__chordElements.append(note)



