# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'lab1ui.ui'
#
# Created: Sun Nov 12 14:46:14 2017
#      by: PyQt4 UI code generator 4.10
#
# WARNING! All changes made in this file will be lost!
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
#from Image import *
import dicom
import os
import numpy as np
from PyQt4 import QtCore, QtGui, QtOpenGL
from PyQt4.QtCore import pyqtSignal, QSize, Qt
from PyQt4.QtGui import *
import sys
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
index=30
inputdir='V-01-CT-BRAIN/'
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

mask1=mask2=mask3=0
M1=M2=M3=0

maskLoot1=maskLoot2=maskLoot3=0
ML1=ML2=ML3=0

imagesGlobal=[]

Lx=Ly=Lz=0



class Ui_Form(QtGui.QWidget):
    def __init__(self):
        QtGui.QWidget.__init__(self)
        self.setupUi(self)
    def setupUi(self, Form):
        params=self.preRenderDir(inputdir)
        Form.setObjectName(_fromUtf8("Form"))
        Form.resize(700, 532)


        self.maskCheckBox=QtGui.QCheckBox(Form)
        self.maskCheckBox.setGeometry(QtCore.QRect(540, 150, 120, 17))
        self.maskCheckBox.setObjectName(_fromUtf8("maskCheckBox"))

        self.horizontalSlider1 = QtGui.QSlider(Form)
        self.horizontalSlider1.setGeometry(QtCore.QRect(540, 10, 700-10-540, 22))
        self.horizontalSlider1.setMinimum(0)
        self.horizontalSlider1.setMaximum(params[0])
        self.horizontalSlider1.setValue(0)
        self.horizontalSlider1.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSlider1.setObjectName(_fromUtf8("horizontalSlider1"))


        self.horizontalSlider2 = QtGui.QSlider(Form)
        self.horizontalSlider2.setGeometry(QtCore.QRect(540, 40, 700-10-540, 22))
        self.horizontalSlider2.setMinimum(0)
        self.horizontalSlider2.setMaximum(params[1])
        self.horizontalSlider2.setValue(params[1]/2)
        self.horizontalSlider2.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSlider2.setObjectName(_fromUtf8("horizontalSlider2"))
        #self.horizontalSlider2.valueChanged.connect(self.valuechange)


        self.horizontalSlider3 = QtGui.QSlider(Form)
        self.horizontalSlider3.setGeometry(QtCore.QRect(540, 70, 700-10-540, 22))
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

        self.addItem = QtGui.QPushButton(Form)
        self.addItem.setGeometry(QtCore.QRect(540 +(700-540)/2 +10, 100, (700-540)/2-10, 40))
        self.addItem.clicked.connect(self.addArea)
        self.addItem.setObjectName(_fromUtf8("addItem"))

        self.clear = QtGui.QPushButton(Form)
        self.clear.setGeometry(QtCore.QRect(540, 100, (700-540)/2-10, 40))
        self.clear.clicked.connect(self.clearRects)
        self.clear.setObjectName(_fromUtf8("clear"))



        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)
    def addArea(self):
        self.openGLWidget.add=1
    def clearRects(self):
        global rects
        rects=[];
        self.openGLWidget.setFocus()
    def retranslateUi(self, Form):
        Form.setWindowTitle(_translate("Form", "Form", None))
        self.addItem.setText(_translate("Form", "add area", None))
        self.clear.setText(_translate("Form", "clear", None))
        self.maskCheckBox.setText(_translate("Form", "Show mask", None))
        self.openGLWidget.setFocus()
    def preRenderDir(self ,dir ):
        list = os.listdir(dir)  # dir is your directory path
        number_files = len(list)
        first=os.listdir(dir)[0]
        plan=dicom.read_file(dir+first)

        return [number_files,plan.Rows,plan.Columns]

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
    def resetTextures(self):
        global IDs, IDs2, IDs3, spacing, slice
        global lim1, lim2, lim3
        global image1, image2, image3, imagesGlobal
        global index1,Lx,Ly,Lz
        #Lz = (window.horizontalSlider1.value()+ (w - w / slice * spacing) / 2) * (w / slice * spacing) * len(imagesGlobal) - 1
        Lz = int(window.horizontalSlider1.value()* (w / slice * spacing)/ len(imagesGlobal)+(w - w / slice * spacing) / 2)
        #Lz = window.horizontalSlider1.value()
        Lx = window.horizontalSlider2.value()

        Ly = window.horizontalSlider3.value()
        tmp1 = (Lz - (w - w / slice * spacing) / 2) / (w / slice * spacing) * len(imagesGlobal) - 1
        index1 = int(window.horizontalSlider1.value())

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
                imageK[0][i][y] = image[i][ii][y]
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
        self.glDraw();


    def loadImage(self, inputdir):
        global IDs, IDs2, IDs3, spacing, slice
        global M1, M2,M3
        global ML1,ML2,ML3
        global lim1, lim2, lim3
        global image1, image2, image3, imagesGlobal,Lx,Ly,Lz
        COLORS = GL_LUMINANCE
        MODE = GL_UNSIGNED_BYTE
        k = 0
        image = []
        print (len(os.listdir(inputdir)))
        IDs = GL.glGenTextures(len(os.listdir(inputdir)))
        tmpplan = dicom.read_file(inputdir + os.listdir(inputdir)[0])
        spacing = tmpplan.PixelSpacing[0]
        #slice = tmpplan.SpacingBetweenSlices
        slice = 3*spacing
        hardlim=2
        for fichier in os.listdir(inputdir):

            hardlim-=1
            if hardlim==0:
                break

            plan = dicom.read_file(inputdir + fichier)
            image.append(plan.pixel_array)
            print (fichier)
            # print fichier
            ix = plan.Rows
            iy = plan.Columns
            max = np.amax(image)

            i = 0
            while i < len(image[k]):
                j = 0
                while j < len(image[k][i]):
                    image[k][i][j] = float(image[k][i][j]) / (max) * 255
                    j += 1
                i += 1

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
        print (ii)
        step = int(256 / float(len(image))) + 1
        for i in range(len(image)):
            for y in range(len(image[i][127])):
                imageK[0][i][y] = image[i][ii][y]
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
        #lim2 = [W + w / slice * spacing / 2, 0, W + w / slice * spacing + (w - w / slice * spacing) / 2, iy]
        lim2 = [len(image[0][ii]), (len(image[0][ii]) - len(os.listdir(inputdir)))/2/spacing*slice, 2*len(image[0][ii]), ((len(image[0][ii]) - len(os.listdir(inputdir)))/2 + len(os.listdir(inputdir)))/spacing*slice]
        lim2 = [(len(image[0][ii]) - len(os.listdir(inputdir))/spacing*slice)/2,len(image[0][ii]) ,
                ((len(image[0][ii]) - len(os.listdir(inputdir))/spacing*slice)/2 + len(os.listdir(inputdir)))/spacing*slice,2*len(image[0][ii]) ]
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
        lim3 = [len(image[0]), (len(image[0]) - len(os.listdir(inputdir))/ spacing * slice) / 2 / spacing * slice, 2 * len(image[0]),
                ((len(image[0]) - len(os.listdir(inputdir))/ spacing * slice) / 2 + len(os.listdir(inputdir))) / spacing * slice]

        #lim3 = [0, H + h / slice * spacing / 2, ix, H + h / slice * spacing + (h - h / slice * spacing) / 2]
        Lz = int(window.horizontalSlider1.value() * (w / slice * spacing) / len(imagesGlobal) + (
        w - w / slice * spacing) / 2)
        # Lz = window.horizontalSlider1.value()
        Lx = window.horizontalSlider2.value()
        Ly = window.horizontalSlider3.value()
        M1 = glGenTextures(1)
        M2 = glGenTextures(1)
        M3 = glGenTextures(1)
        ML1 = glGenTextures(1)
        ML2 = glGenTextures(1)
        ML3 = glGenTextures(1)


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

        glBindTexture(GL_TEXTURE_2D, IDs[index1])
        glBegin(GL_QUADS);

        glTexCoord2f(0.0, 0.0);
        glVertex2f(-w, h);
        glTexCoord2f(1.0, 0.0);
        glVertex2f(0, h);
        glTexCoord2f(1.0, 1.0);
        glVertex2f(0, 0);
        glTexCoord2f(0.0, 1.0);
        glVertex2f(-w, 0);
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

        glTexCoord2f(1.0, 1.0);        glVertex2f(lim2[2]-w,h-lim2[3]);
        glTexCoord2f(0.0, 1.0);        glVertex2f(lim2[0]-w,h-lim2[3]);
        glTexCoord2f(0.0, 0.0);        glVertex2f(lim2[0]-w,h-lim2[1]);
        glTexCoord2f(1.0, 0.0);        glVertex2f(lim2[2]-w,h-lim2[1]);

        glEnd();

        if window.maskCheckBox.isChecked():
            self.drawMask()
        self.drawAreaSelected()
        self.drawLines()
        glFlush()

    def drawMask(self):
        global X_AXIS, Y_AXIS, Z_AXIS
        global DIRECTION, IDs, IDs2, IDs3
        global spacing, slice
        global lim1, lim2, lim3
        global index1

        glDepthMask(GL_FALSE);
        glEnable(GL_BLEND);
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA);
        glAlphaFunc(GL_GREATER, 0.4)
        glBindTexture(GL_TEXTURE_2D, M1)
        glBegin(GL_QUADS);



        glTexCoord2f(0.0, 0.0);
        glVertex2f(-w, h);
        glTexCoord2f(1.0, 0.0);
        glVertex2f(0, h);
        glTexCoord2f(1.0, 1.0);
        glVertex2f(0, 0);
        glTexCoord2f(0.0, 1.0);
        glVertex2f(-w, 0);
        glEnd();

        glDisable(GL_BLEND);
        glDepthMask(GL_TRUE);

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
        if Lz < (w - w / slice * spacing) / 2: Lz = int((w - w / slice * spacing) / 2);
        if Lz > (w - w / slice * spacing) / 2 + w / slice * spacing: Lz = int(
            (w - w / slice * spacing) / 2 + w / slice * spacing);
        glLineWidth(2.0);

        glBegin(GL_LINES);
        glColor3f(1, 0, 0)
        glVertex2i(-W, Ly);
        glVertex2i(0, Ly);
        glEnd();

        glBegin(GL_LINES);
        glColor3f(1, 0, 0)
        #glVertex2i(W, Ly);
        #glVertex2i(0, Ly);
        glVertex2i(W-Ly, H);
        glVertex2i(W-Ly, 0);
        glEnd();

        glBegin(GL_LINES);
        glColor3f(0, 1, 0)
        glVertex2i(Lx - W, H);
        glVertex2i(Lx - W, 0);
        glEnd();

        glBegin(GL_LINES);
        glColor3f(0, 1, 0)
        glVertex2i(Lx - W, -H);
        glVertex2i(Lx - W, 0);
        glEnd();

        glBegin(GL_LINES);
        glColor3f(0, 0, 1)
        glVertex2i(W, Lz);
        glVertex2i(0, Lz);
        glEnd();

        glBegin(GL_LINES);
        glColor3f(0, 0, 1)
        glVertex2i(-W, -H+Lz);
        glVertex2i(0, -H+Lz);
        glEnd();





    def resizeGL(self, width, height):
        global x, y, w, h, W, H
        glOrtho(-W, W, -H, H, -W, W);

    def keyPressEvent(self, event):
        pass

    def mousePressEvent(self, event):
        global mask1,mask2,mask3
        global M1,M2,M3
        x0 = 0;
        y0 = 0;
        pointer=1
        if self.add==1:
            if self.x * self.scaleIndex < W and self.y * self.scaleIndex < H:
                x0 = self.x * self.scaleIndex;
                y0 = self.y * self.scaleIndex;
                pointer=1
            if self.x * self.scaleIndex > W and self.y * self.scaleIndex < H:
                x0 = self.x * self.scaleIndex-W;
                y0 = self.y * self.scaleIndex;
                pointer=2
            if self.x * self.scaleIndex < W and self.y * self.scaleIndex > H:
                x0 = self.x * self.scaleIndex;
                y0 = self.y * self.scaleIndex - H;
                pointer=3
            mask=self.simple_region_growing(int(x0),int(y0),pointer,5)
            COLORS = GL_RGBA
            MODE = GL_UNSIGNED_BYTE
            glBindTexture(GL_TEXTURE_2D, M1);
            glPixelStorei(GL_UNPACK_ALIGNMENT, 1)
            glTexImage2D(GL_TEXTURE_2D, 0, 3, len(mask), len(mask[0])/4, 0, COLORS, MODE, mask)
            glGetIntegerv(GL_TEXTURE_BINDING_2D)
            glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP)
            glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP)
            glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
            glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
            glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
            glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
            self.add=0



    def mouseMoveEvent(self, event):
        self.x = event.pos().x()
        self.y = event.pos().y()
        self.glDraw();

    def simple_region_growing(self, x,y, pointer,threshold=1):
        if pointer == 1:
            lim=lim1
            image=imagesGlobal[window.horizontalSlider1.value()]
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

        reg = np.zeros([len(image), len(image[0])])
        # parameters
        mean_reg = float(image[seed[0]][seed[1]])
        size = 1
        pix_area = len(image) * len(image[0])

        contour = []  # will be [ [[x1,l y1], val1],..., [[xn, yn], van] ]
        contour_val = []
        dist = 0
        # TODO: may be enhanced later with 8th connectivity
        orient = [(1, 0), (0, 1), (-1, 0), (0, -1)]  # 4 connectivity
        cur_pix = [seed[0], seed[1]]

        # Spreading
        while (dist < threshold and size < pix_area):
            # adding pixels
            for j in range(4):
                # select new candidate
                temp_pix = [cur_pix[0] + orient[j][0], cur_pix[1] + orient[j][1]]

                # check if it belongs to the image
                is_in_img = len(image) > temp_pix[0] > 0 and len(image[0]) > temp_pix[1] > 0  # returns boolean
                # candidate is taken if not already selected before
                if ((is_in_img and (reg[temp_pix[1]][temp_pix[0]] == 0))):
                    contour.append(temp_pix)
                    contour_val.append(image[temp_pix[1]][temp_pix[0]])
                    reg[temp_pix[1]][temp_pix[0]] = 2 ** 8
            # add the nearest pixel of the contour in it
            try:
                dist = abs(int(np.mean(contour_val)) - mean_reg)
            except:
                dist = 0

            dist_list = [abs(i - mean_reg) for i in contour_val]
            dist = min(dist_list)  # get min distance
            print dist
            index = dist_list.index(min(dist_list))  # mean distance index
            size += 1  # updating region size
            reg[cur_pix[1]][cur_pix[0]] = 2 ** 8 - 1

            # updating mean MUST BE FLOAT
            mean_reg = (mean_reg * size + float(contour_val[index])) / (size + 1)
            # updating seed
            cur_pix = contour[index]

            # removing pixel from neigborhood
            del contour[index]
            del contour_val[index]
        tmpReg = np.zeros([len(image),4* len(image[0])])
        for i in range(len(reg)):
            for j in range(len(reg[0])):
                tmpReg[i][j*4]=reg[i][j]
                tmpReg[i][j*4+1]=reg[i][j]
                tmpReg[i][j*4+2]=reg[i][j]
                tmpReg[i][j*4+3]=0
        return tmpReg


if __name__ == '__main__':

    app = QtGui.QApplication(sys.argv)
    window = Ui_Form()
    window.show()
    sys.exit(app.exec_())