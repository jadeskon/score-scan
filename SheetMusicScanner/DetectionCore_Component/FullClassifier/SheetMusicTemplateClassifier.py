#!/usr/bin/env python

"""
Der SheetMusicTemplateClassifier ist eine Realisierung des Interfaces IFullClassifier und erkannt anhand von
IClassifier die TemplateMatching betreiben eine IClassification im SheetMusic "format".
"""

from DetectionCore_Component.IFullClassifier import IFullClassifier
from State_Component.State.State import State
from DetectionCore_Component.Detector.NoteLineDetector import NoteLineDetector
from DetectionCore_Component.Detector.HorizontalLineRemoveDetector import HorizontalLineRemoveDetector
from DetectionCore_Component.Detector.TactDetector import TactDetector
from DetectionCore_Component.Detector.NoteDetector import NoteDetector
from DetectionCore_Component.ImageOptimizer.ImageFiller import ImageFiller
from DetectionCore_Component.ImageOptimizer.ImageResizer import ImageResizer
from DetectionCore_Component.ImageOptimizer.ObjectCentering import ObjectCentering
from DetectionCore_Component.Classifier.NoteHeightBlobClassifier import NoteHeightBlobClassifier
from DetectionCore_Component.Classifier.CnnNoteClassifier import CnnNoteClassifier
from DetectionCore_Component.Classification.SheetMusic import SheetMusic

from DetectionCore_Component.ClassificationUnit.Tact import Tact
from DetectionCore_Component.ClassificationUnit.Clef import Clef
from DetectionCore_Component.ClassificationUnit.TimeSignature import TimeSignature
from DetectionCore_Component.ClassificationUnit.KeySignatur import KeySignatur
from DetectionCore_Component.Classifier.TemplateMatcher.ClefTemplateClassifier import ClefTemplateClassifier
from DetectionCore_Component.Classifier.TemplateMatcher.TimeTemplateClassifier import TimeTemplateClassifier
from DetectionCore_Component.Classifier.TemplateMatcher.KeyTemplateClassifier import KeyTemplateClassifier

import cv2
import numpy as np
import os

__author__ = "Bonifaz Stuhr / Juergen Maier / Christian Dufter"
__version__ = "0.0.0"
__status__ = "Production"


