#!/usr/bin/env python
"""
Der CnnNoteClassifier ist eine Realisierung des Interfaces IClassifier und dient zur Klassifizierung einer einzelnen
Musiknote in einem Bild. Er benutzt dazu veschiedene CnnModel die er in ein CnnModelSuit hüllt, um mit diesen die CnnModel
trainiert, evaluiert und mit den CnnModel Noten klassifiziert.
"""

from DetectionCore_Component.IClassifier import IClassifier
from State_Component.State.State import State
from DetectionCore_Component.Classifier.CnnModels.CnnModelSuit import CnnModelSuit
from DetectionCore_Component.Classifier.CnnModels.CnnNotetypeModel import cnnNotetypeModel, predictionToNotetypeClassificationFn, noteTypeToInt
from DetectionCore_Component.Classifier.CnnModels.CnnNoteHightModel import cnnNoteHightModel, predictionToNoteHightClassificationFn, noteHightToInt
from DetectionCore_Component.ClassificationUnit.DurationUnit.Note import Note

import numpy as np
import cv2

__author__  = "Bonifaz Stuhr"
__version__ = "0.0.0"
__status__ = "Production"

class CnnNoteClassifier(IClassifier):

    def __init__(self, modelDir, gdLearnRateForTypeModel, gdLearnRateForHightModel, trainSteps, evalInterval, evalDataSize, testDataSize, trainTypeModel = True, trainHightModel = True):
        """
        Constructor, initialisiert Membervariablen.

        :param modelDir : string Pfad unter welchem die trainierten CnnModelle gespeichert werden.
        :example:
            CnnNoteClassifier("my/path/to/a/model/Dir")
        """
        self.__logger = State().getLogger("DetectionCore_Component_Logger")
        self.__noteTypeCnn = CnnModelSuit(cnnNotetypeModel, predictionToNotetypeClassificationFn, modelDir + "/noteTypeModel", gdLearnRateForTypeModel)
        self.__noteHightCnn = CnnModelSuit(cnnNoteHightModel, predictionToNoteHightClassificationFn, modelDir + "/noteHightModel", gdLearnRateForHightModel)

        self.__gdLearnRateForTypeModel = gdLearnRateForTypeModel
        self.__gdLearnRateForHightModel = gdLearnRateForHightModel

        self.__trainSteps = trainSteps
        self.__evalInterval = evalInterval

        self.__evalDataSize = evalDataSize
        self.__testDataSize = testDataSize

        self.__trainTypeModel = trainTypeModel
        self.__trainHightModel = trainHightModel

    def classify(self, inputDataWithLines, inputDataWithoutLines):
        """
        Bereitet die Inputdaten für das neuronale Netz vor und klassifiziert mit diesem den Input zu einer Note.

        :param inputDataWithLines : Eine Mat welche ein Bild einer Note mit Linien enthält.
        :param inputDataWithoutLines : Eine Mat welche ein Bild einer Note ohne Linien enthält.
        :return: note : Note() Die Klassifizierung einer Musiknote.
        :example:
            cnnNoteClassifier.classify(myInputDataWithLines, myInputDataWithoutLines)
        """

        #Converting the Input
        cnnNoteTypeInput = []
        cnnNoteHightInput = []
        for i in range(0, len(inputDataWithLines)):
            cnnNoteTypeInput.append(inputDataWithoutLines[i].ravel())
            cnnNoteHightInput.append(inputDataWithLines[i].ravel())

        cnnNoteTypeInput, _  = self.convDataForNet(cnnNoteTypeInput)
        cnnNoteHightInput, _ = self.convDataForNet(cnnNoteHightInput)

        #Classify the Input
        noteTypes = self.__noteTypeCnn.classify(cnnNoteTypeInput)
        noteSteps, noteOctaves = self.__noteHightCnn.classify(cnnNoteHightInput)

        #Converting the Classification into internal representation
        notens = []
        for i in range(0, len(noteTypes)):
            # One of i ClassinifcationUnit to classify
            note = Note()
            note.type = noteTypes[i]
            note.pitch["step"] = noteSteps[i]
            note.pitch["octave"] = noteOctaves[i]
            notens.append(note)
            self.__logger.info("Classified following notetype: " + str(note.type) + " step: " + str(note.pitch["step"])
                               + " octave: " + str(note.pitch["octave"]), "CnnNoteClassifier:classify", inputDataWithLines[i])
            #cv2.imshow(note.type, inputDataWithLines[i])
            #cv2.waitKey()

        return notens

    def train(self, inputTrainData, inputTrainLabels):
        """
        Bereitet die Inputdaten für das neuronale Netz vor und trainiert dieses mit den Daten.
        Führt alle n Schritte eine Evaluation auf dem Netz durch.

        :param inputTrainData : Eine Array von Mat welche ein Bild einer Note mit und daneben eins ohne Linien enthält.
        :param inputTrainLabels : Eine Array von Labels für die Bilder von inputTrainData (Gleiche Länge gleiche Sortierung)
        :example:
            cnnNoteClassifier.train(myInputTrainData, myInputTrainaLables)
        """

        self.__logger.info("Starting train()", "CnnNoteClassifier:train")

        #Inputs for the Cnns to train
        noteTypeTrainData = []
        noteTypeTrainLable = []
        noteHightTrainData = []
        noteHightTrainLable = []

        #Converting the Input
        for i in range(0, len(inputTrainData)):
            noteTypeTrainData.append(inputTrainData[i][0:96, 28:57].ravel())
            noteHightTrainData.append(inputTrainData[i][0:96, 0:28].ravel())
            noteTypeTrainLable.append(noteTypeToInt(inputTrainLabels[i]["type"]))
            noteHightTrainLable.append(noteHightToInt(inputTrainLabels[i]["step"], inputTrainLabels[i]["octave"]))

        noteTypeTrainData, noteTypeTrainLable = self.convDataForNet(noteTypeTrainData, noteTypeTrainLable)
        noteHightTrainData, noteHightTrainLable = self.convDataForNet(noteHightTrainData, noteHightTrainLable)

        #Shuffel the Input via Permutation. This is an inital shuffel neeedet to split the data into train, eval, test
        #The Train Shuffel will be made after each step in the train Methode of CnnModelSuit
        p = np.random.permutation(len(noteTypeTrainData))
        noteTypeTrainData = noteTypeTrainData[p]
        noteTypeTrainLable = noteTypeTrainLable[p]
        noteHightTrainData = noteHightTrainData[p]
        noteHightTrainLable = noteHightTrainLable[p]

        #Training the model
        noTrainDataSize = self.__evalDataSize+self.__testDataSize

        if self.__trainTypeModel:
            #Train the model for NoteType
            for i in range(0, self.__trainSteps, self.__evalInterval):
                self.__noteTypeCnn.train(noteTypeTrainData[0:-noTrainDataSize], noteTypeTrainLable[0:-noTrainDataSize], self.__evalInterval)
                self.__noteTypeCnn.eval(noteTypeTrainData[-noTrainDataSize:-self.__testDataSize], noteTypeTrainLable[-noTrainDataSize:-self.__testDataSize])
            #Testing the model
            self.__noteTypeCnn.eval(noteTypeTrainData[-self.__testDataSize:], noteTypeTrainLable[-self.__testDataSize:])

        if self.__trainHightModel:
            #Train the model for NoteHight
            for i in range(0, self.__trainSteps, self.__evalInterval):
                self.__noteHightCnn.train(noteHightTrainData[0:-noTrainDataSize], noteHightTrainLable[0:-noTrainDataSize], self.__evalInterval)
                self.__noteHightCnn.eval(noteHightTrainData[-noTrainDataSize:-self.__testDataSize], noteHightTrainLable[-noTrainDataSize:-self.__testDataSize])
            #Testing the model
            self.__noteHightCnn.eval(noteHightTrainData[-self.__testDataSize:], noteHightTrainLable[-self.__testDataSize:])

        self.__logger.info("Finished train()", "CnnNoteClassifier:train")

    def convDataForNet(self, inputData, lables = None):
        """
        Convertiert die Inputdaten und Lables für das neuronale Netz.

        :param inputData : Eine Array von Mats welche ein Bild einer Note enthält.
        :param lables : Eine Array von Labels für die Bilder von inputData (Gleiche Länge gleiche Sortierung)
        :example:
            cnnNoteClassifier.convDataForNet(myInpuData, mLables)
        """
        #Converting the Input into one Image - each row represents a note
        inputData = np.row_stack(inputData)
        inputData = inputData.astype(np.float32)
        inputData = inputData / 255

        if lables:
            lables = np.array(lables)
            # print(lables)
            # print(type(lables))
            # print(lables.shape)
        # print(inputData)
        # print(type(inputData))
        # print(inputData.shape)
        return inputData, lables


