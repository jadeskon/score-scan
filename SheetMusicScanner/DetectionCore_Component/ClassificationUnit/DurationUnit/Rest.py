#!/usr/bin/env python

from DetectionCore_Component.ClassificationUnit.ADurationUnit import ADurationUnit


__author__  = "Tobias Eigler"
__version__ = "0.0.0"
__status__ = "Production"


"""
Datenstruktur fuer Pausen

"""
class Rest(ADurationUnit):


    def __init__(self):
        self.__duration = 0                                             # Länge/Dauer der Einheit
        self.__tactInternalNumber = 0                                   # Nummer der Note im Takt, in der sich die Note befindet.
        self.__tactNumber = 0                                           # Nummer des Taktes zu der die Note gehört
        self.__types = ["breve", "whole", "half", "quarter",            # https://usermanuals.musicxml.com/MusicXML/Content/EL-MusicXML-type.htm
                        "eighth", "16th", "32nd", "64th", "128th" ]     # Mögliche notentypen welche unterstützt werden
        self.__type = ""                                                # Ausgewählte note
        self.__elementNumber = 0                                        # Nummer im gesamten SheetMusic
        self.__recognitionPercentage = 0
        self.__voice = 1                                                # gibt die Stimme an. 1 = 1. Stimme usw: A voice is a sequence of musical events (e.g. notes, chords, rests) that proceeds linearly in time. The voice element is used to distinguish between multiple voices (what MuseData calls tracks) in individual parts. It is defined within a group due to its multiple uses within the MusicXML schema.
        self.__measure = False                                          # Gibt an ob die Pause den Ganzen Takt ausfüllt.

        @property
        def duration(self):
            return self.__duration

        @duration.setter
        def duration(self, duration):
            self.__duration = duration

        @property
        def tactInternalNumber(self):
            return self.__tactInternalNumber

        @tactInternalNumber.setter
        def tactInternalNumber(self, tactInternalNumber):
            self.__tactInternalNumber = tactInternalNumber

        @property
        def tactNumber(self):
            return self.__tactNumber

        @tactNumber.setter
        def tactNumber(self, tactNumber):
            self.__tactNumber = tactNumber

        @property
        def types(self):
            return self.__types

        @property
        def type(self):
            return self.__type

        @type.setter
        def type(self, type):
            self.__type = type

        @property
        def type(self):
            return self.__type

        @type.setter
        def type(self, type):
            self.__type = type

        @property
        def elementNumber(self):
            return self.__elementNumber

        @elementNumber.setter
        def elementNumber(self, elementNumber):
            self.__elementNumber = elementNumber

        @property
        def voice(self):
            return self.__voice

        @voice.setter
        def voice(self, voice):
            self.__voice = voice


        @property
        def measure(self):
            return self.__measure

        @measure.setter
        def measure(self, measure):
            self.__measure = measure



			
			


