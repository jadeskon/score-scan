#!/usr/bin/env python

"""
Der FilenameToLableParser ist eine Realisierung des Interfaces ILableParser und dient zum einlesen eines Filenames.
FilenameFormat : lableAttribut1_lableAttribut2 Z.b: G_3 (für step_duration)
Dieser Filename wird in ein Lable umgewandelt.
"""

from Input_Component.ILableParser import ILableParser

__author__  = "Bonifaz Stuhr"
__version__ = "0.1.0"
__status__ = "Production"


class FilenameToLableParser(ILableParser):

    def __init__(self, filename):
        self.__filename = filename


    def parseToLable(self):
        """
        Führt den entsprechenden Einlesevorgang durch und erstellt das Lable.

        :return: lable : Array of Dictionarys Das eingelesene Lable.
        """
        fileLables = self.__filename.split('_')
        lable = []
        noteLable={
            "type": fileLables[0],
            "step": fileLables[1],
            "octave": fileLables[2]
        }
        lable.append(noteLable)
        return lable



		
		