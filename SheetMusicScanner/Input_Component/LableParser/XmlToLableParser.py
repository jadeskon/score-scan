#!/usr/bin/env python

"""
Der XmlToLableParser ist eine Realisierung des Interfaces ILableParser und dient zum einlesen eines MusixXML Files.
Dieses File wird in ein Lable umgewandelt.
"""

from Input_Component.ILableParser import ILableParser
import xml.etree.ElementTree as et

__author__  = "Bonifaz Stuhr"
__version__ = "0.1.0"
__status__ = "Production"


class XmlToLableParser(ILableParser):

    def __init__(self, pathToXML):
        self.__pathToXML = pathToXML


    def parseToLable(self):
        """
        Führt den entsprechenden Einlesevorgang durch und erstellt das Lable.

        :return: lable : Array of Dictionarys Das eingelesene Lable.
        """
        xmlTree = et.parse(self.__pathToXML)
        root = xmlTree.getroot()
        notes = root.findall("./part/measure/note")

        lable = []
        for note in notes:
            noteLable={
                "type": note.find('type').text,
                "step": note.find("pitch/step").text,
                "octave": note.find("pitch/octave").text
            }
            lable.append(noteLable)
        return lable

		
		
		