#!/usr/bin/env python

from DetectionCore_Component.IClassificationUnit import IClassificationUnit
from abc import ABCMeta, abstractmethod

__author__  = "Tobias Eigler"
__version__ = "0.0.0"
__status__ = "Production"

"""
Abstrakteklasse fuer Elemente mit zeitlicher Dauer (= Akkorde, Noten, Pausen)

"""
class ADurationUnit(IClassificationUnit):

    @abstractmethod
    def __init__(self):
        self.__duration = 0
        self.__tactInternalNumber = 0
        self.__tactNumber = 0
        self.__type = ''
        self.__elementNumber = 0
        self.__recognitionPercentage = 0





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
    def recognitionPercentage(self):
        pass

    @recognitionPercentage.setter
    def recognitionPercentage(self, recognitionPercentage):
        pass
		
		

