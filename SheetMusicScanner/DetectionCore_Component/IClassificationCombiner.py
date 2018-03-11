#!/usr/bin/env python

"""
IClassificationCombiner bietet das Interface für einen ClassificationCombiner.
Ein ClassificationCombiner wird dazu verwendet, eine Menge von Klassifizierung (IClassification) zu bewerten und diese
zu einer -der Besten- Klassifizierung zusammenzufügen. Dies geschieht i.d.R. im DetectionCore, nachdem alle
IFullClassifier eine IClassification berechnet haben.
"""

from abc import ABCMeta, abstractmethod

__author__  = "Bonifaz Stuhr"
__version__ = "0.0.0"
__status__ = "Production"


class IClassificationCombiner(metaclass=ABCMeta):

    """todo: füge alle geteilten Methoden der ClassificationCombiner hier hinzu"""
    @abstractmethod
    def dummy(self):
        pass

		