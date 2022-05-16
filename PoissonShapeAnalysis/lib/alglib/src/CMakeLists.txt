
set(CMAKE_INCLUDE_CURRENT_DIR ON)
set(CMAKE_INCLUDE_CURRENT_DIR_IN_INTERFACE ON)

add_library(alglib
  alglibinternal.cpp
  alglibmisc.cpp
  ap.cpp
  dataanalysis.cpp
  diffequations.cpp
  fasttransforms.cpp
  integration.cpp
  interpolation.cpp
  linalg.cpp
  optimization.cpp
  solvers.cpp
  specialfunctions.cpp
  statistics.cpp
  )
