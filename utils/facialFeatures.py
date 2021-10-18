import cv2


# change the value as the trackbars do not allow negative numbers
class FacialFeatures(object):

    # change trackbar value to allow negative numbers
    @staticmethod
    def getValue(value, max=20):
        if value == max / 2:
            value = 0
        else:
            value -= max / 2
        return value

    # move the eyes landmarks (36-47) along the Y axis
    @staticmethod
    def moveEyesHorizontal(value, landmarks):
        value = FacialFeatures.getValue(value)
        for t in range(36, 48):
            landmarks[t] = [landmarks[t][0], landmarks[t][1] - value]

        return landmarks


    # move the brows landmarks (17-27) along the Y axis
    @staticmethod
    def moveBrowsHorizontal(value, landmarks):
        value = FacialFeatures.getValue(value)
        for t in range(17, 26):
            landmarks[t] = [landmarks[t][0], landmarks[t][1] - value]

        return landmarks


    # expand or shrink the distance between the eyes landmarks (36-47)
    @staticmethod
    def resizeEyes(value, landmarks):
        value = FacialFeatures.getValue(value)
        for t in range(36, 48):
            if t == 36 or t == 42:
                landmarks[t] = [landmarks[t][0] - value, landmarks[t][1]]
            if t == 39 or t == 45:
                landmarks[t] = [landmarks[t][0] + value, landmarks[t][1]]
            if (37 <= t <= 38) or (43 <= t <= 44):
                landmarks[t] = [landmarks[t][0], landmarks[t][1] - value]
            if (40 <= t <= 41) or (46 <= t <= 47):
                landmarks[t] = [landmarks[t][0], landmarks[t][1] + value]

        return landmarks


    # move the mouth landmarks (48-67) along the Y axis
    @staticmethod
    def moveMouthHorizontal(value, landmarks):
        value = FacialFeatures.getValue(value)
        for t in range(48, 68):
            landmarks[t] = [landmarks[t][0], landmarks[t][1] - value]

        return landmarks


    # expand or shrink the distance between the mouth landmarks (48-67)
    @staticmethod
    def resizeMouth(value, landmarks):
        value = FacialFeatures.getValue(value)
        for t in range(48, 68):
            if t == 48 or t == 60:
                landmarks[t] = [landmarks[t][0] - value, landmarks[t][1]]
            if t == 64 or t == 54:
                landmarks[t] = [landmarks[t][0] + value, landmarks[t][1]]
            if 49 <= t <= 53:
                landmarks[t] = [landmarks[t][0], landmarks[t][1] - value]
            if 55 <= t <= 59:
                landmarks[t] = [landmarks[t][0], landmarks[t][1] + value]

        return landmarks


    # expand or shrink the distance between the eye landmarks (27-35)
    @staticmethod
    def resizeNose(value, landmarks):
        value = FacialFeatures.getValue(value)
        for t in range(27, 36):
            if t == 31 or t == 32:
                landmarks[t] = [landmarks[t][0] - value, landmarks[t][1]]
            if t == 34 or t == 35:
                landmarks[t] = [landmarks[t][0] + value, landmarks[t][1]]

        return landmarks


    # move the nose landmarks (27-35) along the Y axis
    @staticmethod
    def moveNoseHorizontal(value, landmarks):
        value = FacialFeatures.getValue(value)
        for t in range(27, 36):
            landmarks[t] = [landmarks[t][0], landmarks[t][1] - value]

        return landmarks


    # expand or shrink the distance between jaw landmarks (2-14)
    @staticmethod
    def resizeJaw(value, landmarks):
        value = FacialFeatures.getValue(value)
        for t in range(2, 15):
            if 2 <= t <= 7:
                landmarks[t] = [landmarks[t][0] - value, landmarks[t][1]]
            if 9 <= t <= 14:
                landmarks[t] = [landmarks[t][0] + value, landmarks[t][1]]

        return landmarks


    # change the brightness of an image by adjusting the v value in the HSV channel
    @staticmethod
    def changeBrightness(img, value):
        value = FacialFeatures.getValue(value, 100)
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        h, s, v = cv2.split(hsv)
        v = cv2.add(v, value)
        v[v > 255] = 255
        v[v < 0] = 0
        final_hsv = cv2.merge((h, s, v))
        img = cv2.cvtColor(final_hsv, cv2.COLOR_HSV2BGR)
        return img
