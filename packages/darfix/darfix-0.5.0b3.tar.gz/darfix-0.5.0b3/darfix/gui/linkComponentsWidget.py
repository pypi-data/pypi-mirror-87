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
__date__ = "17/01/2020"


import numpy
from pathlib import Path

from silx.gui import qt
from silx.gui.colors import Colormap
from silx.gui.plot import StackView

import darfix
from darfix.core.componentsMatching import ComponentsMatching, Method
from darfix.gui.datasetSelectionWidget import FilenameSelectionWidget
from darfix.io.utils import read_components
import logging

_logger = logging.getLogger(__file__)


class LinkComponentsWidget(qt.QWidget):
    """
    Widget to compare two stacks of images. Each of these stacks represents the
    components of a dataset.
    """
    def __init__(self, parent=None):
        qt.QWidget.__init__(self, parent)
        self.setLayout(qt.QGridLayout())

        self._displayComponents = [False, False]
        self._displayMatches = True

        # Method Widget
        methodsLabel = qt.QLabel("Matching method:")
        self._methodsCB = qt.QComboBox(parent=self)
        for method in Method.values():
            self._methodsCB.addItem(method)
        self.layout().addWidget(methodsLabel, 1, 0, 1, 1)
        self.layout().addWidget(self._methodsCB, 1, 1, 1, 1)

        # Compute button and checkbox widgets
        self._methodsCB.currentTextChanged.connect(self._comboBoxChanged)
        self._computeB = qt.QPushButton("Compute")
        self._computeB.setEnabled(False)
        self._checkbox = qt.QCheckBox("Link features", self)
        self._checkbox.setChecked(True)
        self._checkbox.setToolTip("If checked, lines between matches will be drawn")
        self._checkbox.stateChanged.connect(self._checkBoxToggled)
        widget = qt.QWidget(parent=self)
        layout = qt.QHBoxLayout()
        layout.addWidget(self._checkbox)
        layout.addWidget(self._computeB)
        widget.setLayout(layout)
        self.layout().addWidget(widget, 1, 3, 1, 1, qt.Qt.AlignRight)

        # Stack 1
        self._sv1 = StackView(parent=self)
        self._sv1.setColormap(Colormap(
            name=darfix.config.DEFAULT_COLORMAP_NAME,
            normalization=darfix.config.DEFAULT_COLORMAP_NORM))
        self._sv1.hide()
        stack1Label = qt.QLabel("Path for stack 1: ")
        self._stack1Filename = FilenameSelectionWidget(parent=self)
        self._stack1Filename.filenameChanged.connect(self._setStack1)
        self.layout().addWidget(stack1Label, 0, 0)
        self.layout().addWidget(self._stack1Filename, 0, 1)
        self.layout().addWidget(self._sv1, 3, 0, 1, 2)

        # Stack 2
        self._sv2 = StackView(parent=self)
        self._sv2.setColormap(Colormap(
            name=darfix.config.DEFAULT_COLORMAP_NAME,
            normalization='linear'))
        self._sv2.hide()
        stack2Label = qt.QLabel("Path for stack 2: ")
        self._stack2Filename = FilenameSelectionWidget(parent=self)
        self._stack2Filename.filenameChanged.connect(self._setStack2)
        self.layout().addWidget(stack2Label, 0, 2)
        self.layout().addWidget(self._stack2Filename, 0, 3)
        self.layout().addWidget(self._sv2, 3, 2, 1, 2)

        # Linked stack
        self._linked_sv = StackView(parent=self)
        self._linked_sv.setColormap(Colormap(
            name=darfix.config.DEFAULT_COLORMAP_NAME,
            normalization='linear'))
        self._linked_sv.hide()
        self.layout().addWidget(self._linked_sv, 2, 0, 4, 4)

    def _setStack1(self):
        """
        Update stack 1 components
        """
        filename = self._stack1Filename.getFilename()

        if not Path(filename).is_file():
            if filename != '':
                msg = qt.QMessageBox()
                msg.setIcon(qt.QMessageBox.Warning)
                msg.setText("Filename not valid")
                msg.exec_()
            return

        dimensions, components, W = read_components(filename)

        self._linked_sv.hide()
        self._sv1.setStack(components)
        self._displayComponents[0] = True
        self._sv1.show()

        if all(self._displayComponents):
            self._sv2.show()
            self._componentsMatching = ComponentsMatching(
                components=[components, self._sv2.getStack(False, True)[0]])

    def _setStack2(self):
        """
        Update stack 2 components
        """
        filename = self._stack2Filename.getFilename()

        if filename == '':
            return

        dimensions, components, W = read_components(filename)

        self._linked_sv.hide()
        self._sv2.setStack(components)
        self._displayComponents[1] = True
        self._sv2.show()

        if all(self._displayComponents):
            self._sv1.show()
            self._componentsMatching = ComponentsMatching(
                components=[self._sv1.getStack(False, True)[0], components])

        self._computeB.setEnabled(True)
        self._computeB.pressed.connect(self._linkComponents)

    def _checkBoxToggled(self, linkFeatures):
        """
        Slot to toggle state in function of the checkbox state.
        """
        self._displayMatches = linkFeatures

    def _comboBoxChanged(self, text):

        method = Method(text)
        if method == Method.orb_feature_matching:
            self._checkbox.setEnabled(True)
            self._displayMatches = self._checkbox.checkState()
        else:
            self._checkbox.setEnabled(False)
            self._displayMatches = False

    def _linkComponents(self):
        """
        Link components from stack 1 and 2.
        """
        final_matches, matches = self._componentsMatching.match_components(
            method=Method(self._methodsCB.currentText()))
        self._sv1.hide()
        self._sv2.hide()

        draws = numpy.array(self._componentsMatching.draw_matches(final_matches,
                            matches, displayMatches=self._displayMatches))
        self._linked_sv.setStack(draws)
        self._linked_sv.show()
