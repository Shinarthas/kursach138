# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'lab1ui.ui'
#
# Created: Sun Nov 12 14:46:14 2017
#      by: PyQt4 UI code generator 4.10
#
# WARNING! All changes made in this file will be lost!
import cv2
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
#from Image import *
#from Image import *
import dicom
from dicom.tag import Tag, BaseTag
from dicom.datadict import DicomDictionary, dictionaryVR
import os
import csv
import numpy as np
from PyQt4 import QtCore, QtGui, QtOpenGL
from PyQt4.QtCore import pyqtSignal, QSize, Qt
from PyQt4.QtGui import *
import sys
import PIL
import math
from PIL import Image
#from Image import *
from matplotlib import pyplot as plt
from matplotlib import  cm
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

try:
    from OpenGL import GL
except ImportError:
    app = QtGui.QApplication(sys.argv)
    QtGui.QMessageBox.critical(None, "OpenGL hellogl",
            "PyOpenGL must be installed to run this example.")
    sys.exit(1)


plan=0;
ESCAPE = '\033'
x=y=w=h=0
WIDTH=HEIGHT=0
tr1=0
W=H=0
window = 0
IDs = []
IDs2 = []
IDs3=[]
screen=0
index=30
inputdir='V-06-MR-LEG/'
spacing=0
slice=0
# rotation
X_AXIS = 1
Y_AXIS = 1
Z_AXIS = 1
rect1=[0,0,0,0]
rects=[]
lim1=[0,0,255,255]
rect2=[255,0,255,0]
lim2=[0,0,255,255]
rect3=[0,255,0,255]
lim3=[0,0,255,255]
index1=0
image1=image2=image3=0
lootScheme=0
mask1=mask2=mask3=[]
Cmask1=Cmask2=Cmask3=[]
rawMask1=rawMask2=rawMask3=[]
binaryMask1=[]
M1=M2=M3=0

maskLoot1=maskLoot2=maskLoot3=0
ML1=ML2=ML3=0

imagesGlobal=[]

Lx=Ly=Lz=0



