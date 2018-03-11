#!/usr/bin/env python

"""
To-Do:
Bitte Kommentar bzw. Dokumentaion erstellen!
"""

from DetectionCore_Component.IClassifier import IClassifier
from State_Component.State.State import State
import numpy as np
from operator import itemgetter
import cv2

__author__  = "Juergen Maier"
__version__ = "0.0.0"
__status__ = "Production"


class NoteHeightBlobClassifier(IClassifier):

    def __init__(self,
                 indexOfProcessMatWithoutLines=0,
                 indexOfProcessMatWithLines=1,
                 maxGradeOfLinesInPx=2,
                 marginTop=0.5,
                 marginBottom=0.5,
                 cannyThreshold1=50,
                 cannyThreshold2=150,
                 cannyApertureSize=3,
                 houghLinesRho=1,
                 houghLinesTheta=np.pi / 180,
                 houghLinesThreshold=5,
                 showImagesInWindow=False):
        """
        To-Do:
        Bitte Kommentar bzw. Dokumentaion erstellen!
        """
        self.__logger = State().getLogger("DetectionCore_Component_Logger")
        self.__logger.info("Starting __init__()", "NoteHeightBlobClassifier:__init__")

        self.__indexOfProcessMatWithoutLines = indexOfProcessMatWithoutLines
        self.__indexOfProcessMatWithLines = indexOfProcessMatWithLines
        self.__firstLineHeight = 0
        self.__stepHeight = 0
        self.__maxGradeOfLinesInPx = maxGradeOfLinesInPx
        self.__marginTop = marginTop
        self.__marginBottom = marginBottom
        self.__cannyThreshold1 = cannyThreshold1
        self.__cannyThreshold2 = cannyThreshold2
        self.__cannyApertureSize = cannyApertureSize
        self.__houghLinesRho = houghLinesRho
        self.__houghLinesTheta = houghLinesTheta
        self.__houghLinesThreshold = houghLinesThreshold
        self.__showImagesInWindow = showImagesInWindow

        self.__logger.info("Finsihed __init__()", "NoteHeightBlobClassifier:__init__")

    def classify(self, matArray):
        """
        To-Do:
        Bitte Kommentar bzw. Dokumentaion erstellen!
        """
        self.__logger.info("Starting classify()", "NoteHeightBlobClassifier:classify")

        # Iterate about every note
        for i in range(0, len(matArray[self.__indexOfProcessMatWithoutLines])):

            imageWithLines = matArray[self.__indexOfProcessMatWithLines][i]

            cv2.imshow("Mit Linien", imageWithLines)

            # Apply edge detector canny
            edges = cv2.Canny(imageWithLines,
                              threshold1=self.__cannyThreshold1,
                              threshold2=self.__cannyThreshold2,
                              apertureSize=self.__cannyApertureSize)

            # Apply hough line detection
            lines = cv2.HoughLines(edges,
                                   rho=self.__houghLinesRho,
                                   theta=self.__houghLinesTheta,
                                   threshold=self.__houghLinesThreshold)

            # Extract array of hough line coordinates
            lines_coordinates = []
            for x in range(0, len(lines)):
                for rho, theta in lines[x]:

                    # Calculation of line coordinates
                    a = np.cos(theta)
                    b = np.sin(theta)
                    y0 = b * rho
                    y1 = int(y0 + 1000 * (a))
                    y2 = int(y0 - 1000 * (a))

                    # Extract horizontal lines
                    if (abs(y1 - y2) <= self.__maxGradeOfLinesInPx):
                        lines_coordinates.append([y1, y2])

                        print([y1, y2])

            # Sort coordinates of hough line
            lines_coordinates.sort(key=itemgetter(0))

            #
            yPositionFirsLine = ( ((lines_coordinates[0][0] + lines_coordinates[0][1]) / 2) + ((lines_coordinates[1][0] + lines_coordinates[1][1]) / 2) )/ 2
            yPositionLastLine = (((lines_coordinates[len(lines_coordinates) - 1][0] + lines_coordinates[len(lines_coordinates) - 1][1]) / 2) + (
            (lines_coordinates[len(lines_coordinates) - 2][0] + lines_coordinates[len(lines_coordinates) - 2][1]) / 2)) / 2

            # Berechne die Anzahl der Pixel von einer Notenhoehe zur naechsten Notenhoehe
            numberOfLines = 5
            noteStep = (yPositionFirsLine + yPositionLastLine) / (numberOfLines - 1) / 2



            # Draw hough lines to image
            showMat = cv2.cvtColor(src=matArray[self.__indexOfProcessMatWithoutLines][i],
                                   code=cv2.COLOR_GRAY2BGR)


            # Create array for mats and line groups
            noteLineCoordinates = []
            line_groupe = []
            lineThickness = 1
            lineColor = (0, 255, 0)

            for j in range(0, len(lines_coordinates) - 1):
                """
                Get line coordinates of line
                """
                line = lines_coordinates[j]

                """
                Draw line
                """
                cv2.line(showMat, (0, line[0]), (showMat.shape[1] - 1, line[1]), lineColor, lineThickness)


            # Read image
            imageWithoutLines = matArray[self.__indexOfProcessMatWithoutLines][i]
            imageWithoutLines = 255 - imageWithoutLines;
            #cv2.waitKey(0)
            cv2.imshow("Test1", imageWithoutLines)
            #cv2.waitKey(0)
            imageWithoutLines = 255 - cv2.dilate(imageWithoutLines, np.ones((1, 10)), iterations=1)
            cv2.imshow("Test2", imageWithoutLines)
            imageWithoutLines = cv2.dilate(imageWithoutLines, np.ones((1,16)), iterations=1)
            cv2.imshow("Test3", imageWithoutLines)
            cv2.waitKey(0)


            # Setup SimpleBlobDetector parameters.
            params = cv2.SimpleBlobDetector_Params()

            # Change thresholds
            # params.minThreshold = 0
            # params.maxThreshold = 255


            # Filter by Area.
            params.filterByArea = True
            params.minArea = 20
            # params.maxArea = 500000

            # Filter by Color
            # params.filterByColor = True
            # params.blobColor = 0

            # Filter by Circularity
            # params.filterByCircularity = False
            # params.minCircularity = 0.0

            # Filter by Convexity
            params.filterByConvexity = False
            # params.minConvexity = 0.87

            # Filter by Inertia
            # params.filterByInertia = False
            # params.minInertiaRatio = 0.01

            # Create a detector with the parameters
            detector = cv2.SimpleBlobDetector_create(params)

            # Detect blobs.
            keypoints = detector.detect(imageWithoutLines)

            if(not(len(keypoints) < 1)):

                # Draw detected blobs as red circles.
                # cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS ensures
                # the size of the circle corresponds to the size of blob

                im_with_keypoints = cv2.drawKeypoints(imageWithoutLines, keypoints, np.array([]), (0, 0, 255),
                                                      cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)

                print("Row", imageWithoutLines.shape[0])
                print("Column", imageWithoutLines.shape[1])
                for point in keypoints:
                    print("x=", point.pt[0], "y=", point.pt[1])
                    cv2.circle(showMat, (int(point.pt[0]), int(point.pt[1])), 1, (0, 255, 255), 3)



                difference = yPositionFirsLine - keypoints[0].pt[1]

                note_nr = round(difference / noteStep * 2,0)

                txt = ""
                if (note_nr == 0):
                    txt = "f''" + str(note_nr)
                elif (note_nr == -1):
                    txt = "e''" + str(note_nr)
                elif (note_nr == -2):
                    txt = "d''" + str(note_nr)
                elif (note_nr == -3):
                    txt = "c''" + str(note_nr)
                elif (note_nr == -4):
                    txt = "h'" + str(note_nr)
                elif (note_nr == -5):
                    txt = "a'" + str(note_nr)
                elif (note_nr == -6):
                    txt = "g'" + str(note_nr)
                elif (note_nr == -7):
                    txt = "f'" + str(note_nr)
                elif (note_nr == -8):
                    txt = "e'" + str(note_nr)
                elif (note_nr == -9):
                    txt = "d'" + str(note_nr)
                else:
                    txt = "-" + str(note_nr)




                #cv2.addText(showMat, str(note_nr), (5, 5), font, 4, (243, 127, 53), 2, cv2.LINE_AA)
                cv2.putText(showMat, txt, (0, 75), cv2.FONT_HERSHEY_SIMPLEX, 0.35, 255)

                # Show blobs
                cv2.imshow("Keypoints", im_with_keypoints)
                cv2.imshow("ShowMat", showMat)
                cv2.waitKey(0)


        #return tactMatsNoLines, tactMatsLines