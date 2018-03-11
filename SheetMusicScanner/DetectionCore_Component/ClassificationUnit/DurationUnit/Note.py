#!/usr/bin/env python

from DetectionCore_Component.ClassificationUnit.ADurationUnit import ADurationUnit


__author__  = "Tobias Eigler"
__version__ = "0.0.0"
__status__ = "Production"


"""
Datenstruktur fuer Noten

"""
class Note(ADurationUnit):

    def __init__(self):
        self.__duration = "0.0"                                         # Länge/Dauer der Einheit
        self.__tactInternalNumber = 0                                   # Nummer der Note im Takt, in der sich die Note befindet.
        self.__tactNumber = 0                                           # Nummer des Taktes zu der die Note gehört
        self.__types = ["breve", "whole", "half", "quarter",            # https://usermanuals.musicxml.com/MusicXML/Content/EL-MusicXML-type.htm
                        "eighth", "16th", "32nd", "64th", "128th" ]     # Mögliche notentypen welche unterstützt werden
        self.__type = ""                                                # Ausgewählte note
        self.__elementNumber = 0                                        # Nummer im gesamten SheetMusic
        self.__recognitionPercentage = 0                                # noch nicht verwendet
        self.__chordInternalNumber = 0                                  # Nummer der Noten im Akkord.
        self.__voice = 1                                                # gibt die Stimme an. 1 = 1. Stimme usw: A voice is a sequence of musical events (e.g. notes, chords, rests) that proceeds linearly in time. The voice element is used to distinguish between multiple voices (what MuseData calls tracks) in individual parts. It is defined within a group due to its multiple uses within the MusicXML schema.
        self.__partOfChordCheck = 0                                          #  Bool!! 0= False 1= trueAngabe ob sie diese Note aus musikalischer sicht in einem Akkord befindet.
        __step = "C"
        __semitones = 0.0
        __octave = 4
        self.__pitch = {"step": __step,                             # The step type represents a step of the diatonic scale, represented using the English letters A through G.
                      "alter": __semitones,                         # The alter element represents chromatic alteration in number of semitones (e.g., -1 for flat, 1 for sharp). Decimal values like 0.5 (quarter tone sharp) are used for microtones. The octave element is represented by the numbers 0 to 9, where 4 indicates the octave started by middle C.  In the first example below, notice an accidental element is used for the third note, rather than the alter element, because the pitch is not altered from the the pitch designated to that staff position by the key signature.
                      "octave": __octave}                           # Octaves are represented by the numbers 0 to 9, where 4 indicates the octave started by middle C.

        self.__stems = ["up", "down", "none", "double"]             #Stems can be down, up, none, or double. For down and up stems, the position attributes can be used to specify stem length. The relative values specify the end of the stem relative to the program default. Default values specify an absolute end stem position. Negative values of relative-y that would flip a stem instead of shortening it are ignored. A stem element associated with a rest refers to a stemlet
        self.__stem = ""                                            # Ausgewählter stam, für diese Note
        __stemDefault_x = 0
        __stemDefault_y = 0
        __stemRelative_x = 0
        __stemRelative_y = 0
        self.__stemAttributes = {"default_x": __stemDefault_x,      # Stems can be down, up, none, or double. For down and up stems, the position attributes can be used to specify stem length.
                                "default_y": __stemDefault_y,       # The relative values specify the end of the stem relative to the program default. Default values specify an absolute end stem position.
                                "relative_x": __stemRelative_x,     # Negative values of relative-y that would flip a stem instead of shortening it are ignored. A stem element associated with a rest refers to a stemlet.
                                "relative_y": __stemRelative_y}


        self.__default_x = 0
        self.__default_y = 0
        self.__relative_x = 0
        self.__relative_y = 0



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
    def chordInternalNumber(self):
        return self.__chordInternalNumber

    @chordInternalNumber.setter
    def chordInternalNumber(self, chordInternalNumber):
        self.__chordInternalNumber = chordInternalNumber


    @property
    def voice(self):
        return self.__voice

    @voice.setter
    def voice(self, voice):
        self.__voice = voice


    @property
    def pitch(self):
        return self.__pitch

    @pitch.setter
    def pitch(self, pitch):
        self.__pitch = pitch

    @property
    def stems(self):
        return self.__stems


    @property
    def stem(self):
        return self.__stem

    @stem.setter
    def stem(self, stem):
        self.__stem = stem


    @property
    def stemAttributes(self):
        return self.__stemAttributes

    @stemAttributes.setter
    def stemAttributes(self, stemAttributes):
        self.__stemAttributes = stemAttributes


    @property
    def default_x(self):
        return self.__default_x

    @default_x.setter
    def default_x(self, default_x):
        self.__default_x = default_x


    @property
    def default_y(self):
        return self.__default_y

    @default_y.setter
    def default_y(self, default_y):
        self.__default_y = default_y


    @property
    def relative_x(self):
        return self.__relative_x

    @relative_x.setter
    def relative_x(self, relative_x):
        self.__relative_x = relative_x


    @property
    def relative_y(self):
        return self.__relative_y

    @relative_y.setter
    def relative_y(self, relative_y):
        self.__relative_y = relative_y