#!/usr/bin/env python

"""
Der Output ist eine Realisierung des Interfaces IOutput und dient der Steuerung eines bestimmten Ablaufs des Ausgebens
einer Klassifizierung.
"""

from Output_Component.IOutput import IOutput
from State_Component.State.State import State
from Output_Component.SheetMusicOutput.MusicXmlOutput import MusicXmlOutput
from Output_Component.SheetMusicOutput.MidiOutput import MidiOutput
import os
import cv2
import datetime
import numpy as np

__author__  = "Bonifaz Stuhr"
__version__ = "0.0.0"
__status__ = "Production"


class Output(IOutput):

    def __init__(self, config):
        """
        Constructor, initialisiert Membervariablen.

        :param Config : config Die Konfiguration.
        :example:
            Output(config)
        """
        self.__logger = State().getLogger("Output_Component_Logger")
        self.__logger.info("Starting __init__()", "Postprocessing:__init__")
        """
        Todo: self.__sheetMusicOutput = MusicXMLOutput("config.outputPath")
        """
        self.__sheetMusicOutput = MusicXmlOutput(config["outputpathmusicxml"], config["fillwithrests"])
        self.__sheetMidiOutput = MidiOutput(config["outputpathmidi"], config["playmidi"], config["miditempo"])
        self.__writeTraindataDirectory = "./traindata/"
        self.__logger.info("Finished __init__()", "Postprocessing:__init__")


    def execute(self, classification):
        """
        Führt den entsprechenden Outputvorgang über einen Parser oder ähnliches durch.

        :param classification : Die Klassifizierung auf, welche ausgegeben werden sollen.
        :return: successful : boolean War die Ausgabe erfolgreich?
        :example:
            output.execute(classification)
        """
        self.__logger.info("Starting execute()", "Output:MusicXML execute")
        """
        Todo: check if classification typ of SheetMusic if true:
        """
        self.__sheetMusicOutput.write(classification)
        self.__logger.info("Finished execute()", "Output:MusicXML execute")
        self.__logger.info("Starting execute()", "Output:Midi execute")
        self.__sheetMidiOutput.write(classification)
        self.__logger.info("Finished execute()", "Output:Midiexecute")
        return True


    def writeNextTraindata(self, trainMats, trainLable):
        """
        Fügt die gegebenen Trainingsdaten einem Ordner hinzu.

        :param trainMats : Die Trainingsbilder die geschreiben werden sollen.
        :param trainLable : Die zu den Bildern gehörenden Lable die geschreiben werden sollen.
        :return: successful : boolean War die Ausgabe erfolgreich?
        """
        self.__logger.info("Starting writeNextTraindata()", "Output:writeNextTraindata")

        if not os.path.exists(self.__writeTraindataDirectory):
            os.makedirs(self.__writeTraindataDirectory)

        for i in range(0, len(trainMats[0])):
            if trainMats[0] and i < len(trainLable):
                #Creating Lable with Data-ID
                id = datetime.datetime.now().isoformat().replace(".", "#")
                id = id.replace(":", "-")
                id += str(i)
                lableName = self.__writeTraindataDirectory + trainLable[i]["type"] + "_" + trainLable[i]["step"] + "_" + trainLable[i]["octave"] + "_" + id + ".png"
                mat = np.hstack((trainMats[0][i], trainMats[1][i]))
                height, width = mat.shape
                if height is 96 and width is 56: #Nicht mehr nötig, da nun alle Noten diese Größe haben. Aber sicher ist sicher.
                    cv2.imwrite(lableName, mat)

        self.__logger.info("Finished writeNextTraindata()", "Output:writeNextTraindata")
        return True

