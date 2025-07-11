cmake_minimum_required(VERSION 3.16.3...3.19.7 FATAL_ERROR)

project(DicomNiftiUploader)

#-----------------------------------------------------------------------------
# Extension meta-information
set(EXTENSION_HOMEPAGE "https://www.slicer.org/wiki/Documentation/Nightly/Extensions/DicomNiftiUploader")
set(EXTENSION_CATEGORY "Examples")
set(EXTENSION_CONTRIBUTORS "Minnie Zhang (NYU Tandon)")
set(EXTENSION_DESCRIPTION "Convert DICOM to NIfTI and optionally upload to MONAI Label Server.")
set(EXTENSION_ICONURL "https://www.example.com/Slicer/Extensions/DicomNiftiUploader.png")
set(EXTENSION_SCREENSHOTURLS "https://www.example.com/Slicer/Extensions/DicomNiftiUploader/Screenshots/1.png")
set(EXTENSION_DEPENDS "NA") # Specified as a list or "NA" if no dependencies

#-----------------------------------------------------------------------------
# Extension dependencies
find_package(Slicer REQUIRED)
include(${Slicer_USE_FILE})

#-----------------------------------------------------------------------------
# Extension modules
add_subdirectory(DicomNiftiModule)
## NEXT_MODULE

#-----------------------------------------------------------------------------
include(${Slicer_EXTENSION_GENERATE_CONFIG})
include(${Slicer_EXTENSION_CPACK})
