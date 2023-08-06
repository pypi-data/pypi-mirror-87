# Distributed under the OSI-approved MIT License.  See accompanying
# file LICENSE or https://github.com/Crascit/DownloadProject for details.

cmake_minimum_required(VERSION 2.8.2)

project(json-download NONE)

include(ExternalProject)
ExternalProject_Add(json-download
                    GIT_CONFIG advice.detachedHead=false;URL;https://github.com/nlohmann/json/releases/download/v3.7.3/include.zip;URL_HASH;SHA256=87b5884741427220d3a33df1363ae0e8b898099fbc59f1c451113f6732891014
                    SOURCE_DIR          "D:/code_ws/pb_ws/conmech/cmake/../ext/json"
                    BINARY_DIR          "D:/code_ws/pb_ws/conmech/build/temp.win-amd64-3.7/Release/json-build"
                    CONFIGURE_COMMAND   ""
                    BUILD_COMMAND       ""
                    INSTALL_COMMAND     ""
                    TEST_COMMAND        ""
)
