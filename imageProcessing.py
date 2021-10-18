import cv2
import dlib
import os
import numpy as np
from Ewg2MajorProject.AutomaticFacialEnhancementAndBeautification.App.utils.facialFeatures import FacialFeatures
from Ewg2MajorProject.AutomaticFacialEnhancementAndBeautification.App.utils.openCVUtils import OpenCVUtils



# This class handles face and landmark detection, Delaunay triangulation and user input.

class ImageProcessing(object):

    def __init__(self):

        self.cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

        self.windowName = "Before"
        self.trackBarWindowName = "Settings"

        def nothing(nothing):
            pass

        self.detector = dlib.get_frontal_face_detector()
        self.predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

        self.triangles = np.array([])
        self.indices = []

        # values used for debugging purposes
        # self.rectangle = False
        # self.points = False
        # self.triangleEdges = False

        # create window for trackbars
        settings = np.zeros((10, 100), np.uint8)
        cv2.imshow(self.trackBarWindowName, settings)

        ImageProcessing.createTrackbars(self,nothing)

    def createTrackbars(self, nothing):
        # create trackbars for each functionality
        cv2.createTrackbar("Eyes size", self.trackBarWindowName, 10, 20, nothing)
        cv2.createTrackbar("Nose size", self.trackBarWindowName, 10, 20, nothing)
        cv2.createTrackbar("Mouth size", self.trackBarWindowName, 10, 20, nothing)
        cv2.createTrackbar("Jaw size", self.trackBarWindowName, 10, 20, nothing)
        cv2.createTrackbar("Eyes hor", self.trackBarWindowName, 10, 20, nothing)
        cv2.createTrackbar("Nose hor", self.trackBarWindowName, 10, 20, nothing)
        cv2.createTrackbar("Mouth hor", self.trackBarWindowName, 10, 20, nothing)
        cv2.createTrackbar("Brows hor", self.trackBarWindowName, 10, 20, nothing)
        cv2.createTrackbar("Light", self.trackBarWindowName, 50, 100, nothing)

    def updateData(self):

        global landmarkCopy, triangle_indices, vertices_coordinates, triangle_points

        # get image from the camera and prepare for processing
        ret, frame = self.cap.read()
        frame = cv2.resize(frame, None, None, fx=0.8, fy=0.8)

        grayFrame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        grayFrame = cv2.flip(grayFrame, 1)
        frame = cv2.flip(frame, 1)

        # Get trackbar values
        browsH, eyesH, eyesS, jawS, light, mouthH, mouthS, noseH, noseS = self.getTrackbarValues()

        # get list of facial landmarks from the current frame
        landmarks = OpenCVUtils.getFaceLandmarks(grayFrame, self.detector, self.predictor)

        # keep looking until a face is recognised
        while landmarks is None:
            ret, frame = self.cap.read()
            frame = cv2.resize(frame, None, None, fx=0.8, fy=0.8)
            grayFrame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            grayFrame = cv2.flip(grayFrame, 1)
            frame = cv2.flip(frame, 1)

            landmarks = OpenCVUtils.getFaceLandmarks(grayFrame, self.detector, self.predictor)

        if landmarks is not None:
            for landmark in landmarks:  # in every frame

                # create copy of the recognised landmarks to apply position changes
                landmarkCopy = landmark.copy()

                # update the landmarks position based on trackbars valuesn
                landmarkCopy = FacialFeatures.resizeEyes(eyesS, landmarkCopy)
                landmarkCopy = FacialFeatures.resizeMouth(mouthS, landmarkCopy)
                landmarkCopy = FacialFeatures.resizeNose(noseS, landmarkCopy)
                landmarkCopy = FacialFeatures.resizeJaw(jawS, landmarkCopy)
                landmarkCopy = FacialFeatures.moveEyesHorizontal(eyesH, landmarkCopy)
                landmarkCopy = FacialFeatures.moveNoseHorizontal(noseH, landmarkCopy)
                landmarkCopy = FacialFeatures.moveMouthHorizontal(mouthH, landmarkCopy)
                landmarkCopy = FacialFeatures.moveBrowsHorizontal(browsH, landmarkCopy)

                frame = FacialFeatures.changeBrightness(frame, light)

                # Delaunay triangulation - performed once after running the programme
                if self.triangles.size == 0:
                    self.triangles = OpenCVUtils.getTriangles(landmark)

                # match triangle points to landmarks
                triangle_points = OpenCVUtils.getTrianglesPointsWithLandmarks(self.triangles, landmark)

                # list of landmarks that create triangles
                triangle_indices = np.array(triangle_points)
                triangle_indices = triangle_indices.flatten()
                triangle_indices = list(triangle_indices)

                # x and y coordinates for all the landmarks
                vertices_coordinates = np.array(landmark)

                # this section has been commented out as it is no use for the user
                # it allows to see whether the face, landmarks and triangulation was done by drawing
                # # draw triangles based on landmark points
                # if self.triangleEdges:
                #     OpenCVUtils.drawTrianglesWithLandmarks(frame, landmark, triangle_points)
                # # press 'r' to draw rectangle
                # if self.rectangle:
                #     OpenCVUtils.drawFaceRectangle(frame, self.detector)
                #
                # # press 'p' to draw landmark points
                # if self.points:
                #     # utils.drawPoints(frame, landmark, (0, 255, 0))
                #     OpenCVUtils.drawPoints(frame, landmarkCopy, (0, 255, 0))

        # save current frame to form a texture
        # !!! Change the path to the absolute path of the img.jpg, as it will differ on all devices
        path = os.path.abspath(os.path.expanduser(os.path.expandvars("images/img.jpg")))
        path = '/'.join(path.split('\\'))
        cv2.imwrite(path, frame)

        # display current frame
        cv2.imshow(self.windowName, frame)

        # this section has been commented out as it is no use for the user
        # it allows turning on and off the drawing functions
        # them on the video
        # key = cv2.waitKey(1)
        #
        # if key == ord("r"):
        #     self.rectangle = not self.rectangle
        # if key == ord("p"):
        #     self.points = not self.points
        # if key == ord("t"):
        #     self.triangleEdges = not self.triangleEdges

        # change vertices position into OpenGL coordinate system
        vertices = OpenCVUtils.pointsToOpenGL(frame, landmarkCopy,
                                              vertices_coordinates)
        vertices = np.array(vertices, dtype=np.float32)

        self.indices = triangle_indices
        self.indices = np.array(self.indices, dtype=np.uint32)

        data = np.array(vertices, dtype="float32").flatten()

        return data

    def getTrackbarValues(self):
        eyesS = cv2.getTrackbarPos("Eyes size", self.trackBarWindowName)
        noseS = cv2.getTrackbarPos("Nose size", self.trackBarWindowName)
        mouthS = cv2.getTrackbarPos("Mouth size", self.trackBarWindowName)
        jawS = cv2.getTrackbarPos("Jaw size", self.trackBarWindowName)
        eyesH = cv2.getTrackbarPos("Eyes hor", self.trackBarWindowName)
        noseH = cv2.getTrackbarPos("Nose hor", self.trackBarWindowName)
        mouthH = cv2.getTrackbarPos("Mouth hor", self.trackBarWindowName)
        browsH = cv2.getTrackbarPos("Brows hor", self.trackBarWindowName)
        light = cv2.getTrackbarPos("Light", self.trackBarWindowName)
        return browsH, eyesH, eyesS, jawS, light, mouthH, mouthS, noseH, noseS