class SheetMusicTemplateClassifier(IFullClassifier):
    def __init__(self, config):
        """
        Constructor, initialisiert Membervariablen.

        :param config:          Die Config für den SheetMusicClassifier
        """

        self.__logger = State().getLogger("DetectionCore_Component_Logger")
        self.__logger.info("Starting __init__()", "SheetMusicTemplateClassifier:__init__")
        self.__config = config

        lineRemoveConfig = self.__config["HorizontalLineRemoveDetector"]
        self.__horizontalLineRemoveDetector = HorizontalLineRemoveDetector \
            (indexOfProcessMat=lineRemoveConfig["indexOfProcessMat"],
             anchorPoint=(lineRemoveConfig["anchorPointX"], lineRemoveConfig["anchorPointY"]),
             kernelWidth=lineRemoveConfig["kernelWidth"],
             kernelHeight=lineRemoveConfig["kernelHeight"],
             morphOfKernel=getattr(cv2, lineRemoveConfig["morphOfKernel"]),
             showImagesInWindow=lineRemoveConfig["showImagesInWindow"])

        lineDetectorConfig = self.__config["NoteLineDetector"]
        self.__noteLineDetector = NoteLineDetector \
            (indexOfProcessMat=lineDetectorConfig["indexOfProcessMat"],
             maxGradeOfLinesInPx=lineDetectorConfig["maxGradeOfLinesInPx"],
             minDistanceToNextNoteRow=lineDetectorConfig["minDistanceToNextNoteRow"],
             marginTop=lineDetectorConfig["marginTop"],
             marginBottom=lineDetectorConfig["marginBottom"],
             cannyThreshold1=lineDetectorConfig["cannyThreshold1"],
             cannyThreshold2=lineDetectorConfig["cannyThreshold2"],
             cannyApertureSize=lineDetectorConfig["cannyApertureSize"],
             houghLinesRho=lineDetectorConfig["houghLinesRho"],
             houghLinesTheta=np.pi / 180 * lineDetectorConfig["houghLinesThetaInDegree"],
             houghLinesThreshold=lineDetectorConfig["houghLinesThreshold"],
             showImagesInWindow=lineDetectorConfig["showImagesInWindow"])

        tactDetectorConfig = self.__config["TactDetector"]
        self.__tactDetector = TactDetector \
            (indexOfProcessMat=tactDetectorConfig["indexOfProcessMat"],
             tactLineWidthMax=tactDetectorConfig["tactLineWidthMax"],
             tactLineHeightMin=tactDetectorConfig["tactLineHeightMin"],
             minWidthOfTactLine=tactDetectorConfig["minWidthOfTactLine"],
             findCountersMode=getattr(cv2, tactDetectorConfig["findCountersMode"]),
             findCountersMethode=getattr(cv2, tactDetectorConfig["findCountersMethode"]),
             showImagesInWindow=tactDetectorConfig["showImagesInWindow"])

        self.__clefClassifier = ClefTemplateClassifier(self.__config["ClefTemplateClassifier"])

        self.__timeClassifier = TimeTemplateClassifier(self.__config["TimeTemplateClassifier"])

        self.__keyClassifier = KeyTemplateClassifier(self.__config["KeyTemplateClassifier"])

        noteDetectorConfig = self.__config["NoteDetector"]
        self.__noteDetector = NoteDetector \
            (indexOfProcessMat=noteDetectorConfig["indexOfProcessMat"],
             minNoteWidth_WithStem=noteDetectorConfig["minNoteWidth_WithStem"],
             maxNoteWidth_WithStem=noteDetectorConfig["maxNoteWidth_WithStem"],
             minNoteHeight_WithStem=noteDetectorConfig["minNoteHeight_WithStem"],
             maxNoteHeight_WithStem=noteDetectorConfig["maxNoteHeight_WithStem"],
             minNoteWidth_WithoutStem=noteDetectorConfig["minNoteWidth_WithoutStem"],
             maxNoteWidth_WithoutStem=noteDetectorConfig["maxNoteWidth_WithoutStem"],
             minNoteHeight_WithoutStem=noteDetectorConfig["minNoteHeight_WithoutStem"],
             maxNoteHeight_WithoutStem=noteDetectorConfig["maxNoteHeight_WithoutStem"],
             noteImageWidth=noteDetectorConfig["noteImageWidth"],
             findCountersMode=getattr(cv2, noteDetectorConfig["findCountersMode"]),
             findCountersMethode=getattr(cv2, noteDetectorConfig["findCountersMethode"]),
             showImagesInWindow=noteDetectorConfig["showImagesInWindow"])

        # NoteHeightBlobClassifier wird nicht mehr benoetigt, da die
        # Notenhoehe von einem CNN klassifiziert wird.
        """
        noteDetectorConfig = self.__config["NoteDetector"]
        self.__noteHeightBlobClassifier = NoteHeightBlobClassifier \
            (indexOfProcessMatWithoutLines=noteDetectorConfig["indexOfProcessMatWithoutLines"],
             indexOfProcessMatWithLines=noteDetectorConfig["indexOfProcessMatWithLines"],
             maxGradeOfLinesInPx=noteDetectorConfig["maxGradeOfLinesInPx"],
             marginTop=noteDetectorConfig["marginTop"],
             marginBottom=noteDetectorConfig["marginBottom"],
             cannyThreshold1=noteDetectorConfig["cannyThreshold1"],
             cannyThreshold2=noteDetectorConfig["cannyThreshold2"],
             cannyApertureSize=noteDetectorConfig["cannyApertureSize"],
             houghLinesRho=noteDetectorConfig["houghLinesRho"],
             houghLinesTheta=np.pi / 180 * noteDetectorConfig["houghLinesThetaInDegree"],
             houghLinesThreshold=noteDetectorConfig["houghLinesThreshold"],
             showImagesInWindow=noteDetectorConfig["showImagesInWindow"])
        """

        fillerConfig = self.__config["ImageFiller"]
        self.__imageFiller = ImageFiller \
            (fillRows=fillerConfig["fillRows"],
             fillColumns=fillerConfig["fillColumns"],
             targetNumberOfRows=fillerConfig["targetNumberOfRows"],
             targetNumberOfColumns=fillerConfig["targetNumberOfColumns"],
             appendRowsTop=fillerConfig["appendRowsTop"],
             appendColumnsRight=fillerConfig["appendColumnsRight"],
             showImagesInWindow=fillerConfig["showImagesInWindow"])

        centeringConfig = self.__config["ObjectCentering"]
        self.__objectCentering = ObjectCentering \
            (indexOfProcessMat=centeringConfig["indexOfProcessMat"],
             targetNumberOfRows=centeringConfig["targetNumberOfRows"],
             targetNumberOfColumns=centeringConfig["targetNumberOfColumns"],
             useDeletingVerticalSpaces=centeringConfig["useDeletingVerticalSpaces"],
             useDeletingHorizontalSpaces=centeringConfig["useDeletingHorizontalSpaces"],
             findCountersMode=getattr(cv2, centeringConfig["findCountersMode"]),
             findCountersMethode=getattr(cv2, centeringConfig["findCountersMethode"]),
             colorOfBorder=centeringConfig["colorOfBorder"],
             showImagesInWindow=centeringConfig["showImagesInWindow"])

        resizerConfig = self.__config["ImageResizer"]
        self.__imageResizerForCnn = ImageResizer \
            (targetNumberOfRows=resizerConfig["targetNumberOfRows"],
             targetNumberOfColumns=resizerConfig["targetNumberOfColumns"],
             interpolation=getattr(cv2, resizerConfig["interpolation"]),
             showImagesInWindow=resizerConfig["showImagesInWindow"])

        dirname, _ = os.path.split(os.path.abspath(__file__))
        cnnConfig = self.__config["CnnNoteClassifier"]
        self.__cnnNoteClassifier = CnnNoteClassifier \
            (modelDir=dirname + cnnConfig["modelDir"],
             gdLearnRateForTypeModel=cnnConfig["gdLearnRateForTypeModel"],
             gdLearnRateForHightModel=cnnConfig["gdLearnRateForHightModel"],
             trainSteps=cnnConfig["trainSteps"],
             evalInterval=cnnConfig["evalInterval"],
             evalDataSize=cnnConfig["evalDataSize"],
             testDataSize=cnnConfig["testDataSize"],
             trainTypeModel = cnnConfig["trainTypeModel"],
             trainHightModel = cnnConfig["trainHightModel"])

        self.__logger.info("Finished __init__()", "SheetMusicTemplateClassifier:__init__")

    def executeClassification(self, mat):
        """
        Führt die Klassifizierung auf einer Bildmatrix aus und gibt die erkannte IClassification zurück.

        Parameters
        ----------
        mat : Die Bildmatrix auf welche die Klassifizierung ausgeführt werden soll.

        Returns
        -------
        classification : IClassification
        Aus dem Eingabematrix erkannte IClassification (z.B. Note, Slur, Rest).

        Example
        -------
        >>> sheetMusicTemplateClassifier.executeClassification(mat)
        """
        self.__logger.info("Starting executeClassification()", "SheetMusicTemplateClassifier:executeClassification")
        classification = SheetMusic()

        noteLinesWithoutHLines = self.__horizontalLineRemoveDetector.detect(mat)
        noteLines = self.__noteLineDetector.detect(noteLinesWithoutHLines)
        tacts = self.__tactDetector.detect(noteLines)

        # --- Takt Klassifikation ---
        elementCounter = 1
        lastClefLine = 0
        lastClefSign = ""

        # Führt für jeden erkannten Takt aus
        for i in range(0, len(tacts[0])):
            # self.__logger.debug("Analyzing Tact", image = tacts[0][i])

            tactInternalCounter = 1
            tactClassification = classification.creatTact(i + 1, elementCounter)  # Neuer Takt
            elementCounter += 1

            # ----- Clef -----
            clefClassification = tactClassification.creatClef(tactInternalCounter, elementCounter)

            if self.__clefClassifier.classify(clefClassification, [tacts[0][i], tacts[1][i], tacts[2][i]]):
                if (clefClassification.sign != lastClefSign or clefClassification.line != lastClefLine):
                    tactClassification.addClef(clefClassification)  # Füge Notenschlüssel zu Takt hinzu
                    elementCounter += 1
                    tactInternalCounter += 1
                    lastClefSign = clefClassification.sign
                    lastClefLine = clefClassification.line

            # ----- KeySignature -----
            keyClassification = tactClassification.creatKeySignature(tactInternalCounter, elementCounter)

            if self.__keyClassifier.classify(keyClassification, [tacts[0][i], tacts[1][i], tacts[2][i]]):
                tactClassification.addKeySignatur(keyClassification)  # Füge Tonhöheangabe zu Takt hinzu
                elementCounter += 1
                tactInternalCounter += 1

            # ----- Time -----
            timeClassification = tactClassification.creatTimeSignature(tactInternalCounter, elementCounter)

            if self.__timeClassifier.classify(timeClassification, [tacts[0][i], tacts[1][i], tacts[2][i]]):
                tactClassification.addTimeSignatur(timeClassification)  # Füge Rythmus zu Takt hinzu
                elementCounter += 1
                tactInternalCounter += 1

            classification.addTact(tactClassification)  # Füge Takt zur Klassifikation hinzu
        # --- Takt Klassifikation ---

        notes, noteCountPerTact = self.__noteDetector.detect(tacts)
        self.__logger.debug("Return from noteDetector 0", "SheetMusicTemplateClassifier::executeClassification",
                            notes[0][0])  # Ohne Linien
        self.__logger.debug("Return from noteDetector 1", "SheetMusicTemplateClassifier::executeClassification",
                            notes[1][0])  # Mit Linien

        filledNotes = self.__imageFiller.coreProcess(notes)
        centeredNotes = self.__objectCentering.coreProcess(filledNotes)
        cnnNotes = self.__imageResizerForCnn.coreProcess(centeredNotes)

        # notesHeight = self.__noteHeightBlobClassifier.classify(notes)
        # self.__logger.debug("Return from noteHeightBlobClassifier 0", "SheetMusicTemplateClassifier::executeClassification", notesHeight[0][0]) # Ohne Linien
        # self.__logger.debug("Return from noteHeightBlobClassifier 1", "SheetMusicTemplateClassifier::executeClassification", notesHeight[1][0]) # Mit Linien

        # ----- Classify Notes -----

        notes = self.__cnnNoteClassifier.classify(cnnNotes[0], cnnNotes[1])

        # Fülle die Takte mit den erkannten Noten und nutze zur Vermeidung von Fehlerfortpflanzung noteCountPerTact
        noteIndex = 0
        for t in range(0, len(noteCountPerTact)):
            for n in range(0, noteCountPerTact[t]):
                chord = classification.tacts[t].creatChord(classification.tacts[t].tactNumber, n)
                note = chord.creatNote(classification.tacts[t].tactNumber, n, chord.chordInternalNumber)
                note.pitch = notes[noteIndex].pitch
                note.type = notes[noteIndex].type
                chord.addNote(note)
                classification.tacts[t].addChord(chord)
                noteIndex += 1
                self.__logger.debug(("Tact " + str(t) + " added Note on pos " + str(n) + " type: " + note.type +
                                     " pitch: " + str(note.pitch)),
                                    "SheetMusicTemplateClassifier:executeClassification")

        self.__logger.info("Finished executeClassification()", "SheetMusicTemplateClassifier:executeClassification")
        return classification

    def buildTraindata(self, mat):
        """
        Interface Methode: Jeder FullClassifier muss diese realisieren.
        Erstellt Trainingdaten für das Trainieren seiner Classifier

        :param Bildmatrix : mat Die Bildmatrix aus welcher die Trainingdaten erstellt werden soll.
        :return: trainData : matArray Aus dem Eingabematrix erstellte Trainingdaten.
        """
        self.__logger.info("Starting buildTraindata()", "SheetMusicTemplateClassifier:buildTraindata")

        noteLinesWithoutHLines = self.__horizontalLineRemoveDetector.detect(mat)
        noteLines = self.__noteLineDetector.detect(noteLinesWithoutHLines)
        tacts = self.__tactDetector.detect(noteLines)
        notes, _ = self.__noteDetector.detect(tacts)

        self.__logger.debug("Return from noteDetector 0", "SheetMusicTemplateClassifier::buildTraindata",
                            notes[0][0])  # Ohne Linien
        self.__logger.debug("Return from noteDetector 1", "SheetMusicTemplateClassifier::buildTraindata",
                            notes[1][0])  # Mit Linien

        filledNotes = self.__imageFiller.coreProcess(notes)
        centeredNotes = self.__objectCentering.coreProcess(filledNotes)
        cnnNotes = self.__imageResizerForCnn.coreProcess(centeredNotes)

        self.__logger.info("Finished executeClassification()", "SheetMusicTemplateClassifier:buildTraindata")
        return cnnNotes

    def train(self, inputMatArray, lableArray):
        """
        Trainiert alle trainierbaren Classifier mit den gegebenen Trainingsdaten

        :param Bildmatrizen: inputMatArray Die Bildmatrizen für das Training.
        :param Lable: lableArray Die Lable zu den Bildmatrizen für das Training.
        :return: successful : boolean War das Training erfolgreich?
        """
        self.__logger.info("Started train()", "SheetMusicTemplateClassifier:train")

        self.__cnnNoteClassifier.train(inputMatArray, lableArray)

        self.__logger.info("Finished train()", "SheetMusicTemplateClassifier:train")