class Ui_Form(QtGui.QWidget):
    io=[0,0,0,0,0,0]
    t11='L'; t12='R';
    t21='H'; t22='F';
    t31='A'; t32='S';
    def __init__(self):
        QtGui.QWidget.__init__(self)
        self.setupUi(self)
    def setupUi(self, Form):
        global index1
        self.loadLoot()
        params=self.preRenderDir(inputdir)
        Form.setObjectName(_fromUtf8("Form"))
        Form.resize(940, 532)


        self.maskCheckBox=QtGui.QCheckBox(Form)
        self.maskCheckBox.setGeometry(QtCore.QRect(540, 150, 120, 17))
        self.maskCheckBox.setObjectName(_fromUtf8("maskCheckBox"))

        self.maskLootCheckBox = QtGui.QCheckBox(Form)
        self.maskLootCheckBox.setGeometry(QtCore.QRect(540, 180, 120, 17))
        self.maskLootCheckBox.setObjectName(_fromUtf8("maskLootCheckBox"))

        self.L = QtGui.QLabel(Form)
        self.L.setGeometry(QtCore.QRect(540, 10, 20, 13))
        self.L.setObjectName(_fromUtf8("label"))
        self.R = QtGui.QLabel(Form)
        self.R.setGeometry(QtCore.QRect(540+940-10-540, 10, 20, 13))
        self.R.setObjectName(_fromUtf8("label"))
        self.horizontalSlider1 = QtGui.QSlider(Form)
        self.horizontalSlider1.setGeometry(QtCore.QRect(540+20, 10, 940-10-540-40, 22))
        self.horizontalSlider1.setMinimum(0)
        self.horizontalSlider1.setMaximum(params[0])
        self.horizontalSlider1.setValue(params[0]/2)
        index1=params[0]/2
        self.horizontalSlider1.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSlider1.setObjectName(_fromUtf8("horizontalSlider1"))

        self.A = QtGui.QLabel(Form)
        self.A.setGeometry(QtCore.QRect(540, 40, 20, 13))
        self.A.setObjectName(_fromUtf8("label"))
        self.P = QtGui.QLabel(Form)
        self.P.setGeometry(QtCore.QRect(540 + 940 - 10 - 540, 40, 20, 13))
        self.P.setObjectName(_fromUtf8("label"))
        self.horizontalSlider2 = QtGui.QSlider(Form)
        self.horizontalSlider2.setGeometry(QtCore.QRect(540+20, 40, 940-10-540-40, 22))
        self.horizontalSlider2.setMinimum(0)
        self.horizontalSlider2.setMaximum(params[1])
        self.horizontalSlider2.setValue(params[1]/2)
        self.horizontalSlider2.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSlider2.setObjectName(_fromUtf8("horizontalSlider2"))

        self.opacity = QtGui.QSlider(Form)
        self.opacity.setGeometry(QtCore.QRect(540+(940 - 540) / 2, 210-40, (940 - 540) / 2 - 10, 22))
        self.opacity.setMinimum(0)
        self.opacity.setMaximum(100)
        self.opacity.setValue(50)
        self.opacity.setOrientation(QtCore.Qt.Horizontal)
        self.opacity.setObjectName(_fromUtf8("opacity"))
        #self.horizontalSlider2.valueChanged.connect(self.valuechange)

        self.H = QtGui.QLabel(Form)
        self.H.setGeometry(QtCore.QRect(540, 70, 20, 13))
        self.H.setObjectName(_fromUtf8("label"))
        self.F = QtGui.QLabel(Form)
        self.F.setGeometry(QtCore.QRect(540 + 940 - 10 - 540, 70, 20, 13))
        self.F.setObjectName(_fromUtf8("label"))
        self.horizontalSlider3 = QtGui.QSlider(Form)
        self.horizontalSlider3.setGeometry(QtCore.QRect(540+20, 70, 940-10-540-40, 22))
        self.horizontalSlider3.setMinimum(0)
        self.horizontalSlider3.setMaximum(params[2])
        self.horizontalSlider3.setValue(params[2]/2)
        self.horizontalSlider3.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSlider3.setObjectName(_fromUtf8("horizontalSlider3"))
        #self.horizontalSlider3.valueChanged.connect(self.valuechange)

        self.openGLWidget = GLWidget(Form)
        self.openGLWidget.setGeometry(QtCore.QRect(10, 10, 512, 512))
        self.openGLWidget.setObjectName("openGLWidget")
        self.horizontalSlider1.valueChanged.connect(self.openGLWidget.resetTextures)
        self.horizontalSlider2.valueChanged.connect(self.openGLWidget.resetTextures)
        self.horizontalSlider3.valueChanged.connect(self.openGLWidget.resetTextures)
        self.opacity.valueChanged.connect(self.openGLWidget.glDraw)

        self.addItem = QtGui.QPushButton(Form)
        self.addItem.setGeometry(QtCore.QRect(540 +(940-540)/2 +10, 100, (940-540)/2-20, 40))
        self.addItem.clicked.connect(self.addArea)
        self.addItem.setObjectName(_fromUtf8("addItem"))

        self.clear = QtGui.QPushButton(Form)
        self.clear.setGeometry(QtCore.QRect(540, 100, (940-540)/2-10, 40))
        self.clear.clicked.connect(self.clearRects)
        self.clear.setObjectName(_fromUtf8("clear"))

        self.save = QtGui.QPushButton(Form)
        self.save.setGeometry(QtCore.QRect(540, 210, (940-540)/2-10, 40))
        self.save.clicked.connect(self.saveToFile)
        self.save.setObjectName(_fromUtf8("save"))

        self.screen = QtGui.QPushButton(Form)
        self.screen.setGeometry(QtCore.QRect(540+(940 - 540) / 2, 210-50-20, (940 - 540) / 2 - 10, 40-10))
        self.screen.clicked.connect(self.screenToFile)
        self.screen.setObjectName(_fromUtf8("screen"))

        self.label = QtGui.QLabel(Form)
        self.label.setGeometry(QtCore.QRect(540 + (940-540)/2+10, 210, 200, 13))
        self.label.setObjectName(_fromUtf8("label"))

        self.label2 = QtGui.QLabel(Form)
        self.label2.setGeometry(QtCore.QRect(540 + (940 - 540) / 2 + 10, 230, 200, 13))
        self.label2.setObjectName(_fromUtf8("label"))

        self.verticalLayoutWidget = QtGui.QWidget(Form)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(522, 266, 700 - 276 - 10, 256 ))
        self.verticalLayoutWidget.setObjectName(_fromUtf8("verticalLayoutWidget"))
        self.verticalLayout = QtGui.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setMargin(0)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))

        # self.verticalLayout = QtGui.QVBoxLayout(self.main_widget)
        self.dc = MyDynamicMplCanvas(self.verticalLayoutWidget, width=5, height=4, dpi=100)
        self.verticalLayout.addWidget(self.dc)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)
    def screenToFile(self):
        #window.openGLWidget.updateOverlayGL()
        #window.openGLWidget.updateGL ()
        p2=window.openGLWidget.grabFrameBuffer()
        #p = QPixmap.grabWindow(window.winId())
        p2.save('screen.jpg', 'jpg')

        first = os.listdir(inputdir)[int(window.horizontalSlider1.value())]
        target = inputdir + first
        plan = dicom.read_file(target)
        max = np.max(plan.pixel_array)
        wtf = self.convertQImageToMat(p2)
        plan.SpecificCharacterSet="ISO_IR 100"
        plan.PhotometricInterpretation="RGB"
        plan.SamplesPerPixel=3
        plan.Rows=len(wtf)
        plan.Columns=len(wtf[0])
        plan.BitsAllocated=8
        plan.BitsStored=8
        plan.HighBit=7
        plan.PixelRepresentation=0
        plan.PixelData = wtf.astype(np.uint8).tobytes()
        plan.save_as("rtplan3.dcm")

        print len(wtf),len(wtf[0]),len(wtf[0][0])
        window.openGLWidget.loadScreen(p2)
        print "shot taken"
    def saveToFile(self):
        first = os.listdir(inputdir)[int(window.horizontalSlider1.value())]
        target = inputdir + first
        plan = dicom.read_file(target)
        # a = np.tobuffer(mask1, numpy.uint8)
        max = np.max(plan.pixel_array)

        wtf =np.zeros([256,256],dtype=np.uint16)
        for i in rawMask1:
            wtf[i[0]][i[1]]=1

        step=8
        for i in range(0,len(wtf)-step,step):
            wtf[:,i:i+step]=wtf[:,i+step:i:-1]

        im = Image.fromarray(wtf.astype(np.uint8)*255,"L")
        im.save('my.png')
        wtf2=np.packbits(wtf.ravel())

        print len(wtf) ,len(wtf[0])
        #print np.min(wtf), np.max(wtf)

        # On (60xx,0010) and (60xx,0011) is stored overlay size
        # ds.add_new(tag, VR, value) dictionaryVR

        plan.add_new([0x6000, 0x0010], "US", plan.Rows)
        plan.add_new([0x6000, 0x0011], "US", plan.Columns)
        plan.add_new([0x6000, 0x0040], "CS", "R")
        plan.add_new([0x6000, 0x0050], "SS", [1, 1])
        plan.add_new([0x6000, 0x0100], "US", 1)
        plan.add_new([0x6000, 0x0102], "US", 1)
        plan.add_new([0x6000, 0x3000], "OB", wtf2)
        #plan.PixelData = wtf.astype(np.int16).tobytes()
        plan.save_as("rtplan2.dcm")

    def convertQImageToMat(self,incomingImage):
        '''  Converts a QImage into an opencv MAT format  '''

        incomingImage = incomingImage.convertToFormat(4)

        width = incomingImage.width()
        height = incomingImage.height()

        ptr = incomingImage.bits()
        ptr.setsize(incomingImage.byteCount())
        arr = np.array(ptr).reshape(height, width, 4)  # Copies the data
        #x = np.zeros((106, 106, 3))
        result = arr[:, :, 0:3]
        return result
    def addArea(self):
        self.openGLWidget.add=1
    def clearRects(self):
        self.openGLWidget.resetTextures()
        self.openGLWidget.setFocus()
    def retranslateUi(self, Form):
        Form.setWindowTitle(_translate("Form", "Form", None))
        self.addItem.setText(_translate("Form", "add area", None))
        self.clear.setText(_translate("Form", "clear", None))
        self.maskCheckBox.setText(_translate("Form", "Show mask", None))
        self.maskLootCheckBox.setText(_translate("Form", "Show loot mask", None))
        self.save.setText(_translate("Form", "Save to file", None))
        self.screen.setText(_translate("Form", "Save screen", None))
        self.label.setText(_translate("Form", "M:", None))
        self.label2.setText(_translate("Form", "E:", None))
        self.L.setText(_translate("Form", 'H', None))
        self.R.setText(_translate("Form", "F", None))
        self.A.setText(_translate("Form", "R", None))
        self.P.setText(_translate("Form", "L", None))
        self.H.setText(_translate("Form", "P", None))
        self.F.setText(_translate("Form", "A", None))
        self.openGLWidget.setFocus()
    def preRenderDir(self ,dir ):
        list = os.listdir(dir)  # dir is your directory path
        number_files = len(list)
        first=os.listdir(dir)[0]
        plan=dicom.read_file(dir+first)
        io = plan.ImageOrientationPatient

        self.io = io
        a = "";
        b = "";
        c = "";
        if io[1]>0:
            c+="R"
        if io[1]<0:
            c+="L"
        if io[4]>0:
            c+="H"
        if io[4] < 0:
            c+="F"
        if 1>io[2]>0 or 1>io[5]>0:
            c+="P"
        if -1<io[2]<0 or -1<io[5]<0:
            c+="A"

        if io[0] > 0:
            a = a + "R"
        else:
            if io[0] < 0:
                a = a + "L";
            else:
                a = a;

        if io[1] > 0:
            a = a + "A";
        else:
            if io[1] < 0:
                a = a + "P"
            else:
                a = a

        if io[2] > 0:
            a = a + "F"
        else:
            if io[2] < 0:
                a = a + "H"
            else:
                a = a

        if io[3] > 0:
            b = b + "L"
        else:
            if io[3] < 0:
                b = b + "R"
            else:
                b = b;
        if io[4] > 0:
            b = b + "A"
        else:
            if io[4] < 0:
                b = b + "P"
            else:
                b = b
        if io[5] > 0:
            b = b + "F"
        else:
            if io[5] < 0:
                b = b + "H"
            else:
                b = b
        self.t11=a
        self.t21=b
        self.t31=c
        return [number_files,plan.Rows,plan.Columns]
    def loadLoot(self):
        global lootScheme
        shift=1
        lootScheme=np.zeros([256,4])
        for i in range(len(lootScheme)):
            lootScheme[i][0]=i
        with open('LUT.csv', 'rb') as csvfile:
            spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
            header = next(spamreader)
            for row in spamreader:
                if(row[0]==''):
                    shift+=0.5
                    continue
                lootScheme[int(row[0])][int(shift)]=int(row[6])

