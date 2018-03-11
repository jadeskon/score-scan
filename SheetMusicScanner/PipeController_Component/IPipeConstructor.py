#!/usr/bin/env python

"""
IPipeConstructor bietet das Interface für einen PipeConstructor, der zur Konstruction der Pipe zur Klassifzierung
dient.
"""

from abc import ABCMeta, abstractmethod

__author__  = "Bonifaz Stuhr"
__version__ = "0.0.0"
__status__ = "Production"


class IPipeConstructor(metaclass=ABCMeta):

    @abstractmethod
    def constructPipe(self):
        """
        Interface Methode: Jeder PipeConstructor muss diese realisieren.
        Konstruiert die Pipe für die Klassifizierung und gibt diese zurück.

        :return: successful : boolean
        :return: pipe : dictionary Die Pipe als <name,object> Paar.
        """
        pass

		
		