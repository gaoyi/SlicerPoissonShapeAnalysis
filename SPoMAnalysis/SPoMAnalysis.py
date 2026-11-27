import logging
import os
import colorsys

import vtk
import qt

import slicer
from slicer.ScriptedLoadableModule import *
from slicer.util import VTKObservationMixin


#
# SPoMAnalysis
#

class SPoMAnalysis(ScriptedLoadableModule):
  """Runs the PoissonShapeAnalysis CLI and configures the pValue display."""

  def __init__(self, parent):
    ScriptedLoadableModule.__init__(self, parent)
    self.parent.title = "SPoM Shape Analysis"
    self.parent.categories = ["Shape Analysis"]
    self.parent.dependencies = ["PoissonShapeAnalysis"]
    self.parent.contributors = ["Yi Gao (Shenzhen University), Sylvain Bouix (BWH)"]
    self.parent.helpText = """
This module runs the PoissonShapeAnalysis (SPoM) command line module and displays
the resulting mean shape model. The <b>pValue</b> point scalar is activated and
rendered with a hot-to-cold table: 0 is red, values approaching 0.05 are blue,
and values at or above 0.05 are neutral grey. The scalar range mode is set to
Manual with a display range of 0 to 0.05.
"""
    self.parent.acknowledgementText = """
This work is partially supported by the National Natural Science Foundation of China under Grant 82672620, Shenzhen Science and Technology Program grant JCYJ20250604182556073, Shenzhen Medical Research Fund C2501029, and the Guangdong Provincial Key Laboratory of Mathematical and Neural Dynamical Systems 2024B1212010004. This work was partially funded by NIH R01 MH82918. This work is partially suppored by the Key-Area Research and Development Program of Guangdong Province grant 2021B0101420005, the Key Technology Development Program of Shenzhen grant JSGG20210713091811036, the Department of Education of Guangdong Province grant 2017KZDXM072, the National Natural Science Foundation of China grant 61601302, the Shenzhen Key Laboratory Foundation grant ZDSYS20200811143757022, the Shenzhen Peacock Plan grant KQTD2016053112051497, and the SZU Top Ranking Project grant 86000000210.
"""


#
# SPoMAnalysisWidget
#

