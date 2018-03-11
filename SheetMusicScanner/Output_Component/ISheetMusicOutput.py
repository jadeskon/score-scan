#!/usr/bin/env python

"""
ISheetMusicOutput bietet das Interface für einen SheetMusicOutput, der zum ausgeben einer SheetMusic
Klassifizierung dient.
"""

from abc import ABCMeta, abstractmethod

__author__  = "Bonifaz Stuhr"
__version__ = "0.0.0"
__status__ = "Production"


class ISheetMusicOutput(metaclass=ABCMeta):


    @abstractmethod
    def write(self, sheetMusic):
        """
        Interface Methode: Jeder SheetMusicOutput muss diese realisieren.
        Führt den entsprechenden Ausgabevorgang durch und erstellt ausgebene Datau.

        Parameters
        ----------
        sheetMusic: SheetMusic

        Returns
        -------
        successful : boolean
        War die Ausgabe erfolgreich?
        """
        pass

		