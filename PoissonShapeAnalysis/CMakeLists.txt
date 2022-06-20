
#-----------------------------------------------------------------------------
#add_subdirectory(lib/alglib/src)

#-----------------------------------------------------------------------------
set(MODULE_NAME PoissonShapeAnalysis)

#-----------------------------------------------------------------------------
#
# SlicerExecutionModel
#
find_package(SlicerExecutionModel REQUIRED)
include(${SlicerExecutionModel_USE_FILE})

find_package(Boost 1.45.0) 
include_directories(${Boost_INCLUDE_DIRS})

#
# ITK
#
set(${PROJECT_NAME}_ITK_COMPONENTS
  ITKIOImageBase
  ITKCommon
  ITKIOTransformBase
  ITKTransform
  ITKSmoothing
  ITKOptimizers
  ITKQuadEdgeMesh
  )
find_package(ITK 4.6 COMPONENTS ${${PROJECT_NAME}_ITK_COMPONENTS} REQUIRED)
if(ITK_VERSION VERSION_GREATER_EQUAL "5.3")
  foreach(factory_uc IN ITEMS "IMAGEIO" "MESHIO" "TRANSFORMIO")
    set(ITK_NO_${factory_uc}_FACTORY_REGISTER_MANAGER 1)
  endforeach()
else()
  set(ITK_NO_IO_FACTORY_REGISTER_MANAGER 1) # See Libs/ITKFactoryRegistration/CMakeLists.txt
endif()
include(${ITK_USE_FILE})

#-----------------------------------------------------------------------------
set(MODULE_INCLUDE_DIRECTORIES
  lib
  )

#-----------------------------------------------------------------------------
set(MODULE_SRCS
  lib/itkVtkMeshConversion.cxx
  )

set(MODULE_TARGET_LIBRARIES
  #alglib
  ${ITK_LIBRARIES}
  ${VTK_LIBRARIES}
  ${Boost_LIBRARIES}
  )

#-----------------------------------------------------------------------------
SEMMacroBuildCLI(
  NAME ${MODULE_NAME}
  TARGET_LIBRARIES ${MODULE_TARGET_LIBRARIES}
  INCLUDE_DIRECTORIES ${MODULE_INCLUDE_DIRECTORIES}
  ADDITIONAL_SRCS ${MODULE_SRCS}
  )

#-----------------------------------------------------------------------------
if(BUILD_TESTING)
  add_subdirectory(Testing)
endif()
