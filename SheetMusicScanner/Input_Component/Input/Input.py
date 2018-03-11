1  # !/usr/bin/env python

"""
Der Input ist eine Realisierung des Interfaces IInput und dient zur Steuerung eines bestimmten Ablaufs des Einlesens
einer Bildmatrix für die Klassifizierung dient.
"""

from Input_Component.IInput import IInput
from State_Component.State.State import State
from Input_Component.MatParser.PdfToMatParser import PdfToMatParser
from Input_Component.MatParser.PngToMatParser import PngToMatParser
from Input_Component.LableParser.XmlToLableParser import XmlToLableParser
from Input_Component.LableParser.FilenameToLableParser import FilenameToLableParser

import os
import glob

__author__  = "Dominik Rauch, Bonifaz Stuhr"
__version__ = "0.1.0"
__status__ = "Ready"


class Input(IInput):

    def __init__(self, config):
        """
        Konstruktor
        :param config:
        """
        self.__logger = State().getLogger("Input_Component_Logger")
        self.__logger.info("Starting __init__()", "Input:__init__")

        self.__matParser = None
        self.__lableParser = None

        self.__matXMLPairCounter = 0
        self.__matFileNamesForTestDataCreation = 0
        self.__xmlFileNamesForTestDataCreation = 0

        self.__createTraindataPdfDir = config["pathToCreateTrainDataFolder"]
        self.__createTraindataXmlDir = config["pathToCreateTrainDataLabelFolder"]
        self.__traindataDir = config["pathToTrainDataFolder"]
        self.__pathToFileToClassify = config["pathToClassifiactionImage"]
        # self.__pathToFileToClassify = "./Input_Component\\Input\\clear_basic_1.pdf"
        # self.__pathToFileToClassify = "./Input_Component\\Input\\clear_basic_10.pdf"
        # self.__pathToFileToClassify = "./Input_Component\\Input\\clear_basic_15.pdf"
        # self.__pathToFileToClassify = "./Input_Component\\Input\\clear_basic_rest_9.pdf"
        # self.__pathToFileToClassify = "./Input_Component\\Input\\clear_middle_5.pdf"
        # self.__pathToFileToClassify = "./Input_Component\\Input\\clear_middle_7.pdf"
        # self.__pathToFileToClassify = "./Input_Component\\Input\\clear_elements.pdf"
        # self.__pathToFileToClassify = "./Input_Component\\Input\\clear_basic_38.pdf"
        # self.__pathToFileToClassify = "./Input_Component\\Input\\clear_basic_41.pdf"

        self.__logger.info("Finished __init__()", "Input:__init__")

    def execute(self):
        """
        Führt den entsprechenden Einlesevorgang über einen Parser durch und erstellt die Bildmatrix.
        :return: mat Die Matrix des eingelesenen Bildes
        """
        self.__logger.info("Starting execute()", "Input:execute")

        filename, file_extension = os.path.splitext(self.__pathToFileToClassify)
        if file_extension == ".pdf":
            self.__logger.info("File is detected as PDF.", "Input:execute")
            self.__matParser = PdfToMatParser(self.__pathToFileToClassify)
        else:
            self.__logger.info("File looks like an image-datatype.", "Input:execute")
            self.__matParser = PngToMatParser(self.__pathToFileToClassify)

        mat = self.__matParser.parseToMat()

        self.__logger.info("Readed following Image:", "Input:execute", mat)
        self.__logger.info("Finished execute()", "Input:execute")
        return mat

    def readNextImgXMLPair(self):
        """
        Führt den entsprechenden Einlesevorgang für die nächsten Files im Ordner
        über einen Parser durch und erstellt die Bildmatrix sowie das Lable.
        :return: mat Die Matrix des eingelesenen Bildes.
        :return: lable Das Lable zur Bildmatrix.
        """
        self.__logger.info("Starting readNextImgXMLPair()", "Input:readNextImgXMLPair")

        # Falls es der erste Schritt ist, Filenamen einlesen
        if not self.__matXMLPairCounter:
            self.__matFileNamesForTestDataCreation = glob.glob(self.__createTraindataPdfDir + "*.pdf")
            self.__xmlFileNamesForTestDataCreation = glob.glob(self.__createTraindataXmlDir + "*.xml")
            self.__logger.info("Found following files to create testdata:" +
                               str(self.__matFileNamesForTestDataCreation) +
                               str(self.__xmlFileNamesForTestDataCreation), "Input:readNextImgXMLPair")

        # Falls es der letzte Schritt ist, Counter zurücksetzen
        if (self.__matXMLPairCounter >= self.__matFileNamesForTestDataCreation.__len__()) \
                or (self.__matXMLPairCounter > self.__xmlFileNamesForTestDataCreation.__len__()):
            self.__logger.debug("Max Filecount reached: reset matXMLPairCounter to 0", "Input:readNextImgXMLPair")
            self.__matXMLPairCounter = 0
            return None, None

        # Lese Mat und Lable und erhöhe Counter
        self.__matParser = PdfToMatParser(self.__matFileNamesForTestDataCreation[self.__matXMLPairCounter])
        # test with png:
        # self.__matParser = PngToMatParser(self.__pathToFileToClassify)
        self.__lableParser = XmlToLableParser(self.__xmlFileNamesForTestDataCreation[self.__matXMLPairCounter])
        mat = self.__matParser.parseToMat()
        lable = self.__lableParser.parseToLable()

        self.__matXMLPairCounter = self.__matXMLPairCounter + 1

        self.__logger.info("Finished readNextImgXMLPair()", "Input:readNextImgXMLPair")
        return mat, lable

    def readNoteTrainData(self):
        """
        Führt den entsprechenden Einlesevorgang für einen Ordner über einen Parser durch und gibt die
        Notentrainingsdaten mit ihrem Label zurück.
        :return: matArray Die MAtrizen des eingelesenen Bildes.
        :return: lableArray Die Lable zu den Bildmatrizen.
        """
        self.__logger.info("Starting readNoteTrainData()", "Input:readNoteTrainData")

        # Reading Filenames from traindata dir
        fileNames = glob.glob(self.__traindataDir + "*.png")

        matArray = []
        lableArray = []

        # For each Testdate Parse Mat and Lable
        for fileName in fileNames:
            # Prepare LableString for Parser
            name = fileName.split("\\")[-1]
            name = name.split(".")[0]
            lableArray = lableArray + FilenameToLableParser(name).parseToLable()
            matArray.append(PngToMatParser(fileName).parseToMat())
        self.__logger.info("Finished readNoteTrainData()", "Input:readNoteTrainData")
        return matArray, lableArray
