from PySide2.QtCore import QObject, Signal, Slot, QTimer
import PySide2
from PySide2.QtGui import Qt
import imageprovider
import cv2 as cv
import time


class camera(QObject):
    emit_Qimage = Signal(object)
    emit_Startflag = Signal(float, float, float)

    def __init__(self):
        QObject.__init__(self)
        self.image_provider = imageprovider.MyImageProvider()
        self.cap = cv.VideoCapture()
        self.timer = QTimer()
        self.timer.timeout.connect(self.streamvideo)
        self.fps = 0.0

    @Slot()
    def streamvideo(self):
        ret, img = self.cap.read()
        if not ret:
            print("no image")
            self.cap.release()
            self.timer.stop()
            return
        img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
        self.image_provider.updateImage(img)
        self.emit_Qimage.emit(img)

    @Slot(str)
    def setImage(self, path):
        p = path
        path = path.replace("\\", "/")
        format = path[-4:]
        self.cap.open(p)
        print(self.cap.get(cv.CAP_PROP_FPS))
        if format == ".mp4" or format == ".avi":
            self.cap.open(p)
            fps = self.cap.get(cv.CAP_PROP_FPS)
            self.fps = fps
            width = self.cap.get(cv.CAP_PROP_FRAME_WIDTH)
            height = self.cap.get(cv.CAP_PROP_FRAME_HEIGHT)
            self.timer.start(1000/self.fps)
            self.emit_Startflag.emit(self.fps, width, height)
        else:
            img = cv.imread(path, 0)
            self.image_provider.updateImage(img)
            self.emit_Qimage.emit(img)

    @Slot(str)
    def setfps(self, fps):
        self.fps = fps

