import cv2
import numpy as np
from dlib import rectangle


# detect face and return landmarks
class OpenCVUtils(object):
    @staticmethod
    def getFaceLandmarks(img, detector, predictor):
        height, width = img.shape
        faces = detector(img)

        if len(faces) == 0:
            print("No face found")
            return None

        allLandmarksPoints = []
        for face in faces:
            faceRectangle = rectangle(int(face.left()), int(face.top()), int(face.right()), int(face.bottom()))

            landmarks = predictor(img, faceRectangle)

            landmarkPoints = np.array([[p.x, p.y] for p in landmarks.parts()])

            # add border of the image
            landmarkPoints = np.append(landmarkPoints, [[0.0, 0.0]], axis=0)
            landmarkPoints = np.append(landmarkPoints, [[int(width / 2), 0]], axis=0)
            landmarkPoints = np.append(landmarkPoints, [[width, 0]], axis=0)
            landmarkPoints = np.append(landmarkPoints, [[0, height]], axis=0)
            landmarkPoints = np.append(landmarkPoints, [[int(width / 2), height]], axis=0)
            landmarkPoints = np.append(landmarkPoints, [[width, height]], axis=0)

            allLandmarksPoints.append(landmarkPoints)

        return allLandmarksPoints

    # draw points and their index on the face
    @staticmethod
    def drawPoints(img, points, color):
        n = 0
        for point in points:
            cv2.circle(img, (int(point[0]), int(point[1])), 2, color, -1)
            cv2.putText(img, str(n), (int(point[0]), int(point[1]) - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.3, (255, 0, 0), 1)
            n = n + 1

    # draw a rectangle around detected face
    @staticmethod
    def drawFaceRectangle(img, detector):
        faces = detector(img)
        if len(faces) == 0:
            print("No face found")
            return None
        for face in faces:
            x1 = face.left()  # left point
            y1 = face.top()  # top point
            x2 = face.right()  # right point
            y2 = face.bottom()  # bottom point
            # Draw a rectangle
            cv2.rectangle(img=img, pt1=(x1, y1), pt2=(x2, y2), color=(255, 0, 0), thickness=4)

    # Delaunay triangulation - returns an array of points and their coordinates for each triangle found in a face
    @staticmethod
    def getTriangles(points):
        trianglePoints = []
        for point in points:
            trianglePoints.append((int(point[0]), int(point[1])))

        convexPoints = np.array(trianglePoints, np.int32)
        convexhull = cv2.convexHull(convexPoints)  # border points of the face

        # get the region of interest
        rect = cv2.boundingRect(convexhull)

        subdiv = cv2.Subdiv2D(rect)
        subdiv.insert(trianglePoints)

        triangles = subdiv.getTriangleList()
        triangles = np.array(triangles, dtype=np.int32)  # all the triangles found in the face

        return triangles

    @staticmethod
    def getLandmarkPointsFromTriangles(nparray):
        index = None

        for coordinate in nparray[0]:
            index = coordinate
            break
        return index

    # draw triangles on an image
    @staticmethod
    def drawTriangles(img, triangles):
        for t in triangles:
            pt1 = (t[0], t[1])  # x and y of the first point
            pt2 = (t[2], t[3])
            pt3 = (t[4], t[5])

            cv2.line(img, pt1, pt2, (0, 0, 255), 1)
            cv2.line(img, pt2, pt3, (0, 0, 255), 1)
            cv2.line(img, pt3, pt1, (0, 0, 255), 1)

    # match triangle points from delaunay triangulation with landmark points
    # returns an array of 3 landmark points that form a triangle, for each triangle found in a face
    @staticmethod
    def getTrianglesPointsWithLandmarks(triangles, points):
        indexes_triangles = []

        for t in triangles:
            pt1 = (t[0], t[1])  # x and y of the first point
            pt2 = (t[2], t[3])
            pt3 = (t[4], t[5])

            index_pt1 = np.where((points == pt1).all(axis=1))
            index_pt1 = OpenCVUtils.getLandmarkPointsFromTriangles(index_pt1)
            index_pt2 = np.where((points == pt2).all(axis=1))
            index_pt2 = OpenCVUtils.getLandmarkPointsFromTriangles(index_pt2)
            index_pt3 = np.where((points == pt3).all(axis=1))
            index_pt3 = OpenCVUtils.getLandmarkPointsFromTriangles(index_pt3)

            if index_pt1 is not None and index_pt2 is not None and index_pt3 is not None:
                triangle = [index_pt1, index_pt2, index_pt3]
                indexes_triangles.append(triangle)

        return indexes_triangles

    # draw triangles made by landmark points
    @staticmethod
    def drawTrianglesWithLandmarks(img, landmarkPoints, trianglePoints):
        for point in trianglePoints:
            pt1 = (int(landmarkPoints[point[0]][0]), int(landmarkPoints[point[0]][1]))  # x and y of the first point
            pt2 = (int(landmarkPoints[point[1]][0]), int(landmarkPoints[point[1]][1]))  # x and y of the first point
            pt3 = (int(landmarkPoints[point[2]][0]), int(landmarkPoints[point[2]][1]))  # x and y of the first point

            cv2.line(img, pt1, pt2, (0, 0, 255), 1)
            cv2.line(img, pt2, pt3, (0, 0, 255), 1)
            cv2.line(img, pt3, pt1, (0, 0, 255), 1)

    # transform points from openCV coordinate system to openGL system
    @staticmethod
    def pointsToOpenGL(img, vertices_coordinates, texture_coordinates):
        height, width, channels = img.shape
        points = np.array([], dtype="float32")

        for n in range(len(vertices_coordinates)):
            x = vertices_coordinates[n][0]
            y = vertices_coordinates[n][1]

            s = texture_coordinates[n][0]
            t = texture_coordinates[n][1]

            points = np.append(points,
                               [((x / width) - 0.5) * 2, -((y / width) - 0.5) * 2, 0.0, 0.0, 0.0, 0.0, s / width,
                                t / height])

        return points
