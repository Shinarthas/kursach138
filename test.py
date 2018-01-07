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
imagesGlobal=[]

Lx=Ly=Lz=0



class Ui_Form(QtGui.QWidget):
    def __init__(self):
        QtGui.QWidget.__init__(self)
        self.setupUi(self)
    def setupUi(self, Form):
        Form.setObjectName(_fromUtf8("Form"))
        Form.resize(700, 532)

        self.openGLWidget = GLWidget(Form)
        self.openGLWidget.setGeometry(QtCore.QRect(10, 10, 512, 512))
        self.openGLWidget.setObjectName("openGLWidget")

        self.horizontalSlider1 = QtGui.QSlider(Form)
        self.horizontalSlider1.setGeometry(QtCore.QRect(540, 10, 700-10-540, 22))
        self.horizontalSlider1.setMinimum(0)
        self.horizontalSlider1.setMaximum(19)
        self.horizontalSlider1.setValue(10)
        self.horizontalSlider1.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSlider1.setObjectName(_fromUtf8("horizontalSlider1"))
        self.horizontalSlider1.valueChanged.connect(self.openGLWidget.resetTextures)

        self.horizontalSlider2 = QtGui.QSlider(Form)
        self.horizontalSlider2.setGeometry(QtCore.QRect(540, 40, 700-10-540, 22))
        self.horizontalSlider2.setMinimum(0)
        self.horizontalSlider2.setMaximum(255)
        self.horizontalSlider2.setValue(125)
        self.horizontalSlider2.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSlider2.setObjectName(_fromUtf8("horizontalSlider2"))
        #self.horizontalSlider2.valueChanged.connect(self.valuechange)
        self.horizontalSlider2.valueChanged.connect(self.openGLWidget.resetTextures)

        self.horizontalSlider3 = QtGui.QSlider(Form)
        self.horizontalSlider3.setGeometry(QtCore.QRect(540, 70, 700-10-540, 22))
        self.horizontalSlider3.setMinimum(0)
        self.horizontalSlider3.setMaximum(255)
        self.horizontalSlider3.setValue(125)
        self.horizontalSlider3.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSlider3.setObjectName(_fromUtf8("horizontalSlider3"))
        #self.horizontalSlider3.valueChanged.connect(self.valuechange)
        self.horizontalSlider3.valueChanged.connect(self.openGLWidget.resetTextures)

        self.addItem = QtGui.QPushButton(Form)
        self.addItem.setGeometry(QtCore.QRect(540 +(700-540)/2 +10, 100, (700-540)/2-10, 40))
        self.addItem.clicked.connect(self.addRect)
        self.addItem.setObjectName(_fromUtf8("addItem"))

        self.clear = QtGui.QPushButton(Form)
        self.clear.setGeometry(QtCore.QRect(540, 100, (700-540)/2-10, 40))
        self.clear.clicked.connect(self.clearRects)
        self.clear.setObjectName(_fromUtf8("clear"))



        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)
    def addRect(self):
        self.openGLWidget.add=1
    def clearRects(self):
        global rects
        rects=[];
        self.openGLWidget.setFocus()
    def retranslateUi(self, Form):
        Form.setWindowTitle(_translate("Form", "Form", None))
        self.addItem.setText(_translate("Form", "add item", None))
        self.clear.setText(_translate("Form", "clear", None))
        self.openGLWidget.setFocus()

class GLWidget(QtOpenGL.QGLWidget):
    x=0
    y=0
    move=0
    rectIndex=0
    pointIndex=0
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
        index1 = 0

        image = imagesGlobal
        ix = len(image[0])
        iy = len(image[0][0])
        self.glDraw();


    def loadImage(self, inputdir):
        global IDs, IDs2, IDs3, spacing, slice
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
        slice = 0.1
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
                    image[k][i][j] = 255
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
        image1 = image[0]


    def __init__(self, parent=None):

        super(GLWidget, self).__init__(parent)
        #sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        self.setFixedSize(1024, 1024)
        self.setMouseTracking(True)


    def minimumSizeHint(self):
        return QtCore.QSize(1024, 1024)
    def maximumSizeHint(self):
        return QtCore.QSize(1024, 1024)
    def sizeHint(self):
        return QtCore.QSize(1024,1024)


    def initializeGL(self):
        #self.qglClearColor(self.trolltechPurple.dark())
        #self.object = self.makeObject()
        #GL.glShadeModel(GL.GL_FLAT)
        #GL.glEnable(GL.GL_DEPTH_TEST)
        #GL.glEnable(GL.GL_CULL_FACE)
        global WIDTH, HEIGHT
        global x, y, w, h, W, H
        plan = dicom.read_file("V-01-CT-BRAIN/000000.dcm")
        WIDTH = plan.Rows * 2
        HEIGHT = plan.Columns * 2
        H = plan.Rows
        W = plan.Columns
        x = H / 2
        y = W / 2
        h = H
        w = W
        glViewport(0, 0, WIDTH, HEIGHT)
        #GL.glClear()
        self.loadImage(inputdir)

    def paintGL(self):
        global X_AXIS, Y_AXIS, Z_AXIS
        global DIRECTION, IDs, IDs2, IDs3
        global spacing, slice
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


        glFlush()




    def resizeGL(self, width, height):
        global x, y, w, h, W, H
        glOrtho(-W, W, -H, H, -W, W);

    def keyPressEvent(self, event):
        pass

    def mousePressEvent(self, event):
        pass

    def mouseMoveEvent(self, event):
        pass

if __name__ == '__main__':

    app = QtGui.QApplication(sys.argv)
    window = Ui_Form()
    window.show()
    sys.exit(app.exec_())