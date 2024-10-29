# Define the path to the source folder, which is one level up in the main project directory
set(SOURCE_PATH ${CMAKE_CURRENT_LIST_DIR})

# Configure the project using the vcpkg CMake helper functions
vcpkg_cmake_configure(
    SOURCE_PATH ${SOURCE_PATH}
)

vcpkg_cmake_build()

vcpkg_cmake_install()