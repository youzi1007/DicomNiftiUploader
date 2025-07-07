import os
import shutil
import subprocess
import slicer
import ctk
from slicer.ScriptedLoadableModule import *
from slicer.util import VTKObservationMixin
from qt import QTimer, QMessageBox


class DicomNiftiModule(ScriptedLoadableModule):
    def __init__(self, parent):
        ScriptedLoadableModule.__init__(self, parent)
        self.parent.title = "DicomNiftiModule"
        self.parent.categories = ["Examples"]
        self.parent.dependencies = []
        self.parent.contributors = ["Minnie Zhang (NYU)"]
        self.parent.helpText = "DICOM to NIfTI Converter with optional MONAI Label Server upload."
        self.parent.acknowledgementText = "This project is developed by Minnie Zhang."


class DicomNiftiModuleWidget(ScriptedLoadableModuleWidget, VTKObservationMixin):
    def __init__(self, parent=None):
        ScriptedLoadableModuleWidget.__init__(self, parent)
        VTKObservationMixin.__init__(self)
        self.progressValue = 0
        self.progressTimer = QTimer()
        self.progressTimer.timeout.connect(self.updateProgressBar)
        self.skipAll = False

    def setup(self):
        ScriptedLoadableModuleWidget.setup(self)

        uiWidget = slicer.util.loadUI(self.resourcePath('UI/DicomNiftiModule.ui'))
        self.layout.addWidget(uiWidget)
        self.ui = slicer.util.childWidgetVariables(uiWidget)

        uiWidget.setMRMLScene(slicer.mrmlScene)

        self.ui.convertButton.connect('clicked(bool)', self.onConvertButtonClicked)
        self.ui.uploadButton.connect('clicked(bool)', self.onUploadButtonClicked)

        self.ui.inputFolderSelector.filters = ctk.ctkPathLineEdit.Dirs
        self.ui.outputFolderSelector.filters = ctk.ctkPathLineEdit.Dirs
        self.ui.studiesFolderSelector.filters = ctk.ctkPathLineEdit.Dirs

        # 绑定路径变化，自动重置进度条和 skipAll
        self.ui.inputFolderSelector.currentPathChanged.connect(self.resetProgressBars)
        self.ui.outputFolderSelector.currentPathChanged.connect(self.resetProgressBars)
        self.ui.studiesFolderSelector.currentPathChanged.connect(self.resetProgressBars)

    def cleanup(self):
        self.removeObservers()

    def resetProgressBars(self):
        self.ui.conversionProgressBar.setValue(0)
        self.ui.uploadProgressBar.setValue(0)
        self.skipAll = False  # 目录变化时重置 skipAll

    def onConvertButtonClicked(self):
        inputPath = self.ui.inputFolderSelector.currentPath
        outputPath = self.ui.outputFolderSelector.currentPath

        if not inputPath:
            slicer.util.errorDisplay('Please select a DICOM folder.')
            return

        if not os.path.exists(inputPath):
            slicer.util.errorDisplay('Input folder does not exist.')
            return

        if not outputPath:
            slicer.util.infoDisplay('No output folder selected, using default output folder.')
            outputPath = '/tmp/convertedNifti'

        if not os.path.exists(outputPath):
            os.makedirs(outputPath)

        slicer.util.showStatusMessage(f'Converting: {inputPath} to {outputPath}')

        cmd = ['dcm2niix', '-z', 'y', '-o', outputPath, inputPath]
        slicer.util.showStatusMessage(f'Executing: {" ".join(cmd)}')

        self.ui.conversionProgressBar.setValue(0)
        self.progressValue = 0
        self.progressTimer.start(100)

        try:
            result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            fullLog = result.stdout + '\n' + result.stderr
            self.ui.logTextBox.setPlainText(fullLog)

            if result.returncode == 0:
                slicer.util.showStatusMessage('Conversion completed successfully.')
                slicer.util.infoDisplay('Conversion completed.')

                if self.ui.autoUploadCheckBox.isChecked():
                    self.onUploadButtonClicked()

            else:
                slicer.util.errorDisplay('Conversion failed. Check the log below.')

        except Exception as e:
            slicer.util.errorDisplay(f'Error running dcm2niix: {str(e)}')
        finally:
            if self.progressTimer:
                self.progressTimer.stop()
            self.ui.conversionProgressBar.setValue(100)
            slicer.app.processEvents()

    def updateProgressBar(self):
        if self.progressValue < 90:
            self.progressValue += 5
            self.ui.conversionProgressBar.setValue(self.progressValue)
        else:
            self.progressTimer.stop()

    def onUploadButtonClicked(self):
        self.skipAll = False  # 每次上传重置 skipAll 状态
        outputPath = self.ui.outputFolderSelector.currentPath
        studiesPath = self.ui.studiesFolderSelector.currentPath
        skipExisting = self.ui.skipExistingCheckBox.isChecked()

        if not outputPath:
            slicer.util.errorDisplay('No output folder to upload.')
            return
        if not os.path.exists(outputPath):
            slicer.util.errorDisplay('Output folder does not exist.')
            return
        if not studiesPath:
            slicer.util.errorDisplay('Please select the MONAI studies folder path.')
            return
        if not os.path.exists(studiesPath):
            slicer.util.errorDisplay('Studies folder path does not exist.')
            return

        slicer.util.showStatusMessage(f'Uploading to studies folder: {studiesPath}')
        self.ui.uploadProgressBar.setValue(0)

        uploadFiles = [f for f in os.listdir(outputPath) if f.endswith('.nii.gz') or f.endswith('.json')]
        if not uploadFiles:
            slicer.util.errorDisplay('No NIfTI or JSON files found to upload.')
            return

        try:
            total = len(uploadFiles)
            processed = 0

            for file in uploadFiles:
                srcPath = os.path.join(outputPath, file)
                dstPath = os.path.join(studiesPath, file)

                if os.path.exists(dstPath):
                    if skipExisting:
                        self.ui.logTextBox.append(f'Skipped (already exists): {file}')
                        processed += 1
                        self.ui.uploadProgressBar.setValue(int(processed / total * 100))
                        slicer.app.processEvents()
                        continue

                    if not self.skipAll:
                        msgBox = QMessageBox(slicer.util.mainWindow())
                        msgBox.setWindowTitle("File Exists")
                        msgBox.setText(f"File {file} already exists. What do you want to do?")
                        skipButton = msgBox.addButton("Skip", QMessageBox.NoRole)
                        overwriteButton = msgBox.addButton("Overwrite", QMessageBox.YesRole)
                        skipAllButton = msgBox.addButton("Skip All", QMessageBox.RejectRole)
                        msgBox.exec()

                        clickedButton = msgBox.clickedButton()

                        if clickedButton == overwriteButton:
                            self.ui.logTextBox.append(f'Overwritten: {file}')
                        elif clickedButton == skipButton:
                            self.ui.logTextBox.append(f'Skipped: {file}')
                            processed += 1
                            self.ui.uploadProgressBar.setValue(int(processed / total * 100))
                            slicer.app.processEvents()
                            continue
                        else:
                            self.skipAll = True
                            self.ui.logTextBox.append(f'Skipped (skip all triggered): {file}')
                            processed += 1
                            self.ui.uploadProgressBar.setValue(int(processed / total * 100))
                            slicer.app.processEvents()
                            continue
                    else:
                        self.ui.logTextBox.append(f'Skipped (skip all triggered): {file}')
                        processed += 1
                        self.ui.uploadProgressBar.setValue(int(processed / total * 100))
                        slicer.app.processEvents()
                        continue
                else:
                    self.ui.logTextBox.append(f'Copied: {file}')

                shutil.copy(srcPath, dstPath)
                slicer.util.showStatusMessage(f'Copying {file} to {dstPath}')

                processed += 1
                self.ui.uploadProgressBar.setValue(int(processed / total * 100))
                slicer.app.processEvents()

            slicer.util.infoDisplay('Upload (copy) completed.')
            slicer.util.showStatusMessage('Upload (copy) completed.')

        except Exception as e:
            slicer.util.errorDisplay(f'Error during upload (copy): {str(e)}')