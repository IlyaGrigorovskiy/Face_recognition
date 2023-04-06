
from PySide2.QtCore import *
from PySide2 import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *
import qimage2ndarray

import os, sys
import cv2
import numpy as np
from mtcnn import MTCNN
import time
import shutil





class Face_recognition(QtWidgets.QWidget):
    def __init__(self, fps=30, wight = 740, height = 520):
        QtWidgets.QWidget.__init__(self)

        self.setupUi(self)

        self.video_size = QSize(wight, height)

        self.cap = cv2.VideoCapture(cv2.CAP_DSHOW)

        self.frame_timer = QTimer()
        self.fps = fps

        self.setup_camera()
        self.detector = MTCNN()

        self.Play_Button.clicked.connect(self.setup_camera)
        self.Stop_Button.clicked.connect(self.stop)


        self.Frame_counter = 0

     #Настройки камеры и запуск видеопотока
    def setup_camera(self):
        self.cap = cv2.VideoCapture(cv2.CAP_DSHOW)
        self.cap.set(3,self.video_size.width())
        self.cap.set(4,self.video_size.height())

        self.frame_timer.timeout.connect(self.display_video)
        self.frame_timer.start(int(1000//self.fps))

    #Обработка видео потока, поиск лиц
    def display_video(self):
        self.Frame_counter += 1

        print(self.Frame_counter)
        rep, frame = self.cap.read()

        if not rep:
            return False

        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)


        image_detected = frame.copy()


        faces = self.detector.detect_faces(image_detected)

        for face in faces:
            bounding_box = face['box']
            keypoints = face['keypoints']

            if face['confidence'] > 0.90:  # 0.90 - уверенность сети в процентах что это лицо

                cv2.rectangle(image_detected,(bounding_box[0], bounding_box[1]),
                                       (bounding_box[0]+bounding_box[2], bounding_box[1] + bounding_box[3]),
                                      (255,0,0),
                                      1)


        image = qimage2ndarray.array2qimage(image_detected)
        self.label_video.setPixmap(QtGui.QPixmap.fromImage(image))

    #Пауза видео потока и отключение камеры
    def stop(self):
        self.Frame_counter = 0
        self.cap.release()
        self.frame_timer.stop()


    #Закрытие программы
    def closeEvent(self, event):
        # Переопределить colseEvent
        reply = QMessageBox.question\
        (self, 'Выход из приложения',
            "Вы уверены, что хотите уйти?",
             QMessageBox.Yes,
             QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.cap.release()
            event.accept()
        else:
            event.ignore()


    #Интерфейс
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")

        pathIcon = os.path.dirname(sys.argv[0]) + "\icon\icon.png"
        Icon = QIcon(pathIcon)
        Form.setWindowIcon(Icon)

        Form.setEnabled(True)
        Form.resize(1300, 600)
        Form.setMinimumSize(QSize(1300, 570))
        Form.setMaximumSize(QSize(1300, 570))
        Form.setAutoFillBackground(False)

        self.Toolbar_groupBox = QGroupBox(Form)
        self.Toolbar_groupBox.setObjectName(u"Toolbar_groupBox")
        self.Toolbar_groupBox.setGeometry(QRect(10, 10, 1280, 51))
        self.Toolbar_groupBox.setCheckable(False)
        icon_play = os.path.dirname(sys.argv[0]) + "\icon\play.png"
        self.Play_Button = QPushButton(self.Toolbar_groupBox)
        self.Play_Button.setIcon(QIcon(icon_play))
        self.Play_Button.setIconSize(QSize(25, 25))
        self.Play_Button.setObjectName(u"Play_Button")
        self.Play_Button.setGeometry(QRect(1240, 10, 31, 31))


        icon_stop = os.path.dirname(sys.argv[0]) + "\icon\stop.png"
        self.Stop_Button = QPushButton(self.Toolbar_groupBox)
        self.Stop_Button.setIcon(QIcon(icon_stop))
        self.Stop_Button.setIconSize(QSize(25, 25))
        self.Stop_Button.setObjectName(u"Stop_Button")
        self.Stop_Button.setGeometry(QRect(1200, 10, 31, 31))

        self.Video_groupBox = QGroupBox(Form)
        self.Video_groupBox.setObjectName(u"Video_groupBox")
        self.Video_groupBox.setGeometry(QRect(10, 70, 640, 485))

        self.label_video = QLabel(self.Video_groupBox)
        self.label_video.setGeometry(QRect(0, 0, 640,485))
        self.label_video.setObjectName("label_video")


        self.Face_groupBox_1 = QGroupBox(Form)
        self.Face_groupBox_1.setObjectName(u"Face_groupBox_1")
        self.Face_groupBox_1.setGeometry(QRect(660, 70, 630, 240))
        self.Face_groupBox_2 = QGroupBox(Form)
        self.Face_groupBox_2.setObjectName(u"Face_groupBox_2")
        self.Face_groupBox_2.setGeometry(QRect(660, 315, 630, 240))


        QMetaObject.connectSlotsByName(Form)
    # setupUi

        Form.setWindowTitle(QCoreApplication.translate("Form", u"Распознавание лица онлайн", None))
        self.Toolbar_groupBox.setTitle("")
        self.Play_Button.setText("")
        self.Stop_Button.setText("")
        self.Video_groupBox.setTitle("")
        self.Face_groupBox_1.setTitle("")
        self.Face_groupBox_2.setTitle("")
    # retranslateUi







if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    start= Face_recognition()
    start.show()
    sys.exit(app.exec_())
