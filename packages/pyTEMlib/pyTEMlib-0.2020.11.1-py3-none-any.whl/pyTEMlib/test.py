#####################################################################
#
# Part of Quantifit
#
### SI Dialog
### contains the dialog of the Spectrum Image
# - Set Slider : this does all the update things - rename for consistency
# - doAllClick : analyses full SI data set
# - onStoreClick: outpu in CVS file format
#
# #### Spectrum Image Analysis options effects 'SetSlider' and 'DoAll'
# -  QuantifitcheckClick
# -  LLcheckClick
# -  PeakFitClick
# -  EfixClick
#
####################################################################

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

import numpy as np
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as Canvas
from matplotlib.figure import Figure
import math as math
from matplotlib.widgets import RectangleSelector
import matplotlib.gridspec as gridspec
import matplotlib as mpl
from mpl_toolkits.axes_grid1 import make_axes_locatable

import os as os

import pyqtgraph as pg


# import pyqtgraph.opengl as gl


class MySICanvas(Canvas):
    def __init__(self, parent, width=10, height=10, dpi=100):
        self.figure = Figure(figsize=(width, height), dpi=dpi)
        self.figure.subplots_adjust(bottom=.2)
        Canvas.__init__(self, self.figure)
        self.setParent(parent)

        Canvas.setSizePolicy(self,
                             QSizePolicy.Expanding,
                             QSizePolicy.Expanding)

        Canvas.updateGeometry(self)


