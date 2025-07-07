# DicomNiftiModule
A 3D Slicer extension for converting DICOM series to NIfTI (`.nii.gz`) format using
`dcm2niix`, with optional one-click upload to a MONAI Label Server studies folder.
---
## Features
- Convert DICOM to compressed NIfTI using `dcm2niix`
- Optional auto-upload to MONAI Label Server
- Skip / overwrite / skip-all dialog for upload conflicts
- Real-time progress bars and logs
- Simple Qt-based GUI fully integrated with 3D Slicer
---
## File Structure
```
DicomNiftiModule/
├── DicomNiftiModule.py # Main module logic
├── Resources/
│ └── UI/
│ └── DicomNiftiModule.ui # Qt Designer UI file
├── README.md
├── .gitignore
└── LICENSE (optional)
```
---
## Quick Start (Detailed Instructions)
### 1. Install Required Tools
#### Install 3D Slicer
Download and install the latest stable version of 3D Slicer from:
https://www.slicer.org/
#### Install `dcm2niix`
This tool is required to convert DICOM to NIfTI format.
- **Windows (via MRIcroGL)**:
Download MRIcroGL from https://www.nitrc.org/projects/mricrogl/.
Inside the zip, find `dcm2niix.exe` and note the folder path.
- **Mac (via Homebrew)**:
```bash
brew install dcm2niix
```
- **Ubuntu/Debian**:
```bash
sudo apt install dcm2niix
```
Open a terminal and verify:
```bash
dcm2niix --version
```
---
### 2. Download or Clone This Module
Click "Code" → "Download ZIP", or clone the repository:
```bash
git clone https://github.com/your-username/DicomNiftiModule.git
```
Unzip or open the folder to locate `DicomNiftiModule/`.
---
### 3. Install the Module in 3D Slicer
#### Option A: Add as a scripted module (Recommended)
1. Open Slicer
2. Go to `Edit` → `Application Settings` → `Modules`
3. Scroll to **Additional Module Paths**
4. Click ➕ and select the `DicomNiftiModule` folder
5. Restart Slicer
You will now find "DicomNiftiModule" in the **Modules** dropdown.
#### Option B: Load Manually for Testing
1. Open Slicer
2. Open `View` → `Python Interactor`
3. Run this (update path accordingly):
```python
slicer.util.loadUI('/full/path/to/DicomNiftiModule/Resources/UI/DicomNiftiModule.ui')
```
---
### 4. Using the Module
1. Open the **DicomNiftiModule** from the Modules dropdown
2. Set:
- **Input folder** (DICOM `.dcm` files)
- **Output folder** (NIfTI `.nii.gz` files will go here)
- **Studies folder** (folder used by MONAI Label Server)
3. (Optional) Check "Auto-upload"
4. Click **Convert**
- Wait for progress bar and logs to complete
5. Click **Upload** to push files to server (or auto if enabled)
---
## MONAI Label Server Setup (Optional)
To test auto-segmentation with MONAI:
1. Install MONAI Label:
```bash
pip install monailabel
```
2. Start a sample server:
```bash
monailabel start_server --app apps/radiology --studies /path/to/studies/folder
--conf models "deepedit,segmentation" --conf preload true
```
Make sure the "Studies Folder" in the UI matches `/path/to/studies/folder`.
You can then connect MONAI Label to 3D Slicer and test auto-segmentation workflows.
---
## Requirements
- 3D Slicer
- dcm2niix
- (Optional) MONAI Label
---
## To Do
- Add batch folder support
- Add support for specifying model upload targets
- Integrate MONAI client API for full pipeline
---
## Credits
Developed by Minnie Zhang (NYU Tandon School of Engineering).
