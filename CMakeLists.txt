cmake_minimum_required(VERSION 3.10)
option(BUILD_EXE "Build an Executable" FALSE)

project(incc)

find_package(fmt CONFIG REQUIRED)
find_package(Boost REQUIRED COMPONENTS thread)

# find all the files within src
file(GLOB_RECURSE SOURCES CONFIGURE_DEPENDS "src/*.cpp")

if (BUILD_EXE)
    message("Building executable")
    add_executable(incc ${SOURCES})
else()
    message("Building library")
    add_library(incc STATIC ${SOURCES})
endif()

target_include_directories(incc PUBLIC "${CMAKE_CURRENT_SOURCE_DIR}/include")

target_link_libraries(incc PRIVATE fmt::fmt)
target_link_libraries(incc PRIVATE Boost::thread)

# Specify install directories
install(TARGETS incc DESTINATION lib)
install(DIRECTORY include/ DESTINATION include/incc)