# DicomNiftiModule

A 3D Slicer extension for converting DICOM series to NIfTI (`.nii.gz`) format using `dcm2niix`, with optional one-click upload to a MONAI Label Server studies folder.
**
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
├── DicomNiftiModule.py              # Main module logic
├── Resources/
│   └── UI/
│       └── DicomNiftiModule.ui     # Qt Designer UI file
├── README.md
├── .gitignore
└── LICENSE (optional)
```

---

## Quick Start (Step-by-Step)

### 1. Install Required Tools

#### Install 3D Slicer

Download and install the latest stable version from:  
https://www.slicer.org/

#### Install `dcm2niix`

This tool is required to convert DICOM series into NIfTI format.

##### 🪟 Windows (via GitHub release)

1. Go to: https://github.com/rordenlab/dcm2niix/releases  
2. Download `dcm2niix_win64.zip`  
3. Extract it to a folder, e.g., `C:\dcm2niix\`  
4. Add that folder to your system `PATH`:  
   - Search "Environment Variables" in Windows
   - Edit the "Path" under **System Variables**
   - Add: `C:\dcm2niix\`
5. Open Command Prompt and run:
   ```bash
   dcm2niix --version
   ```
   If it prints version info, you’re good to go!

##### 🍎 macOS (via Homebrew)

```bash
brew install dcm2niix
```

##### 🐧 Ubuntu/Debian

```bash
sudo apt install dcm2niix
```

Then verify with:
```bash
dcm2niix --version
```

---

### 2. Download or Clone This Module

Option A – Download ZIP  
Click “Code” → “Download ZIP” and unzip

Option B – Clone with Git:
```bash
git clone https://github.com/youzi1007/DicomNiftiUploader.git
```

---

### 3. Install the Module in 3D Slicer

#### Option A: Scripted Module (Recommended)

1. Open Slicer  
2. Go to `Edit → Application Settings → Modules`  
3. Under "Additional Module Paths", click ➕  
4. Select the `DicomNiftiModule` folder  
5. Restart Slicer  

You’ll now see **DicomNiftiModule** in the Modules dropdown.

#### Option B: Load UI manually

1. Open Slicer  
2. Open `View → Python Interactor`  
3. Run this (update the path):
```python
slicer.util.loadUI('/full/path/to/DicomNiftiModule/Resources/UI/DicomNiftiModule.ui')
```

---

### 4. Using the Module

1. Open **DicomNiftiModule** in the Modules panel  
2. Set:
   - **Input Folder**: folder with `.dcm` DICOM files
   - **Output Folder**: where converted `.nii.gz` files go
   - **Studies Folder**: your MONAI Label Server studies path
3. (Optional) Check "Auto-upload" if you want automatic push after convert  
4. Click **Convert**
   - Watch the progress bar and logs
5. Click **Upload** (if not auto-uploaded)

---

## MONAI Label Server Setup (Optional)

To use this with MONAI Label auto-segmentation:

1. Install MONAI Label:
```bash
pip install monailabel
```

2. Start the server:
```bash
monailabel start_server --app apps/radiology \
--studies /path/to/studies/folder \
--conf models "deepedit,segmentation" --conf preload true
```

Make sure the "Studies Folder" you set in the GUI matches the one above.

---

## Requirements

- 3D Slicer
- dcm2niix
- (Optional) MONAI Label

---

## To Do

- Batch folder conversion
- Server model target customization
- MONAI client-side API integration

---

## Credits

Developed by **Minnie Zhang**  
NYU Tandon School of Engineering
