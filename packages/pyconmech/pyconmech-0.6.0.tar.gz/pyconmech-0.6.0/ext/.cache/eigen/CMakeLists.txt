# Distributed under the OSI-approved MIT License.  See accompanying
# file LICENSE or https://github.com/Crascit/DownloadProject for details.

cmake_minimum_required(VERSION 2.8.2)

project(eigen-download NONE)

include(ExternalProject)
ExternalProject_Add(eigen-download
                    GIT_CONFIG advice.detachedHead=false;GIT_REPOSITORY;https://github.com/eigenteam/eigen-git-mirror.git;GIT_TAG;3.3.7
                    SOURCE_DIR          "D:/code_ws/pb_ws/conmech/cmake/../ext/eigen"
                    BINARY_DIR          "D:/code_ws/pb_ws/conmech/build/temp.win-amd64-3.7/Release/eigen-build"
                    CONFIGURE_COMMAND   ""
                    BUILD_COMMAND       ""
                    INSTALL_COMMAND     ""
                    TEST_COMMAND        ""
)
