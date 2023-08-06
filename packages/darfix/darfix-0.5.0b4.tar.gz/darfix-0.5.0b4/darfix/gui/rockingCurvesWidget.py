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
__date__ = "19/11/2020"

import numpy

from silx.gui import qt
from silx.gui.colors import Colormap
from silx.gui.plot import StackView, Plot1D, Plot2D
from .utils import ChooseDimensionDock
from silx.utils.enum import Enum as _Enum

import darfix
from darfix.core.mapping import fit_rocking_curve
from darfix.core.dataset import Operation
from .operationThread import OperationThread


class Method(_Enum):
    """
    Different maps that can be showed after fitting the data
    """
    INTENSITY = "Integrated intensity"
    FWHM = "FWHM"
    PEAK = "Peak position"


class RockingCurvesWidget(qt.QMainWindow):
    """
    Widget to apply fit to a set of images and plot the integrated intensity, fwhm and peak position maps.
    """
    sigFitted = qt.Signal()

    def __init__(self, parent=None):
        qt.QWidget.__init__(self, parent)

        widget = qt.QWidget(parent=self)
        layout = qt.QGridLayout()

        self._sv = StackView(parent=self)
        self._sv.setColormap(Colormap(name=darfix.config.DEFAULT_COLORMAP_NAME))
        self._plot = Plot1D(parent=self)
        self._plot.setGraphTitle("Rocking curves")
        self._plot.setGraphXLabel("Image id")
        self._plotMaps = Plot2D(self)
        self._plotMaps.setDefaultColormap(Colormap(name='cividis', normalization='linear'))
        self._methodCB = qt.QComboBox(self)
        self._methodCB.addItems(Method.values())
        self._methodCB.currentTextChanged.connect(self._updatePlot)
        self._plotMaps.hide()
        self._methodCB.hide()
        self._chooseDimensionDock = ChooseDimensionDock(self)
        intLabel = qt.QLabel("Intensity threshold:")
        self._intThresh = "15"
        self._intThreshLE = qt.QLineEdit(self._intThresh)
        self._intThreshLE.setValidator(qt.QDoubleValidator())
        self._computeFit = qt.QPushButton("Fit data")
        self._computeFit.clicked.connect(self._grainPlot)
        self._abortFit = qt.QPushButton("Abort")
        self._abortFit.clicked.connect(self.__abort)
        spacer1 = qt.QWidget(parent=self)
        spacer1.setLayout(qt.QVBoxLayout())
        spacer1.setSizePolicy(qt.QSizePolicy.Minimum, qt.QSizePolicy.Expanding)
        self._dimension = None
        self._chooseDimensionDock.widget.layout().addWidget(spacer1)
        self._chooseDimensionDock.hide()
        self._chooseDimensionDock.widget.filterChanged.connect(self._filterStack)
        self._chooseDimensionDock.widget.stateDisabled.connect(self._wholeStack)

        layout.addWidget(self._sv, 0, 0, 1, 2)
        layout.addWidget(self._plot, 0, 2, 1, 2)
        layout.addWidget(intLabel, 1, 0, 1, 1)
        layout.addWidget(self._intThreshLE, 1, 1, 1, 1)
        layout.addWidget(self._computeFit, 1, 2, 1, 2)
        layout.addWidget(self._abortFit, 1, 2, 1, 2)
        layout.addWidget(self._methodCB, 2, 0, 1, 4)
        layout.addWidget(self._plotMaps, 3, 0, 1, 4)
        self._abortFit.hide()
        self.addDockWidget(qt.Qt.RightDockWidgetArea, self._chooseDimensionDock)
        widget.setLayout(layout)
        self.setCentralWidget(widget)

    def setDataset(self, dataset, indices=None, bg_indices=None, bg_dataset=None):
        """
        Dataset setter.

        :param Dataset dataset: dataset
        """
        self.dataset = dataset
        self.indices = indices
        self._update_dataset = dataset
        self._thread = OperationThread(self, self.dataset.apply_fit)
        self.setStack()
        self._sv.getPlotWidget().sigPlotSignal.connect(self._mouseSignal)
        if len(self.dataset.data.shape) > 3:
            self._chooseDimensionDock.show()
            self._chooseDimensionDock.widget.setDimensions(self.dataset.dims)
        if not self._chooseDimensionDock.widget._checkbox.isChecked():
            self._wholeStack()

    def setStack(self, dataset=None):
        """
        Sets new data to the stack.
        Mantains the current frame showed in the view.

        :param Dataset dataset: if not None, data set to the stack will be from the given dataset.
        """
        if dataset is None:
            dataset = self.dataset
        nframe = self._sv.getFrameNumber()
        if self.indices is None:
            self._sv.setStack(dataset.get_data() if dataset is not None else None)
        else:
            self._sv.setStack(dataset.get_data(self.indices) if dataset is not None else None)
        self._sv.setFrameNumber(nframe)

    def _mouseSignal(self, info):
        """
        Method called when a signal from the stack is called
        """
        if info['event'] == 'mouseClicked':
            # In case the user has clicked on a pixel in the stack
            data = self.dataset.get_data(self.indices, self._dimension)
            px = info['x']
            py = info['y']
            # Show vertical and horizontal lines for clicked pixel
            self._sv.getPlotWidget().addCurve((px, px), (0, data.shape[1]), legend='x', color='r')
            self._sv.getPlotWidget().addCurve((0, data.shape[2]), (py, py), legend='y', color='r')
            self._plot.clear()
            # Get rocking curves from data
            if self.dataset.in_memory:
                y = data[:, int(py), int(px)]
            else:
                y = [image[int(py), int(px)] for image in data]
            if self._dimension is not None:
                axis = self.dataset.dims.ndim - self._dimension[0][0] - 1
                dim = self.dataset.dims.get(axis)
                x = numpy.array([data.metadata[i].get_value(kind=dim.kind, name=dim.name) for i in range(len(data))]).reshape(-1)
                item = [numpy.array(y), None]
            else:
                item = [numpy.array(y), None]
                x = numpy.arange(data.shape[0])
            # Show rocking curves and fitted curve into plot
            self._plot.addCurve(x, y, legend="data", color='b')
            y_gauss = fit_rocking_curve(item, values=x, num_points=1000)
            self._plot.addCurve(numpy.linspace(x[0], x[-1], len(y_gauss)), y_gauss, legend="fit", color='r')

    def _grainPlot(self):
        """
        Method called when button for computing fit is clicked
        """
        self._computeFit.hide()
        self._intThresh = self._intThreshLE.text()
        self.sigFitted.emit()
        self._thread.setArgs(self.indices, self._dimension, float(self._intThresh))
        self._thread.finished.connect(self._updateData)
        self._thread.start()
        self._abortFit.show()

    def _updatePlot(self, method):
        """
        Updates the plots with the chosen method
        """
        method = Method(method)
        data = self._update_dataset.get_data(self.indices, self._dimension)
        if method == Method.INTENSITY:
            self._plotMaps.addImage(data.sum(axis=0))
        elif method == Method.FWHM:
            std = numpy.std(data, axis=0)
            self._plotMaps.addImage(darfix.config.FWHM_VAL * std)
        elif method == Method.PEAK:
            self._plotMaps.addImage(numpy.argmax(data, axis=0))

    def __abort(self):
        self._abortFit.setEnabled(False)
        self.dataset.stop_operation(Operation.FIT)

    def _updateData(self):
        """
        Method called when fit computation has finished
        """
        self._thread.finished.disconnect(self._updateData)
        self._abortFit.hide()
        self._computeFit.show()
        if self._thread.data:
            self._update_dataset = self._thread.data
            assert self._update_dataset is not None
            self._updatePlot(self._methodCB.currentText())
            self._plotMaps.show()
            self._methodCB.show()
        else:
            print("\nCorrection aborted")

    def _filterStack(self, dim=0, val=0):
        if type(dim) is int:
            self._dimension = [[dim], [val]]
        else:
            self._dimension = [dim, val]
        data = self.dataset.get_data(self.indices, self._dimension)
        if data.shape[0]:
            self._sv.setStack(data)
        else:
            self._sv.setStack(None)

    def _wholeStack(self):
        self._dimension = None
        self.setStack(self.dataset)

    @property
    def intThresh(self):
        return self._intThresh

    @intThresh.setter
    def intThresh(self, intThresh):
        self._intThresh = intThresh
        self._intThreshLE.setText(intThresh)

    @property
    def dimension(self):
        return self._dimension
