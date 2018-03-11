#!/usr/bin/env python

"""
MidiOutput erzeugt eine MidiDatei
"""
from Output_Component.ISheetMusicOutput import ISheetMusicOutput
from DetectionCore_Component.Classification.SheetMusic import SheetMusic
from DetectionCore_Component.ClassificationUnit.Tact import Tact
from DetectionCore_Component.ClassificationUnit.DurationUnit.Note import Note
from DetectionCore_Component.ClassificationUnit.DurationUnit.Chord import Chord
from DetectionCore_Component.ClassificationUnit.Clef import Clef
from DetectionCore_Component.ClassificationUnit.KeySignatur import KeySignatur
from DetectionCore_Component.ClassificationUnit.DurationUnit.Rest import Rest
from DetectionCore_Component.ClassificationUnit.TimeSignature import TimeSignature
from Output_Component.SheetMusicOutput.midiutil.MidiFile import MIDIFile


__author__ = "Bernhard Rimkus"
__version__ = "0.1.0"
__status__ = "Ready"


class MidiOutput(ISheetMusicOutput):

    def __init__(self, outputPath = None , playmidi = True, miditempo = 640):
        if (outputPath == None):
            self.__outputPath = "output_midi.mid"
        else:
            self.__outputPath = outputPath

        self.__miditempo = miditempo
        self.__playmidi = playmidi
        self.__time = 0.0;
        #MUSS DANN GELÖSCHT WERDEN
        #self.__outputPath = "output_midi.mid"

       #pass

    def write(self, sheetMusic):
        """
        Interface Methode: Jeder SheetMusicOutput muss diese realisieren.
        Führt den entsprechenden Ausgabevorgang durch und erstellt ausgebene Datai.

        Parameters
        ----------
        sheetMusic: SheetMusic

        Returns
        -------
        successful : boolean
        War die Ausgabe erfolgreich?
        """

        ########Erstelle Test-SheetMusic
        #self.create_testdata()

        ########Ausgabe Test-SheetMusic
        #self.print_ausgabe_sheetMusic()

        #Übernehme eingehendes sheetMusic
        self.sheetMusic = sheetMusic;




        #Erstelle Midifile-Inhalts Datei mit 1 Spur
        midifile = MIDIFile(1,adjust_origin=True)

        #Schreibt Temmpo der Midifile
        midifile.addTempo(1,0,self.__miditempo)

        #Schreibe sheetMusic in die Erstellte MidiDatei
        self.write_part(midifile, self.sheetMusic.sheetMusicClassificationUnits, '1')

        #Erstelle Mididatei
        file_out_path = open("output_midi.mid", 'wb')
        midifile.writeFile(file_out_path)
        file_out_path.close()

        #Gibt die Midi-File mit Standardaudiowiedergabeprogramm wieder
        #############Bei Bedarf auskommentieren
        if (self.__playmidi):
            import os
            os.startfile('"output_midi.mid"')

        return None

