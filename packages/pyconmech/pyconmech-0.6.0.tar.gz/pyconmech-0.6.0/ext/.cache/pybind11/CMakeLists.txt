# Distributed under the OSI-approved MIT License.  See accompanying
# file LICENSE or https://github.com/Crascit/DownloadProject for details.

cmake_minimum_required(VERSION 2.8.2)

project(pybind11-download NONE)

include(ExternalProject)
ExternalProject_Add(pybind11-download
                    GIT_CONFIG advice.detachedHead=false;GIT_REPOSITORY;https://github.com/pybind/pybind11.git;GIT_TAG;97784dad3e518ccb415d5db57ff9b933495d9024
                    SOURCE_DIR          "D:/code_ws/pb_ws/conmech/cmake/../ext/pybind11"
                    BINARY_DIR          "D:/code_ws/pb_ws/conmech/build/temp.win-amd64-3.7/Release/pybind11-build"
                    CONFIGURE_COMMAND   ""
                    BUILD_COMMAND       ""
                    INSTALL_COMMAND     ""
                    TEST_COMMAND        ""
)
