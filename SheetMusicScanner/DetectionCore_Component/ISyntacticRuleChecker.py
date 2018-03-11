#!/usr/bin/env python

"""
IClassificationUnit bietet das Interface für einen SyntacticRuleChecker.
Ein SyntacticRuleChecker wird dazu verwendet, eine Menge von Klassifizierung die im Zusammenhang stehen zu prüfen.
Hierbei werden über die Regeln des Zusammenhangs mögliche Fehler in der Klassifizierung erkannt.
IFullClassifier können einen ISyntacticRuleChecker benutzen und auf dessen Ergebnisse reagieren.
"""

from abc import ABCMeta, abstractmethod

__author__  = "Bonifaz Stuhr"
__version__ = "0.0.0"
__status__ = "Production"


class ISyntacticRuleChecker(metaclass=ABCMeta):

    """todo: füge alle geteilten Methoden der RuleChecker hier hinzu"""
    @abstractmethod
    def dummy(self):
        pass

		
		