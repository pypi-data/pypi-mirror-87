cmake_minimum_required(VERSION 3.14...3.17)

project(libfibomat)  # VERSION "0.1"


# https://github.com/scikit-build/scikit-build/issues/386


set(CMAKE_CXX_STANDARD 17)
set(PYBIND11_CPP_STANDARD -std=c++17)

# Define CMAKE_INSTALL_xxx: LIBDIR, INCLUDEDIR
include(GNUInstallDirs)

# Fetch pybind11
include(FetchContent)

FetchContent_Declare(
        pybind11
        GIT_REPOSITORY https://github.com/pybind/pybind11
        GIT_TAG v2.6.0
)
FetchContent_MakeAvailable(pybind11)

FetchContent_Declare(
        nlohmann_json
        GIT_REPOSITORY https://github.com/nlohmann/json
        GIT_TAG v3.9.1
)

set(JSON_BuildTests OFF CACHE INTERNAL "")
set(JSON_Install OFF CACHE INTERNAL "")

FetchContent_MakeAvailable(nlohmann_json)

#FetchContent_Declare(
#        rangev3
#        GIT_REPOSITORY https://github.com/ericniebler/range-v3
#        GIT_TAG 0.11.0
#)
#FetchContent_MakeAvailable(rangev3)

SET(CAVC_HEADER_ONLY ON CACHE BOOL "")
FetchContent_Declare(
        cavc
        GIT_REPOSITORY https://github.com/jbuckmccready/CavalierContours
        GIT_TAG master
)
FetchContent_MakeAvailable(cavc)

set(python_module_name _libfibomat)
pybind11_add_module(${python_module_name} MODULE
        src_cpp/libfibomat.cpp
        )

target_include_directories(${python_module_name} PRIVATE ${cavc_SOURCE_DIR}/include)
target_link_libraries(${python_module_name} PRIVATE CavalierContours)  # range-v3

install(TARGETS ${python_module_name} DESTINATION .)

# Quiet a warning, since this project is only valid with SKBUILD
set(ignoreMe "${SKBUILD}")




#cmake_minimum_required(VERSION 3.5)
#
#project(libfibomat)
#
#set(CMAKE_CXX_STANDARD 17)
#
##cmake .. -DBUILD_STANDALONE_LIB=ON
## option(BUILD_STANDALONE_LIB "Set to ON if cmake is not called from setup.py to fix path issue" OFF)
#
## if (BUILD_STANDALONE_LIB)
##     set(output_name "_libfibomat")
## else()
##     set(output_name "fibomat/_libfibomat")
## endif(BUILD_STANDALONE_LIB)
#
#set(output_name "fibomat/_libfibomat")
#
#
#SET(CAVC_HEADER_ONLY ON CACHE BOOL "using headers only")
#add_subdirectory(${CMAKE_SOURCE_DIR}/third_party/CavalierContours)
#
#set(JSON_BuildTests OFF CACHE INTERNAL "")
#add_subdirectory(${CMAKE_SOURCE_DIR}/third_party/json)
#
#add_subdirectory(${CMAKE_SOURCE_DIR}/third_party/range-v3)
#
## https://github.com/pybind/pybind11/issues/1330
##set(MY_TARGET_PYTHON_INCLUDE_DIRS "/home/yorgo/.wine/drive_c/users/yorgo/Local Settings/Application Data/Programs/Python/Python38/include")
##
### Tell pybind11 where the target python installation is
##set(PYTHON_INCLUDE_DIRS ${MY_TARGET_PYTHON_INCLUDE_DIRS} CACHE INTERNAL "Cross python include path")
##set(PYTHON_MODULE_EXTENSION ".dll" CACHE INTERNAL "Cross python lib extension")
##
### Disable pybind11 python search mechanism
##set(PYTHONLIBS_FOUND TRUE CACHE INTERNAL "")
#
## set(PYBIND11_CPP_STANDARD -std=c++1z)
#add_subdirectory(${CMAKE_SOURCE_DIR}/third_party/pybind11)
#
##pybind11_add_module(libfibomat ${CMAKE_SOURCE_DIR}/src_cpp/curve.h ${CMAKE_SOURCE_DIR}/src_cpp/libfibomat.cpp)
#
## ${CMAKE_SOURCE_DIR}/src_cpp/svg_import/svgpp_parser_impl.cpp
#add_library(libfibomat MODULE ${CMAKE_SOURCE_DIR}/src_cpp/libfibomat.cpp)
#target_link_libraries(libfibomat PRIVATE pybind11::module)
#set_target_properties(libfibomat PROPERTIES PREFIX "${PYTHON_MODULE_PREFIX}"
#        SUFFIX "${PYTHON_MODULE_EXTENSION}")
#
#target_compile_options(libfibomat PUBLIC -fvisibility=hidden -O3)
#set_target_properties(libfibomat PROPERTIES OUTPUT_NAME ${output_name})
#
#target_link_libraries(libfibomat PRIVATE CavalierContours range-v3::range-v3 )
#
## target_include_directories(libfibomat PRIVATE ${CMAKE_SOURCE_DIR}/third_party/svgpp/include)
## target_include_directories(libfibomat PRIVATE ${CMAKE_SOURCE_DIR}/third_party/svgpp/third_party)
#target_include_directories(libfibomat PRIVATE ${CMAKE_SOURCE_DIR}/third_party/pybind11_json/include)
#
#target_link_libraries(libfibomat PRIVATE nlohmann_json::nlohmann_json)
#
#
## add_executable(libfibomat_test src_cpp/main.cpp)
## target_link_libraries(libfibomat_test CavalierContours)
