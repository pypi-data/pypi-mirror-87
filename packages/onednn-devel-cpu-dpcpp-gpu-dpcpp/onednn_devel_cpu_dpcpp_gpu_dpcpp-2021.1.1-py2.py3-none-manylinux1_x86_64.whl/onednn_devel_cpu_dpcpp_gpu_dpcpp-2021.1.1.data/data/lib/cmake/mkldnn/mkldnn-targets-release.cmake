#----------------------------------------------------------------
# Generated CMake target import file for configuration "release".
#----------------------------------------------------------------

# Commands may need to know the format version.
set(CMAKE_IMPORT_FILE_VERSION 1)

# Import target "MKLDNN::mkldnn" for configuration "release"
set_property(TARGET MKLDNN::mkldnn APPEND PROPERTY IMPORTED_CONFIGURATIONS RELEASE)
set_target_properties(MKLDNN::mkldnn PROPERTIES
  IMPORTED_LINK_INTERFACE_LIBRARIES_RELEASE "sycl;OpenCL;-lpthread;TBB::tbb"
  IMPORTED_LOCATION_RELEASE "${_IMPORT_PREFIX}/lib/libdnnl.so.2.0"
  IMPORTED_SONAME_RELEASE "libdnnl.so.2"
  )

list(APPEND _IMPORT_CHECK_TARGETS MKLDNN::mkldnn )
list(APPEND _IMPORT_CHECK_FILES_FOR_MKLDNN::mkldnn "${_IMPORT_PREFIX}/lib/libdnnl.so.2.0" )

# Commands beyond this point should not need to know the version.
set(CMAKE_IMPORT_FILE_VERSION)