#################################################################################
    #Schreiben einer Stimme in Midi
    def write_part(self, input_file, input_list, part_id):
        """
        Schreibt den Inhalt für eine Stimme.

        :param input_file:
        Die Midi-Datei in die geschrieben werden soll.
        :param input_list:
        Die Liste von sheetMusic, die aktuell bearbeitet wird
        :return:
        """

        #Startet die write-measure Funktion für jeweils einen Takt der input_list
        counter = 0
        while counter < len(input_list):
            self.write_measure(input_file, input_list[counter])
            counter += 1

    #Schreiben eines Taktes in Midi
    def write_measure(self, input_file, input_list):
        """
        Schreibt den Inhalt eines Taktes in die Midi-Datei.

        :param input_file:
        Die Midi-Datei in die geschrieben werden soll.
        :param input_list:
        Die Liste von sheetMusic, die aktuell bearbeitet wird
        :return:
        """

        #Startet für jedes Element der input_list, die jeweilige Write____ Funktion.
        counter = 0
        while counter < len(input_list.tactElements):
            if (type(input_list.tactElements[counter]) == Chord):
                self.write_note(input_file, input_list.tactElements[counter])
                counter += 1
            elif (type(input_list.tactElements[counter]) == Clef):
                counter +=1
            elif (type(input_list.tactElements[counter]) == KeySignatur):
                counter += 1
            elif (type(input_list.tactElements[counter]) == TimeSignature):
                counter += 1
            elif (type(input_list.tactElements[counter]) == Rest):
                self.write_rest(input_file, input_list.tactElements[counter])
                counter += 1

    #Schreiben einer Note in MusicXML
    def write_note(self, input_file, input_tupel):
        """
        Schreibt ein Chord-Element in das Midifile

        :param input_file:
        Die Midi-Datei in die geschrieben werden soll.
        :param input_tupel:
        Die Liste des jeweiligen Chord-Elements
        :return:
        """


        global time
        # print(time)
        counter = 0
        #Falls ein Chord-Element unterschiedlich Lange Noten besitzt, wird hier die Kürzeste Note verwendet
        temp_duration = 0.0

        #Durchläuft das Chord-Element für jedes Note-Element
        while counter < len(input_tupel.chordElements):
            # Liest aus dem .type der Note die .duration der Note
            if input_tupel.chordElements[counter].type == 'quarter':
                duration = 1.0
            elif input_tupel.chordElements[counter].type == 'half':
                duration = 2.0
            elif input_tupel.chordElements[counter].type == 'whole':
                duration = 4.0
            elif input_tupel.chordElements[counter].type == 'eighth':
                duration = 0.5
            elif input_tupel.chordElements[counter].type == '16th':
                duration = 0.25
            elif input_tupel.chordElements[counter].type == '32nd':
                duration = 0.125
            elif input_tupel.chordElements[counter].type == '64th':
                duration = 0.0625
            elif input_tupel.chordElements[counter].type == '128th':
                duration = 0.03125
            """Schreibt die eigentliche Note in das Midifile mit (  Nr. Track,
                                                                    Spur,
                                                                    Pitch der Note,
                                                                    Zeitpunkt  der Note,
                                                                    Länge der Note,
                                                                    Lautstärke der Note)
            """
            input_file.addNote(0,
                        0,
                        (12 + input_tupel.chordElements[counter].pitch["octave"] * 12 + self.rewrite(input_tupel.chordElements[counter])),
                        self.__time,
                        duration,
                        100)
            temp_duration = duration
            counter +=1
        #inkrementiert den Zeitpunkt des Liedes um die Länge des kürzesten Chord-Elements
        self.__time += float(temp_duration)

    def write_rest(self, input_file, input_tupel):
        """

        :param input_file:
        Die Midi-Datei in die geschrieben werden soll.
        :param input_tupel:
        Das Tupel des Rest-Elements
        :return:
        """

        # Liest aus dem .type der Pause die .duration der Pause
        if input_tupel.type == 'quarter':
            duration = 1.0
        elif input_tupel.type == 'half':
            duration = 2.0
        elif input_tupel.type == 'whole':
            duration = 4.0
        elif input_tupel.type == 'eighth':
            duration = 0.5
        elif input_tupel.type == '16th':
            duration = 0.25
        elif input_tupel.type == '32nd':
            duration = 0.125
        elif input_tupel.type == '64th':
            duration = 0.0625
        elif input_tupel.type == '128th':
            duration = 0.03125
        global time
        #Schreibt eine c Note in der 4ten Oktave mit Lautstärke 0(siehe write_note Zeile 170)
        input_file.addNote(0,
                    0,
                    60,
                    self.__time,
                    duration,
                    0)
        self.__time += float(duration)
################################################################################
    #Print Ausgabe
    def print_ausgabe_sheetMusic(self):
        print("\n")
        self.ausgabe_takt_element(0, 0,self.sheetMusic.sheetMusicClassificationUnits)
        self.ausgabe_takt_element(0, 1,self.sheetMusic.sheetMusicClassificationUnits)
        self.ausgabe_takt_element(0, 2,self.sheetMusic.sheetMusicClassificationUnits)
        self.ausgabe_takt_element(0, 3,self.sheetMusic.sheetMusicClassificationUnits)
        self.ausgabe_takt_element(1, 0,self.sheetMusic.sheetMusicClassificationUnits)
        self.ausgabe_takt_element(1, 1,self.sheetMusic.sheetMusicClassificationUnits)
        self.ausgabe_takt_element(2, 0,self.sheetMusic.sheetMusicClassificationUnits)
        self.ausgabe_takt_element(2, 1,self.sheetMusic.sheetMusicClassificationUnits)
        self.ausgabe_takt_element(2, 2,self.sheetMusic.sheetMusicClassificationUnits)
        self.ausgabe_takt_element(2, 3,self.sheetMusic.sheetMusicClassificationUnits)
    #Print Ausgabe eines Elements eines Taktes
    def ausgabe_takt_element(self, number_takt, number_element, liste):
        print("Ausgabe erstes TaktElement(Chord) : \t", liste[number_takt].tactElements[number_element].chordElements[0].pitch["step"])
        #print("Ausgabe erstes TaktElement(Chord) : \t", liste[number_takt].tactElements[number_element].chordElements[0].pitch["octave"])
        print("Ausgabe erstes TaktElement(Chord) : \t", liste[number_takt].tactElements[number_element].chordElements[0].duration)
