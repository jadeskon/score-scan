#!/usr/bin/env python

"""
IPipeController bietet das Interface für einen PipeController, der zur Steuerung des Hauptprogrammablaufes (der
Klassifizierungs-Pipe) dient.
"""

from abc import ABCMeta, abstractmethod

__author__  = "Bonifaz Stuhr"
__version__ = "0.0.0"
__status__ = "Production"


class IPipeController(metaclass=ABCMeta):

    @abstractmethod
    def init(self):
        """
        Interface Methode: Jeder PipeController muss diese realisieren.
        Baue mithilfe eines PipeContructors, die Pipe zur Klassifizierung auf.

        :return: successful : boolean Initialisierung erfolgreich?
        """
        pass

    @abstractmethod
    def execute(self):
        """
        Interface Methode: Jeder PipeController muss diese realisieren.
        Führt die Befehle über die Pipe aus und steuert diese.

        :return: successful : boolean War die Klassifizierung erfolgreich?
        """
        pass

		
		