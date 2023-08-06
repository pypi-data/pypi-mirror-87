# Distributed under the OSI-approved MIT License.  See accompanying
# file LICENSE or https://github.com/Crascit/DownloadProject for details.

cmake_minimum_required(VERSION 2.8.2)

project(Catch2-download NONE)

include(ExternalProject)
ExternalProject_Add(Catch2-download
                    GIT_CONFIG advice.detachedHead=false;URL;https://github.com/catchorg/Catch2/archive/v2.3.0.tar.gz;URL_MD5;1fc90ff3b7b407b83057537f4136489e
                    SOURCE_DIR          "D:/code_ws/pb_ws/conmech/cmake/../ext/Catch2"
                    BINARY_DIR          "D:/code_ws/pb_ws/conmech/build/temp.win-amd64-3.7/Release/Catch2-build"
                    CONFIGURE_COMMAND   ""
                    BUILD_COMMAND       ""
                    INSTALL_COMMAND     ""
                    TEST_COMMAND        ""
)
