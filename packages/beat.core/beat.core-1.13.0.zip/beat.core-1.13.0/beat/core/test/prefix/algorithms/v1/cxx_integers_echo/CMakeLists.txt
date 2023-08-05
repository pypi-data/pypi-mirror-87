cmake_minimum_required(VERSION 3.0)
project(BEAT_CORE_CXX_INTEGERS_ECHO)


set(BEAT_BACKEND_CXX_DIR "/usr/local/beat")


# CMake setup
set(CMAKE_CXX_STANDARD 14)
set(CMAKE_CXX_STANDARD_REQUIRED ON)


# Retrieve the dependencies
find_package(Boost REQUIRED)


# Setup the search paths
include_directories(
    "${BEAT_BACKEND_CXX_DIR}/include"
    "${Boost_INCLUDE_DIRS}"
)

link_directories(
    "${BEAT_BACKEND_CXX_DIR}/bin"
)


# List the source files
set(HEADERS "algorithm.h"
            "beat_setup.h"
            "user_single_integer_1.h"
)

set(SRCS "algorithm.cpp"
         "beat_setup.cpp"
         "user_single_integer_1.cpp"
)

# Create and link the library
add_library(cxx_integers_echo SHARED ${SRCS} ${HEADERS})

target_link_libraries(cxx_integers_echo beat_backend_cxx)
set_target_properties(cxx_integers_echo PROPERTIES
                                        COMPILE_FLAGS "-fPIC"
                                        OUTPUT_NAME "1"
                                        PREFIX ""
                                        LIBRARY_OUTPUT_DIRECTORY "${BEAT_CORE_CXX_INTEGERS_ECHO_SOURCE_DIR}"
)