class SIDialog(QWidget):
    def __init__(self, parent):
        super(SIDialog, self).__init__(parent)
        self.parent = parent
        self.debug = 0

        foreMem = self.parent.tags['QF']['Fore']
        tags = self.parent.tags['QF'][str(foreMem)]
        si = self.parent.tags['QF']['SI'] = {}

        # self.nb = wx.aui.AuiNotebook(self)
        # sizer = wx.BoxSizer()
        si['Xsum'] = 0
        si['Ysum'] = 0
        si['Ssum'] = 0

        si['Xsize'] = 1
        si['Ysize'] = 1

        si['Xpos'] = 1
        si['Ypos'] = 1
        si['binning'] = 1
        si['Sliding Aver'] = 0

        si['select'] = []
        si['rectangles'] = {}
        self.rect = 0
        self.select = []
        self.col = QColor(0, 0, 0)

        '''
        self.square = QFrame(self)
        self.square.setGeometry(10, 70, 220, 220)
        self.square.setStyleSheet("QWidget { background-color: %s }" %  
            self.col.name())
        '''
        self.plotSIwin = MySICanvas(self.parent, width=10, height=10, dpi=70)

        # Defining a plot instance (axes) and asigning a variable to it
        self.plotSIwin.axes = self.plotSIwin.figure.add_subplot(1, 1, 1)
        self.plotSIwin.axes.set_axis_off()
        # self.plotSIwin.axes.hold(False)

        cid = self.plotSIwin.mpl_connect('button_press_event', self.onMouseButtonClick)

        # cid = self.plotSIwin.mpl_connect('button_release_event', self.onMouseReleaseClick)

        plotLayout = QGridLayout()

        # Ading SI image and sliders to the layout
        plotLayout.addWidget(self.plotSIwin, 0, 0)

        self.slider1 = QSlider(Qt.Horizontal, self)

        self.slider2 = QSlider(Qt.Vertical, self)

        self.slider1.valueChanged[int].connect(self.sliderUpdate)
        self.slider1.setMinimum(1)

        self.slider2.valueChanged[int].connect(self.sliderUpdate)
        self.slider2.setMinimum(1)

        plotLayout.addWidget(self.slider2, 0, 1)
        plotLayout.addWidget(self.slider1, 1, 0)

        # making a single widget out of image and slider
        siPlot = QWidget()
        siPlot.setLayout(plotLayout)

        layout = QGridLayout()
        layout.setVerticalSpacing(2)
        # self.setMaximumHeight(500)

        self.label = QLabel()
        self.label.setText(
            "<font style='color: white;background: blue;'>       Spectrum Image Sliders           </font>")
        layout.addWidget(self.label, 0, 0, 1, 3)
        layout.addWidget(siPlot, 1, 0, 1, 3)

        i = 10
        self.Xcheck = QCheckBox('sum X')
        layout.addWidget(self.Xcheck, i, 0)
        self.Xcheck.clicked.connect(self.XcheckClick)

        self.Ycheck = QCheckBox('sum Y')
        layout.addWidget(self.Ycheck, i, 1)
        self.Ycheck.clicked.connect(self.YcheckClick)

        self.Scheck = QCheckBox('selected')
        layout.addWidget(self.Scheck, i, 2)
        self.Scheck.clicked.connect(self.selectSumClick)

        i += 1
        self.sScheck = QCheckBox('show Sum')
        layout.addWidget(self.sScheck, i, 0)
        self.sScheck.setChecked(True)
        self.sScheck.clicked.connect(self.showSUMclick)

        self.sZcheck = QCheckBox('show Z')
        layout.addWidget(self.sZcheck, i, 1)
        self.sZcheck.clicked.connect(self.showZclick)

        self.sBcheck = QCheckBox('show BF')
        layout.addWidget(self.sBcheck, i, 2)
        self.sBcheck.clicked.connect(self.showBFclick)

        i += 1
        self.label2 = QLabel()
        self.label2.setText(
            "<font style='color: white;background: blue;'>       Spectrum Image Processing           </font>")
        layout.addWidget(self.label2, i, 0, 1, 3)
        self.setLayout(layout)

        i += 1
        self.QBinLabel = QLabel('Binning')
        layout.addWidget(self.QBinLabel, i, 0)
        self.binList = ['1x1', '2x2', '4x4']
        self.BinEList = QComboBox()
        self.BinEList.setEditable(False)
        self.BinEList.addItems(self.binList)
        self.BinEList.activated[str].connect(self.OnBinListEnter)
        layout.addWidget(self.BinEList, i, 1)
        self.QSlidecheck = QCheckBox('Sliding')
        layout.addWidget(self.QSlidecheck, i, 2)
        self.QSlidecheck.clicked.connect(self.SlidecheckClick)

        i += 1
        self.Qcheck = QCheckBox('QFit')
        layout.addWidget(self.Qcheck, i, 0)
        self.Qcheck.clicked.connect(self.QuantifitcheckClick)

        self.doAllButton = QPushButton("Do All")
        layout.addWidget(self.doAllButton, i, 1)
        self.doAllButton.clicked.connect(self.doAllClick)

        self.Lcheck = QCheckBox('LL')
        layout.addWidget(self.Lcheck, i, 2)
        self.Lcheck.clicked.connect(self.LLcheckClick)

        i += 1

        self.Pcheck = QCheckBox('PFit')
        layout.addWidget(self.Pcheck, i, 0)
        self.Pcheck.clicked.connect(self.PeakFitClick)

        self.storeButton = QPushButton("Store")
        layout.addWidget(self.storeButton, i, 1)
        # do not do anything, this is a dummy button
        self.storeButton.clicked.connect(self.OnStoreClick)

        self.Echeck = QCheckBox('Fix E')
        layout.addWidget(self.Echeck, i, 2)
        self.Echeck.clicked.connect(self.EfixClick)

        #
        # respond to changes in slider position ...
        #
        # self.Bind(wx.EVT_SLIDER, self.sliderUpdate)

        # self.SetSizerAndFit(sizer)

        self.setSlider()

    '''
        ####################################
        # Set Values
        ####################################
        self.R_outcheck.SetValue(parent.Rout)
        self.S_outcheck.SetValue(parent.Sout)
        self.R_verbosecheck.SetValue(parent.Vout)
    '''

    def OnBinListEnter(self):
        si = self.parent.tags['QF']['SI']
        eNum = self.BinEList.currentIndex()
        if eNum == 0:
            si['binning'] = 1
        if eNum == 1:
            si['binning'] = 2
        if eNum == 2:
            si['binning'] = 4
        print(eNum, self.binList[eNum])

    def SlidecheckClick(self):
        self.parent.tags['QF']['SI']['Sliding Aver'] = self.QSlidecheck.isChecked()

    def OnStoreClick(self):
        foreMem = self.parent.tags['QF']['Fore']
        qf = self.parent.tags['QF'][str(foreMem)]
        si = self.parent.tags['QF']['SI']

        height = si['data'].shape[1]
        width = si['data'].shape[0]

        if si['Xsum'] + si['Ysum'] > 0:
            if 'LS' not in qf['Results']:
                qf['Results']['LS'] = {}
            res = qf['Results']['LS']
            datashape = 1
        else:
            if 'SI' not in qf['Results']:
                qf['Results']['SI'] = {}
            res = qf['Results']['SI']
            datashape = 2

        eNum = qf['whichEdge']
        if eNum == 6:
            gtags = qf['GF']['LL']
        else:
            gtags = qf['GF'][str(eNum)]
            self.LLGauss = 0
        '''
        if si['Pcheck']:
            if qf['plotmode'] == 1:  # output in number of electrons
                scaleP = scaleP* qf['norm']
                unit = ' [# e-]'

            if qf['plotmode'] == 2:  # output in areal density
                multp = 1e10       #  xsec  is in barns = 10^28 m2 = 10^10 nm2
                scaleP = scaleP* qf['norm']*multp ## check this
                unit = ' [# atoms/nm2]'
            res['unitGFa'+str(eNum)] = unit  # Gerd implement
            res['scaleGFa'+str(eNum)] = scaleP
            nGauss = gtags['numGauss']
            x = int(si('Xpos'))
            y = int(si('Ypos'))

            for i in range(int(nGauss)):
                res['GF'+str(eNum)][x,y,i*3] = gtags['gaussF'][str(i)]['peakPos'] 
                res['GF'+str(eNum)][x,y,i*3+1] = gtags['gaussF'][str(i)]['peakAmpl'] * scaleP
                res['GF'+str(eNum)][x,y,i*3+2] = gtags['gaussF'][str(i)]['peakWidth']

        #plotSIoutput(self)

        if si['Qcheck']:
            res['GF']=self.pQF
        self.pQF[i,j,:] = self.parent.spec[foreMem].FitModel(0)
        '''
        import csv
        if datashape == 1:
            with open(qf['filename'] + '-LS.csv', 'w', newline='') as csvfile:
                xlwriter = csv.writer(csvfile, dialect='excel', delimiter=',', )
                xlwriter.writerow(['File Name', qf['filename']])
                res = qf['Results']['LS']

                xlwriter.writerow(['X-Scale', res['xscale']])
                xlwriter.writerow(['Y-units', res['unit']])
                xlwriter.writerow(['Y-scale', res['scale']])
                xlwriter.writerow(['Y-scaleP', res['scaleP']])

                #########################
                # Write titles
                #########################

                columns = 0
                title = []
                title.append('distance [' + si['Xunit'] + ']')

                if si['Qcheck'] > 0:

                    for i in range(int(qf['numberOfEdges'])):
                        columns += 1
                        title.append(res['QF-legend'][str(i)])
                    columns += 1
                    title.append('SUM')
                    for i in range(int(qf['numberOfEdges'])):
                        columns += 1
                        title.append(res['QF-legend'][str(i)] + '[atom%]')
                if si['Efix']:
                    columns += 1
                    title.append('Eshift')
                if si['LLcheck']:
                    columns += 1
                    title.append('ZL width')
                if si['Pcheck']:
                    for i in range(int(gtags['numGauss'])):
                        columns += 1
                        title.append('Peak ' + str(i + 1) + ' Position Edge' + str(eNum))
                        columns += 1
                        title.append('Peak ' + str(i + 1) + ' Area Edge' + str(eNum))
                        columns += 1
                        title.append('Peak ' + str(i + 1) + ' Width Edge' + str(eNum))

                xlwriter.writerow(title)
                #########################
                # Write Values
                #########################

                for l in range(res['Length']):
                    value = []

                    value.append('=' + str(l) + '*$B$2')
                    if si['Qcheck'] > 0:
                        numE = int(qf['numberOfEdges'])
                        sumE = 0
                        for i in range(numE):
                            value.append('=' + str(res['QF'][l, i]) + '*$B$4')
                            sumE += res['QF'][l, i]
                        value.append('=' + str(sumE) + '*$B$4')
                        for i in range(numE):
                            value.append('=' + str(res['QF'][l, i] / sumE * 100.0))

                    if si['Pcheck']:
                        for i in range(int(gtags['numGauss'])):
                            value.append('=' + str(res['GFp' + str(eNum)][l, i]))
                            value.append('=' + str(res['GFa' + str(eNum)][l, i]) + '*$B$5')
                            value.append('=' + str(res['GFw' + str(eNum)][l, i]))

                    xlwriter.writerow(value)
        if datashape == 2:

            with open(qf['filename'] + '-IM.csv', 'w', newline='') as csvfile:
                xlwriter = csv.writer(csvfile, dialect='excel', delimiter=',', )
                xlwriter.writerow(['File Name', qf['filename']])
                # xlwriter.writerow(['X-Scale',xscale])
                # xlwriter.writerow(['Z-units',res['unit']])
                # xlwriter.writerow(['Z-scale',res['scale']])
                # xlwriter.writerow(['Z-scaleP',res['scaleP']])

                for i in range(si['numOutImages']):
                    imI = si['images'][str(i)]
                    xlwriter.writerow([str(imI['name'])])
                    im = imI['image']
                    for j in range(im.shape[1]):
                        xlwriter.writerow(im[:, j])

    def setSlider(self):
        # print('setslider')

        foreMem = self.parent.tags['QF']['Fore']
        qf = self.parent.tags['QF'][str(foreMem)].tags

        si = self.parent.tags['QF']['SI']

        if 'LLSI' not in qf:
            qf['LLSI'] = 'False'

        def line_select_callback(eclick, erelease):
            'eclick and erelease are the press and release events'
            x1, y1 = eclick.xdata, eclick.ydata
            x2, y2 = erelease.xdata, erelease.ydata

            if self.debug > 0:
                print("(%3.2f, %3.2f) --> (%3.2f, %3.2f)" % (x1, y1, x2, y2))
                print(" The button you used were: %s %s" % (eclick.button, erelease.button))

            if x1 > x2:
                x1 = int(x2 + 0.5)
                x2 = int(x1 + 0.5)
            else:
                x1 = int(x1 + 0.5)
                x2 = int(x2 + 0.5)
            if y1 > y2:
                y1 = int(y2 + 0.5)
                y2 = int(y1 + 0.5)
            else:
                y1 = int(y1 + 0.5)
                y2 = int(y2 + 0.5)

            if erelease.button == 3:
                if self.parent.tags['QF']['SI']['Ssum'] > 0:
                    print("(%3.2f, %3.2f) --> (%3.2f, %3.2f)" % (x1, y1, x2, y2))
                    for i in range(x1, x2):
                        for j in range(y1, y2):
                            if (i, j) not in si['select']:
                                si['select'].append((i, j))
                                self.rect += 1
                                si['rectangles'][str(self.rect)] = [x1, y1, x2 - x1, y2 - y1]
                # print( si['select'])
                self.setSlider()

            if erelease.button == 1:
                if self.parent.tags['QF']['SI']['Ssum'] > 0:
                    si['select'] = []
                    print("(%d, %d) --> (%d, %d)" % (x1, y1, x2, y2))
                    for i in range(x1, x2):
                        for j in range(y1, y2):
                            self.rect = 0
                            if (i, j) not in si['select']:
                                si['select'].append((i, j))
                                self.rect = 1
                                si['rectangles'][str(self.rect)] = [x1, y1, x2 - x1, y2 - y1]
                print(si['select'])
                self.setSlider()

        def toggle_selector(event):
            if self.debug > 0:
                print(' Key pressed.')
            if event.key() in ['Q', 'q'] and toggle_selector.RS.active:
                print(' RectangleSelector deactivated.')
                toggle_selector.RS.set_active(False)
            if event.key() in ['A', 'a'] and not toggle_selector.RS.active:
                print(' RectangleSelector activated.')
                toggle_selector.RS.set_active(True)

        if 'Xpos' in si:

            # if self.debug > 0:
            # print(si['Xpos'],si['Ypos'])
            if si['Xpos'] < 1:
                si['Xpos'] = 1
            if si['Ypos'] < 1:
                si['Ypos'] = 1
            self.slider1.setMaximum(si['Xsize'])
            self.slider1.setMinimum(1)
            self.slider2.setMinimum(1)
            self.slider2.setMaximum(si['Ysize'])
            self.slider2.setInvertedAppearance(True)
            self.slider1.setTracking(True)
            self.slider2.setTracking(True)
            self.slider2.setTickPosition(QSlider.TicksRight)
            # self.slider2.setTickInterval(1)
            self.slider1.setTickPosition(QSlider.TicksBelow)

        ene = np.array(qf['ene']).copy()

        # self.plotSIwin.axes.hold(False)

        if 'data' in si:

            if len(si['data']) == 0:
                return
            if len(ene) != si['data'].shape[2]:
                qf.update(self.parent.tags['QF']['SI']['specTags'])
                ene = np.array(qf['ene']).copy()

            # print('print image')
            height = si['data'].shape[1]
            width = si['data'].shape[0]

            LSdisplay = False
            if height == 1:
                LSdisplay = True
                if self.debug > 0:
                    print('LS display')
            im = np.zeros((width, height, 3))
            title = []
            numOutImages = 0
            if 'showZ' not in si:
                si['showZ'] = False

            self.showZ = si['showZ']

            if 'showBF' not in si:
                si['showBF'] = False

            self.showBF = si['showBF']

            if 'showSum' not in si:
                si['showSum'] = False

            self.showSum = si['showSum']

            self.showZa = 0
            self.showBFa = 0
            self.showSuma = 0

            if self.showZ:
                self.showZa = 1
                # im[:,:,numOutImages] = np.array(si['Zcontrast']).copy()
                title.append('Z-contrast')
                numOutImages += 1
                if self.debug > 0:
                    print('add Z')

            if self.showBF:
                self.showBFa = 1
                # im[:,:,numOutImages] = (si['BrightField'])
                title.append('Bright Field')
                numOutImages += 1

            if self.showSum or numOutImages == 0:
                self.showSa = 1
                self.showSum = True
                im[:, :, numOutImages] = np.sum(si['data'], axis=2)
                title.append('sum')
                numOutImages += 1
            pl = self.plotSIwin
            pl.figure.clear()

            if LSdisplay:
                axes = pl.figure.add_subplot(1, 1, 1)
                data = np.sum(si['data'], axis=2)
                axes.plot(range(1, width + 1), data[:, 0])
                if self.debug > 0:
                    print('at do spectrum')
                si['Ypos'] = 1
                qf['spec'] = np.array(si['data'][si['Xpos'] - 1, 0, :]).copy()
                axes.plot(si['Xpos'], data[si['Xpos'] - 1, 0], 'o')
                qf['name'] = 'Spect. ' + str(si['Xpos'])

                # self.parent.SelectDialog.MemoryAssign(qf['spec'],ene,foreMem,1,qf['name'],qf)
                # self.plotSIwin.draw()

            else:
                debug = 0
                # print('Should not be here')
                ########### Determine Best Grid Layout #########
                grid_x = int(np.sqrt(height * width * numOutImages) / height + 0.5)
                if grid_x < 1:
                    grid_x = 1

                grid_y = math.ceil(numOutImages / grid_x)
                if self.debug > 0:
                    print(numOutImages, grid_x, grid_y)

                gs = gridspec.GridSpec(grid_x, grid_y)

                ######## initialize plot #####
                pl.figure.set_tight_layout(True)

                axes = []
                myImage = []
                index = 0

                ## plot figures
                for i in range(grid_x):
                    for j in range(grid_y):

                        axes.append(pl.figure.add_subplot(gs[i, j]))
                        if self.debug > 0:
                            print('index & numoutimages', index, numOutImages)

                        if self.showZa > 0:
                            myImage.append(axes[index].imshow(np.transpose(si['Zcontrast']), origin='upper', ))
                            self.showZa = 0
                            axes[index].set_title(title[index])
                        elif self.showBFa > 0:
                            myImage.append(axes[index].imshow(np.transpose(si['BrigthField']), origin='upper', ))
                            self.showBFa = 0
                            axes[index].set_title(title[index])
                        elif self.showSa > 0:
                            myImage.append(axes[index].imshow(np.transpose(im[:, :, index]), origin='upper', ))
                            # pl.figure.colorbar(myImage[index], ax=axes[index], orientation='vertical')
                            axes[index].set_title(title[index])
                            if self.debug > 0:
                                print(myImage[index])

                        index += 1
                        if index == numOutImages:
                            break
                    if index == numOutImages:
                        if self.debug > 0:
                            print(index)
                            print(im[:, :, index - 1])
                            print('drawing')
                        pl.draw()
                        break

                if self.debug > 0:
                    print('past drawing')
                # self.plotSIwin.axes.hold(True)

                # Make select array
                for i in range(numOutImages):
                    if self.debug > 0:
                        print(i, numOutImages)
                    myImage[i].set_extent((0.5, width + 0.5, height + 0.5, 0.5))

                    axes[i].set_xlim(0.5, width + 0.5)
                    axes[i].set_ylim(height + 0.5, +0.5)

                if self.debug > 0:
                    print('set limits drawing')

                '''
                if len(self.select) == 0:
                    self.select = np.zeros((height, width),'uint8')
                if height != self.select.shape[0]:
                    del(self.select)
                    self.select = np.zeros((height, width),'uint8')
                if width != self.select.shape[1] :
                    del(self.select)
                    self.select = np.zeros((height, width),'uint8')
                '''

                qf['expTime'] = si['expTime']
                if si['Xsum'] + si['Ysum'] == 0:
                    if self.debug > 0:
                        print('at do spectrum')
                    if 'spec' not in qf:
                        print('no spec')
                    qf['spec'] = np.zeros(len(qf['spec']))

                    for k in range(si['binning']):
                        for l in range(si['binning']):
                            if i + l < si['data'].shape[0]:
                                if j + k < si['data'].shape[1]:
                                    qf['spec'] = qf['spec'] + np.array(
                                        si['data'][si['Xpos'] - 1 + k, si['Ypos'] - 1 + l, :])
                                    qf['expTime'] = si['expTime'] * si['binning'] * si['binning']
                    if qf['LLSI'] == 'True':
                        qf['LorentzLL'] = np.array(si['LLdata'][si['Xpos'] - 1, si['Ypos'] - 1, :]).copy()
                    for i in range(numOutImages):
                        axes[i].plot(si['Xpos'], si['Ypos'], 'o')
                    qf['name'] = 'Spect. ' + str(si['Xpos']) + ',' + str(si['Ypos'])

                elif si['Xsum'] > 0:
                    if self.debug > 0:
                        print('xsum')
                    for j in range(numOutImages):
                        for i in range(1, si['data'].shape[0] + 1):
                            axes[j].plot(i, si['Ypos'], 'o')
                    cts = np.array(np.sum(si['data'], axis=0))
                    qf['spec'] = np.array(cts[si['Ypos'] - 1]).copy()
                    qf['name'] = 'Row ' + str(si['Ypos'])
                    qf['expTime'] = si['expTime'] * si['data'].shape[0]

                    if qf['LLSI'] == 'True':
                        llcts = np.array(np.sum(si['LLdata'], axis=0))
                        qf['LorentzLL'] = np.array(llcts[si['Ypos'] - 1]).copy()

                if si['Ysum'] > 0:
                    for j in range(numOutImages):
                        for i in range(1, si['data'].shape[1] + 1):
                            axes[j].plot(si['Xpos'], i, 'o')
                    cts = np.array(np.sum(si['data'], axis=1))
                    qf['expTime'] = si['expTime'] * si['data'].shape[1]

                    qf['spec'] = np.array(cts[si['Xpos'] - 1]).copy()
                    qf['name'] = 'Column ' + str(si['Xpos'])

                    if qf['LLSI'] == 'True':
                        llcts = np.array(np.sum(si['LLdata'], axis=1))
                        qf['LorentzLL'] = np.array(llcts[si['Xpos'] - 1]).copy()

                if si['Ssum'] > 0:
                    if self.rect > 0:
                        self.parent.text2.insertPlainText('\n rectangles of Selected Spectra: ')
                        for i in range(self.rect):
                            pos = si['rectangles'][str(i + 1)]
                            self.parent.text2.insertPlainText(str(pos[2]) + ' x ' + str(pos[3]) + ',')
                            rect = mpl.patches.Rectangle((pos[0], pos[1]), pos[2], pos[3], alpha=0.350, ec='black',
                                                         fc="Blue")
                            for j in range(numOutImages):
                                axes[j].add_patch(rect)
                        spec = np.zeros(len(qf['spec']))
                        self.parent.text2.insertPlainText('\n Selected Spectra: ')
                        k = 0
                        for pos in si['select']:
                            k += 1
                            fp = np.array(si['data'][pos[0] - 1, pos[1] - 1, :])
                            if si['Efix']:
                                pG = self.parent.tags['QF'][foreMem].fixE(fp)
                                if k == 1:
                                    qf['ene'] = qf['ene'] - pG[1]

                                else:
                                    x = qf['ene'] - pG[1]
                                    fp = np.interp(x, qf['ene'], fp)
                            spec = spec + fp  # Gerd May need a -1

                            self.parent.text2.insertPlainText(str(pos) + ' , ')
                        qf['expTime'] = si['expTime'] * k

                        qf['spec'] = spec
                        qf['name'] = 'Selected'

                toggle_selector.RS = RectangleSelector(axes[0], line_select_callback,
                                                       drawtype='box', useblit=True,
                                                       button=[1, 3],  # don't use middle button
                                                       minspanx=5, minspany=5,
                                                       spancoords='pixels')
                self.plotSIwin.mpl_connect('key_press_event', toggle_selector)



        else:
            if self.debug > 0:
                print('no data did not do anything')
            return

        self.parent.tags['QF'][str(foreMem)].SetConv()
        # MemoryAssign(self,key,mem,fore,bank,name,spectrum)
        self.parent.SelectDialog.MemoryAssign('spec', foreMem, 1, 'QF', qf['name'], foreMem)
        # print(self.parent.tags['QF'][]
        ypos = si['Ypos']
        self.slider1.setValue(si['Xpos'])

        self.slider2.setValue(ypos)
        si['Ypos'] = ypos

        self.plotSIwin.draw()

        ## Current Spectrum Analysis

        if 'LLcheck' not in si:
            si['LLcheck'] = False
        if 'Qcheck' not in si:
            si['Qcheck'] = False
        if 'Pcheck' not in si:
            si['Pcheck'] = False
        if 'Efix' not in si:
            si['Efix'] = False

        self.Lcheck.setCheckState(si['LLcheck'])
        self.Qcheck.setCheckState(si['Qcheck'])
        self.Pcheck.setCheckState(si['Pcheck'])
        self.Echeck.setCheckState(si['Efix'])
        self.Xcheck.setCheckState(si['Xsum'])
        # print ('XSum ' , si['Xsum'])
        self.Ycheck.setCheckState(si['Ysum'])
        self.sZcheck.setCheckState(si['showZ'])
        self.sBcheck.setCheckState(si['showBF'])
        self.sScheck.setCheckState(si['showSum'])

        if si['Efix']:
            self.parent.LLDialog.OnEFixClick()
        if si['LLcheck']:
            self.parent.LLDialog.OnSSDClick()

        if si['Qcheck']:
            self.parent.QuantifitDialog.QuantifitClick()
            if self.debug > 0:
                print('Qcheck')
        if si['Pcheck']:
            self.parent.gFitDialog.GaussFitClick()

        self.parent.text2.ensureCursorVisible()
        self.parent.plotUpdate('Select')
        self.parent.tags['QF']['SI']['specTags'] = qf
        if self.debug > 0:
            print('update')

    def keyPressEvent(self, event):

        si = self.parent.tags['QF']['SI']
        # QMessageBox.information(None,"Received Key Press Event!!","You Pressed: "+ event.text())
        signals = ['u', 'd', 'l', 'r', '4', '2', '8', '6']
        move = event.text()

        # print(event.text())
        # print(event.key())

        if '1' in si['rectangles']:
            print(si['rectangles']['1'])
        if event.text() not in signals:
            if event.key() == 16777234:
                move = 'left'
            elif event.key() == 16777236:
                move = 'right'
            elif event.key() == 16777235:
                move = 'up'
            elif event.key() == 16777237:
                move = 'down'
        else:
            if move == '2' or move == 'd':
                move = 'down'
            elif move == '8' or move == 'u':
                move = 'up'
            elif move == '4' or move == 'l':
                move = 'left'
            elif move == '6' or move == 'r':
                move = 'right'
        if self.rect == 1:
            if move == 'left':
                print('event l')
                si['rectangles'][str(1)][0] = si['rectangles'][str(1)][0] - 1
                if si['rectangles'][str(1)][0] < 1:
                    si['rectangles'][str(1)][0] = 1
            elif move == 'right':
                print('event r')
                si['rectangles'][str(1)][0] = si['rectangles'][str(1)][0] + 1
                if si['rectangles'][str(1)][0] < 1:
                    si['rectangles'][str(1)][0] = 1
            elif move == 'up':
                print('event u')
                si['rectangles'][str(1)][1] = si['rectangles'][str(1)][1] - 1
                if si['rectangles'][str(1)][1] < 1:
                    si['rectangles'][str(1)][1] = 1
            elif move == 'down':
                print('event d')
                si['rectangles'][str(1)][1] = si['rectangles'][str(1)][1] + 1
                if si['rectangles'][str(1)][1] < 1:
                    si['rectangles'][str(1)][1] = 1
            si['select'] = []
            for i in range(si['rectangles'][str(1)][0], si['rectangles'][str(1)][0] + si['rectangles'][str(1)][2]):
                for j in range(si['rectangles'][str(1)][1], si['rectangles'][str(1)][1] + si['rectangles'][str(1)][3]):
                    si['select'].append((i, j))
            self.setSlider()
        else:
            if 'Xpos' in si:
                if move == 'left':
                    si['Xpos'] -= 1
                if move == 'right':
                    si['Xpos'] += 1
                    if si['Xpos'] > si['data'].shape[0]:
                        si['Xpos'] = si['data'].shape[0]
                if move == 'up':
                    si['Ypos'] -= 1
                if move == 'down':
                    si['Ypos'] += 1
                    if si['Ypos'] > si['data'].shape[1]:
                        si['Ypos'] = si['data'].shape[1]
                self.setSlider()
                # self.slider1.setValue(si['Xpos'])
                # self.slider2.setValue(si['Ypos'])

    def QuantifitcheckClick(self):
        self.parent.tags['QF']['SI']['Qcheck'] = self.Qcheck.isChecked()

    def LLcheckClick(self):
        self.parent.tags['QF']['SI']['LLcheck'] = self.Lcheck.isChecked()

    def PeakFitClick(self):
        self.parent.tags['QF']['SI']['Pcheck'] = self.Pcheck.isChecked()

    def EfixClick(self):
        self.parent.tags['QF']['SI']['Efix'] = self.Echeck.isChecked()

    def showBFclick(self):
        self.showBF = self.sBcheck.isChecked()
        si = self.parent.tags['QF']['SI']

        if 'showBF' not in si:
            si['showBF'] = True

        if si['showBF']:
            si['showBF'] = False
        else:
            si['showBF'] = True

        self.showBF = si['showBF']

        if self.showBF:

            if len(si['BrightField']) == 0:
                if self.debug > 0:
                    print(' read  image')
                try:
                    path = settings.value("path")
                    if self.debug > 0:
                        print('Found  path ' + path)
                except:
                    print('path not read')
                filename, filters = QFileDialog.getOpenFileName(self,
                                                                'Open a Bright field Image', self.parent.path,
                                                                'DM files (*.dm3);;QF files (*.qf3);;QF session (*.qfs);;All Files (*.*)')

                self.parent.path, fname = os.path.split(filename)
                extension = os.path.splitext(filename)[1][1:]
                if extension == 'dm3':
                    si['BrightField'] = self.parent.readdm3Image(filename)
                    self.setSlider()
                else:
                    self.sBcheck.toggle()
                    self.showBF = False
                    si['showBF'] = self.showBF
                    return
        self.setSlider()

    def showZclick(self):

        self.showZ = self.sZcheck.isChecked()
        si = self.parent.tags['QF']['SI']

        if 'showZ' not in si:
            si['showZ'] = True

        if si['showZ']:
            si['showZ'] = False
        else:
            si['showZ'] = True

        self.showZ = si['showZ']
        if self.showZ:
            if len(si['Zcontrast']) == 0:
                if self.debug > 0:
                    print(' read Zcontrast image')
                try:
                    path = settings.value("path")
                    if self.debug > 0:
                        print('Found  path ' + path)
                except:
                    print('path not read')
                filename, filters = QFileDialog.getOpenFileName(self,
                                                                'Open a spectrum', self.parent.path,
                                                                'DM files (*.dm3);;QF files (*.qf3);;QF session (*.qfs);;All Files (*.*)')

                self.path, fname = os.path.split(filename)
                extension = os.path.splitext(filename)[1][1:]
                if extension == 'dm3':
                    si['Zcontrast'] = self.parent.readdm3Image(filename)
                    self.setSlider()
                else:
                    self.sZcheck.toggle()
                    self.showZ = False
                    si['showZ'] = self.showZ
                    return

        self.setSlider()

        # 0516

    def showSUMclick(self):
        si = self.parent.tags['QF']['SI']
        if 'showSum' not in si:
            si['showSum'] = True

        if si['showSum']:
            si['showSum'] = False
        else:
            si['showSum'] = True
        self.showSum = self.sScheck.isChecked()
        self.showSum = si['showSum']
        self.setSlider()

    #########################################
    ### 1D data plotting #############
    #####################################
    def plotSI(self):
        print('1D data plotting')
        foreMem = self.parent.tags['QF']['Fore']
        qf = self.parent.tags['QF'][str(foreMem)].tags
        si = self.parent.tags['QF']['SI']

        eNum = qf['whichEdge']
        if eNum == 6:
            gtags = qf['GF']['LL']
        else:
            gtags = qf['GF'][str(eNum)]
            self.LLGauss = 0

        height = si['data'].shape[1]
        width = si['data'].shape[0]

        spec = qf['spec']

        # we do LS data first and define resolution dictionary as such
        if 'LS' not in qf['Results']:
            return
        res = qf['Results']['LS']

        xscale = res['xscale']
        dimen = res['Length']

        # Here OUTPUT BEGINS

        if self.parent.tab.tabText(2) == 'SI':
            plot = pg.PlotItem()

        self.parent.plotParamWindow3 = pg.GraphicsWindow()
        plot = self.parent.plotParamWindow3
        plot3 = QWidget()
        plotLayout3 = QVBoxLayout()
        plotLayout3.addWidget(plot)
        plot3.setLayout(plotLayout3)

        self.parent.tab.removeTab(2)
        self.parent.tab.insertTab(2, plot3, 'SI LS')

        self.parent.tab.setCurrentIndex(2)
        plot = self.parent.plotParamWindow3
        # plot.clear()
        col = self.parent.tags['QF']['Colors']
        lin = self.parent.tags['QF']['LineWidth']

        # Enable antialiasing for prettier plots
        pg.setConfigOptions(antialias=True)

        #########################################################
        ## Output to SI Window
        #########################################################

        scale = np.ones((dimen))
        scaleP = 1.0
        unit = 'counts'
        if si['Qcheck']:

            if qf['plotmode'] == 0:  # output in atom %
                if np.sum(self.pQF[:, 0:qf['numberOfEdges']], axis=1).any == 0:
                    scale = scale * 100.0 / (np.sum(self.pQF[:, 0:qf['numberOfEdges']], axis=1) + 1)
                else:
                    scale = scale * 100.0 / (np.sum(self.pQF[:, 0:qf['numberOfEdges']], axis=1) + 1)
                unit = ' [atom %]'
            if qf['plotmode'] == 1:  # output in number of electrons
                scale = scale * qf['norm']
                unit = ' [# e-]'

            if qf['plotmode'] == 2:  # output in areal density
                multp = 1e10  # xsec  is in barns = 10^28 m2 = 10^10 nm2
                scale = scale * qf['norm'] * multp  ## check this
                unit = ' [# atoms/nm2]'

        if si['Pcheck']:
            if qf['plotmode'] == 1:  # output in number of electrons
                scaleP = scaleP * qf['norm']
                unit = ' [# e-]'

            if qf['plotmode'] == 2:  # output in areal density
                multp = 1e10  # xsec  is in barns = 10^28 m2 = 10^10 nm2
                scaleP = scaleP * qf['norm'] * multp  ## check this
                unit = ' [# atoms/nm2]'

        res['unit'] = unit
        res['scale'] = scale
        res['scaleP'] = scaleP

        bins = np.linspace(0, dimen * xscale, dimen)  # *height/len(data)

        # Here OUTPUT BEGINS

        plot = self.parent.plotParamWindow3
        # plot.figure.clear()
        col = self.parent.tags['QF']['Colors']
        lin = self.parent.tags['QF']['LineWidth']

        numOutImages = 0

        if si['Qcheck'] > 0:
            numOutImages = 1
            '''
            if si['Pcheck']:
                plot.axes  =  plot.figure.add_subplot(numOutImages+3,1,numOutImages+1)
            else:
                plot.axes  =  plot.figure.add_subplot(1,1,1)
            '''
            res['QF-legend'] = {}
            self.parent.text2.insertPlainText('\n Edge \t Median (' + unit + ') \t median abs dev \t std dev')
            p1 = plot.addPlot(title=' Chemical Composition')
            for i in range(int(qf['numberOfEdges'])):
                titleStr = qf['edgeXtags'][str(i)]['element']
                titleStr += '-'
                titleStr += qf['edgeXtags'][str(i)]['subshell']
                res['QF-legend'][str(i)] = titleStr
                # plot.axes.plot(bins, res['QF'][:,i]*scale ,color=col[str(numOutImages)],linewidth = lin[str(numOutImages)], label =titleStr)
                # curve = pg.PlotCurveItem(bins, res['QF'][:,i]*scale, stepMode=False, fillLevel=0, pen = ( col[str(i)]),  brush=(col[str(foreMem)]), padding = 0)

                curve1 = pg.PlotCurveItem(bins, res['QF'][:, i] * scale, stepMode=False, padding=0, name=titleStr)
                curve1.setPen(pg.mkPen(col[str(i)], width=lin[str(i)]))
                # plot.addItem(curve1)
                self.parent.text2.insertPlainText('\n {0:s} \t  {1:3.3f} eV \t {2:3.3f} \t {3:3.3f}'
                                                  .format(titleStr, np.median(res['QF'][:, i] * scale), np.median(
                    abs(res['QF'][:, i] * scale - np.median(res['QF'][:, i] * scale)) / 0.6745),
                                                          float(np.std(res['QF'][:, i] * scale))))

                p1.plot(bins, res['QF'][:, i] * scale, pen=(col[str(i)]))
                # p1.setPen(pg.mkPen(col[str(i)], width=lin[str(i)]))
                numOutImages += 1
                # plot.show()
                print(i)
            if self.parent.show:
                p1.addLegend()
            '''if si['showZ'] >0:
                ## create a new ViewBox, link the right axis to its coordinate system
                p2 = pg.ViewBox()
                plot.showAxis('right')
                plot.scene().addItem(p2)
                plot.getAxis('right').linkToView(p2)
                p2.setXLink(plot)
                plot.getAxis('right').setLabel('Z-contrast', color='#0000ff')
                p2.addItem((curve1))
            '''
            p1.setLabel('bottom', "distance", units='nm')  # si['Xunit'])
            p1.setLabel('left', "chemical compositon", units=res['unit'])
            plot.nextRow()
        if si['Pcheck']:

            self.parent.text2.insertPlainText('\n Peak \t parameter \t Median  \t median abs dev \t std dev')

            p1 = plot.addPlot(title=' Peak Position')
            plot.nextRow()
            p2 = plot.addPlot(title=' Peak Area ')
            plot.nextRow()
            p3 = plot.addPlot(title=' Peak Width')

            plot.nextRow()
            # plot.axes1  =  plot.figure.add_subplot(numOutImages+3,1,numOutImages+1)
            # plot.axes2  =  plot.figure.add_subplot(numOutImages+3,1,numOutImages+2)
            # plot.axes3  =  plot.figure.add_subplot(numOutImages+3,1,numOutImages+3)
            for i in range(int(gtags['numGauss'])):
                titleStr = ' Peak ' + str(i + 1)
                p1.plot(bins, res['GFp' + str(eNum)][:, i], pen=col[str(i)], linewidth=lin[str(numOutImages)],
                        name=titleStr)
                p2.plot(bins, res['GFa' + str(eNum)][:, i] * scaleP, pen=col[str(i)], linewidth=lin[str(numOutImages)],
                        name=titleStr)
                p3.plot(bins, res['GFw' + str(eNum)][:, i], pen=col[str(i)], linewidth=lin[str(numOutImages)],
                        name=titleStr)

                self.parent.text2.insertPlainText('\n {0:2d} \t position \t {1:3.3f} eV \t {2:3.3f} \t {3:3.3f}'
                                                  .format(i, np.median(res['GFp' + str(eNum)][:, i]), np.median(
                    abs(res['GFp' + str(eNum)][:, i] - np.median(res['GFp' + str(eNum)][:, i])) / 0.6745),
                                                          float(np.std(res['GFp' + str(eNum)][:, i]))))
                self.parent.text2.insertPlainText('\n \t width \t {1:3.3f} eV \t {2:3.3f} \t {3:3.3f}'
                                                  .format(i, np.median(res['GFw' + str(eNum)][:, i]), np.median(
                    abs(res['GFw' + str(eNum)][:, i] - np.median(res['GFw' + str(eNum)][:, i])) / 0.6745),
                                                          float(np.std(res['GFw' + str(eNum)][:, i]))))
                self.parent.text2.insertPlainText('\n  \t area \t {1:3.3f}   \t {2:3.3f} \t {3:3.3f}'
                                                  .format(unit, np.median(res['GFa' + str(eNum)][:, i]) * scaleP,
                                                          np.median(abs(res['GFa' + str(eNum)][:, i] - np.median(
                                                              res['GFa' + str(eNum)][:, i])) / 0.6745) * scaleP,
                                                          float(np.std(res['GFa' + str(eNum)][:, i])) * scaleP))

                numOutImages += 1

            print(si['Xunit'])
            p3.setLabel('bottom', "distance", units='nm')  # si['Xunit'])
            p1.setLabel('left', "position", units='eV')
            p2.setLabel('left', "area", units=unit)
            p3.setLabel('left', "width", units='eV')

            if self.parent.show:
                p1.addLegend()
                p2.addLegend()
                p3.addLegend()

        if self.showZ > 0:
            p1 = plot.addPlot(title='Image')
            plot.nextRow()
            numOutImages = 0
            if si['Xsum']:
                data = np.sum(si['Zcontrast'], axis=0)
            else:
                data = np.sum(si['Zcontrast'], axis=1)
            data = data - data.min()
            sc = 100.0 / np.max(data)
            bins = np.linspace(0, dimen * xscale, len(data))  # *height/len(data)
            p1.plot(bins, data * sc, pen=col[str(numOutImages)], linewidth=lin[str(numOutImages)], name='Z contrast')

            if self.debug > 0:
                print(len(data), len(bins), data.shape, sc)
            if si['showSum'] > 0:
                numOutImages += 1
                ssum = np.sum(si['data'], axis=2)
                if si['Xsum']:
                    data = np.sum(ssum, axis=0)
                else:
                    data = np.sum(ssum, axis=1)
                data = data - data.min()
                sc = 100.0 / np.max(data)
                p1.plot(bins, data * sc, pen=col[str(numOutImages)], linewidth=lin[str(numOutImages)],
                        name='Spectrum Sum')

                p1.setLabel('left', 'Contrast', units='%')
                if self.parent.show:
                    p1.addLegend()

        self.parent.text2.ensureCursorVisible()
        # plot.draw()

        if 'Sout' not in self.parent.tags:
            self.parent.tags['Sout'] = False

        if self.parent.tags['Sout']:
            import csv
            with open(qf['filename'] + '-LS.csv', 'w', newline='') as csvfile:
                xlwriter = csv.writer(csvfile, dialect='excel', delimiter=',', )
                xlwriter.writerow(['File Name', qf['filename']])

                xlwriter.writerow(['X-Scale', xscale])
                xlwriter.writerow(['Y-units', res['unit']])
                xlwriter.writerow(['Y-scale', res['scale']])
                xlwriter.writerow(['Y-scaleP', res['scaleP']])

                #########################
                # Write titles
                #########################

                columns = 0
                title = []
                title.append('distance [' + si['Xunit'] + ']')

                if si['Qcheck'] > 0:

                    for i in range(int(qf['numberOfEdges'])):
                        columns += 1
                        title.append(res['QF-legend'][str(i)])
                    columns += 1
                    title.append('SUM')
                    for i in range(int(qf['numberOfEdges'])):
                        columns += 1
                        title.append(res['QF-legend'][str(i)] + '[atom%]')
                if si['Efix']:
                    column += 1
                    title.append('Eshift')
                if si['LLcheck']:
                    column += 1
                    title.append('ZL width')
                if si['Pcheck']:
                    for i in range(int(gtags['numGauss'])):
                        column += 1
                        title.append('Peak ' + str(i + 1) + ' Position Edge' + str(eNum))
                        column += 1
                        title.append('Peak ' + str(i + 1) + ' Area Edge' + str(eNum))
                        column += 1
                        title.append('Peak ' + str(i + 1) + ' Width Edge' + str(eNum))

                xlwriter.writerow(title)
                #########################
                # Write Values
                #########################

                for l in range(dimen):
                    value = []

                    value.append('=' + str(l) + '*$B$2')
                    if si['Qcheck'] > 0:
                        numE = int(qf['numberOfEdges'])
                        sumE = 0
                        for i in range(numE):
                            value.append('=' + str(res['QF'][l, i]) + '*$B$4')
                            sumE += res['QF'][l, i]
                        value.append('=' + str(sumE) + '*$B$4')
                        for i in range(numE):
                            value.append('=' + str(res['QF'][l, i] / sumE * 100.0))

                    if si['Pcheck']:
                        for i in range(int(gtags['numGauss'])):
                            value.append('=' + str(res['GFp' + str(eNum)][l, i]))
                            value.append('=' + str(res['GFa' + str(eNum)][l, i]) + '*$B$5')
                            value.append('=' + str(res['GFw' + str(eNum)][l, i]))

                    xlwriter.writerow(value)

    def doAllClick(self):

        ## Define dictionaries and important dimensions

        foreMem = self.parent.tags['QF']['Fore']
        qf = self.parent.tags['QF'][str(foreMem)].tags
        qfspec = self.parent.tags['QF'][str(foreMem)]

        multSpec = qf['norm']
        multS = qf['multS']
        multFac = multSpec * multS

        si = self.parent.tags['QF']['SI']
        if 'SI' not in qf['Results']:
            qf['Results']['SI'] = {}
        height = si['data'].shape[1]
        width = si['data'].shape[0]

        spec = qf['spec']

        # we do LS data first and define resolution dictionary as such
        if 'LS' not in qf['Results']:
            qf['Results']['LS'] = {}
        res = qf['Results']['LS']

        eNum = qf['whichEdge']
        if eNum == 6:
            gtags = qf['GF']['LL']
        if eNum == 7:
            gtags = qf['GF']['EG']
        else:
            gtags = qf['GF'][str(eNum)]
            self.LLGauss = 0

        if si['Xsum'] + si['Ysum'] > 0:
            ##########################################
            ####### 1 D Data Analysis ################
            ##########################################
            if (si['Xsum'] + si['Ysum']) > 1:
                qf['name'] = 'SI Sum'
                qf['spec'] = np.array(np.sum(cts, axis=0))
                return
            xscale = float(si['Xscale'])

            # dimension of Output arrays or matrices

            if si['Xsum'] > 0:
                data = np.sum(si['data'], axis=0)
                dimen = height
                res['X'] = 1
                res['Y'] = 0
            if si['Ysum'] > 0:
                data = np.sum(si['data'], axis=1)
                dimen = width
                res['X'] = 0
                res['Y'] = 1

            if si['Efix']:
                self.pELL = np.zeros((dimen, 2))
            if si['LLcheck'] > 0:
                self.pZL = np.zeros((dimen, 9))

            if si['Qcheck'] > 0:
                self.pQF = np.zeros((dimen, 13))

            if si['Pcheck']:
                p = self.parent.gFitDialog.GaussFit(qf['spec'], qf['spec'], qf['pGF'])

                s = len(p)
                self.pGF = np.zeros((dimen, s))
                self.pGFp = np.zeros((dimen, s))
                self.pGFa = np.zeros((dimen, s))
                self.pGFw = np.zeros((dimen, s))

            # --------------------------------------------------
            # Main loop over data
            # --------------------------------------------------
            for i in range(dimen):

                qf['spec'] = data[i, :].copy()

                if si['Efix']:
                    pG = self.parent.spec[foreMem].fixE(qf['spec'])
                    self.pELL[i, j, :] = pG
                    qf['ene'] = qf['ene'] - pG[1]
                    print('Efix ', qf['ene'][0])

                if si['LLcheck']:
                    # self.parent.LLDialog.OnResolutionClick()
                    # print(qf['pZL'])
                    tmfp = self.parent.spec[foreMem].doSSD(qf['spec'])
                    # self.parent.LLDialog.OnSSDClick()
                    self.pZL[i, 0] = tmfp
                    self.pZL[i, 1] = qf['ZL FWHM']
                    self.pZL[i, 2] = qf['ZL Max']
                    self.pZL[i, 3] = qf['Drude P Pos']
                    self.pZL[i, 4] = qf['Drude P Width']
                    self.pZL[i, 5] = qf['Drude P thick']
                    self.pZL[i, 6] = qf['Drude P Assym']
                    self.pZL[i, 7] = qf['Drude P Probab'] * 100.0
                    self.pZL[i, 8] = qf['Drude P IMFP']

                if si['Qcheck']:
                    self.pQF[i, :] = np.array(self.parent.spec[foreMem].FitModel(0))[0:13]

                if si['Pcheck']:
                    self.pGF[i, :] = p[0:s]
                    p = self.parent.gFitDialog.GaussFit(qf['spec'], qf['spec'], qf['pGF'])
                    if self.debug > 0:
                        print('Spec ', i, ': ', p[0], p[1], p[2])
                    # self.parent.gFitDialog.GaussFitClick()
                    self.pGF[i, :] = p[0:s]  # qf['pGF']
                    for j in range(int(gtags['numGauss'])):
                        self.pGFp[i, j] = p[3 * j]
                        self.pGFa[i, j] = p[3 * j + 1]
                        self.pGFw[i, j] = p[3 * j + 2]

                    # print(self.pQF[i,:])

            #########################################################
            ## Save output to Result Dictionary
            #########################################################
            res['Length'] = dimen
            res['xscale'] = xscale
            if si['Efix']:
                res['Efix'] = self.pELL

            if si['LLcheck']:
                res['LL'] = self.pZL

            if si['Pcheck']:
                res['GFp' + str(eNum)] = self.pGFp
                res['GFa' + str(eNum)] = self.pGFa * multFac / 10000.0
                res['GFw' + str(eNum)] = self.pGFw

            if si['Qcheck']:
                res['QF'] = self.pQF

            # if si['LLcheck'] == 0:
            #   self.pZL = np.zeros((dimen,9))

            # reset to original state

            qf['spec'] = spec
            self.setSlider()
            self.plotSI()
            return

        ############################################
        ## 2D SI Evaluation
        #############################################

        numOutImages = 0
        if 'SI' not in qf['Results']:
            qf['Results']['SI'] = {}

        res = qf['Results']['SI']
        if self.showSum:
            numOutImages += 1  # sum of spectra

        if self.showZ:
            numOutImages += 1
        if self.showBF:
            numOutImages += 1

        oimages = numOutImages

        if si['Efix']:
            self.pELL = np.zeros((width, height, 2))
            # numOutImages = oimages+ 2
            numOutImages += 2

            pos = np.zeros((width, height))

        if si['LLcheck'] > 0:
            self.pZL = np.zeros((width, height, 9))
            pos = np.zeros((width, height))

            numOutImages += 9
        if si['Qcheck'] > 0:
            self.pQF = np.zeros((width, height, 13))
            pos = np.zeros((width, height))
            # numOutImages = oimages+int(qf['numberOfEdges'])
            numOutImages += int(qf['numberOfEdges'])
        if si['Pcheck']:
            nGauss = gtags['numGauss']
            p = self.parent.gFitDialog.GaussFit(qf['spec'], qf['spec'], qf['pGF'])

            s = len(p)
            self.pGF = np.zeros((width, height, s))
            # numOutImages = int(gtags['numGauss'])*3 #but we take position only now
            numOutImages += int(nGauss * 3)  # we could also use other values like times xsec.

            p = np.zeros(s)
        ritesh = 0

        si['numOutImages'] = numOutImages

        step = si['binning']
        stepI = step
        if si['Sliding Aver'] > 0:
            stepI = 1
        ene = qf['ene']

        for j in range(0, height, stepI):
            print('spectrum image line: ', j)
            if self.debug > 0:
                self.parent.status.showMessage(" row: " + str(j))
                # print('row ',j)
            for i in range(0, width, stepI):

                if ritesh:
                    if i + j == 0:
                        i = i + 1
                        print('Omitting first spectrum, do second twice')

                qf['spec'] = np.zeros(len(qf['spec']))
                for k in range(step):
                    for l in range(step):
                        if i + l < si['data'].shape[0]:
                            if j + k < si['data'].shape[1]:
                                qf['spec'] = qf['spec'] + si['data'][i + l, j + k, :]

                if si['Efix']:
                    qf['ene'] = ene.copy()
                    qf['offset'] = ene[0]
                    pG = qfspec.fixE(qf['spec'])
                    self.pELL[i, j, :] = pG
                    qf['ene'] = ene - pG[1]
                    # print(qf['ene'][0],ene[0], pG)

                if si['LLcheck']:
                    # self.parent.LLDialog.OnResolutionClick()
                    # print(qf['pZL'])

                    tmfp = qfspec.doSSD(qf['spec'])
                    # tmfp = self.parent.LLDialog.OnSSDClick()

                    self.pZL[i, j, 0] = tmfp
                    self.pZL[i, j, 1] = qf['ZL FWHM']
                    self.pZL[i, j, 2] = qf['ZL Max']
                    self.pZL[i, j, 3] = qf['Drude P Pos']
                    self.pZL[i, j, 4] = qf['Drude P Width']
                    self.pZL[i, j, 5] = qf['Drude P thick']
                    # print(i,j,qf['Drude P thick'])
                    self.pZL[i, j, 6] = qf['Drude P Assym']
                    self.pZL[i, j, 7] = qf['Drude P Probab'] * 100.0
                    self.pZL[i, j, 8] = qf['Drude P IMFP']

                if si['Qcheck']:
                    # print (i,j)
                    self.pQF[i, j, :] = np.array(qfspec.FitModel(0))[0:13]

                    if self.debug > 0:
                        print(self.pQF[i, j, :])

                if si['Pcheck']:

                    self.pGF[i, j, :] = p

                    p = self.parent.gFitDialog.GaussFit(qf['spec'], qf['spec'], qf['pGF'])
                    nGauss = gtags['numGauss']
                    for i in range(int(nGauss)):
                        p[i * 3 + 1] = p[i * 3 + 1] * multFac

                    if self.debug > 0:
                        print(j, i, qf['ene'][0], p[0], p[1], p[2])

                    # self.parent.gFitDialog.GaussFitClick()
                    self.pGF[i, j, :] = p  # qf['pGF']

        # reset to original state

        qf['spec'] = spec
        self.setSlider()

        ##########################
        # Store results
        ##########################

        ##########################
        # Output to SI window
        ##########################

        # Estimate Grid Layout
        grid_y = int(np.sqrt(height * width * numOutImages) / height + 0.5)
        if grid_y > 4:
            grid_y = 4

        grid_x = math.ceil(numOutImages / grid_y)
        if grid_x > 4:
            grid_x = 4

        if si['Pcheck']:
            nGauss = gtags['numGauss']
            grid_x = int(3)
            grid_y = int(nGauss)
        if grid_y > 4:
            grid_y = 4

        if self.debug > 0:
            print(numOutImages, grid_x, grid_y)

        im = np.zeros((width, height, numOutImages))
        title = []

        showZa = 0
        showBFa = 0
        showSa = 0

        #########################################################
        ## Save output to Result Dictionary
        #########################################################

        if si['Efix']:
            res['Efix'] = self.pELL

        if si['LLcheck']:
            res['LL'] = self.pZL

        if si['Pcheck']:
            res['GF' + str(eNum)] = self.pGF

        if si['Qcheck']:
            res['GF'] = self.pQF

        index = 0
        ## using median and median absolute deviation as a robust statistical measure instead of mean and standard deviation
        ## These robust statistic is necessary for our noisy data with outlayers
        ## median absolute deviation is scaled for consistency to standard deviation
        if si['Pcheck']:
            self.parent.text2.insertPlainText(
                '\n Peak \t parameter \t Median value  \t median absolute deviation \t Standard deviation')
            nGauss = gtags['numGauss']
            for i in range(int(nGauss)):
                im[:, :, i * 3] = self.pGF[:, :, i * 3]
                title.append('Peak ' + str(i + 1) + ' position')
                self.parent.text2.insertPlainText('\n {0:2d} \t position \t  {1:3.3f} eV \t {2:3.3f} \t {3:3.3f}'
                                                  .format(i + 1, np.median(im[:, :, i * 3]),
                                                          np.median(abs(
                                                              im[:, :, i * 3] - np.median(im[:, :, i * 3])) / 0.6745),
                                                          float(np.std(im[:, :,
                                                                       i * 3]))))  # 0.6745 consistence scale factor to standard deviation
                self.pGF[:, :, i * 3 + 1] = abs(self.pGF[:, :, i * 3 + 1])
                im[:, :, i * 3 + 1] = np.array(self.pGF[:, :, i * 3 + 1])
                title.append('Peak ' + str(i + 1) + ' area')
                self.parent.text2.insertPlainText('\n  \t area \t  {1:3.3f} eV \t {2:3.3f} \t {3:3.3f}'
                                                  .format(i, np.median(im[:, :, i * 3 + 1]), np.median(
                    abs(im[:, :, i * 3 + 1] - np.median(im[:, :, i * 3 + 1])) / 0.6745),
                                                          float(np.std(im[:, :, i * 3 + 1]))))
                self.pGF[:, :, i * 3 + 2] = abs(self.pGF[:, :, i * 3 + 2])
                im[:, :, i * 3 + 2] = np.array(self.pGF[:, :, i * 3 + 2])
                title.append('Peak ' + str(i + 1) + ' width')
                self.parent.text2.insertPlainText('\n  \t width \t  {1:3.3f} eV \t {2:3.3f} \t {3:3.3f}'
                                                  .format(i, np.median(im[:, :, i * 3 + 2]), np.median(
                    abs(im[:, :, i * 3 + 2] - np.median(im[:, :, i * 3 + 2])) / 0.6745),
                                                          float(np.std(im[:, :, i * 3 + 2]))))

            index = nGauss * 3
        print(index, numOutImages)
        if self.showSum:
            showSa = 1
            im[:, :, index] = np.sum(si['data'], axis=2)
            title.append('sum')
            index += 1
        if self.showZ:
            showZa = 1
            im[:, :, index] = si['Zcontrast']
            title.append('Z contrast')
            index += 1
        if self.showBF:
            showBFa = 1
            im[:, :, index] = si['BrightField']
            title.append('bright field')
            index += 1
        if si['Qcheck']:
            scale = np.ones((width, height))
            if qf['plotmode'] == 0:  # output in atom %
                if self.debug > 0:
                    print('shape', self.pQF.shape)
                    print('sum pqf')
                    print(np.sum(self.pQF[:, :, 0:qf['numberOfEdges']], axis=2))
                    print('pqf')
                    print((self.pQF[:, :, 0:qf['numberOfEdges']]))
                scale = 100.0 / (np.sum(self.pQF[:, :, 0:qf['numberOfEdges']], axis=2) + 0.00001)
                unit = ' [atom %]'
            if qf['plotmode'] == 1:  # output in number of electrons
                scale = scale * qf['norm']
                unit = ' [# e-]'

            if qf['plotmode'] == 2:  # output in areal density
                multp = 1e10  # xsec  is in barns = 10^28 m2 = 10^10 nm2
                scale = scale * qf['norm'] * multp  ## check this
                unit = ' [# atoms/nm2]'
            self.parent.text2.insertPlainText('\n')
            self.parent.text2.insertPlainText(
                '\n Edge \t Median value (' + unit + ') \t median absolute deviation \t Standard deviation')
            for i in range(int(qf['numberOfEdges'])):
                im[:, :, index] = self.pQF[:, :, i] * scale
                # title.append('Edge '+str(i-oimages+1)) # Look up element - check scale
                # print('Mean value of ZL Position: ',np.mean(im[:,:,1]),' with standard deviation: ',np.std(im[:,:,1]))
                index += 1
                titleStr = qf['edgeXtags'][str(i)]['element']
                titleStr += '-'
                titleStr += qf['edgeXtags'][str(i)]['subshell']
                self.parent.text2.insertPlainText('\n' + titleStr + '\t {0:3.3f} \t {1:3.3f} \t {2:3.3f}'
                                                  .format(np.median(im[:, :, i]),
                                                          np.median(abs(im[:, :, i] - np.median(im[:, :, i])) / 0.6745),
                                                          float(np.std(im[:, :, i]))))

                titleStr += unit
                title.append(titleStr)

        if si['LLcheck']:
            titelsLL = ['rel. thick', 'ZL FWHM', 'ZL Max', 'Drude P Pos', 'Drude P Width', 'Drude P thick',
                        'Drude P Assym', 'Drude P Probab', 'Drude P IMFP']
            for i in range(9):
                im[:, :, index] = self.pZL[:, :, i]
                title.append(titelsLL[i])
                self.parent.text2.insertPlainText('\n' + 'Mean value of' + titelsLL[i] + ': ' + str(
                    +np.mean(im[:, :, index])) + ' with standard deviation: ' + str(np.std(im[:, :, index])))
                index += 1

        if si['Efix']:
            im[:, :, index] = self.pELL[:, :, 1]
            title.append('ZL Gauss position')
            index += 1
            im[:, :, index] = self.pELL[:, :, 0]
            title.append('ZL Gauss width')
            index += 1
        # print('defined si', index)

        if 'Sliding Aver' not in si:
            si['Sliding Aver'] = 0
        if si['Sliding Aver'] == 0:
            for ind in range(im.shape[2]):
                for j in range(0, height, stepI):
                    for i in range(0, width, stepI):
                        for k in range(step):
                            for l in range(step):
                                if i + l < si['data'].shape[0]:
                                    if j + k < si['data'].shape[1]:
                                        im[i + l, j + k, ind] = im[i, j, ind]
        Imdefined = index
        if 'images' not in si:
            si['images'] = {}
        if 'outimage' in si['images']:
            del si['images']['outimage']
        # si['images'] = {}
        si['images']['gridx'] = grid_x
        si['images']['gridy'] = grid_y

        si['images']['xscale'] = float(si['Xscale'])
        si['images']['pixel_size'] = float(si['Xscale'])
        si['images']['width'] = width * si['images']['xscale']
        si['numOutImages'] = numOutImages
        index = 0
        grid = np.zeros((4, 4))
        si['images']['grid'] = grid

        if 'image_list' not in si['images']:
            si['images']['image_list'] = []

        for index in range(numOutImages):
            si['images'][title[index]] = {}

            if title[index] not in si['images']['image_list']:
                si['images']['image_list'].append(title[index])

            imI = si['images'][title[index]]
            imI['image'] = im[:, :, index]
            # imI['name'] = title[index]
            print(index, title[index])
            imI['min'] = imI['image'].min()
            imI['max'] = imI['image'].max()
            imI['Z min'] = imI['image'].min()
            imI['Z max'] = imI['image'].max()
            xscale = float(si['Xscale'])
            imI['xlim'] = (0, width * xscale)
            imI['ylim'] = (height * xscale, 0)

            imI['extend'] = (0, width * xscale, height * xscale, 0)
            imI['xlabel'] = 'Distance [' + si['Xunit'] + ']'

        print(si['images']['image_list'])
        for index in range(numOutImages):
            si['images'][str(index)] = {}
            imI = si['images'][str(index)]

            imI['image'] = im[:, :, index]
            imI['name'] = title[index]
            imI['min'] = imI['image'].min()
            imI['max'] = imI['image'].max()
            # imI['Z min'] = imI['image'].min()
            # imI['Z max'] = imI['image'].max()
            xscale = float(si['Xscale'])
            imI['xlim'] = (0, width * xscale)
            imI['ylim'] = (height * xscale, 0)

            imI['extend'] = (0, width * xscale, height * xscale, 0)
            imI['xlabel'] = 'Distance [' + si['Xunit'] + ']'

        index = 0
        # print(grid_x,grid_y)

        for j in range(grid_y):
            for i in range(grid_x):

                si['images']['grid'][j][i] = index + 1

                index += 1
                if index == numOutImages:
                    break

            if index == numOutImages:
                break

        if 'Sout' not in self.parent.tags:
            self.parent.tags['Sout'] = False

        if self.parent.tags['Sout']:
            import csv
            with open(qf['filename'] + '-IM.csv', 'w', newline='') as csvfile:
                xlwriter = csv.writer(csvfile, dialect='excel', delimiter=',', )
                xlwriter.writerow(['File Name', qf['filename']])
                xlwriter.writerow(['X-Scale', xscale])
                xlwriter.writerow(['Y-units', res['unit']])
                xlwriter.writerow(['Y-scale', res['scale']])
                xlwriter.writerow(['Y-scaleP', res['scaleP']])

                for i in range(Imdefined):
                    imI = si['images'][str(i)]
                    xlwriter.writerow(imI['title'])
                    im = imI['image']
                    for j in im.shape[1]:
                        xlwriter.writerow(im[j, :])

        self.plotSIimages()
        if len(self.parent.SIImageDialog.process) > 1:
            self.parent.SIImageDialog.process = ['None']

    def plotSIimages(self):
        ## Define dictionaries and important dimensions

        foreMem = self.parent.tags['QF']['Fore']
        qf = self.parent.tags['QF'][str(foreMem)]
        si = self.parent.tags['QF']['SI']

        # if self.parent.tab.tabText(2) == 'SI LS':

        self.parent.tab.removeTab(2)
        self.parent.plotParamWindow3 = MySICanvas(self.parent.centralWidget, width=10, height=10, dpi=70)
        plotLayout3 = QVBoxLayout()
        plot3 = QWidget()
        plotLayout3.addWidget(self.parent.plotParamWindow3)
        plot3.setLayout(plotLayout3)

        self.parent.tab.setCurrentIndex(2)
        self.parent.tab.insertTab(2, plot3, 'SI')

        plot = self.parent.plotParamWindow3

        plot.figure.clear()

        plot.figure.set_tight_layout(True)
        axes = []
        myImage = []

        self.parent.tab.setCurrentIndex(2)

        if 'images' not in si:
            return
        # si['images'].clear()
        if 'outimage' in si['images']:
            del si['images']['outimage']
        grid_x = si['images']['gridx']
        grid_y = si['images']['gridy']
        numOutImages = si['numOutImages']
        si['images']['imageList'] = []
        # print(si['images']['imageList'])
        if 'whichGrid' not in si['images']:
            si['images']['whichGrid'] = [0, 0]

        index = 0
        if 'grid' not in si['images']:
            grid = np.zeros((4, 4))
            index = 0
            for i in range(4):
                for j in range(4):
                    if j < grid_x:
                        if i < grid_y:
                            grid[i, j] = int(index + 1)
                            index += 1
                    if index == numOutImages:
                        break
                if index == numOutImages:
                    break
            si['images']['grid'] = grid
        if 'whichGrid' not in si['images']:
            si['images']['whichGrid'] = [0, 0]
        import matplotlib.gridspec as gridspec
        gs = gridspec.GridSpec(grid_y, grid_x)  # columns, rows, )
        index = 0
        print('print grid\n', si['images']['grid'])
        for i in range(grid_x):
            for j in range(grid_y):
                Imageindex = int(si['images']['grid'][j, i])
                if Imageindex > 0:
                    Imageindex -= 1

                imI = si['images'][str(Imageindex)]
                axes.append(plot.figure.add_subplot(gs[j, i]))
                myImage.append(axes[index].imshow(np.transpose(imI['image']), origin='upper'))
                # print(myImage[index], axes[index],index)

                """///*
                # create an axes on the right side of ax. The width of cax will be 5%
                # of ax and the padding between cax and ax will be fixed at 0.05 inch.
                 = mpl.pyplot.gca(plot.figure.add_subplot(gs[j,i]))
                divider = make_axes_locatable(ax)
                cax = divider.append_axes("right", size="5%", pad=0.05)

                cbar = plot.figure.colorbar(myImage[index], ax=axes[index], cax=cax)
                """
                # cbar = plot.figure.colorbar(myImage[index], ax=axes[index], orientation='vertical', shrink=.5, pad=.0, aspect=10)
                axes[index].set_title(imI['name'])
                myImage[index].set_extent(imI['extend'])

                # cbar = plot.figure.colorbar(myImage[index], ax=axes[index], orientation='vertical', shrink=.5, pad=.0, aspect=10)
                if 'Z min' in imI:
                    norm = mpl.colors.Normalize(vmin=imI['Z min'], vmax=imI['Z max'])
                    myImage[index].set_norm(norm)

                cbar = plot.figure.colorbar(myImage[index], ax=axes[index], orientation='vertical', shrink=.5, pad=.05,
                                            aspect=10)

                axes[index].set_xlim(imI['xlim'])
                axes[index].set_ylim(imI['ylim'])
                index += 1
                if index == numOutImages:
                    break

            if index == numOutImages:
                break

        for i in range(grid_x):
            ind = len(axes) - grid_x + i
            axes[ind].set_xlabel('Distance [' + si['Xunit'] + ']')
            print(ind)
        maxI = 0
        for key in si['images']:
            try:
                if si['images'][key]['name'] not in si['images']['imageList']:
                    maxI += 1
            except:
                pass
        for i in range(maxI - 1):
            si['images']['imageList'].append(si['images'][str(i)]['name'])

        plot.draw()
        plot.show()
        self.parent.SIImageWidget.setVisible(True)
        # self.parent.SIImageDialog.update()

    def onclick(self, event):
        print('button=%d, x=%d, y=%d, xdata=%f, ydata=%f' % (
            event.button, event.x, event.y, event.xdata, event.ydata))

    def onMouseReleaseClick(self, event):
        print('onMouseReleaseClick')
        if event.inaxes:
            if event.button == 3:

                nix = 1
                if int(event.xdata) == self.xsel:
                    nix = 0
                if int(event.ydata) == self.ysel:
                    nix = 0
                    for i in range(self.xsel, int(event.xdata)):
                        for j in range(self.ysel, int(event.ydata)):
                            self.select[j, i] = 1
                    self.parent.text2.insertPlainText(
                        '\n Selected spectra from :  (' + str(self.ysel + 1) + ',' + str(self.xsel + 1) + ') ')
                    self.parent.text2.insertPlainText(
                        ' to (' + str(int(event.ydata + 1)) + ',' + str(int(event.xdata + 1)) + ') \n')
                else:
                    self.parent.text2.insertPlainText(
                        '\n Selected spectrum :  (' + str(self.ysel + 1) + ',' + str(self.xsel + 1) + ') ')

                # print 'moved'
                self.setSlider()

    def onMouseButtonClick(self, event):
        print('onMouseButtonClick')

        if event is None:
            return
        x, y = event.xdata, event.ydata

        foreMem = self.parent.tags['QF']['Fore']
        qf = self.parent.tags['QF'][str(foreMem)]
        si = self.parent.tags['QF']['SI']

        if event.inaxes:
            # print event.button

            if event.button == 1:
                si['Xpos'] = int(x + 0.5)
                si['Ypos'] = int(y + 0.5)

                s = 'Click, x: ' + str(si['Xpos']) + ', y: ' + str(si['Ypos'])
                print(s)

                self.setSlider()

                return

            if event.button == 3:
                s = 'Right Click '
                if event.key == 'shift':
                    print('shift')
                '''
                self.xsel = int(x)
                self.ysel = int(y)
                #print int(event.xdata),int(event.ydata)
                if self.select[int(x),int(y)] == 0:
                    self.select[int(x),int(y)] = 1
                else:
                    self.select[int(event.ydata),int(event.xdata)] = 0
                #print self.select[int(event.ydata),int(event.xdata)]
                '''

        else:
            if event.button == 3:
                si['select'] = []
                si['rectangles'] = {}
                self.rect = 0
                # del(self.select)
                # self.select = np.zeros((height, width),'uint8')

    def XcheckClick(self, event):
        if self.parent.tags['QF']['SI']['Xsum']:
            self.parent.tags['QF']['SI']['Xsum'] = False
        else:
            self.parent.tags['QF']['SI']['Xsum'] = True

        self.setSlider()

    def YcheckClick(self, event):
        if self.parent.tags['QF']['SI']['Ysum']:
            self.parent.tags['QF']['SI']['Ysum'] = False
        else:
            self.parent.tags['QF']['SI']['Ysum'] = True
        self.setSlider()

    def selectSumClick(self, event):
        if self.Scheck.isChecked():
            self.parent.tags['QF']['SI']['Ssum'] = 1
        else:
            self.parent.tags['QF']['SI']['Ssum'] = 0
        self.setSlider()

    '''
    def OnMotion(self,event):
        s= "Mouse Motion"#t: (%.4f, %.4f)" % self.GetXY(event)
        print(s)
        #print event
        event.Skip()
    '''

    def sliderUpdate(self):

        si = self.parent.tags['QF']['SI']
        if self.debug > 0:
            print('slider Update')
        xold = si['Xpos']
        yold = si['Ypos']
        if xold < 1:
            xold = 1
        if yold < 1:
            yold = 1

        si['Ypos'] = int(self.slider2.value() + .2)
        if si['Ypos'] < 1:
            si['Ypos'] = 1

        si['Xpos'] = int(self.slider1.value() + .2)
        if si['Xpos'] < 1:
            si['Xpos'] = 1

        # str1 = "pos1 = %d pos2 = %d" % (si['Xpos'], si['Ypos'])
        #
        # display current slider positions in the self.parent's title
        #
        # print (str1)
        if si['Xpos'] != xold or si['Ypos'] != yold:
            if self.debug > 0:
                print('set slider update')
            self.setSlider()






