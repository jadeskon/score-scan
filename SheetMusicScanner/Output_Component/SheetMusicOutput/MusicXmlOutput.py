#!/usr/bin/env python

"""
MusicXMLOutput erzeugt eine MusicXML Datei
"""
from Output_Component.ISheetMusicOutput import ISheetMusicOutput
from State_Component.State.State import State
from DetectionCore_Component.Classification.SheetMusic import SheetMusic
from DetectionCore_Component.ClassificationUnit.Tact import Tact
from DetectionCore_Component.ClassificationUnit.DurationUnit.Note import Note
from DetectionCore_Component.ClassificationUnit.DurationUnit.Chord import Chord
from DetectionCore_Component.ClassificationUnit.Clef import Clef
from DetectionCore_Component.ClassificationUnit.KeySignatur import KeySignatur
from DetectionCore_Component.ClassificationUnit.DurationUnit.Rest import Rest
from DetectionCore_Component.ClassificationUnit.TimeSignature import TimeSignature
from xml.dom import minidom

__author__ = "Bernhard Rimkus"
__version__ = "0.1.0"
__status__ = "Ready"


class MusicXmlOutput(ISheetMusicOutput):

    def __init__(self, outputPath = None , fillwithrests = True):
        if (outputPath == None):
            self.__outputPath = "output_musicxml.xml"
        else:
            self.__outputPath = outputPath

        self.compare_lenght = 0.0
        self.__fillwithrests = fillwithrests
        self.__logger = State().getLogger("Output_Component_Logger")
        #MUSS DANN GELÖSCHT WERDEN
        #self.__outputPath = "output_mxml.xml"

       #pass

    def write(self, sheetMusic):
        """
        Interface Methode: Jeder SheetMusicOutput muss diese realisieren.
        Führt den entsprechenden Ausgabevorgang durch und erstellt ausgebene Datau.

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


        # Öffnet neues XML-Dokument und füllt den Header der Datei
        temp = minidom.DOMImplementation()
        doctype = temp.createDocumentType('score-partwise', "-//Recordare//DTD MusicXML 3.0 Partwise//EN",
                                          "http://www.musicxml.org/dtds/partwise.dtd")
        self.__doc = temp.createDocument(None, 'score-partwise', doctype)

        #Erstellt root-Element der XML-Datei
        root = self.__doc.documentElement

        #Schreibt Headerinformationen in das root-Element
        self.write_header(root)

        #Schreibt die part-list in das root-Element
        self.write_part_list(root)

        # Schreibt den erzeugten stream in das Xml-Dokument
        xml_str = self.__doc.toprettyxml(indent="  ")
        with open(self.__outputPath, "w") as f:
        #with open("output_mxml.xml", "w") as f:

            f.write(xml_str)

        return None

#################################################################################
    #Schreiben von Standard-Header mit Seitenformatierung etc.
    def write_header(self, input_root):
        """
        <work>
            <work-title>Title</work-title>
        </work>
        <identification>
            <encoding>
                <software>Score Scanner 1.0</software>
                <encoding-date>2017-12-13</encoding-date>
            </encoding>
        </identification>
        <defaults>
            <scaling>
                <millimeters>7.05556</millimeters>
                <tenths>40</tenths>
            </scaling>
            <page-layout>
                <page-height>1683.78</page-height>
                <page-width>1190.55</page-width>
                <page-margins type="even">
                    <left-margin>56.6929</left-margin>
                    <right-margin>56.6929</right-margin>
                    <top-margin>56.6929</top-margin>
                    <bottom-margin>113.386</bottom-margin>
                </page-margins>
                <page-margins type="odd">
                    <left-margin>56.6929</left-margin>
                    <right-margin>56.6929</right-margin>
                    <top-margin>56.6929</top-margin>
                    <bottom-margin>113.386</bottom-margin>
                </page-margins>
            </page-layout>
        </defaults>

        :param input_root:
        Das root-Element der XML-Datei
        :return:
        """

        work = self.__doc.createElement('work')
        work_title = self.__doc.createElement('work-title')
        work_title_text = self.__doc.createTextNode('ScoreScan 1.0 SheetMusic MusicXML')
        work_title.appendChild(work_title_text)
        work.appendChild(work_title)
        input_root.appendChild(work)

        identification = self.__doc.createElement('identification')
        encoding = self.__doc.createElement('encoding')
        identification.appendChild(encoding)
        software = self.__doc.createElement('software')

        software_text = self.__doc.createTextNode('Score Scanner 1.0')
        software.appendChild(software_text)
        encoding.appendChild(software)
        input_root.appendChild(identification)

        import datetime as dt
        encoding_date = self.__doc.createElement('encoding-date')
        encoding_date_text = self.__doc.createTextNode(str(dt.date.today()))
        encoding_date.appendChild(encoding_date_text)
        encoding.appendChild(encoding_date)

        defaults = self.__doc.createElement('defaults')
        scaling = self.__doc.createElement('scaling')
        defaults.appendChild(scaling)
        millimeters = self.__doc.createElement('millimeters')
        millimeters_text = self.__doc.createTextNode('7.05556')
        millimeters.appendChild(millimeters_text)
        scaling.appendChild(millimeters)
        tenths = self.__doc.createElement('tenths')
        tenths_text = self.__doc.createTextNode('40')
        tenths.appendChild(tenths_text)
        scaling.appendChild(tenths)
        input_root.appendChild(defaults)

        page_layout = self.__doc.createElement('page-layout')
        defaults.appendChild(page_layout)
        page_height = self.__doc.createElement('page-height')
        page_height_text = self.__doc.createTextNode('1683.78')
        page_height.appendChild(page_height_text)
        page_layout.appendChild(page_height)

        page_width = self.__doc.createElement('page-width')
        page_width_text = self.__doc.createTextNode('1190.55')
        page_width.appendChild(page_width_text)
        page_layout.appendChild(page_width)

        page_margins = self.__doc.createElement('page-margins')
        page_margins.setAttribute('type','even')
        page_layout.appendChild(page_margins)

        left_margin = self.__doc.createElement('left-margin')
        left_margin_text = self.__doc.createTextNode('56.6929')
        left_margin.appendChild(left_margin_text)
        page_margins.appendChild(left_margin)

        right_margin = self.__doc.createElement('right-margin')
        right_margin_text = self.__doc.createTextNode('56.6929')
        right_margin.appendChild(right_margin_text)
        page_margins.appendChild(right_margin)

        top_margin = self.__doc.createElement('top-margin')
        top_margin_text = self.__doc.createTextNode('56.6929')
        top_margin.appendChild(top_margin_text)
        page_margins.appendChild(top_margin)

        bottom_margin = self.__doc.createElement('bottom-margin')
        bottom_margin_text = self.__doc.createTextNode('113.386')
        bottom_margin.appendChild(bottom_margin_text)
        page_margins.appendChild(bottom_margin)

        page_margins_2 = self.__doc.createElement('page-margins')
        page_margins_2.setAttribute('type', 'odd')
        left_margin_2 = self.__doc.createElement('left-margin')
        left_margin_2_text = self.__doc.createTextNode('56.6929')
        left_margin_2.appendChild(left_margin_2_text)
        page_margins_2.appendChild(left_margin_2)
        right_margin_2 = self.__doc.createElement('right-margin')
        right_margin_2_text = self.__doc.createTextNode('56.6929')
        right_margin_2.appendChild(right_margin_2_text)
        page_margins_2.appendChild(right_margin_2)
        top_margin_2 = self.__doc.createElement('top-margin')
        top_margin_2_text = self.__doc.createTextNode('56.6929')
        top_margin_2.appendChild(top_margin_2_text)
        page_margins_2.appendChild(top_margin_2)
        bottom_margin_2 = self.__doc.createElement('bottom-margin')
        bottom_margin_2_text = self.__doc.createTextNode('113.386')
        bottom_margin_2.appendChild(bottom_margin_2_text)
        page_margins_2.appendChild(bottom_margin_2)
        page_layout.appendChild(page_margins_2)

    #Schreiben der part-list in MusicXML
    def write_part_list(self, input_root):
        """Gibt die part-list wieder und ruft hierfür für jeden Part die f_newpart() Funktion auf
          <part-list>
            ...
          </part-list>
          ...

        :param input_root:
        Das root-Element der XML-Datei
        :return:
        """

        part_list = self.__doc.createElement('part-list')
        input_root.appendChild(part_list)

        self.write_newpart(part_list, 'P1')
        #self.write_newpart(part_list, 'P2')

        self.write_part(input_root, self.sheetMusic.sheetMusicClassificationUnits, 'P1')
        #write_part(root, list2, 'P2')

    #Schreiben eines parts innerhalb der part-list in MusicXML
    def write_newpart(self, input_part_list, input_part_id):
        """Erstellt innerhalb des "part-list" Elements einen neuen Part
            <score-part id="P1">
              <part-name>Music</part-name>
            </score-part>

        :param input_part_list:
        Das XML Part-list-Element in das die zu erzeugenden Elemente geschrieben werden sollen.
        :param input_part_id:
        Die ID der Stimme
        :return:
        """

        score_part = self.__doc.createElement('score-part')
        score_part.setAttribute('id', str(input_part_id))
        input_part_list.appendChild(score_part)

        part_name = self.__doc.createElement('part-name')
        part_name_text = self.__doc.createTextNode('Music')
        part_name.appendChild(part_name_text)
        score_part.appendChild(part_name)

    #Schreiben einer Stimme in MusicXML
    def write_part(self, input_root, input_list, input_part_id):
        """Gibt den eigentlichen Part wieder, wobei ein Part eine einzelne "Stimme" ist
        <part id="P1">
        ...
        </part>

        :param input_root:
        Das root-Element der XML-Datei
        :param input_list:
        Die Liste mit den Takten von sheetMusic
        :param input_part_id:
        Die ID der Stimme
        :return:
        """

        part = self.__doc.createElement('part')
        part.setAttribute('id', str(input_part_id))
        counter = 0
        #Startet für jeden Takt die write_measure Funktion
        while (counter < (len(input_list))):
            self.write_measure(part, input_list[counter], counter)
            counter += 1
            input_root.appendChild(part)

    #Schreiben eines Taktes in MusicXML
    def write_measure(self, input_part, input_tact, input_measure_counter):
        """Gibt den jeweiligen Takt wieder
           <measure number="1">
           ...
           </measure>

        :param input_part:
        Das XML Part-Element in das die zu erzeugenden Elemente geschrieben werden sollen.
        :param input_tact:
        Der Takt der in XML geschrieben werden soll.
        :param input_measure_counter:
        Die ID des Taktes
        :return:
        """

        """ """
        measure = self.__doc.createElement('measure')
        measure.setAttribute('number', str(input_measure_counter + 1))
        counter = 0
        #if measure_counter == 0:
            #self.write_clef(measure, list1)
        #Durchläuft die Liste tactElements und startet die jeweilige write Funktion

        ausgabe = 0.0
        while counter < len(input_tact.tactElements):
            if (type(input_tact.tactElements[counter]) == Chord):
                ausgabe += self.write_chord(measure, input_tact.tactElements[counter])

            elif (type(input_tact.tactElements[counter]) == Clef):
                self.write_clef(measure, input_tact.tactElements[counter])
            elif (type(input_tact.tactElements[counter]) == KeySignatur):
                self.write_key_signatur(measure, input_tact.tactElements[counter])
            elif (type(input_tact.tactElements[counter]) == TimeSignature):
                self.write_timeSignature(measure, input_tact.tactElements[counter])

                #schreibt Vergleichstaktlänge zur überprüfung
                self.compare_lenght = input_tact.tactElements[counter].beats * (4/input_tact.tactElements[counter].beatType)
            elif (type(input_tact.tactElements[counter]) == Rest):
                self.write_rest(measure, input_tact.tactElements[counter])
            counter += 1
            input_part.appendChild(measure)
        #if (input_measure_counter == 0):
            #TODO: bei korrekter erkennung der Taktangabe -1 entfernen
            #self.compare_lenght = (ausgabe-1.0)
        #outputmessage = str("Takt Nr.: ", (input_measure_counter + 1), " ist ", ausgabe, " lang")
        #self.__logger.info("Takt Nr.: " + str(input_measure_counter + 1) + " ist " + str(ausgabe) + " lang", "Output:MusicXML execute")
        #überprüfung der taktlänge mit solltaktlänge
        if((self.compare_lenght != ausgabe) & (self.compare_lenght != 0.0)):

            if((self.compare_lenght > ausgabe) & self.__fillwithrests):
                #test_rest = Rest()
                test_rest = input_tact.creatRest( input_measure_counter, (len(input_tact.tactElements)+1))
                test_rest.duration = (self.compare_lenght - ausgabe)

                #füllen mit pausen bei zu kurzen takten
                self.write_rest(measure, test_rest)
                self.__logger.info("Takt Nr.: " + str(input_measure_counter + 1) +
                                   " hat Abweichung!  (Soll:" + str(self.compare_lenght) + "/Ist:" + str(ausgabe) +
                                   ") und wurde mit Pause aufgefüllt",
                                   "Output:MusicXML execute")

            else:
                self.__logger.info("Takt Nr.: " + str(input_measure_counter + 1) +
                                   " hat Abweichung!  (Soll:" + str(self.compare_lenght) + "/Ist:" + str(ausgabe),
                                   "Output:MusicXML execute")
        #print("Takt Nr.: ", (input_measure_counter+1), " ist ", ausgabe, " Lang")

    #Schreiben eines Schlüssels in MusicXML
    def write_clef(self, input_measure, input_clef):
        """Gibt einen Notenschllüssel
        z.B. Violinschlüssel
             <attributes>
                <clef>
                  <sign>G</sign>
                  <line>2</line>
                </clef>
              </attributes>

        :param input_measure:
        Das XML Element in das geschrieben werden soll
        :param input_clef:
        Das Clef Element, das erzeugt werden soll
        :return:
        """

        attributes = self.__doc.createElement('attributes')
        input_measure.appendChild(attributes)

        #divisions = self.__doc.createElement('divisions')
        #divisions_text = self.__doc.createTextNode('1')
        #divisions.appendChild(divisions_text)
        #attributes.appendChild(divisions)

        clef = self.__doc.createElement('clef')
        attributes.appendChild(clef)

        sign = self.__doc.createElement('sign')
        sign_text = self.__doc.createTextNode(input_clef.sign)
        sign.appendChild(sign_text)
        clef.appendChild(sign)

        line = self.__doc.createElement('line')
        line_text = self.__doc.createTextNode(str(input_clef.line))
        line.appendChild(line_text)
        clef.appendChild(line)

    #Schreiben einer Note in MusicXML
    def write_chord(self, input_measure, input_list):
        """Gibt ein einzelnes Chord-Element wieder, dass in der Regel eine Note enthält
        z.B. ein C in der vierten Oktave mit länge einer Viertel Note
              <note>
                <pitch>
                  <step>C</step>
                  <alter>0.0</alter>
                  <octave>4</octave>
                </pitch>
                <duration>1</duration>
                <type>quarter</type>
              </note>

        :param input_measure:
        Das XML Element in das geschrieben werden soll
        :param input_list:
        Die Liste des Chord-Elements, welches die Note Elemente enthält
        :return:
        """

        min_chord_duration = 0.0
        counter = 0
        #Durchläuft jede Note der Liste des Chord-Elements
        while counter < len(input_list.chordElements):
            note = self.__doc.createElement('note')
            input_measure.appendChild(note)

            if counter >= 1:
                chord = self.__doc.createElement('chord')
                note.appendChild(chord)

            pitch = self.__doc.createElement('pitch')
            note.appendChild(pitch)

            step = self.__doc.createElement('step')
            step_text = self.__doc.createTextNode(str(input_list.chordElements[counter].pitch["step"]))
            step.appendChild(step_text)
            pitch.appendChild(step)

            alter = self.__doc.createElement('alter')
            alter_text = self.__doc.createTextNode(str(input_list.chordElements[counter].pitch["alter"]))
            alter.appendChild(alter_text)
            pitch.appendChild(alter)

            octave = self.__doc.createElement('octave')
            octave_text = self.__doc.createTextNode(str(input_list.chordElements[counter].pitch["octave"]))
            octave.appendChild(octave_text)
            pitch.appendChild(octave)


            temp_float = 0.0
            duration = self.__doc.createElement('duration')

            if (input_list.chordElements[counter].duration == "0.0"):
                # Liest aus .type   -> .duration
                if input_list.chordElements[counter].type == 'quarter':
                    duration_text = self.__doc.createTextNode(str(1.0))
                    temp_float = 1.0
                elif input_list.chordElements[counter].type == 'half':
                    duration_text = self.__doc.createTextNode(str(2.0))
                    temp_float = 2.0
                elif input_list.chordElements[counter].type == 'whole':
                    duration_text = self.__doc.createTextNode(str(4.0))
                    temp_float = 4.0
                elif input_list.chordElements[counter].type == 'eighth':
                    duration_text = self.__doc.createTextNode(str(0.5))
                    temp_float = 0.5
                elif input_list.chordElements[counter].type == '16th':
                    duration_text = self.__doc.createTextNode(str(0.25))
                    temp_float = 0.25
                elif input_list.chordElements[counter].type == '32nd':
                    duration_text = self.__doc.createTextNode(str(0.125))
                    temp_float = 0.125
                elif input_list.chordElements[counter].type == '64th':
                    duration_text = self.__doc.createTextNode(str(0.0625))
                    temp_float = 0.0625
                elif input_list.chordElements[counter].type == '128th':
                    duration_text = self.__doc.createTextNode(str(0.03125))
                    temp_float = 0.03125
            else:
                duration_text = self.__doc.createTextNode(str(input_list.chordElements[counter].duration))
                temp_float = float(input_list.chordElements[counter].duration)


            duration.appendChild(duration_text)
            note.appendChild(duration)



            type = self.__doc.createElement('type')

            if input_list.chordElements[counter].type != "":
                type_text = self.__doc.createTextNode(input_list.chordElements[counter].type)

            # Liest aus .duration   -> .type
            elif input_list.chordElements[counter].duration == 1.0:
                type_text = self.__doc.createTextNode('quarter')
            elif input_list.chordElements[counter].duration == 2.0:
                type_text = self.__doc.createTextNode('half')
            elif input_list.chordElements[counter].duration == 4.0:
                type_text = self.__doc.createTextNode('whole')
            elif input_list.chordElements[counter].duration == 0.5:
                type_text = self.__doc.createTextNode('eighth')
            elif input_list.chordElements[counter].duration == 0.25:
                type_text = self.__doc.createTextNode('16th')
            elif input_list.chordElements[counter].duration == 0.125:
                type_text = self.__doc.createTextNode('32nd')
            elif input_list.chordElements[counter].duration == 0.0625:
                type_text = self.__doc.createTextNode('64th')
            elif input_list.chordElements[counter].duration == 0.03125:
                type_text = self.__doc.createTextNode('128th')

            type.appendChild(type_text)
            note.appendChild(type)


            if ((min_chord_duration == 0.0) or (min_chord_duration > input_list.chordElements[counter].duration)):
                #if (float(input_list.chordElements[counter].duration) == 0.0):
                    min_chord_duration = temp_float
                #else:
                #    min_chord_duration = float(input_list.chordElements[counter].duration)

            counter += 1
        return float(min_chord_duration)

    #Schreiben eines KeySignature in MusicXML
    def write_key_signatur(self, input_measure, input_key_signature):
        """ Erzeugt ein KeySignature Element in XML.
            Also die Vorzeichen der jeweiligen Tonart, z.B. fifths = 0  --> C-Dur
           <attributes>
                <key>
                    <fifths>0</fifths>
                </key>
            </attributes>

        :param input_measure:
        Das XML Element in das geschrieben werden soll
        :param input_key_signature:
        Das KeySignature Element von sheetMusic, zu dem ein jeweiliges XML Element erzeugt werden soll
        :return:
        """
        attributes = self.__doc.createElement('attributes')
        input_measure.appendChild(attributes)

        key = self.__doc.createElement('key')
        attributes.appendChild(key)

        fifths = self.__doc.createElement('fifths')
        fifths_text = self.__doc.createTextNode(str(input_key_signature.fifths))
        fifths.appendChild(fifths_text)
        key.appendChild(fifths)

    #Schreiben einer TimeSignature in MusicXML
    def write_timeSignature(self, input_measure, input_timesignature):
        """Schreibt das XML TimeSignature Element, welches den Taktart angiebt, z.B. 4/4 Takt mit beats = 4 und beat-type = 4
             <attributes>
                    <time>
                        <beats>4</beats>
                        <beat-type>4</beat-type>
                    </time>
                </attributes>

        :param input_measure:
        Das XML Element in das geschrieben werden soll
        :param input_timesignature:
        Das TimeSignature Element aus sheetMusic, zu dem das jeweilige XML Gegenstück erzeugt werden soll
        :return:
        """
        """"""
        attributes = self.__doc.createElement('attributes')
        input_measure.appendChild(attributes)

        time = self.__doc.createElement('time')
        attributes.appendChild(time)

        beats = self.__doc.createElement('beats')
        beats_text = self.__doc.createTextNode(str(input_timesignature.beats))
        beats.appendChild(beats_text)
        time.appendChild(beats)

        beat_type = self.__doc.createElement('beat-type')
        beat_type_text = self.__doc.createTextNode(str(input_timesignature.beatType))
        beat_type.appendChild(beat_type_text)
        time.appendChild(beat_type)

    #Schreiben einer Pause in MusicXML
    def write_rest(self, input_measure, input_rest):
        """Schreibt eine Pause in XML
            <note>
                </rest>
                <duration>2.0</duration>
            </note>

        :param input_measure:
        Das XML Element in das geschrieben werden soll
        :param input_rest:
        Das Rest Element von sheetMusic, zu dem ein XML Element erzeugt werden soll
        :return:
        """
        note = self.__doc.createElement('note')
        input_measure.appendChild(note)

        rest = self.__doc.createElement('rest')
        note.appendChild(rest)

        duration = self.__doc.createElement('duration')
        duration_text = self.__doc.createTextNode(str(input_rest.duration))
        duration.appendChild(duration_text)
        note.appendChild(duration)

        type = self.__doc.createElement('type')
        # Liest aus .duration   -> .type
        if input_rest.duration == 1.0:
            type_text = self.__doc.createTextNode('quarter')
        elif input_rest.duration == 2.0:
            type_text = self.__doc.createTextNode('half')
        elif input_rest.duration == 4.0:
            type_text = self.__doc.createTextNode('whole')
        elif input_rest.duration == 0.5:
               type_text = self.__doc.createTextNode('eighth')
        elif input_rest.duration == 0.25:
            type_text = self.__doc.createTextNode('16th')
        elif input_rest.duration == 0.125:
            type_text = self.__doc.createTextNode('32nd')
        elif input_rest.duration == 0.0625:
            type_text = self.__doc.createTextNode('64th')
        elif input_rest.duration == 0.03125:
            type_text = self.__doc.createTextNode('128th')
        else:
            type_text = self.__doc.createTextNode('half')

        type.appendChild(type_text)
        note.appendChild(type)



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
    #Hinzufügen eines Chord-Elements mit zwei Noten zum TestSheetMusic
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
