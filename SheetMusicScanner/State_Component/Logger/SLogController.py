__author__  = "Christian Dufter"
__version__ = "0.1.0"
__status__ = "Ready"

from State_Component.Logger.TSingleton import TSingleton
from State_Component.Logger.Logger import Logger
import os


class SLogController(metaclass=TSingleton):
    """
    Singletonklasse zur Verwaltung mehrerer Logger

    :Attrubutes:
        __logger    Liste aller registrierten Logger
        __folder    Standart Ordner in den die Log-Dateien angelegt werden
        __index     Pfad zum Index-file
        __file      Link zur Datei
    """

    def __init__(self):
        """
        Der Konstruktor für den LogController.
        Bestimmt den Speicherort für die Logdateien und erstellt eine Indexdatei in der alle registrierten Logger aufgelistet werden.
        """
        self.__logger = []
        self.__folder = "Logs"
        self.__index = self.__folder + "/index.html"
        self.__file = None

        if self.__folder != "":
            if not os.path.exists(self.__folder):
                os.mkdir(self.__folder)

        self.__file = open(self.__index, "w")
        self.__file.write("<h1 style='font-family: courier new; font-wight: bold;'>List of registered Loggers</h1>")

    def getLogger(self, name, append = False):
        """
        Getter für einen Logger.
        Gibt den Logger mit gegebenen Namen zurück oder erstellt einen neuen, falls noch nicht vorhanden.

        :param name: Der Name des Loggers.
        :param append: Bestimmt ob Logmeldungen an ein bereits bestehendes Logfile angehängt werden, oder das alte Logfile überschrieben wird. Gilt nur beim ersten Aufruf des Loggers. [False] by default.
        :return: Der Logger.
        """
        for log in self.__logger:
            if(log.getName() == name):
                break
        else:
            log = Logger(name, self.__folder, append)
            self.__logger.append(log)
            self.__file.write("<a style='font-family: courier new; font-wight: bold;' href='./" + name + "/index.html'>" + name + "</a><br>")

        return log
		
		
