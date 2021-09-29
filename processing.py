from PySide2.QtCore import QObject, Signal, Slot
import cv2 as cv
import imageprovider
from skimage import (
    restoration, img_as_ubyte, img_as_float
)


class processor(QObject):
    emit_Processed = Signal()

    def __init__(self):
        QObject.__init__(self)
        self.image_provider = imageprovider.MyImageProvider()
        self.isblur = True
        self.blksize = 28
        self.radius = 0
        self.clip = 3.0
        self.crop = True
        self.subtract = None
        self.fps = 0
        self.frames = []
        self.w = 0
        self.h = 0

    @Slot(object)
    def processImage(self, img):
        self.image_provider.updateImage(img)
        if self.crop:
            img = img[0:2054, 0:2048]
        if self.isblur:
            img = cv.blur(img, (3, 3))
        if self.blksize != 0:
            clahe = cv.createCLAHE(clipLimit=3.0, tileGridSize=(self.blksize, self.blksize))
            img = clahe.apply(img)
        if self.radius != 0:
            img = img_as_float(img)
            bg = restoration.rolling_ball(img, radius=self.radius)
            img = img_as_ubyte(bg)
        if self.subtract is not None:
            if self.crop:
                self.subtract = self.subtract[0:2054, 0:2048]
            img = cv.subtract(img, self.subtract)
        if self.fps != 0:
            self.frames.append(img)
        self.image_provider.updateImage(img)
        self.emit_Processed.emit()

    @Slot()
    def setblur(self):
        self.isblur = False if self.isblur else True

    @Slot()
    def setcrop(self):
        self.crop = False if self.crop else True

    @Slot(int)
    def setclip(self, clip):
        clip = int(clip)
        self.clip = clip

    @Slot(int)
    def setblksize(self, size):
        size = int(size)
        self.blksize = size

    @Slot(int)
    def setradius(self, radius):
        radius = int(radius)
        self.radius = radius

    @Slot(str)
    def saveimage(self, path):
        path = path.replace("file:///", "")
        print(path)
        if self.fps != 0:
            f = self.frames[0]
            out = cv.VideoWriter(path, cv.VideoWriter_fourcc(*'XVID'), self.fps, (f.shape[1],f.shape[0]),0)
            for f in self.frames:
                out.write(f)
            out.release()
        else:
            cv.imwrite(path, self.image_provider.im)

    @Slot()
    def updateimage(self):
        self.processImage(self.image_provider.im)

    @Slot(str)
    def subtract_bg(self, path):
        path = path.replace("file:///", "")
        bg = cv.imread(path, 0)
        self.subtract = bg

    @Slot(float)
    def saveframe(self, fps, width, height):
        self.fps = fps
        self.w = width
        self.h = height
