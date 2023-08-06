# coding: utf-8
# /*##########################################################################
#
# Copyright (c) 2016-2017 European Synchrotron Radiation Facility
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#
# ###########################################################################*/


__authors__ = ["J. Garriga"]
__license__ = "MIT"
__date__ = "30/11/2020"

from matplotlib.colors import hsv_to_rgb
import numpy

from silx.gui import qt
from silx.gui.colors import Colormap
from silx.gui.plot import Plot2D
from silx.image.marchingsquares import find_contours
from silx.math.medianfilter import medfilt2d
from silx.utils.enum import Enum as _Enum

import darfix
from .operationThread import OperationThread


class Method(_Enum):
    """
    Different maps to show
    """
    COM = "Center of mass"
    FWHM = "FWHM"
    SKEWNESS = "Skewness"
    KURTOSIS = "Kurtosis"
    ORI_DIST = "Orientation distribution"
    MOSAICITY = "Mosaicity"


class GrainPlotWidget(qt.QMainWindow):
    """
    Widget to apply PCA to a set of images and plot the eigenvalues found.
    """
    sigComputed = qt.Signal()

    def __init__(self, parent=None):
        qt.QWidget.__init__(self, parent)

        self._methodCB = qt.QComboBox()
        self._methodCB.addItems(Method.values())
        for i in range(len(Method)):
            self._methodCB.model().item(i).setEnabled(False)
        self._methodCB.currentTextChanged.connect(self._updatePlot)
        self._plotWidget = qt.QWidget()
        plotsLayout = qt.QHBoxLayout()
        self._plotWidget.setLayout(plotsLayout)
        self._contoursPlot = Plot2D(parent=self)
        self._contoursPlot.setDefaultColormap(Colormap(name='viridis', normalization='linear'))
        self._contoursPlot.setAxesDisplayed(False)
        widget = qt.QWidget(parent=self)
        layout = qt.QVBoxLayout()
        self._levelsWidget = qt.QWidget()
        levelsLayout = qt.QGridLayout()
        levelsLabel = qt.QLabel("Number of levels:")
        self._levelsLE = qt.QLineEdit("20")
        self._levelsLE.setToolTip("Number of levels to use when finding the contours")
        self._levelsLE.setValidator(qt.QIntValidator())
        self._computeContoursB = qt.QPushButton("Compute")
        levelsLayout.addWidget(levelsLabel, 0, 0, 1, 1)
        levelsLayout.addWidget(self._levelsLE, 0, 1, 1, 1)
        levelsLayout.addWidget(self._computeContoursB, 0, 2, 1, 1)
        levelsLayout.addWidget(self._contoursPlot, 1, 0, 1, 3)
        self._levelsWidget.setLayout(levelsLayout)
        self._mosaicityPlot = Plot2D(parent=self)
        layout.addWidget(self._methodCB)
        layout.addWidget(self._levelsWidget)
        layout.addWidget(self._plotWidget)
        layout.addWidget(self._mosaicityPlot)
        self._plotWidget.hide()
        self._mosaicityPlot.hide()
        self._mosaicityPlot.getColorBarWidget().hide()
        widget.setLayout(layout)
        widget.setSizePolicy(qt.QSizePolicy.Minimum, qt.QSizePolicy.Minimum)
        self.setCentralWidget(widget)

    def setDataset(self, dataset, indices=None, bg_indices=None, bg_dataset=None):
        """
        Dataset setter.

        :param Dataset dataset: dataset
        """
        self.dataset = dataset
        self.indices = indices
        self.bg_indices = bg_indices
        self.bg_dataset = bg_dataset
        self.ori_dist, self.hsv_key = self.dataset.compute_mosaicity_colorkey()
        self._methodCB.model().item(4).setEnabled(True)
        self._methodCB.setCurrentIndex(4)
        self._curvesColormap = Colormap(name='temperature',
                                        vmin=numpy.min(self.ori_dist),
                                        vmax=numpy.max(self.ori_dist))
        self._computeContoursB.clicked.connect(self._computeContours)
        self._thread = OperationThread(self, self.dataset.apply_moments)
        self._thread.setArgs(self.indices)
        self._thread.finished.connect(self._updateData)
        self._thread.start()
        for i in reversed(range(self._plotWidget.layout().count())):
            self._plotWidget.layout().itemAt(i).widget().setParent(None)

        self._plots = []
        for dim in self.dataset.dims:
            self._plots += [Plot2D(parent=self)]
            self._plots[-1].setAxesDisplayed(False)
            self._plots[-1].setDefaultColormap(Colormap(name='viridis'))
            self._plotWidget.layout().addWidget(self._plots[-1])
        self._updatePlot(self._methodCB.currentText())

    def _updateData(self):
        """
        Updates the plots with the data computed in the thread
        """
        self._thread.finished.disconnect(self._updateData)
        if self._thread.data is not None:
            self._moments = self._thread.data
            for i in range(len(Method)):
                self._methodCB.model().item(i).setEnabled(True)
        else:
            print("\nComputation aborted")

    def _computeContours(self):
        self._contoursPlot.remove(kind='curve')

        if self.ori_dist is not None:
            polygons = []
            levels = []
            for i in numpy.linspace(numpy.min(self.ori_dist), numpy.max(self.ori_dist), int(self._levelsLE.text())):
                polygons.append(find_contours(self.ori_dist, i))
                levels.append(i)

            colors = self._curvesColormap.applyToData(levels)

            for ipolygon, polygon in enumerate(polygons):
                # iso contours
                for icontour, contour in enumerate(polygon):
                    if len(contour) == 0:
                        continue
                    # isClosed = numpy.allclose(contour[0], contour[-1])
                    x = contour[:, 1] + 0.5
                    y = contour[:, 0] + 0.5
                    legend = "custom-polygon-%d" % icontour * (ipolygon + 1)
                    self._contoursPlot.addCurve(x=x, y=y, linestyle="-", linewidth=2.0,
                                                legend=legend, resetzoom=False,
                                                color=colors[ipolygon])

    def _computeMosaicity(self):

        norms0 = (self._moments[0][0] - numpy.min(self._moments[0][0])) / numpy.ptp(self._moments[0][0])
        norms1 = (self._moments[1][0] - numpy.min(self._moments[1][0])) / numpy.ptp(self._moments[1][0])

        mosaicity = numpy.stack((norms0, norms1, numpy.ones(self._moments[0].shape[1:])), axis=2)
        return mosaicity

    def _updatePlot(self, method):
        method = Method(method)
        self._levelsWidget.hide()
        self._mosaicityPlot.hide()
        if method == Method.ORI_DIST:
            if self.hsv_key is not None:
                self._levelsWidget.show()
                self._plotWidget.hide()
                self._contoursPlot.addImage(hsv_to_rgb(self.hsv_key))
                self._contoursPlot.getColorBarWidget().hide()
        elif method == Method.FWHM:
            self._plotWidget.show()
            for i, plot in enumerate(self._plots):
                plot.addImage(self._opticolor(darfix.config.FWHM_VAL * self._moments[i][1], 0.02, 0.98))
        elif method == Method.COM:
            self._plotWidget.show()
            for i, plot in enumerate(self._plots):
                plot.addImage(self._opticolor(self._moments[i][0], 0.02, 0.98))
        elif method == Method.SKEWNESS:
            self._plotWidget.show()
            for i, plot in enumerate(self._plots):
                plot.addImage(self._opticolor(self._moments[i][2], 0.02, 0.98))
        elif method == Method.KURTOSIS:
            self._plotWidget.show()
            for i, plot in enumerate(self._plots):
                plot.addImage(self._opticolor(self._moments[i][3], 0.02, 0.98))
        elif method == Method.MOSAICITY:
            self._plotWidget.hide()
            self._mosaicityPlot.addImage(hsv_to_rgb(self._computeMosaicity()))
            self._mosaicityPlot.show()

    def _opticolor(self, img, minc, maxc):
        Cnn = img[~numpy.isnan(img)]
        sortC = sorted(Cnn)
        Imin = sortC[int(numpy.floor(len(sortC) * minc))]
        Imax = sortC[int(numpy.floor(len(sortC) * maxc))]
        img[img > Imax] = Imax
        img[img < Imin] = Imin

        return medfilt2d(img)
