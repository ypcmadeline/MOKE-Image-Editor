# This Python file uses the following encoding: utf-8
import os
from pathlib import Path
import sys
import camera
from processing import processor
import cv2 as cv


from PySide2.QtGui import QGuiApplication
from PySide2.QtQml import QQmlApplicationEngine, qmlRegisterType
from PySide2.QtCore import Slot, QObject

import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from os.path import expanduser


class Watcher(QObject):
    def __init__(self, path):
        QObject.__init__(self)
        self.observer = Observer()
        self.path = path
        self.event_handler = ExampleHandler()
        self.observer.start()

    @Slot(str)
    def updatepath(self, path):
        path = path.replace("file:///", "")
        self.path = path
        self.run()

    def run(self):
        self.observer.schedule(self.event_handler, self.path, recursive=False)


class ExampleHandler(FileSystemEventHandler):
    def on_created(self, event):  # when file is created
        # do something, eg. call your function to process the image
        path = event.src_path
        time.sleep(0.1)
        image_source.setImage(path)


folder = expanduser('~/Pictures')
watcher = Watcher(folder)
watcher.run()
observer = Observer()
event_handler = ExampleHandler()  # create event handler
# set observer to use created handler in directory
observer.schedule(event_handler, path='read')
observer.start()

app = QGuiApplication(sys.argv)
engine = QQmlApplicationEngine()

image_source = camera.camera()
p = processor()
image_source.emit_Qimage.connect(p.processImage)
image_source.emit_Startflag.connect(p.saveframe)
engine.rootContext().setContextProperty("camera", image_source)
engine.rootContext().setContextProperty("processor", p)
engine.rootContext().setContextProperty("watcher", watcher)
engine.addImageProvider("myprovider", image_source.image_provider)
engine.addImageProvider("processprovider", p.image_provider)
engine.load(os.fspath(Path(__file__).resolve().parent / "main.qml"))
if not engine.rootObjects():
    sys.exit(-1)
sys.exit(app.exec_())
