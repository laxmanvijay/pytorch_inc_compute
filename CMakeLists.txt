cmake_minimum_required(VERSION 3.10)

project(incc)

find_package(fmt CONFIG REQUIRED)

add_library(incc STATIC src/master.cpp)
target_include_directories(incc PUBLIC "${CMAKE_CURRENT_SOURCE_DIR}/include")

target_link_libraries(incc PRIVATE fmt::fmt)

# Specify install directories
install(TARGETS incc DESTINATION lib)
install(DIRECTORY include/ DESTINATION include/incc)