#################################################################################
    #Funktionen um TestSheetMusic zu erstellen
    def create_testdata(self):
        # TEST_ERSTELLUNG alle meine Entchen
        self.sheetMusic = SheetMusic()

        # Erster Takt
        test_tact = Tact()


        test_tact.addChord(self.testing_add_Note("C", 4, 1.0,0.0))
        test_tact.addChord(self.testing_add_Note("D", 4, 1.0,0.0))
        test_tact.addChord(self.testing_add_Note("E", 4, 1.0,0.0))
        test_tact.addChord(self.testing_add_Note("F", 4, 1.0,0.0))
        test_tact.tactNumber = 1
        self.sheetMusic.addTact(test_tact)

        # Zweiter Takt
        test_tact_2 = Tact()
        test_clef = Clef()
        test_tact_2.addClef(test_clef)

        test_keysignatur = KeySignatur()
        test_keysignatur.fifths = 3
        test_tact_2.addKeySignatur(test_keysignatur)

        test_tact_2.addChord(self.testing_add_Note("G", 4, 2.0,0.0))
        test_tact_2.addChord(self.testing_add_Note("G", 4, 2.0,0.0))
        test_tact_2.tactNumber = 2
        self.sheetMusic.addTact(test_tact_2)

        # Dritter Takt
        test_tact_3 = Tact()
        test_tact_3.addChord(self.testing_add_Note("A", 4, 1.0,0.0))
        test_tact_3.addChord(self.testing_add_Note("A", 4, 1.0,0.0))
        test_tact_3.addChord(self.testing_add_Note("A", 4, 1.0,0.0))
        test_tact_3.addChord(self.testing_add_Note("A", 4, 1.0,0.0))
        test_tact_3.tactNumber = 3;
        self.sheetMusic.addTact(test_tact_3)

        # Dritter Takt
        test_tact_4 = Tact()
        test_tact_4.addChord(self.testing_add_Note("A", 4, 1.0,0.0))
        test_tact_4.addChord(self.testing_add_chord("A", 4, 1.0,0.0, "C", 5, 1.0,0.0))
        test_rest = Rest()
        test_rest.duration = 2
        test_tact_4.addRest(test_rest)
        test_tact_4.tactNumber = 4;
        self.sheetMusic.addTact(test_tact_4)

        testliste = []
        testliste.append(test_tact)
        testliste.append(test_tact_2)
        testliste.append(test_tact_3)
        testliste.append(test_tact_4)
        #print(len(testliste))
        #print("testliste ist :", type(testliste))
    #Hinzufügen einer Note zum TestSheetMusic
    def testing_add_Note(self, pitch, octave, duration, semitones):
        """Gibt die entsprechende Note als ein Chord-Element zurück"""
        test_chord = Chord()
        test_note = Note()
        test_note.duration = duration
        test_note.pitch["step"] = pitch
        test_note.pitch["octave"] = octave
        test_note.pitch["alter"] = semitones
        test_chord.addNote(test_note)
        return test_chord
    #Hinzufügen eines Chord-Elements mit zwei Noten
    def testing_add_chord(self, pitch, octave, duration, semitones, pitch2, octave2, duration2, semitones2):
        """Gibt die entsprechende Note als ein Chord-Element zurück"""
        test_chord = Chord()
        test_note = Note()
        test_note.duration = duration
        test_note.pitch["step"] = pitch
        test_note.pitch["octave"] = octave
        test_note.pitch["alter"] = semitones
        test_chord.addNote(test_note)
        test_note_2 = Note()
        test_note_2.duration = duration2
        test_note_2.pitch["step"] = pitch2
        test_note_2.pitch["octave"] = octave2
        test_note_2.pitch["alter"] = semitones2
        test_chord.addNote(test_note_2)
        return test_chord
#################################################################################
    #Notenwert umschreiben, sodass es mit der addNote Funktion des midiutils verwendet werden kann
    def rewrite(self, input_tupel):
        """

        :param input_tupel:
        Das Tupel der zu bearbeitenden Note
        :return: compare_value:
        Gibt den benötigten int Wert zurück
        """

        #Schreibt den Wert für die jeweilge Note
        if (input_tupel.pitch["step"] == 'C'):
            compare_value = 0
        #elif (string_input.pitch["step"] == 'CIS'):
            #compare_value = 1
        elif (input_tupel.pitch["step"] == 'D'):
            compare_value = 2
        #elif (string_input.pitch["step"] == 'DIS'):
            #compare_value = 3
        elif (input_tupel.pitch["step"] == 'E'):
            compare_value = 4
        elif (input_tupel.pitch["step"] == 'F'):
            compare_value = 5
        #elif (string_input.pitch["step"] == 'FIS'):
            #compare_value = 6
        elif (input_tupel.pitch["step"] == 'G'):
            compare_value = 7
        #elif (string_input.pitch["step"] == 'GIS'):
            #compare_value = 8
        elif (input_tupel.pitch["step"] == 'A'):
            compare_value = 9
        #elif (string_input.pitch["step"] == 'AS'):
            #compare_value = 10
        elif (input_tupel.pitch["step"] == 'B'):
            compare_value = 11

        #Modifiziert den Wert bei dem jeweiligen Vorzeichen
        if (input_tupel.pitch["alter"] == 1.0):
            compare_value += 1
        elif (input_tupel.pitch["alter"] == -1.0):
            compare_value -= 1
        return compare_value

