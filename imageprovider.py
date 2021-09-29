import cv2 as cv
from PySide2.QtQuick import QQuickImageProvider
from PySide2.QtGui import QImage
from PySide2.QtCore import QUrl, Qt
import numpy as np


class MyImageProvider(QQuickImageProvider):
    def __init__(self):
        super(MyImageProvider, self).__init__(QQuickImageProvider.Image)
        self.im = 255 * np.ones((1000,1000,3), np.uint8)

    def requestImage(self, url, size, requestedSize):
        # s = self.im.strides[0]
        h = self.im.shape[0]
        w = self.im.shape[1]
        qimage = QImage(self.im, w, h, QImage.Format_Indexed8)
        if requestedSize.height() > 0:
            qimage = qimage.scaledToHeight(requestedSize.height(), Qt.SmoothTransformation)
        return qimage

    def updateImage(self, img):
        # print("update")
        self.im = img
