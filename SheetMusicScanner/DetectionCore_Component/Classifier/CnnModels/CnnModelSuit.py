#!/usr/bin/env python
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

"""
Ein CnnModelSuit benutzt ein Cnn (eine cnnModelFn) und eine Funktion um den Output-Vector des Cnns zu interpretieren.
Er dient dazu um Funktionen wie trian, eval und classify bzw. predict auf das Cnn anzuwenden, die Ergebnisse zu speichern,
zu loggen und für das TensorBoard zugänglich zu machen.
"""

from State_Component.State.State import State

import tensorflow as tf

__author__  = "Bonifaz Stuhr"
__version__ = "0.0.0"
__status__ = "Production"

class CnnModelSuit:

    def __init__(self, cnnModelFn, preditcionToClassificationFn, modelDir = "/tmp/cnn_model", learnRate = 0.001):
        """
        Constructor, initialisiert Membervariablen.

        :param cnnModelFn : function Ein CnnModel mit den Methoden train, predict, evaluate.
        :param predictedClassesToClassificationFn : function Eine Funktion um die Klassifizierung der cnnModelFn zu interpretieren,
        :param modelDir : string Pfad unter welchem das trainierte CnnModel gespeichert wird.
        :example:
            CnnModelSuit(cnnNotetypeModel, predictedClassesToNotetypeClassificationFn, "my/path/to/a/model/Dir")
        """
        # Set model params
        modelParams = {"learning_rate": learnRate}

        #Setting up the Loggers
        tf.logging.set_verbosity(tf.logging.INFO)
        self.__logger = State().getLogger("DetectionCore_Component_Logger")

        #The Function to interprete the Classification Vector
        self.preditcionToClassificationFn = preditcionToClassificationFn

        #The Cnn to be trained and to classify the inputs
        self.__cnnClassifier = tf.estimator.Estimator(
            model_fn=cnnModelFn, model_dir=modelDir, params=modelParams)

        # Set up logging for predictions
        # Log the values in the "Softmax" tensor with label "probabilities"
        self.__tensorsToLog = {"probabilities": "softmax_tensor"}
        self.__loggingHook = tf.train.LoggingTensorHook(
            tensors=self.__tensorsToLog, every_n_iter=50)

    def classify(self, inputData):
        """
        Bereitet die Inputdaten für das neuronale Netz vor und klassifiziert mit diesem den Input.

        :param inputData : Eine Mat welche den zu klassifizierenden Input enthält.
        :return: predictedClass : Die Klassifizierung welche durch die predictedClassesToClassificationFn bestimmt wird.
        :example:
            cnnModelSuit.classify(myInputData)
        """
        self.__logger.info("Starting classify()", "CnnModelSuit:classify")

        #Classify Input with the trained model
        predictInputFn = tf.estimator.inputs.numpy_input_fn(
            x={"x": inputData},
            num_epochs=1,
            shuffle=False)

        predictions = list(self.__cnnClassifier.predict(input_fn=predictInputFn))

        self.__logger.info("Finished classify()", "CnnModelSuit:classify")

        return self.preditcionToClassificationFn(predictions)

    def train(self, trainData, trainLabels, steps):
        """
        Bereitet die Inputdaten für das neuronale Netz vor und trainiert dieses mit den Daten.

        :param trainData : Eine Array von Mats welche traineirt werden sollen.
        :param trainLabels : Eine Array von Labels für die Mats von trainData (Gleiche Länge gleiche Sortierung)
        :param steps : Anzahl der Trainingsschritte
        :example:
            cnnNoteClassifier.train(myTrainData, myInputTrainLables)
        """
        self.__logger.info("Starting train()", "CnnModelSuit:train")

        #Train the model
        trainInputFn = tf.estimator.inputs.numpy_input_fn(
            x={"x": trainData},
            y=trainLabels,
            batch_size=100,
            num_epochs=None,
            shuffle=True)

        self.__cnnClassifier.train(
            input_fn=trainInputFn,
            steps=steps,
            hooks=[self.__loggingHook])

        self.__logger.info("Finished train()", "CnnModelSuit:train")

    def eval(self, evalData, evalLabels):
        """
        Bereitet die Inputdaten für das neuronale Netz vor und evaluiert dieses mit den Daten.

        :param evalData : Eine Array von Mats mit welchen evaluiert werden sollen.
        :param evalLabels : Eine Array von Labels für die Mats von evalData (Gleiche Länge gleiche Sortierung)
        :example:
            cnnNoteClassifier.eval(myEvalData, myEvalLabels)
        """
        self.__logger.info("Starting eval()", "CnnModelSuit:eval")

        #Evaluate the model and print results
        evalInputFn = tf.estimator.inputs.numpy_input_fn(
            x={"x": evalData},
            y=evalLabels,
            num_epochs=1,
            shuffle=False)
        evalResults = self.__cnnClassifier.evaluate(input_fn=evalInputFn)

        self.__logger.info("Finished eval()", "CnnModelSuit:eval")

