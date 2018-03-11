#!/usr/bin/env python

"""
Der PipeController ist eine Realisierung des Interfaces IPipeController und dient zur Steuerung des
Hauptprogrammablaufes (der Klassifizierungs-Pipe).
"""

from PipeController_Component.IPipeController import IPipeController
from PipeController_Component.PipeConstructor.PipeConstructor import PipeConstructor
from ConfigInput_Component.ConfigInput.ConfigInput import ConfigInput
from State_Component.State.State import State

__author__  = "Bonifaz Stuhr"
__version__ = "0.0.0"
__status__ = "Production"


class PipeController(IPipeController):

    def __init__(self, configFilePath):
        """
        Constructor, initialisiert Membervariablen

        :param configFilePath : string Pfad zum Configurations-File
        :example:
            PipeController("my/path/to/a/config/File")
        """
        print("PipeController: Starting __init__()")

        self.__configFilePath = configFilePath
        self.__config = 0;
        self.__controllerConfig = 0;
        self.__pipe = 0;
        self.__pipeConstructor = 0
        self.__configInput = 0;
        self.__state = 0;

        print("PipeController: Finished __init__()")

    def init(self):
        """
        Baut mithilfe eines PipeContructors, die Pipe zur Klassifizierung auf.

        :return: successful : boolean Initialisierung erfolgreich?
        :example:
            pipeController.init()
        """
        print("PipeController: Starting init() components with Config" + self.__configFilePath)

        """Hier kann der ConfigInput mit einer anderen Realisierung des IConfigInput ausgetauscht werden."""
        self.__configInput = ConfigInput(self.__configFilePath)
        self.__config = self.__configInput.execute()
        self.__controllerConfig = self.__config.getConfigForComponent("PipeController")
        """Todo: Check if Config ok """

        """Hier kann der ConfigInput mit einer anderen Realisierung des IConfigInput ausgetauscht werden."""
        self.__state = State()
        self.__state.init(self.__config.getConfigForComponent("State"))
        self.__logger = State().getLogger("PipeController_Component_Logger")

        """Todo: Check if init ok """

        """Hier kann der PipeConstructor mit einer anderen Realisierung des IPipeConstructors ausgetauscht werden."""
        self.__pipeConstructor = PipeConstructor(self.__config)
        self.__pipe = self.__pipeConstructor.constructPipe()
        """Todo: Check if pipe ok """

        self.__logger.info("Finished init() components with Config-Path: " + self.__configFilePath, "PipeController:init")
        return True

    def execute(self):
        """
        Führt die Befehle über die Pipe aus und steuert diese.

        :return: successful : boolean War die Klassifizierung erfolgreich?
        :example:
            pipeController.execute()
        """
        self.__logger.info("Starting execute()", "PipeController:execute")

        if self.__controllerConfig["executeBuildTraindata"]:
            outPutOk = self.executeBuildTraindata()

        if self.__controllerConfig["executeTrain"]:
            outPutOk = self.executeTrain()

        if self.__controllerConfig["executeClassification"]:
            outPutOk = self.executeClassification()

        self.__logger.info("Finished execute()", "PipeController:execute")
        return outPutOk

    def executeClassification(self):
        """
        Führt die Klassifizierung über die Pipe aus und steuert diese.

        :return: successful : boolean War die Klassifizierung erfolgreich?
        :example:
            pipeController.executeClassification()
        """
        self.__logger.info("Starting executeClassification()", "PipeController:executeClassification")

        inputMat = self.__pipe["Input"].execute()
        preprocessingMats = self.__pipe["Preprocessing"].execute(inputMat)
        classification = self.__pipe["DetectionCore"].execute(preprocessingMats)
        postProcessedClassification = self.__pipe["Postprocessing"].execute(classification)
        outPutOk = self.__pipe["Output"].execute(postProcessedClassification)

        self.__logger.info("Finished executeClassification()", "PipeController:executeClassification")
        return outPutOk


    def executeBuildTraindata(self):
        """
        Erstellt ein Trainingsdatenset über die Pipe und speichert diese.

        :return: successful : boolean War der Aufbau erfolgreich?
        :example:
            pipeController.executeBuildTraindata()
        """
        self.__logger.info("Starting executeBuildTraindate()", "PipeController:executeBuildTraindate")

        while True:
            inputMat, lable = self.__pipe["Input"].readNextImgXMLPair()
            if inputMat is None:
                break
            if lable is not None:
                preprocessingMats = self.__pipe["Preprocessing"].execute(inputMat)
                trainMats = self.__pipe["DetectionCore"].buildNextTraindata(preprocessingMats)
                self.__pipe["Output"].writeNextTraindata(trainMats, lable)
        self.__logger.info("Finished executeBuildTraindate()", "PipeController:executeBuildTraindate")
        return True


    def executeTrain(self):
        """
        Führt das Training der Classifier im DetectionCore über die Pipe aus.
        :return: successful : boolean War dir Aufbau erfolgreich?
        :example:
            pipeController.executeTrain()
        """
        self.__logger.info("Starting executeTrain()", "PipeController:executeTrain")

        inputMatArray, lableArray = self.__pipe["Input"].readNoteTrainData()

        self.__pipe["DetectionCore"].executeTrain(inputMatArray, lableArray)

        self.__logger.info("Finished executeTrain()", "PipeController:executeTrain")
        return True