class SPoMAnalysisWidget(ScriptedLoadableModuleWidget, VTKObservationMixin):
  """Uses ScriptedLoadableModuleWidget base class."""

  def __init__(self, parent=None):
    ScriptedLoadableModuleWidget.__init__(self, parent)
    VTKObservationMixin.__init__(self)
    self.logic = None
    self._parameterNode = None
    self._updatingGUIFromParameterNode = False

  def setup(self):
    ScriptedLoadableModuleWidget.setup(self)

    uiWidget = slicer.util.loadUI(self.resourcePath('UI/SPoMAnalysis.ui'))
    self.layout.addWidget(uiWidget)
    self.ui = slicer.util.childWidgetVariables(uiWidget)
    uiWidget.setMRMLScene(slicer.mrmlScene)

    self.logic = SPoMAnalysisLogic()

    self.addObserver(slicer.mrmlScene, slicer.mrmlScene.StartCloseEvent, self.onSceneStartClose)
    self.addObserver(slicer.mrmlScene, slicer.mrmlScene.EndCloseEvent, self.onSceneEndClose)

    self.ui.group1Button.connect('clicked(bool)', self.onSelectGroup1)
    self.ui.group2Button.connect('clicked(bool)', self.onSelectGroup2)
    self.ui.outputVolumeSelector.connect("currentNodeChanged(vtkMRMLNode*)", self.updateParameterNodeFromGUI)
    self.ui.outputModelSelector.connect("currentNodeChanged(vtkMRMLNode*)", self.updateParameterNodeFromGUI)
    self.ui.doRegistrationCheckBox.connect("toggled(bool)", self.updateParameterNodeFromGUI)
    self.ui.applyButton.connect('clicked(bool)', self.onApplyButton)

    self.initializeParameterNode()

  def cleanup(self):
    self.removeObservers()

  def enter(self):
    self.initializeParameterNode()

  def exit(self):
    if self._parameterNode is not None:
      self.removeObserver(self._parameterNode, vtk.vtkCommand.ModifiedEvent, self.updateGUIFromParameterNode)

  def onSceneStartClose(self, caller, event):
    self.setParameterNode(None)

  def onSceneEndClose(self, caller, event):
    if self.parent.isEntered:
      self.initializeParameterNode()

  def initializeParameterNode(self):
    self.setParameterNode(self.logic.getParameterNode())

  def setParameterNode(self, inputParameterNode):
    if inputParameterNode:
      self.logic.setDefaultParameters(inputParameterNode)

    if self._parameterNode is not None:
      self.removeObserver(self._parameterNode, vtk.vtkCommand.ModifiedEvent, self.updateGUIFromParameterNode)
    self._parameterNode = inputParameterNode
    if self._parameterNode is not None:
      self.addObserver(self._parameterNode, vtk.vtkCommand.ModifiedEvent, self.updateGUIFromParameterNode)

    self.updateGUIFromParameterNode()

  def updateGUIFromParameterNode(self, caller=None, event=None):
    if self._parameterNode is None or self._updatingGUIFromParameterNode:
      return

    self._updatingGUIFromParameterNode = True
    try:
      self.ui.group1LineEdit.setText(self._parameterNode.GetParameter("Group1Folder") or "")
      self.ui.group2LineEdit.setText(self._parameterNode.GetParameter("Group2Folder") or "")
      self.ui.outputVolumeSelector.setCurrentNode(self._parameterNode.GetNodeReference("OutputVolume"))
      self.ui.outputModelSelector.setCurrentNode(self._parameterNode.GetNodeReference("OutputModel"))
      self.ui.doRegistrationCheckBox.checked = (self._parameterNode.GetParameter("Register") == "true")
      self.updateApplyButtonState()
    finally:
      self._updatingGUIFromParameterNode = False

  def updateParameterNodeFromGUI(self, caller=None, event=None):
    if self._parameterNode is None or self._updatingGUIFromParameterNode:
      return

    wasModified = self._parameterNode.StartModify()
    self._parameterNode.SetParameter("Group1Folder", self.ui.group1LineEdit.text)
    self._parameterNode.SetParameter("Group2Folder", self.ui.group2LineEdit.text)
    self._parameterNode.SetNodeReferenceID("OutputVolume", self.ui.outputVolumeSelector.currentNodeID)
    self._parameterNode.SetNodeReferenceID("OutputModel", self.ui.outputModelSelector.currentNodeID)
    self._parameterNode.SetParameter("Register", "true" if self.ui.doRegistrationCheckBox.checked else "false")
    self._parameterNode.EndModify(wasModified)

    self.updateApplyButtonState()

  def updateApplyButtonState(self):
    inputFoldersSet = bool(self.ui.group1LineEdit.text.strip()) and bool(self.ui.group2LineEdit.text.strip())
    outputsSet = bool(self.ui.outputVolumeSelector.currentNode()) and bool(self.ui.outputModelSelector.currentNode())
    self.ui.applyButton.enabled = inputFoldersSet and outputsSet

  def onSelectGroup1(self):
    folder = qt.QFileDialog.getExistingDirectory(self.parent, "Select folder with the group 1 shape volumes", self.ui.group1LineEdit.text)
    if folder:
      self.ui.group1LineEdit.setText(folder)
      self.updateParameterNodeFromGUI()

  def onSelectGroup2(self):
    folder = qt.QFileDialog.getExistingDirectory(self.parent, "Select folder with the group 2 shape volumes", self.ui.group2LineEdit.text)
    if folder:
      self.ui.group2LineEdit.setText(folder)
      self.updateParameterNodeFromGUI()

  def onApplyButton(self):
    with slicer.util.tryWithErrorDisplay("Failed to compute the SPoM results.", waitCursor=True):
      self.logic.process(
        self.ui.group1LineEdit.text,
        self.ui.group2LineEdit.text,
        self.ui.outputVolumeSelector.currentNode(),
        self.ui.outputModelSelector.currentNode(),
        self.ui.doRegistrationCheckBox.checked)


#
# SPoMAnalysisLogic
#

