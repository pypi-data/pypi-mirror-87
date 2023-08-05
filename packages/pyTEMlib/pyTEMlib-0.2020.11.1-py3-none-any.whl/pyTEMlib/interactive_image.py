"""
Interactive EELS provides dialogs for input
"""
import numpy as np

from PyQt5 import QtWidgets, QtCore, QtGui
import sidpy
import matplotlib.patches as patches
from matplotlib.widgets import SpanSelector

import matplotlib.pyplot as plt

from IPython.display import display
import ipywidgets as widgets
from skimage import exposure

from pyTEMlib import image_dlg
import pyTEMlib.file_tools as ft
import pyTEMlib.image_tools as it
from pyTEMlib.microscope import microscope

###

from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as Canvas


class ImageDialog(QtWidgets.QWidget):
    def __init__(self, dataset, parent=None):
        super(ImageDialog, self).__init__(parent, QtCore.Qt.WindowStaysOnTopHint)

        if dataset is None:
            # make a dummy dataset for testing
            dataset = ft.make_dummy_dataset(sidpy.DataTypes.IMAGE)
        if not isinstance(dataset, sidpy.Dataset):
            raise TypeError('dataset has to be a sidpy dataset')

        self.image_dims = ft.get_dimensions_by_type([sidpy.DimensionTypes.RECIPROCAL, sidpy.DimensionTypes.SPATIAL],
                                                    dataset)
        if len(self.image_dims) != 2:
            raise TypeError('We need exactly two SPATIAL or RECIPROCAL dimensions')
        self.dim_x = self.image_dims[0][1]
        self.dim_y = self.image_dims[1][1]
        self.fov_x = 0.
        self.fov_y = 0.
        self.v_min = np.array(dataset).min()
        self.v_max = np.array(dataset).max()

        self.parent = parent

        self.ui = image_dlg.UiDialog(self)

        self.set_action()

        self.dataset = dataset
        self.image = np.array(self.dataset)

        self.experiment = {}
        self.set_dataset()

        self.dataset.plot()
        if hasattr(self.dataset.view, 'axes'):
            self.axis = self.dataset.view.axes[-1]
        elif hasattr(self.dataset.view, 'axis'):
            self.axis = self.dataset.view.axis

        self.figure = self.axis.figure
        self.plot()
        self.histogram()

        self.update()

        self.spatial_dlg = None
        self.histogram()
        self.cid = self.ui.histogram.axes.figure.canvas.mpl_connect('button_press_event', self.onclick)

        self.show()

    def histogram(self, bins=256):
        ax_hist = self.ui.histogram.axes
        ax_hist.clear()

        hist, bin_edges = np.histogram(self.image, bins=bins, range=[self.v_min, self.v_max], density=True)
        ax_hist.plot(np.array(bin_edges)[:-1], np.array(hist))

        ax_hist.set_yticks([])
        self.span = SpanSelector(self.ui.histogram.axes, self.on_select, 'horizontal', useblit=False,
                                 button=1,
                                 rectprops=dict(alpha=0.5, facecolor='blue'))

        image = self.image * 1.0
        image[image < self.v_min] = self.v_min
        image[image > self.v_max] = self.v_max

        img_cdf, bins = exposure.cumulative_distribution(np.array(image), bins)
        ax_hist.plot(bins, img_cdf * hist.max(), 'r')
        ax_hist.figure.canvas.draw()

        self.plot()

    def onclick(self, event):
        if event.dblclick:
            self.v_min = np.array(self.image).min()
            self.v_max = np.array(self.image).max()
            self.histogram()

    def on_select(self, v_min, v_max):
        self.v_min = v_min
        self.v_max = v_max
        # self.setWindowTitle(f'{v_min:.1f}, {v_max:.1f}')
        self.histogram()

    def plot(self):
        ax = self.dataset.view.axis
        img = self.dataset.view.img
        img.set_data(self.image)
        img.set_clim(vmin=self.v_min, vmax=self.v_max)
        self.dataset.view.axis.figure.canvas.draw()

    def update(self):
        self.ui.fovXEdit.setText(f'{self.fov_x:.2f}')
        self.ui.fovYEdit.setText(f'{self.fov_y:.2f}')
        self.ui.timeEdit.setText(f"{self.experiment['exposure_time'] :.2f}")
        self.ui.E0Edit.setText(f"{self.experiment['acceleration_voltage']/1000.:.2f}")
        self.ui.collEdit.setText(f"{self.experiment['collection_angle']:.2f}")
        self.ui.convEdit.setText(f"{self.experiment['convergence_angle']:.2f}")
        self.ui.fluxEdit.setText(f"{self.experiment['flux']:.2f}")

    def set_dataset(self):
        extent = self.dataset.get_extent([self.image_dims[0][0], self.image_dims[1][0]])
        self.fov_x = extent[1]-extent[0]
        self.fov_y = extent[2]-extent[3]

        self.ui.fovXUnit.setText(self.dim_x.units)
        self.ui.fovYUnit.setText(self.dim_y.units)

        minimum_info = {'FOV_x': self.fov_x,
                        'FOV_y': self.fov_y,
                        'exposure_time': 0.0,
                        'convergence_angle': 0.0, 'collection_angle': 0.0,
                        'acceleration_voltage': 0.0,
                        'flux': 0.0}

        if 'experiment' not in self.dataset.metadata:
            self.dataset.metadata['experiment'] = {}
        if 'DM' in self.dataset.original_metadata:
            self.dataset.metadata['experiment'].update(it.read_dm3_image_info(self.dataset.original_metadata))

        self.experiment = self.dataset.metadata['experiment']
        for key, value in minimum_info.items():
            if key not in self.experiment:
                self.experiment[key] = value
    def on_enter(self):
        sender = self.sender()
        if sender == self.ui.E0Edit:
            self.experiment['acceleration_voltage'] = float(self.ui.E0Edit.displayText())
        elif sender == self.ui.collEdit:
            self.experiment['collection_angle'] = float(self.ui.collEdit.displayText())
        elif sender == self.ui.convEdit:
            self.experiment['convergence_angle'] = float(self.ui.convEdit.displayText())
        elif sender == self.ui.timeEdit:
            self.experiment['exposure_time'] = float(self.ui.timeEdit.displayText())
        elif sender == self.ui.fovXEdit:
            self.experiment['FOV_x'] = float(self.ui.fovXEdit.displayText())
        elif sender == self.ui.fovYEdit:
            self.experiment['FOV_y'] = float(self.ui.fovYEdit.displayText())
        elif sender == self.ui.fluxEdit:
            self.experiment['flux'] = float(self.ui.fluxEdit.displayText())
        self.update()

    def on_list_enter(self):
        sender = self.sender()
        if sender == self.ui.TEMList:
            microscope.set_microscope(self.ui.TEMList.currentText())
            self.experiment['microscope'] = microscope.name
            self.experiment['convergence_angle'] = microscope.alpha
            self.experiment['collection_angle'] = microscope.beta
            self.experiment['acceleration_voltage'] = microscope.E0
            self.update()


    def on_check_enter(self):
        sender = self.sender()
        if sender == self.ui.logCheck:
            if self.ui.logCheck.isChecked():
                self.ui.gammaCheck.setChecked(False)
                self.log_gamma = 1.0
                self.ui.gammaEdit.setText(f'{self.log_gamma:.2f}')
                self.image = np.log(1.0+np.array(self.dataset-self.dataset.min()+1e-12))
                self.image = np.nan_to_num(self.image)
                self.v_min = self.image.min()
                self.v_max = self.image.max()
            else:
                self.image = np.array(self.dataset-self.dataset.min())
                self.v_min = self.image.min()
                self.v_max = self.image.max()
            self.histogram()

        elif sender == self.ui.gammaCheck:
            if self.ui.gammaCheck.isChecked():
                self.ui.logCheck.setChecked(False)
                self.gamma = 0.8
                self.ui.gammaEdit.setText(f'{self.gamma:.2f}')
                self.image = np.array(self.dataset)**self.gamma
                self.v_min = self.image.min()
                self.v_max = self.image.max()
            else:
                self.image = np.array(self.dataset)
                self.v_min = self.image.min()
                self.v_max = self.image.max()
            self.histogram()

    def set_action(self):
        self.ui.fovXEdit.editingFinished.connect(self.on_enter)
        self.ui.fovYEdit.editingFinished.connect(self.on_enter)

        self.ui.timeEdit.editingFinished.connect(self.on_enter)
        self.ui.E0Edit.editingFinished.connect(self.on_enter)
        self.ui.collEdit.editingFinished.connect(self.on_enter)
        self.ui.convEdit.editingFinished.connect(self.on_enter)
        self.ui.fluxEdit.editingFinished.connect(self.on_enter)

        self.ui.TEMList.activated[str].connect(self.on_list_enter)

        self.ui.logCheck.clicked.connect(self.on_check_enter)
        self.ui.gammaCheck.clicked.connect(self.on_check_enter)
