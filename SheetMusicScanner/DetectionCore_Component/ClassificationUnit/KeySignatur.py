from DetectionCore_Component.IClassificationUnit import IClassificationUnit

__author__ = "Tobias Eigler"
__version__ = "0.0.0"
__status__ = "Production"

"""
Datenstruktur für Tonarten.

"""

class KeySignatur(IClassificationUnit):



    def __init__(self):
        self.__elementNumber = 0                                  # Nummer im gesamten SheetMusic
        self.__recognitionPercentage = 0
        self.__tactInternalNumber = 0                             # Nummer der Note im Takt, in der sich die Note befindet.
        self.__fifths = 0                                         # angabe der tonart 0 = C-Dur, 1 = G-Dur, -1 = F-Dur -> pos. zahl = kreuz; neg. zahl = b
        self.__modes = ["major", "minor","dorian",
                        "phrygian", "lydian","mixolydian",
                        "aeolian","ionian", "locrian", "none"]    # The mode type is used to specify major/minor and other mode distinctions. Valid mode values include major, minor, dorian, phrygian, lydian, mixolydian, aeolian, ionian, locrian, and none.
        self.__mode = ""                                          # Ausgewälter mode



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
    def tactInternalNumber(self):
        return self.__tactInternalNumber

    @tactInternalNumber.setter
    def tactInternalNumber(self, tactInternalNumber):
        self.__tactInternalNumber = tactInternalNumber


    @property
    def fifths(self):
        return self.__fifths

    @fifths.setter
    def fifths(self, fifths):
        self.__fifths = fifths


    @property
    def modes(self):
        return self.__modes


    @property
    def mode(self):
        return self.__mode

    @mode.setter
    def mode(self, mode):
        self.__mode = mode
		
		
