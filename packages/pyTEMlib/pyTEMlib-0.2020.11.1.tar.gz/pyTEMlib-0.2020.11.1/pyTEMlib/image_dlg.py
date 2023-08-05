# -*- coding: utf-8 -*-
"""
InfoDialog user interface definitions
"""

from PyQt5 import QtCore, QtGui, QtWidgets
from pyTEMlib.microscope import microscope
import matplotlib
import matplotlib.figure

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as Canvas


class HistogramCanvas(Canvas):
    def __init__(self, parent, width=10, height=10, dpi=100):
        self.figure = matplotlib.figure.Figure(figsize=(width, height), dpi=dpi)
        self.figure.subplots_adjust(bottom=.2)

        Canvas.__init__(self, self.figure)
        self.setParent(parent)

        Canvas.setSizePolicy(self, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)

        Canvas.updateGeometry(self)


class UiDialog(object):
    def __init__(self, dialog, parent=None):
        dialog.setObjectName('Spectrum Info')
        dialog.resize(371, 784)

        self.parent = parent

        self.TEM = []
        self.TEM = microscope.get_available_microscope_names()

        valid_float = QtGui.QDoubleValidator()
        # valid_int = QtGui.QIntValidator()
        self.histogram = HistogramCanvas(self.parent, width=10, height=10, dpi=70)

        # Defining a plot instance (axes) and assigning a variable to it
        self.histogram.axes = self.histogram.figure.add_subplot(1, 1, 1)
        # self.histogram.axes.set_axis_off()

        plot_layout = QtWidgets.QGridLayout()

        # Adding Histogram to the layout
        plot_layout.addWidget(self.histogram, 0, 0)

        # making a single widget out of image and slider
        histogram_plot = QtWidgets.QWidget()
        histogram_plot.setLayout(plot_layout)

        self.layout = QtWidgets.QGridLayout()
        self.layout.setVerticalSpacing(2)

        self.separator1 = QtWidgets.QLabel()
        self.separator1.setAutoFillBackground(True)
        palette = self.separator1.palette()
        palette.setColor(self.separator1.backgroundRole(), QtCore.Qt.blue)
        palette.setColor(self.separator1.foregroundRole(), QtCore.Qt.white)
        self.separator1.setAlignment(QtCore.Qt.AlignCenter)
        self.separator1.setMaximumHeight(50)

        self.separator1.setPalette(palette)
        ######################################################################
        self.separator1.setText("Experimental Parameters")
        self.layout.addWidget(self.separator1, 0, 0, 1, 3)
        row = 0
        self.layout.addWidget(self.separator1, row, 0, 1, 4)
        ######################################################################

        row += 1
        self.fovXLabel = QtWidgets.QLabel("FOV x")
        self.fovXEdit = QtWidgets.QLineEdit(" 1.00")
        self.fovXEdit.setValidator(valid_float)
        self.fovXUnit = QtWidgets.QLabel("nm")

        self.layout.addWidget(self.fovXLabel, row, 0)
        self.layout.addWidget(self.fovXEdit, row, 1)
        self.layout.addWidget(self.fovXUnit, row, 2)

        row += 1
        self.fovYLabel = QtWidgets.QLabel("FOV y")
        self.fovYEdit = QtWidgets.QLineEdit(" 1.00")
        self.fovYEdit.setValidator(valid_float)
        self.fovYUnit = QtWidgets.QLabel("nm")

        self.layout.addWidget(self.fovYLabel, row, 0)
        self.layout.addWidget(self.fovYEdit, row, 1)
        self.layout.addWidget(self.fovYUnit, row, 2)

        row += 1
        self.scale_button = QtWidgets.QPushButton('Set Spatial Scale', dialog)
        self.layout.addWidget(self.scale_button, row, 1)

        row += 1
        self.timeLabel = QtWidgets.QLabel("Exp. Time")
        self.timeEdit = QtWidgets.QLineEdit(" 100.0")
        self.timeEdit.setValidator(valid_float)
        self.timeUnit = QtWidgets.QLabel("s")

        self.layout.addWidget(self.timeLabel, row, 0)
        self.layout.addWidget(self.timeEdit, row, 1)
        self.layout.addWidget(self.timeUnit, row, 2)

        self.separator2 = QtWidgets.QLabel(dialog)
        self.separator2.setAutoFillBackground(True)
        self.separator2.setAlignment(QtCore.Qt.AlignCenter)
        self.separator2.setMaximumHeight(50)
        self.separator2.setPalette(palette)

        row += 1
        ######################################################################
        self.separator2.setText("Microscope")
        self.layout.addWidget(self.separator2, row, 0, 1, 4)
        ######################################################################

        row += 1
        self.TEMList = QtWidgets.QComboBox()
        self.TEMList.setEditable(False)
        self.TEMList.addItems(self.TEM)

        self.layout.addWidget(self.TEMList, row, 1)

        row += 1
        self.convLabel = QtWidgets.QLabel("Conv. Angle")
        self.convEdit = QtWidgets.QLineEdit(" 100.0")
        self.convEdit.setValidator(valid_float)
        self.convUnit = QtWidgets.QLabel("mrad")
        self.layout.addWidget(self.convLabel, row, 0)
        self.layout.addWidget(self.convEdit, row, 1)
        self.layout.addWidget(self.convUnit, row, 2)

        row += 1
        self.collLabel = QtWidgets.QLabel("Coll. Angle")
        self.collEdit = QtWidgets.QLineEdit(" 10.0")
        self.collEdit.setValidator(valid_float)
        self.collUnit = QtWidgets.QLabel("mrad")
        self.layout.addWidget(self.collLabel, row, 0)
        self.layout.addWidget(self.collEdit, row, 1)
        self.layout.addWidget(self.collUnit, row, 2)

        row += 1
        self.E0Label = QtWidgets.QLabel("Acc. Voltage")
        self.E0Edit = QtWidgets.QLineEdit(" 0.0")
        self.E0Edit.setValidator(valid_float)
        self.E0Unit = QtWidgets.QLabel("kV")
        self.layout.addWidget(self.E0Label, row, 0)
        self.layout.addWidget(self.E0Edit, row, 1)
        self.layout.addWidget(self.E0Unit, row, 2)

        row += 1
        self.fluxLabel = QtWidgets.QLabel("Flux")
        self.fluxEdit = QtWidgets.QLineEdit("0.0")
        self.fluxEdit.setValidator(valid_float)
        self.fluxUnit = QtWidgets.QLabel("e<sup>-</sup>/s")
        self.layout.addWidget(self.fluxLabel, row, 0)
        self.layout.addWidget(self.fluxEdit, row, 1)
        self.layout.addWidget(self.fluxUnit, row, 2)

        self.separator3 = QtWidgets.QLabel(dialog)
        self.separator3.setAutoFillBackground(True)
        self.separator3.setAlignment(QtCore.Qt.AlignCenter)
        self.separator3.setMaximumHeight(50)
        self.separator3.setPalette(palette)
        row += 1
        ######################################################################
        self.separator3.setText("Histogram")
        self.layout.addWidget(self.separator3, row, 0, 1, 4)

        row += 1
        self.layout.addWidget(histogram_plot, row, 0, 1, 3)

        row += 1
        self.logCheck = QtWidgets.QCheckBox("log")
        self.gammaEdit = QtWidgets.QLineEdit(" 1.0")
        self.gammaEdit.setValidator(valid_float)
        self.gammaCheck = QtWidgets.QCheckBox("gamma")
        self.layout.addWidget(self.logCheck, row, 0)
        self.layout.addWidget(self.gammaCheck, row, 1)
        self.layout.addWidget(self.gammaEdit, row, 2)
        dialog.setLayout(self.layout)

        dialog.setWindowTitle("Image Info")

        QtCore.QMetaObject.connectSlotsByName(dialog)


