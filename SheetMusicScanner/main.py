#!/usr/bin/env python

"""
Entry File, welches die Main-Methode enthält.
"""

from PipeController_Component.PipeController.PipeController import PipeController

__author__ = "Bonifaz Stuhr"
__version__ = "0.0.0"
__status__ = "Production"



def main():
    """
    Main-Method. Initialisiert PipeController mit einem Config-Pfad und initialisiert damit alle gewünschten Komponenten.
    Führt darauffolgend die Klassifizierung aus.

    Parameters
    ----------
    Returns
    -------
    Example
    -------
    """
    """Hier kann der PipeController mit einer anderen Realisierung des IPipControlles ausgetauscht werden."""
    pipeController = PipeController("config.json")

    initOk = pipeController.init()
    """Todo: Do something if initOk == false"""
    executionOk = pipeController.execute()
    """Todo: Do something if executionOk == false"""

main()