class GLWidget(QtOpenGL.QGLWidget):
    x=0
    y=0
    move=0
    rectIndex=0
    pointIndex=0
    scaleIndex=1
    staticWidgetSize=512
    add=0

    #xRotationChanged = QtCore.pyqtSignal(int)
    #yRotationChanged = QtCore.pyqtSignal(int)
    #zRotationChanged = QtCore.pyqtSignal(int)
    def loadScreen(self, tex):
        global screen
        screen = glGenTextures(1)
        glEnable(GL_TEXTURE_2D);
        teximg=tex.constBits()
        #print teximg[0]
        glBindTexture(GL_TEXTURE_2D, screen);
        image = Image.open("screen.jpg")
        print type(image)
        #ix = image.size[0]
        #iy = image.size[1]
        image = image.tobytes("raw", "RGBX", 0, -1)

        glPixelStorei(GL_UNPACK_ALIGNMENT, 1)
        glTexImage2D(GL_TEXTURE_2D, 0, 3, 512, 512, 0, GL_RGBA, GL_UNSIGNED_BYTE, image)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_DECAL)

    def resetTextures(self):
        global IDs, IDs2, IDs3, spacing, slice,screen
        global lim1, lim2, lim3
        global image1, image2, image3, imagesGlobal
        global mask1,mask2,mask3
        global Cmask1,Cmask2,Cmask3
        global maskLoot1,maskLoot2,maskLoot3
        global rawMask1,rawMask2,rawMask3
        global index1,Lx,Ly,Lz
        Lz = int(window.horizontalSlider1.value()* (w)/ len(imagesGlobal))
        Lx = window.horizontalSlider2.value()

        Ly = window.horizontalSlider3.value()
        tmp1 = (Lz - (w - w / slice * spacing) / 2) / (w / slice * spacing) * len(imagesGlobal) - 1
        index1 = int(window.horizontalSlider1.value())
        image1=imagesGlobal[index1]
        image = imagesGlobal
        ix = len(image[0])
        iy = len(image[0][0])

        COLORS = GL_LUMINANCE
        MODE = GL_UNSIGNED_BYTE
        k = 0
        imageK = []
        IDs2 = glGenTextures(2)
        ii = len(image[0][0])-Ly-1
        imageK.append(np.zeros([len(image), len(image[0][ii])]));
        imageK[0].fill(255)
        step = int(256 / float(len(image))) + 1
        for i in range(len(image)):
            for y in range(len(image[i][127])):
                imageK[0][i][y] = imagesGlobal[i][ii][y]
        glBindTexture(GL_TEXTURE_2D, IDs2[0]);
        glPixelStorei(GL_UNPACK_ALIGNMENT, 1)
        glTexImage2D(GL_TEXTURE_2D, 0, 3, len(image[0][ii]), len(image), 0, COLORS, MODE, imageK[0])
        glGetIntegerv(GL_TEXTURE_BINDING_2D)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        image2 = imageK[0]

        ii = Lx
        IDs3 = glGenTextures(3)
        imageS = (np.zeros([len(image), len(image[0][ii])]));
        imageS.fill(255)
        step = int(256 / float(len(image))) + 1
        for i in range(len(image)):
            for y in range(len(image[i][ii])):
                imageS[i][y] = imagesGlobal[i][y][ii]

        glBindTexture(GL_TEXTURE_2D, IDs3[0]);
        glPixelStorei(GL_UNPACK_ALIGNMENT, 1)
        glTexImage2D(GL_TEXTURE_2D, 0, 3, len(image[0][ii]), len(image), 0, COLORS, MODE, imageS)
        glGetIntegerv(GL_TEXTURE_BINDING_2D)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        image3=imageS

        mask1 = np.copy(image1)
        mask2 = np.copy(image2)
        mask3 = np.copy(image3)

        glBindTexture(GL_TEXTURE_2D, M1);
        glPixelStorei(GL_UNPACK_ALIGNMENT, 1)
        glTexImage2D(GL_TEXTURE_2D, 0, 3, len(mask1), len(mask1[0]), 0, COLORS, MODE, mask1)
        glGetIntegerv(GL_TEXTURE_BINDING_2D)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)

        glBindTexture(GL_TEXTURE_2D, M2);
        glPixelStorei(GL_UNPACK_ALIGNMENT, 1)
        glTexImage2D(GL_TEXTURE_2D, 0, 3, len(mask2), len(mask2[0]), 0, COLORS, MODE, mask2)
        glGetIntegerv(GL_TEXTURE_BINDING_2D)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)

        glBindTexture(GL_TEXTURE_2D, M3);
        glPixelStorei(GL_UNPACK_ALIGNMENT, 1)
        glTexImage2D(GL_TEXTURE_2D, 0, 3, len(mask3), len(mask3[0]), 0, COLORS, MODE, mask3)
        glGetIntegerv(GL_TEXTURE_BINDING_2D)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)

        mask1 = np.copy(image1)
        mask2 = np.copy(image2)
        mask3 = np.copy(image3)
        Cmask1 = np.dstack(3 * [mask1]).reshape((mask1.shape[0], 3 * mask1.shape[1]))
        Cmask2 = np.dstack(3 * [mask2]).reshape((mask2.shape[0], 3 * mask2.shape[1]))
        Cmask3 = np.dstack(3 * [mask3]).reshape((mask3.shape[0], 3 * mask3.shape[1]))
        glBindTexture(GL_TEXTURE_2D, M1);
        glPixelStorei(GL_UNPACK_ALIGNMENT, 1)
        glTexImage2D(GL_TEXTURE_2D, 0, 3, len(mask1), len(mask1[0]), 0, GL_RGB, MODE, Cmask1)
        glGetIntegerv(GL_TEXTURE_BINDING_2D)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)

        glBindTexture(GL_TEXTURE_2D, M2);
        glPixelStorei(GL_UNPACK_ALIGNMENT, 1)
        glTexImage2D(GL_TEXTURE_2D, 0, 3, len(mask2[0]), len(mask2), 0, GL_RGB, MODE, Cmask2)
        glGetIntegerv(GL_TEXTURE_BINDING_2D)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)

        glBindTexture(GL_TEXTURE_2D, M3);
        glPixelStorei(GL_UNPACK_ALIGNMENT, 1)
        glTexImage2D(GL_TEXTURE_2D, 0, 3, len(mask3[0]), len(mask3), 0, GL_RGB, MODE, Cmask3)
        glGetIntegerv(GL_TEXTURE_BINDING_2D)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        if (window.maskLootCheckBox.isChecked()):
            maskLoot1 = np.dstack(3*[mask1]).reshape((mask1.shape[0],3*mask1.shape[1]))
            maskLoot2 = np.dstack(3*[mask2]).reshape((mask2.shape[0],3*mask2.shape[1]))
            maskLoot3 = np.dstack(3*[mask3]).reshape((mask3.shape[0],3*mask3.shape[1]))


            glBindTexture(GL_TEXTURE_2D, ML1);
            glPixelStorei(GL_UNPACK_ALIGNMENT, 1)
            glTexImage2D(GL_TEXTURE_2D, 0, 3, len(maskLoot1), len(maskLoot1[0]) / 3, 0, GL_RGB, MODE, maskLoot1)
            glGetIntegerv(GL_TEXTURE_BINDING_2D)
            glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP)
            glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP)
            glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
            glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
            glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
            glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)

            glBindTexture(GL_TEXTURE_2D, ML3);
            glPixelStorei(GL_UNPACK_ALIGNMENT, 1)
            glTexImage2D(GL_TEXTURE_2D, 0, 3, len(maskLoot2[0]) / 3, len(maskLoot2), 0, GL_RGB, MODE, maskLoot2)
            glGetIntegerv(GL_TEXTURE_BINDING_2D)
            glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP)
            glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP)
            glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
            glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
            glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
            glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)

            glBindTexture(GL_TEXTURE_2D, ML2);
            glPixelStorei(GL_UNPACK_ALIGNMENT, 1)
            glTexImage2D(GL_TEXTURE_2D, 0, 3, len(maskLoot3[0]) / 3, len(maskLoot3), 0, GL_RGB, MODE, maskLoot3)
            glGetIntegerv(GL_TEXTURE_BINDING_2D)
            glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP)
            glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP)
            glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
            glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
            glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
            glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        rawMask1 = list()
        rawMask2 = list()
        rawMask3 = list()
        self.glDraw();


    def loadImage(self, inputdir):
        global IDs, IDs2, IDs3, spacing, slice
        global M1, M2,M3
        global mask1,mask2,mask3
        global Cmask1,Cmask2,Cmask3
        global ML1,ML2,ML3
        global maskLoot1,maskLoot2,maskLoot3
        global lim1, lim2, lim3
        global image1, image2, image3, imagesGlobal,Lx,Ly,Lz
        COLORS = GL_LUMINANCE
        MODE = GL_UNSIGNED_BYTE
        k = 0
        image = []
        #print (len(os.listdir(inputdir)))
        IDs = GL.glGenTextures(len(os.listdir(inputdir)))
        tmpplan = dicom.read_file(inputdir + os.listdir(inputdir)[0])
        spacing = tmpplan.PixelSpacing[0]
        plans=[]
        order=[]
        for i in range(len(os.listdir(inputdir))):
            tmp0=dicom.read_file(inputdir + os.listdir(inputdir)[i])
            plans.append(tmp0)
            order.append(tmp0.InstanceNumber)
        order, plans = zip(*sorted(zip(order, plans)))
        #slice = tmpplan.SpacingBetweenSlices
        slice = 512/float(len(os.listdir(inputdir)))*spacing
        hardlim=200
        for member in plans:


            plan = member
            image.append(plan.pixel_array)
            #print (fichier)
            # print fichier
            ix = plan.Rows
            iy = plan.Columns

            # image is a list with images
            max = np.amax(image[k])# k is current image index in loop
            # here i try to normalize SHORT color to BYTE color and make it fill all range from 0 to 255
            # in images max color value is like 30000 min is usually 0
            image[k] = image[k] / float(max) * 255

            glBindTexture(GL_TEXTURE_2D, IDs[k]);
            glPixelStorei(GL_UNPACK_ALIGNMENT, 1)
            glTexImage2D(GL_TEXTURE_2D, 0, 3, ix, iy, 0, COLORS, MODE, image[k])
            glGetIntegerv(GL_TEXTURE_BINDING_2D)
            glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP)
            glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP)
            glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
            glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
            glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
            glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
            glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_DECAL)
            k += 1
        lim1 = [0, 0, ix, iy]
        imagesGlobal = image
        image1 = image[window.horizontalSlider1.value()]

        imageK = []
        IDs2 = glGenTextures(2)
        ii = window.horizontalSlider2.value()
        imageK.append(np.zeros([len(image), len(image[0][ii])]));
        imageK[0].fill(255)
        step = int(256 / float(len(image))) + 1
        for i in range(len(image)):
            for y in range(len(image[i][127])):
                imageK[0][i][y] = image[i][ii][y]
        glBindTexture(GL_TEXTURE_2D, IDs2[0]);
        glPixelStorei(GL_UNPACK_ALIGNMENT, 1)
        print len(imageK[0]), len(imageK[0][0])
        glTexImage2D(GL_TEXTURE_2D, 0, 3, len(imageK[0][0]), len(imageK[0]), 0, COLORS, MODE, imageK[0])
        glGetIntegerv(GL_TEXTURE_BINDING_2D)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        image2 = imageK[0]
        '''
        #lim2 = [W + w / slice * spacing / 2, 0, W + w / slice * spacing + (w - w / slice * spacing) / 2, iy]
        lim2 = [len(image[0][ii]), (len(image[0][ii]) - len(os.listdir(inputdir)))/2/spacing*slice, 2*len(image[0][ii]), ((len(image[0][ii]) - len(os.listdir(inputdir)))/2 + len(os.listdir(inputdir)))/spacing*slice]
        lim2 = [(len(image[0][ii]) - len(os.listdir(inputdir))/spacing*slice)/2,len(image[0][ii]) ,
                ((len(image[0][ii]) - len(os.listdir(inputdir))/spacing*slice)/2 + len(os.listdir(inputdir)))/spacing*slice,2*len(image[0][ii]) ]
        '''
        rect2 = lim2
        ii = window.horizontalSlider3.value()
        IDs3 = glGenTextures(3)
        imageS = (np.zeros([len(image), len(image[0][ii])]));
        imageS.fill(255)
        step = int(256 / float(len(image))) + 1
        for i in range(len(image)):
            for y in range(len(image[i][ii])):
                imageS[i][y] = image[i][y][ii]

        glBindTexture(GL_TEXTURE_2D, IDs3[0]);
        glPixelStorei(GL_UNPACK_ALIGNMENT, 1)
        glTexImage2D(GL_TEXTURE_2D, 0, 3, len(image[0][ii]), len(image), 0, COLORS, MODE, imageS)
        glGetIntegerv(GL_TEXTURE_BINDING_2D)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        image3 = imageS
        '''
        lim3 = [len(image[0]), (len(image[0]) - len(os.listdir(inputdir))/ spacing * slice) / 2 / spacing * slice, 2 * len(image[0]),
                ((len(image[0]) - len(os.listdir(inputdir))/ spacing * slice) / 2 + len(os.listdir(inputdir))) / spacing * slice]
        '''
        #lim3 = [0, H + h / slice * spacing / 2, ix, H + h / slice * spacing + (h - h / slice * spacing) / 2]
        Lz = int(window.horizontalSlider1.value() * (w) / len(imagesGlobal))
        # Lz = window.horizontalSlider1.value()
        Lx = window.horizontalSlider2.value()
        Ly = window.horizontalSlider3.value()
        M1 = glGenTextures(1)
        M2 = glGenTextures(1)
        M3 = glGenTextures(1)
        ML1 = glGenTextures(1)
        ML2 = glGenTextures(1)
        ML3 = glGenTextures(1)
        mask1 = np.copy(image1)
        mask2 = np.copy(image2)
        mask3 = np.copy(image3)
        Cmask1 = np.dstack(3 * [mask1]).reshape((mask1.shape[0], 3 * mask1.shape[1]))
        Cmask2 = np.dstack(3 * [mask2]).reshape((mask2.shape[0], 3 * mask2.shape[1]))
        Cmask3 = np.dstack(3 * [mask3]).reshape((mask3.shape[0], 3 * mask3.shape[1]))
        glBindTexture(GL_TEXTURE_2D, M1);
        glPixelStorei(GL_UNPACK_ALIGNMENT, 1)
        glTexImage2D(GL_TEXTURE_2D, 0, 3, len(mask1), len(mask1[0]), 0, GL_RGB, MODE, Cmask1)
        glGetIntegerv(GL_TEXTURE_BINDING_2D)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)

        glBindTexture(GL_TEXTURE_2D, M2);
        glPixelStorei(GL_UNPACK_ALIGNMENT, 1)
        glTexImage2D(GL_TEXTURE_2D, 0, 3, len(mask2[0]), len(mask2), 0, GL_RGB, MODE, Cmask2)
        glGetIntegerv(GL_TEXTURE_BINDING_2D)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)

        glBindTexture(GL_TEXTURE_2D, M3);
        glPixelStorei(GL_UNPACK_ALIGNMENT, 1)
        glTexImage2D(GL_TEXTURE_2D, 0, 3, len(mask3[0]), len(mask3), 0, GL_RGB, MODE, Cmask3)
        glGetIntegerv(GL_TEXTURE_BINDING_2D)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)

        maskLoot1 = np.dstack(3 * [mask1]).reshape((mask1.shape[0], 3 * mask1.shape[1]))
        maskLoot2 = np.dstack(3 * [mask2]).reshape((mask2.shape[0], 3 * mask2.shape[1]))
        maskLoot3 = np.dstack(3 * [mask3]).reshape((mask3.shape[0], 3 * mask3.shape[1]))


        glBindTexture(GL_TEXTURE_2D, ML1);
        glPixelStorei(GL_UNPACK_ALIGNMENT, 1)
        glTexImage2D(GL_TEXTURE_2D, 0, 3, len(maskLoot1), len(maskLoot1[0])/3, 0, GL_RGB, MODE, maskLoot1)
        glGetIntegerv(GL_TEXTURE_BINDING_2D)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)

        glBindTexture(GL_TEXTURE_2D, ML3);
        glPixelStorei(GL_UNPACK_ALIGNMENT, 1)
        glTexImage2D(GL_TEXTURE_2D, 0, 3, len(maskLoot2[0])/3, len(maskLoot2), 0, GL_RGB, MODE, maskLoot2)
        glGetIntegerv(GL_TEXTURE_BINDING_2D)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)

        glBindTexture(GL_TEXTURE_2D, ML2);
        glPixelStorei(GL_UNPACK_ALIGNMENT, 1)
        glTexImage2D(GL_TEXTURE_2D, 0, 3, len(maskLoot3[0])/3,len(maskLoot3) , 0, GL_RGB, MODE, maskLoot3)
        glGetIntegerv(GL_TEXTURE_BINDING_2D)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)

        rawMask1=list()
        rawMask2=list()
        rawMask3=list()



        print lim3
        window.dc.update_figure(0)

    def createTexture(self, ix,iy,colors, mode,image):
        glPixelStorei(GL_UNPACK_ALIGNMENT, 1)
        glTexImage2D(GL_TEXTURE_2D, 0, 3, ix, iy, 0, colors, mode, image)
        glGetIntegerv(GL_TEXTURE_BINDING_2D)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)


    def __init__(self, parent=None):

        super(GLWidget, self).__init__(parent)
        #sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        self.setFixedSize(self.staticWidgetSize, self.staticWidgetSize)
        self.setMouseTracking(True)


    def minimumSizeHint(self):
        return QtCore.QSize(self.staticWidgetSize, self.staticWidgetSize)
    def maximumSizeHint(self):
        return QtCore.QSize(self.staticWidgetSize, self.staticWidgetSize)
    def sizeHint(self):
        return QtCore.QSize(self.staticWidgetSize,self.staticWidgetSize)


    def initializeGL(self):
        #self.qglClearColor(self.trolltechPurple.dark())
        #self.object = self.makeObject()
        #GL.glShadeModel(GL.GL_FLAT)
        #GL.glEnable(GL.GL_DEPTH_TEST)
        #GL.glEnable(GL.GL_CULL_FACE)
        global WIDTH, HEIGHT
        global x, y, w, h, W, H
        first = os.listdir(inputdir)[0]
        plan = dicom.read_file(inputdir+first)
        WIDTH = plan.Rows * 2
        HEIGHT = plan.Columns * 2
        H = plan.Rows
        W = plan.Columns
        x = H / 2
        y = W / 2
        h = H
        w = W
        self.scaleIndex=WIDTH/(float) (self.staticWidgetSize)
        glViewport(0, 0, self.staticWidgetSize, self.staticWidgetSize)
        #GL.glClear()
        self.loadImage(inputdir)

    def paintGL(self):
        global X_AXIS, Y_AXIS, Z_AXIS
        global DIRECTION, IDs, IDs2, IDs3
        global spacing, slice
        global lim1, lim2,lim3
        global index1

        glEnable(GL_TEXTURE_2D)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        glLoadIdentity()

        glOrtho(-W, W, -H, H, -W, W);
        glEnable(GL_BLEND);
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA);
        glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_REPLACE);
        glColor4f(1.0, 1.0, 1.0, 1.0);
        glBindTexture(GL_TEXTURE_2D, IDs[index1])
        glBegin(GL_QUADS);

        glTexCoord2f(0.0, 0.0);        glVertex2f(-w, 0);
        glTexCoord2f(1.0, 0.0);        glVertex2f(0, 0);
        glTexCoord2f(1.0, 1.0);        glVertex2f(0, -h);
        glTexCoord2f(0.0, 1.0);        glVertex2f(-w, -h);
        glEnd();

        glBindTexture(GL_TEXTURE_2D, IDs3[0])
        glBegin(GL_QUADS);

        glTexCoord2f(0.0, 0.0);        glVertex2f(lim3[0]-w,h-lim3[1]);
        glTexCoord2f(0.0, 1.0);        glVertex2f(lim3[0]-w,h-lim3[3]);
        glTexCoord2f(1.0, 1.0);        glVertex2f(lim3[2]-w,h-lim3[3]);
        glTexCoord2f(1.0, 0.0);        glVertex2f(lim3[2]-w,h-lim3[1]);



        glEnd();

        glBindTexture(GL_TEXTURE_2D, IDs2[0])
        glBegin(GL_QUADS);

        glTexCoord2f(1.0, 1.0);        glVertex2f(lim2[2],h-lim2[3]);
        glTexCoord2f(0.0, 1.0);        glVertex2f(lim2[0],h-lim2[3]);
        glTexCoord2f(0.0, 0.0);        glVertex2f(lim2[0],h-lim2[1]);
        glTexCoord2f(1.0, 0.0);        glVertex2f(lim2[2],h-lim2[1]);
        glEnd();

        if screen>0:
            glBindTexture(GL_TEXTURE_2D, screen)
            glBegin(GL_QUADS);

            glTexCoord2f(1.0, 1.0);
            glVertex2f(w, 0);
            glTexCoord2f(0.0, 1.0);
            glVertex2f(0, 0);
            glTexCoord2f(0.0, 0.0);
            glVertex2f(0,-h);
            glTexCoord2f(1.0, 0.0);
            glVertex2f(w, -h);

            glEnd();
        glColor4f(1.0, 1.0, 1.0, window.opacity.value()/100.0);
        glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_COMBINE);
        if window.maskCheckBox.isChecked():
            self.drawMask()
        if window.maskLootCheckBox.isChecked():
            self.drawMaskLoot()
        glDisable(GL_BLEND);
        self.drawAreaSelected()
        self.drawLines()
        self.drawText()
        glFlush()
    def drawText(self):
        glDisable(GL_TEXTURE_2D)
        glLineWidth(1.0);
        glColor3f(1, 1, 1)
        self.renderText(-W+10, -H/2, 0, window.t11)
        self.renderText(-W/2, 0-20, 0, window.t21)

        self.renderText(-W / 2, H - 20, 0, window.t31)
        self.renderText(-W+10, H/2, 0, window.t21)

        self.renderText(W/2, H-20, 0, window.t31)
        self.renderText( 10, H/2, 0, window.t11)

    def drawMask(self):
        global X_AXIS, Y_AXIS, Z_AXIS
        global DIRECTION, IDs, IDs2, IDs3
        global spacing, slice
        global lim1, lim2, lim3
        global index1

        glBindTexture(GL_TEXTURE_2D, M1)
        glBegin(GL_QUADS);

        glTexCoord2f(0.0, 0.0);
        glVertex2f(-w, 0);
        glTexCoord2f(1.0, 0.0);
        glVertex2f(0, 0);
        glTexCoord2f(1.0, 1.0);
        glVertex2f(0, -h);
        glTexCoord2f(0.0, 1.0);
        glVertex2f(-w, -h);
        glEnd();

        glBindTexture(GL_TEXTURE_2D, M3)
        glBegin(GL_QUADS);

        glTexCoord2f(0.0, 0.0);
        glVertex2f(lim3[0] - w, h - lim3[1]);
        glTexCoord2f(0.0, 1.0);
        glVertex2f(lim3[0] - w, h - lim3[3]);
        glTexCoord2f(1.0, 1.0);
        glVertex2f(lim3[2] - w, h - lim3[3]);
        glTexCoord2f(1.0, 0.0);
        glVertex2f(lim3[2] - w, h - lim3[1]);

        glEnd();

        glBindTexture(GL_TEXTURE_2D, M2)
        glBegin(GL_QUADS);

        glTexCoord2f(1.0, 1.0);
        glVertex2f(lim2[2], h - lim2[3]);
        glTexCoord2f(0.0, 1.0);
        glVertex2f(lim2[0], h - lim2[3]);
        glTexCoord2f(0.0, 0.0);
        glVertex2f(lim2[0], h - lim2[1]);
        glTexCoord2f(1.0, 0.0);
        glVertex2f(lim2[2], h - lim2[1]);

        glEnd();

    def drawMaskLoot(self):
        global X_AXIS, Y_AXIS, Z_AXIS
        global spacing, slice
        global lim1, lim2, lim3
        global ML2, ML1, ML3
        global index1

        glBindTexture(GL_TEXTURE_2D, ML1)
        glBegin(GL_QUADS);

        glTexCoord2f(0.0, 0.0);
        glVertex2f(-w, 0);
        glTexCoord2f(1.0, 0.0);
        glVertex2f(0, 0);
        glTexCoord2f(1.0, 1.0);
        glVertex2f(0, -h);
        glTexCoord2f(0.0, 1.0);
        glVertex2f(-w, -h);
        glEnd();

        glBindTexture(GL_TEXTURE_2D, ML2)
        glBegin(GL_QUADS);

        glTexCoord2f(0.0, 0.0);
        glVertex2f(lim3[0] - w, h - lim3[1]);
        glTexCoord2f(0.0, 1.0);
        glVertex2f(lim3[0] - w, h - lim3[3]);
        glTexCoord2f(1.0, 1.0);
        glVertex2f(lim3[2] - w, h - lim3[3]);
        glTexCoord2f(1.0, 0.0);
        glVertex2f(lim3[2] - w, h - lim3[1]);
        glEnd();

        glBindTexture(GL_TEXTURE_2D, ML3)
        glBegin(GL_QUADS);

        glTexCoord2f(1.0, 1.0);
        glVertex2f(lim2[2], h - lim2[3]);
        glTexCoord2f(0.0, 1.0);
        glVertex2f(lim2[0], h - lim2[3]);
        glTexCoord2f(0.0, 0.0);
        glVertex2f(lim2[0], h - lim2[1]);
        glTexCoord2f(1.0, 0.0);
        glVertex2f(lim2[2], h - lim2[1]);

        glEnd();

    def drawAreaSelected(self):
        global W, H
        glDisable(GL_TEXTURE_2D)
        x0 = 0;
        y0 = 0;
        if self.x*self.scaleIndex < W and self.y*self.scaleIndex < H:
            x0=-W; y0=0;
        if self.x*self.scaleIndex > W and self.y*self.scaleIndex < H:
            x0 = 0;
            y0 = 0;
        if self.x*self.scaleIndex < W and self.y*self.scaleIndex > H:
            x0 = -W;
            y0 = -H;
        glLineWidth(2.0);

        glBegin(GL_LINES);
        glColor3f(1, 1, 1)
        glVertex2i(x0, y0);
        glVertex2i(x0+W, y0);
        glVertex2i(x0+W, y0);
        glVertex2i(x0+W, y0+H);
        glVertex2i(x0+W, y0+H);
        glVertex2i(x0, y0+H);
        glVertex2i(x0, y0+H);
        glVertex2i(x0, y0);
        glEnd();

    def drawLines(self):
        global Lx, Ly, Lz, W, H,w,h
        '''
        if Lz < (w - w / float(slice) * spacing) / 2: Lz = int((w - w / slice * spacing) / 2);
        if Lz > (w - w / float(slice) * spacing) / 2 + w / slice * spacing: Lz = int(
            (w - w / slice * spacing) / 2 + w / slice * spacing);
        '''
        glLineWidth(2.0);

        glBegin(GL_LINES);
        glColor3f(1, 0, 0)
        glVertex2i(-W,-H+Ly);
        glVertex2i(0, -H+Ly);
        glEnd();

        glBegin(GL_LINES);
        glColor3f(1, 0, 0)
        glVertex2i(-Ly, 0);
        glVertex2i(-Ly, H);
        glEnd();

        glBegin(GL_LINES);
        glColor3f(0, 1, 0)
        glVertex2i(Lx , H);
        glVertex2i(Lx , 0);
        glEnd();

        glBegin(GL_LINES);
        glColor3f(0, 1, 0)
        glVertex2i(Lx - W, -H);
        glVertex2i(Lx - W, 0);
        glEnd();

        glBegin(GL_LINES);
        glColor3f(0, 0, 1)
        glVertex2i(0, W-Lz);
        glVertex2i(W, W-Lz);
        glEnd();

        glBegin(GL_LINES);
        glColor3f(0, 0, 1)
        glVertex2i(0, W - Lz);
        glVertex2i(-W, W - Lz);
        glEnd();





    def resizeGL(self, width, height):
        global x, y, w, h, W, H
        glOrtho(-W, W, -H, H, -W, W);

    def keyPressEvent(self, event):
        pass

    def mousePressEvent(self, event):
        global mask1,mask2,mask3
        global Cmask1,Cmask2,Cmask3
        global rawMask1,rawMask2,rawMask3
        global maskLoot1,maskLoot2,maskLoot3
        global lootScheme
        global M1,M2,M3
        global lim1,lim2,lim3
        x0 = 0;
        y0 = 0;
        pointer=1
        print self.scaleIndex
        if self.x * self.scaleIndex < W and self.y * self.scaleIndex > H:
            y0 = self.x * self.scaleIndex;
            x0 = self.y * self.scaleIndex-H;
            pointer = 1
        if self.x * self.scaleIndex < W and self.y * self.scaleIndex < H:
            y0 = int((self.x * self.scaleIndex) * len(image3[0]) / float(W));
            x0 = int((self.y * self.scaleIndex) * len(image3) / float(H));
            print len(image3), len(image3[0])
            print x0, y0
            pointer = 3
        if self.x * self.scaleIndex > W and self.y * self.scaleIndex < H:
            # x0 = int((self.x * self.scaleIndex)*len(image2[0])/float(W));
            x0 = int((self.y * self.scaleIndex) * len(image2) / float(H));
            y0 = int((self.x * self.scaleIndex-W) * len(image2[0]) / float(W));
            print image2[x0][y0]
            pointer = 2
        if self.add==1:
            COLORS = GL_LUMINANCE
            MODE = GL_UNSIGNED_BYTE
            result=self.simple_region_growing(int(x0),int(y0),pointer,30)
            mask=result[0]
            rawMask=result[1]
            if pointer == 1:
                rawMask1=rawMask1+result[1]
                #rawMask1 = set(rawMask1)
                glBindTexture(GL_TEXTURE_2D, M1);
                valmask=[]
                for i in rawMask:
                    valmask.append(image1[i[0]][i[1]])
                minmask=min(valmask)
                maxmask=max(valmask)
                for i in range(len(mask1)):
                    for j in range(len(mask1[0])):
                        if (mask[i][j] > 250):
                            li=int((image1[i][j]-minmask)/float(maxmask-minmask)*255)
                            maskLoot1[i][j * 3] = lootScheme[li][1]
                            maskLoot1[i][j * 3+1] = lootScheme[li][2]
                            maskLoot1[i][j * 3+2] = lootScheme[li][3]
                            Cmask1[i][j * 3] = 255
                            Cmask1[i][j * 3+1] = 213
                            Cmask1[i][j * 3+2] = 0
                        mask1[i][j]=max(mask[i][j],mask1[i][j])
                mask=Cmask1
                maskLoot=maskLoot1
            if pointer == 2:
                rawMask2 =rawMask2+ result[1]
                #rawMask2 = set(rawMask2)
                glBindTexture(GL_TEXTURE_2D, M2);
                valmask = []
                for i in rawMask:
                    valmask.append(image2[i[0]][i[1]])
                minmask = min(valmask)
                maxmask = max(valmask)
                for i in range(len(mask2)):
                    for j in range(len(mask2[0])):
                        if (mask[i][j] > 250):
                            li = int((image2[i][j] - minmask) / float(maxmask - minmask) * 255)
                            maskLoot2[i][j * 3] = int(lootScheme[li][1])
                            maskLoot2[i][j * 3 + 1] = int(lootScheme[li][2])
                            maskLoot2[i][j * 3 + 2] = int(lootScheme[li][3])
                            Cmask2[i][j * 3 ] = 255
                            Cmask2[i][j * 3 +1] = 213
                            Cmask2[i][j * 3 + 2] = 0
                        mask2[i][j] = max(mask[i][j], mask2[i][j])
                mask = Cmask2
                maskLoot = maskLoot2
            if pointer == 3:
                rawMask3 = rawMask3+result[1]
                #rawMask3 = set(rawMask3)
                glBindTexture(GL_TEXTURE_2D, M3);
                valmask = []
                for i in rawMask:
                    valmask.append(image3[i[0]][i[1]])
                minmask = min(valmask)
                maxmask = max(valmask)
                for i in range(len(mask3)):
                    for j in range(len(mask3[0])):
                        if (mask[i][j] > 250):
                            li = int((image3[i][j] - minmask) / float(maxmask - minmask) * 255)
                            maskLoot3[i][j * 3] = int(lootScheme[li][1])
                            maskLoot3[i][j * 3+1] = int(lootScheme[li][2])
                            maskLoot3[i][j * 3+2] = int(lootScheme[li][3])
                            Cmask3[i][j * 3] = 255
                            Cmask3[i][j * 3+1] = 213
                            Cmask3[i][j * 3+2] = 0
                        mask3[i][j] = max(mask[i][j], mask3[i][j])
                mask = Cmask3
                maskLoot = maskLoot3
            glPixelStorei(GL_UNPACK_ALIGNMENT, 1)
            glTexImage2D(GL_TEXTURE_2D, 0, 3, len(mask[0])/3, len(mask), 0, GL_RGB, MODE, mask)
            glGetIntegerv(GL_TEXTURE_BINDING_2D)
            glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP)
            glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP)
            glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
            glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
            glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
            glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)

            if pointer == 1:
                glBindTexture(GL_TEXTURE_2D, ML1);
            if pointer == 2:
                glBindTexture(GL_TEXTURE_2D, ML3);
            if pointer == 3:
                glBindTexture(GL_TEXTURE_2D, ML2);
            glPixelStorei(GL_UNPACK_ALIGNMENT, 1)
            glTexImage2D(GL_TEXTURE_2D, 0, 3, len(maskLoot[0])/3, len(maskLoot), 0, GL_RGB, MODE, maskLoot)
            glGetIntegerv(GL_TEXTURE_BINDING_2D)
            glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP)
            glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP)
            glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
            glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
            glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
            glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)

            window.dc.update_figure(0)

            self.add=0
        else:
            if pointer == 1:
                lim = lim1
                image = np.copy(imagesGlobal[window.horizontalSlider1.value()])
                mask=mask1
                Cmask=Cmask1
                maskLoot=maskLoot1
            if pointer == 2:
                lim = lim2
                image = image2
                maskLoot = maskLoot2
                mask = mask2
                Cmask = Cmask2
            if pointer == 3:
                lim = lim3
                image = image3
                maskLoot = maskLoot3
                mask = mask3
                Cmask = Cmask3
            mask=mask
            Cmask=Cmask

            for i in range (int(x0-10),int(x0+10)):
                for j in range(int(y0 - 10), int(y0 + 10)):
                    is_in_img = len(image) > i >= 0 and len(image[0]) > j >= 0  # returns boolean
                    if is_in_img:
                        mask[i][j]=255
                        Cmask[i][3*j]=255
                        Cmask[i][3*j+1]=213
                        Cmask[i][3*j+2]=0
                        maskLoot[i][3*j]=lootScheme[int(image[i][j])][1]
                        maskLoot[i][3*j+1]=lootScheme[int(image[i][j])][2]
                        maskLoot[i][3*j+2]=lootScheme[int(image[i][j])][3]
                        if pointer == 1:
                            rawMask1.append([i,j])
            if pointer == 1:
                glBindTexture(GL_TEXTURE_2D, M1);
            if pointer == 2:
                glBindTexture(GL_TEXTURE_2D, M2);
            if pointer == 3:
                glBindTexture(GL_TEXTURE_2D, M3);
            COLORS = GL_LUMINANCE
            MODE = GL_UNSIGNED_BYTE
            glPixelStorei(GL_UNPACK_ALIGNMENT, 1)
            glTexImage2D(GL_TEXTURE_2D, 0, 3, len(Cmask[0])/3, len(Cmask), 0, GL_RGB, MODE, Cmask)
            glGetIntegerv(GL_TEXTURE_BINDING_2D)
            glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP)
            glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP)
            glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
            glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
            glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
            glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
            if pointer == 1:
                glBindTexture(GL_TEXTURE_2D, ML1);
            if pointer == 2:
                glBindTexture(GL_TEXTURE_2D, ML3);
            if pointer == 3:
                glBindTexture(GL_TEXTURE_2D, ML2);
            glPixelStorei(GL_UNPACK_ALIGNMENT, 1)
            glTexImage2D(GL_TEXTURE_2D, 0, 3, len(maskLoot[0]) / 3, len(maskLoot), 0, GL_RGB, MODE, maskLoot)
            glGetIntegerv(GL_TEXTURE_BINDING_2D)
            glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP)
            glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP)
            glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
            glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
            glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
            glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
    def mouseMoveEvent(self, event):
        self.x = event.pos().x()
        self.y = event.pos().y()
        self.glDraw();

    def simple_region_growing(self, x,y, pointer,threshold=1):
        if pointer == 1:
            lim=lim1
            image= np.copy(imagesGlobal[window.horizontalSlider1.value()])
        if pointer == 2:
            lim = lim2
            image = image2
        if pointer == 3:
            lim = lim3
            image = image3
        seed=(x,y)
        # threshold tests
        if (not isinstance(threshold, int)):
            raise TypeError("(%s) Int expected!" % (sys._getframe().f_code.co_name))
        elif threshold < 0:
            raise ValueError("(%s) Positive value expected!" % (sys._getframe().f_code.co_name))
        # seed tests
        if not ((isinstance(seed, tuple)) and (len(seed) is 2)):
            raise TypeError("(%s) (x, y) variable expected!" % (sys._getframe().f_code.co_name))

        if (seed[0] or seed[1]) < 0:
            raise ValueError("(%s) Seed should have positive values!" % (sys._getframe().f_code.co_name))
        elif ((seed[0] > len(image)) or (seed[1] > len(image[0]))):
            raise ValueError("(%s) Seed values greater than img size!" % (sys._getframe().f_code.co_name))
        countur=[]
        min=int(image[x][y]-threshold)
        max=int(image[x][y]+threshold)
        shit1, ret1 = cv2.threshold(image.astype(np.uint8), min, 255, cv2.THRESH_BINARY)
        shit1, ret2 = cv2.threshold(image.astype(np.uint8), max, 255, cv2.THRESH_BINARY)
        ret=ret1-ret2
        for i in range(len(ret)):
            for j in range(len(ret[0])):
                if ret[i][j]>=255:
                    countur.append([i,j])

        #print len(ret), len(ret[0]), len(countur)
        return (ret, countur)