class SPoMAnalysisLogic(ScriptedLoadableModuleLogic):
  """Runs the PoissonShapeAnalysis CLI and configures the pValue display."""

  P_VALUE_ARRAY_NAME = "pValue"
  COLOR_NODE_NAME = "SPoM p-value"
  DISPLAY_RANGE = (0.0, 0.05)
  NUMBER_OF_COLORS = 256

  def setDefaultParameters(self, parameterNode):
    if not parameterNode.GetParameter("Group1Folder"):
      parameterNode.SetParameter("Group1Folder", "")
    if not parameterNode.GetParameter("Group2Folder"):
      parameterNode.SetParameter("Group2Folder", "")
    if not parameterNode.GetParameter("Register"):
      parameterNode.SetParameter("Register", "false")

  def process(self, group1Folder, group2Folder, outputVolume, outputModel, doRegistration=False):
    if not group1Folder or not os.path.isdir(group1Folder):
      raise ValueError("Select a valid folder for group 1.")
    if not group2Folder or not os.path.isdir(group2Folder):
      raise ValueError("Select a valid folder for group 2.")
    if outputVolume is None:
      raise ValueError("Select an output mean shape volume.")
    if outputModel is None:
      raise ValueError("Select an output mean shape model.")

    logging.info('SPoM processing started')

    cliParameters = {
      'shapeNameList1': group1Folder,
      'shapeNameList2': group2Folder,
      'meanImageName': outputVolume,
      'meanVTKName': outputModel,
      'doRegistration': doRegistration,
    }

    cliNode = slicer.cli.runSync(slicer.modules.poissonshapeanalysis, None, cliParameters)
    if cliNode is None:
      raise RuntimeError("Failed to start the PoissonShapeAnalysis CLI module.")

    try:
      errorsMask = getattr(slicer.vtkMRMLCommandLineModuleNode, "ErrorsMask", 0x40)
      if cliNode.GetStatus() & errorsMask:
        raise RuntimeError("PoissonShapeAnalysis failed: " + cliNode.GetErrorText())
      self.configurePValueDisplay(outputModel)
    finally:
      slicer.mrmlScene.RemoveNode(cliNode)

    logging.info('SPoM processing completed')

  def getPValueColorNode(self):
    colorNode = slicer.mrmlScene.GetFirstNodeByName(self.COLOR_NODE_NAME)
    if colorNode is None or not colorNode.IsA("vtkMRMLColorTableNode"):
      colorNode = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLColorTableNode", self.COLOR_NODE_NAME)
    self.setupPValueColorTable(colorNode)
    return colorNode

  def setupPValueColorTable(self, colorNode):
    colorNode.SetTypeToUser()
    colorNode.SetNumberOfColors(self.NUMBER_OF_COLORS)

    wasModifying = colorNode.StartModify()
    try:
      for index in range(self.NUMBER_OF_COLORS):
        if index == self.NUMBER_OF_COLORS - 1:
          red = green = blue = 0.5
        else:
          fraction = index / float(self.NUMBER_OF_COLORS - 2)
          hue = (2.0 / 3.0) * fraction
          red, green, blue = colorsys.hsv_to_rgb(hue, 1.0, 1.0)
        colorNode.SetColor(index, red, green, blue, 1.0)

      lookupTable = colorNode.GetLookupTable()
      lookupTable.SetRampToLinear()
      lookupTable.SetTableRange(self.DISPLAY_RANGE[0], self.DISPLAY_RANGE[1])
      colorNode.SetDescription("SPoM p-value: 0 red, 0.05 blue, >=0.05 grey")
    finally:
      colorNode.EndModify(wasModifying)

    return colorNode

  def configurePValueDisplay(self, modelNode):
    polyData = modelNode.GetPolyData()
    if polyData is None:
      raise RuntimeError("The output model does not contain any polydata.")
    if polyData.GetPointData().GetArray(self.P_VALUE_ARRAY_NAME) is None:
      raise RuntimeError("The output model does not contain the '%s' point scalar." % self.P_VALUE_ARRAY_NAME)

    if modelNode.GetDisplayNode() is None:
      modelNode.CreateDefaultDisplayNodes()
    displayNode = modelNode.GetDisplayNode()
    if displayNode is None:
      raise RuntimeError("Failed to create a display node for the output model.")

    displayNode.SetScalarVisibility(True)
    displayNode.SetActiveScalarName(self.P_VALUE_ARRAY_NAME)
    displayNode.SetAndObserveColorNodeID(self.getPValueColorNode().GetID())
    displayNode.SetScalarRangeFlag(
      getattr(slicer.vtkMRMLDisplayNode, "UseManualScalarRange", 0))
    displayNode.SetScalarRange(self.DISPLAY_RANGE[0], self.DISPLAY_RANGE[1])
