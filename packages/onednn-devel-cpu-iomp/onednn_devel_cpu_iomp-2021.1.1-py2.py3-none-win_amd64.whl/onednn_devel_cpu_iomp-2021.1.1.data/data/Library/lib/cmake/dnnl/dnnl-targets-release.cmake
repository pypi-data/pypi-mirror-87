#----------------------------------------------------------------
# Generated CMake target import file for configuration "Release".
#----------------------------------------------------------------

# Commands may need to know the format version.
set(CMAKE_IMPORT_FILE_VERSION 1)

# Import target "DNNL::dnnl" for configuration "Release"
set_property(TARGET DNNL::dnnl APPEND PROPERTY IMPORTED_CONFIGURATIONS RELEASE)
set_target_properties(DNNL::dnnl PROPERTIES
  IMPORTED_IMPLIB_RELEASE "${_IMPORT_PREFIX}/lib/dnnl.lib"
  IMPORTED_LOCATION_RELEASE "${_IMPORT_PREFIX}/bin/dnnl.dll"
  )

list(APPEND _IMPORT_CHECK_TARGETS DNNL::dnnl )
list(APPEND _IMPORT_CHECK_FILES_FOR_DNNL::dnnl "${_IMPORT_PREFIX}/lib/dnnl.lib" "${_IMPORT_PREFIX}/bin/dnnl.dll" )

# Commands beyond this point should not need to know the version.
set(CMAKE_IMPORT_FILE_VERSION)
