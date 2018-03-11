__author__ = "Christian Dufter"
__version__ = "0.1.0"
__status__ = "Ready"

import datetime
import os
import cv2
import glob



class LogLevel():
    """
    Eine "Enum" Klasse zum setzen der LogLevel Flags.
    """
    DEBUG = 1
    INFO = 2
    WARNING = 4
    ERROR = 8
    ALL = 15

    Color = {1: "blue", 2: "black", 4: "orange", 8: "red"}
    String = {1: "DEBUG", 2: "INFO", 4: "WARNING", 8: "ERROR"}


class Logger:
    """
    Klasse zum Loggen von Meldungen.
    Meldungen, welche ein dem LogLevel entsprechen, werden in eine .log Datei geschrieben und auf der Konsole ausgegeben.

    :Attributes:
        __name          Der Name des Loggers und der Log-Datei die dieser beschreibt.
        __logLevel      Gibt an welche Nachrichten geloggt werden.
        __printLevel    Gibt an welche Nachrichten geloggt werden.
        __fileName      Name der Logdatei
        __folder        Relativer Pfad zur Log-Datei
        __mode          Schreibmodus
        __indexFile     Die Verbindung zur Log-Datei
        __counter       Für die Benennung der Bilder, damit keine zwei Bilder zur selben Zeit geschrieben werden.
        __saveImages    Flag ob Bilder gespeichert werden sollen
    """

    def __init__(self, name, folder="", append=False, logLevel=LogLevel.ALL, printLevel=LogLevel.ALL):
        """
        Konstruktor für einen Logger.

        :param name: Name des Loggers. Name des Unterverzeichnisses in dem die Logdateien liegen.
        :param folder: Relativer Pfad zum Logordner
        :param append: Bestimmt ob Logmeldungen an ein bestehendes File angehängt werden, oder das Logfile überschrieben wird.
        :param logLevel: Gibt an welche Meldungen ins Logfile geschrieben werden.
        :param printLevel: Gibt an welche Meldungen auf der Konsole ausgegeben werden.
        """
        self.__name = name
        self.__logLevel = logLevel
        self.__printLevel = printLevel
        self.__fileName = "index.html"
        self.__folder = name + "/"
        self.__mode = ""
        self.__counter = 0
        self.__saveImages = True

        if folder != "":
            self.__folder = folder + "/" + name + "/"

            if not os.path.exists(folder):
                os.mkdir(folder)

        if not os.path.exists(self.__folder):
            os.mkdir(self.__folder)

        if not os.path.exists(self.__folder + "images"):
            os.mkdir(self.__folder + "images")

        if (append):
            self.__mode = "a"
        else:
            self.__mode = "w"

            for image in glob.glob(self.__folder + "images/*.jpg"):
                os.remove(image)

        self.__indexFile = open(self.__folder + "/" + self.__fileName, self.__mode)

    def __del__(self):
        """
        Desktruktor
        Schließt den Link zur Logdatei.
        """
        self.__indexFile.close()

    def getName(self):
        """
        Getter für den Namen.

        :return: Der Name des Loggers.
        """
        return self.__name

    def setLogLevel(self, level):
        """
        Setter für das LogLevel.
        Bestimmt welche Level in die Logdatei geschrieben werden.

        :param level: Das LogLevel

        :example:
            logger.setLogLevel(LogLevel.DEBUG)
            logger.setLogLevel(LogLevel.DEBUG | LogLevel.INFO)
            logger.setLogLevel(LogLevel.DEBUG | LogLevel.WARNING | LogLevel.ERROR)
            logger.setLogLevel(LogLevel.ALL)
        """
        self.__logLevel = level

    def setPrintLevel(self, level):
        """
        Setter für das PrintLevel.
        Bestimmt welche Level auf der Kosole ausgegeben werden.

        :param level: Das PrintLevel

        :example:
            logger.setPrintLevel(LogLevel.DEBUG)
            logger.setPrintLevel(LogLevel.DEBUG | LogLevel.INFO)
            logger.setPrintLevel(LogLevel.DEBUG | LogLevel.WARNING | LogLevel.ERROR)
            logger.setPrintLevel(LogLevel.ALL)
        """
        self.__printLevel = level

    def saveImages(self, value):
        """
        Bestimmt ob Bilder gespeichert werden (True) oder nicht (False).

        :param value: Wert für das __saveImage Flag
        """
        self.__saveImages = value

    def debug(self, message, sender=None, image=None):
        """
        Logger für eine Debug-Nachricht.

        :param message: Die Nachricht.
        :param sender: Der Absender. [None] by default.
        :param image: Ein Bild, welches der Nachricht im Logfile angehängt wird. [None] by default.
        """
        if (LogLevel.DEBUG & self.__logLevel) > 0:
            self.__log(LogLevel.DEBUG, message, sender, image)

        if (LogLevel.DEBUG & self.__logLevel) > 0:
            self.__print(LogLevel.DEBUG, message, sender)

    def info(self, message, sender=None, image=None):
        """
        Logger für eine Info-Nachricht.

        :param message: Die Nachricht.
        :param sender: Der Absender. [None] by default.
        :param image: Ein Bild, welches der Nachricht im Logfile angehängt wird. [None] by default.
        """
        if (LogLevel.INFO & self.__logLevel) > 0:
            self.__log(LogLevel.INFO, message, sender, image)

        if (LogLevel.INFO & self.__logLevel) > 0:
            self.__print(LogLevel.INFO, message, sender)

    def warning(self, message, sender=None, image=None):
        """
        Logger für eine Warnung.

        :param message: Die Nachricht.
        :param sender: Der Absender. [None] by default.
        :param image: Ein Bild, welches der Nachricht im Logfile angehängt wird. [None] by default.
        """
        if (LogLevel.WARNING & self.__logLevel) > 0:
            self.__log(LogLevel.WARNING, message, sender, image)

        if (LogLevel.WARNING & self.__logLevel) > 0:
            self.__print(LogLevel.WARNING, message, sender)

    def error(self, message, sender=None, image=None):
        """
        Logger für eine Error-Nachricht.

        :param message: Die Nachricht.
        :param sender: Der Absender. [None] by default.
        :param image: Ein Bild, welches der Nachricht im Logfile angehängt wird. [None] by default.
        """
        if (LogLevel.ERROR & self.__logLevel) > 0:
            self.__log(LogLevel.ERROR, message, sender, image)

        if (LogLevel.ERROR & self.__logLevel) > 0:
            self.__print(LogLevel.ERROR, message, sender)

    def __log(self, level, message, sender, image):
        """
        Schreibt eine Nachricht in das Logfile.

        :param level: Das LogLevel der Nachricht.
        :param message: Die Nachricht.
        :param sender: Der Absender.
        :param image: Ein Bild, welches der Nachricht im Logfile angehängt wird.
        """
        if sender is None:
            sender = "UNDEFINED"

        output = "<font style='color: " + LogLevel.Color[
            level] + "; font-family: courier new; font-weight: bold'>" + datetime.datetime.now().strftime(
            "%Y-%m-%d_%H:%M:%S") + ": " + LogLevel.String[
                     level] + " from " + sender + ": '" + message + "'" + "</font><br>"

        if image is not None and self.__saveImages:
            img = "images/" + datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S-%f") + "_" + str(
                self.__counter) + ".jpg"
            self.__counter += 1
            cv2.imwrite(self.__folder + img, image)
            output += "<a href='" + img + "'><img style='max-width:300px;' src='" + img + "' /></a><br>"

        self.__indexFile.write(output + "<br>")

    def __print(self, level, message, sender):
        """
        Schreibt eine Nachricht auf die Konsole.

        :param level: Das LogLevel der Nachricht.
        :param message: Die Nachricht.
        :param sender: Der Absender.
        """
        if sender is None:
            sender = "UNDEFINED"

        print(self.__name + ": " + datetime.datetime.now().strftime("%Y-%m-%d_%H:%M:%S") + ": " + LogLevel.String[
            level] + " from " + sender + ": '" + message + "'")