class MyMplCanvas(FigureCanvas):
    """Ultimately, this is a QWidget (as well as a FigureCanvasAgg, etc.)."""

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)

        self.compute_initial_figure()

        FigureCanvas.__init__(self, fig)
        self.setParent(parent)

        FigureCanvas.setSizePolicy(self,
                                   QtGui.QSizePolicy.Expanding,
                                   QtGui.QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)

    def compute_initial_figure(self):
        pass
class MyDynamicMplCanvas(MyMplCanvas):
    """A canvas that updates itself every second with a new plot."""

    def __init__(self, *args, **kwargs):
        MyMplCanvas.__init__(self, *args, **kwargs)

    def compute_initial_figure(self):
        self.axes.plot([0, 1, 2, 3], [1, 2, 0, 4], 'r')

    def update_figure(self,rect):
        global rawMask1,image1,lootScheme
        histData=list()
        for i in rawMask1:
            pixel=int(image1[i[0]][i[1]])
            if(lootScheme[pixel][1]<lootScheme[pixel][3] and lootScheme[pixel][2]<lootScheme[pixel][3]):
                histData.append(pixel)
        if len(histData)<2:
            return

        subImage=np.asarray(histData)
        min=subImage.min()
        max=subImage.max()
        mean=subImage.mean()
        energy=0
        for i in subImage:
            energy+=i**2
        energy=energy
        window.label.setText('M: '+str("%.2f" % (mean)))
        window.label2.setText('E: '+str("%.2f" % (energy)))

        count = int(math.floor(2 * (max - min) * (len(subImage) ** (-1 / 3.0))))
        print count
        ox = range(min, max, count)
        # ox = [min + x * (max - min) / float(len(hist[0])) for x in ox]
        hist = np.histogram(subImage, len(ox), [min, max])

        #print hist
        self.axes.cla()
        self.axes.plot( ox,hist[0])
        self.draw()

if __name__ == '__main__':

    app = QtGui.QApplication(sys.argv)
    window = Ui_Form()
    window.show()
    sys.exit(app.exec_())


def qsort(arr):
    if len(arr) <= 1:
        return arr
    else:
        return qsort([x for x in arr[1:] if x < arr[0]]) + [arr[0]] + qsort([x for x in arr[1:] if x >= arr[0]])