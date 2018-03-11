#!/usr/bin/env python

"""
IClassification bietet das Interface für eine Classification - eine vollständige Klassifizierung.
Eine Classification besteht i.d.R. aus mehreren IClassificationUnits.
Z.b. Eine MusicSheet (IClassification) besthet aus Takten, Noten, usw. welche allesamt IClassificationUnits darstellen.
"""

from abc import ABCMeta, abstractmethod

__author__  = "Bonifaz Stuhr"
__version__ = "0.0.0"
__status__ = "Production"


class IClassification(metaclass=ABCMeta):

    """todo: füge alle geteilten Methoden von IClassifications hier hinzu"""
    #@abstractmethod
    #def dummy(self):
        #pass

		