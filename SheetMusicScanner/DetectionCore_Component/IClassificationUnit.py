#!/usr/bin/env python



from abc import ABCMeta, abstractmethod

__author__  = "Tobias Eigler"
__version__ = "0.0.0"
__status__ = "Production"

"""
IClassificationUnit bietet das Interface für eine ClassificationUnit, eine Einheit (z.B. Note), welche
im Eingabebild erkannt werden kann.
Jede Klasse (z.B. Noten) die von einem IClassifier erkannt wird, muss dieses Interface implementieren.
"""
class IClassificationUnit(metaclass=ABCMeta):


    @abstractmethod
    def __init__(self):
        pass


    @property
    def elementNumber(self):
        pass

    @elementNumber.setter
    def elementNumber(self, elementNumber):
        pass

    @property
    def recognitionPercentage(self):
        pass

    @recognitionPercentage.setter
    def recognitionPercentage(self, recognitionPercentage):
        pass




		

