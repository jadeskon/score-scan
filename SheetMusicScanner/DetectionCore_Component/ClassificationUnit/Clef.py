from DetectionCore_Component.IClassificationUnit import IClassificationUnit


__author__  = "Tobias Eigler"
__version__ = "0.0.0"
__status__ = "Production"


class Clef(IClassificationUnit):
    """
    Datenstruktur für Notenschluessel.

    """
    def __init__(self):
        self.__elementNumber = 0                # Nummer im gesamten SheetMusic
        self.__recognitionPercentage = 0
        self.__tactInternalNumber = 0           # Nummer der Note im Takt, in der sich die Note befindet.
        self.__sign = "G"                       # The sign element represents the clef symbol.  https://usermanuals.musicxml.com/MusicXML/Content/CT-MusicXML-clef.htm
        self.__line = 2                         # Line numbers are counted from the bottom of the staff. Standard values are 2 for the G sign (treble clef), 4 for the F sign (bass clef), 3 for the C sign (alto clef) and 5 for TAB (on a 6-line staff).


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
    def sign(self):
        return self.__sign

    @sign.setter
    def sign(self, sign):
        self.__sign = sign


    @property
    def line(self):
        return self.__line

    @line.setter
    def line(self, line):
        self.__line = line

		
		