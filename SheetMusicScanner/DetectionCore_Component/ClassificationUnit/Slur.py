from DetectionCore_Component.IClassificationUnit import IClassificationUnit


__author__  = "Tobias Eigler"
__version__ = "0.0.0"
__status__ = "Production"


"""
Datenstruktur für Bindeboegen. (Bindebogen = Slur)

"""
class Slur(IClassificationUnit):



    def __init__(self):
        self.__elementNumber = 0                # Nummer im gesamten SheetMusic
        self.__recognitionPercentage = 0

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


		
