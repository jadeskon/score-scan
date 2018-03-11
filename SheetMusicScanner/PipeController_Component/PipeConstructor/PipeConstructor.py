#!/usr/bin/env python

"""
Der PipeConstructor ist eine Realisierung des Interfaces IPipeConstructor und dient zur Konstruierung der
Pipe für die Klassifizierung.
"""

from PipeController_Component.IPipeConstructor import IPipeConstructor
from Input_Component.Input.Input import Input
from Preprocessing_Component.Preprocessing.Preprocessing import Preprocessing
from DetectionCore_Component.DetectionCore.DetectionCore import DetectionCore
from Postprocessing_Component.Postprocessing.Postprocessing import Postprocessing
from Output_Component.Output.Output import Output
from State_Component.State.State import State

__author__  = "Bonifaz Stuhr"
__version__ = "0.0.0"
__status__ = "Production"


class PipeConstructor(IPipeConstructor):

    def __init__(self, config):
        """
        Constructor, initialisiert Membervariablen

        :param Config : config Die Konfiguration.
        :example:
            PipeConstructor(config)
        """
        self.__logger = State().getLogger("PipeController_Component_Logger")
        self.__logger.info("Starting __init__()", "PipeConstructor:__init__")
        self.__config = config
        self.__logger.info("Finished __init__()", "PipeConstructor:__init__")

    def constructPipe(self):
        """
        Konstruiert die Pipe für die Klassifizierung und gibt diese zurück.

        :return: successful : boolean
        :return: pipe : dictionary Die Pipe als <name,object> Paar.
        :example:
            pipeConstructor.constructPipe()
        """
        self.__logger.info("Starting to constructPipe()", "PipeConstructor:constructPipe")
        pipe = {
            "Input": Input(self.__config.getConfigForComponent("Input")),
            "Preprocessing": Preprocessing(self.__config.getConfigForComponent("Preprocessing")),
            "DetectionCore": DetectionCore(self.__config.getConfigForComponent("DetectionCore")),
            "Postprocessing": Postprocessing(self.__config.getConfigForComponent("Postprocessing")),
            "Output": Output(self.__config.getConfigForComponent("Output"))
        }
        self.__logger.info("Finished to constructPipe()", "PipeConstructor:constructPipe")
        return pipe

		
		