"""
class UiDialog2(object):
    def __init__(self, dialog):

        self.separator4 = QtWidgets.QLabel(dialog)
        self.separator4.setAutoFillBackground(True)
        self.separator4.setAlignment(QtCore.Qt.AlignCenter)
        self.separator4.setMaximumHeight(50)
        self.separator4.setPalette(palette)
        ######################################################################
        self.separator4.setText("Spectrum Stack")

        row += 2
        self.layout.addWidget(self.separator4, row, 0, 1, 4)
        ######################################################################

        self.binXLabel = QtWidgets.QLabel('Bin X:')
        self.binXEdit = QtWidgets.QLineEdit('1')
        self.binXEdit.setValidator(valid_int)
        self.binXUnit = QtWidgets.QLabel('pixel')

        row += 1
        self.layout.addWidget(self.binXLabel, row, 0)
        self.layout.addWidget(self.binXEdit, row, 1)
        self.layout.addWidget(self.binXUnit, row, 2)

        self.binYLabel = QtWidgets.QLabel('Bin Y:')
        self.binYEdit = QtWidgets.QLineEdit('1')
        self.binYEdit.setValidator(valid_int)
        self.binYUnit = QtWidgets.QLabel('pixel')

        row += 1
        self.layout.addWidget(self.binYLabel, row, 0)
        self.layout.addWidget(self.binYEdit, row, 1)
        self.layout.addWidget(self.binYUnit, row, 2)

        dialog.setLayout(self.layout)

        dialog.setWindowTitle("Spectrum Info")

        QtCore.QMetaObject.connectSlotsByName(dialog)

"""
