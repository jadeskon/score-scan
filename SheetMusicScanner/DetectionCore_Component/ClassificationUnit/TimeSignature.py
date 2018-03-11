
#!/usr/bin/env python


from DetectionCore_Component.IClassificationUnit import IClassificationUnit

__author__  = "Tobias Eigler"
__version__ = "0.0.0"
__status__ = "Production"


"""
Datenstruktur fuer Taktarten

"""
class TimeSignature(IClassificationUnit):
    def __init__(self):
        self.__beats = 0                        # Zähler 3/4 -> Zähler ist 3.    The beats element indicates the number of beats, as found in the numerator of a time signature
        self.__beatType = 0                     # Nenner 3/4 -> Nenner ist 4.    The beat-type element indicates the beat unit, as found in the denominator of a time signature
        self.__recognitionPercentage = 0
        self.__elementNumber = 0                # Nummer im gesamten SheetMusic
        self.__tactInternalNumber = 0           # Nummer der Taktart im Takt, in der sich die Taktart befindet.


    @property
    def beats(self):
        return self.__beats

    @beats.setter
    def beats(self, beats):
        self.__beats = beats

    @property
    def beatType(self):
        return self.__beatType

    @beatType.setter
    def beatType(self, beatType):
        self.__beatType = beatType

    @property
    def recognitionPercentage(self):
        return self.__recognitionPercentage

    @recognitionPercentage.setter
    def recognitionPercentage(self, recognitionPercentage):
        self.__recognitionPercentage = recognitionPercentage

    @property
    def elementNumber(self):
        return self.__elementNumber

    @elementNumber.setter
    def elementNumber(self, elementNumber):
        self.__elementNumber = elementNumber


    @property
    def tactInternalNumber(self):
        return self.__tactInternalNumber

    @tactInternalNumber.setter
    def tactInternalNumber(self, tactInternalNumber):
        self.__tactInternalNumber = tactInternalNumber

