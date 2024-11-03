cmake_minimum_required(VERSION 3.10)

project(incc)

find_package(fmt CONFIG REQUIRED)
find_package(Boost REQUIRED COMPONENTS thread)

# add_executable(incc src/main.cpp src/master.cpp src/worker.cpp)
add_library(incc STATIC src/master.cpp src/worker.cpp)
target_include_directories(incc PUBLIC "${CMAKE_CURRENT_SOURCE_DIR}/include")

target_link_libraries(incc PRIVATE fmt::fmt)
target_link_libraries(incc PRIVATE Boost::thread)

# Specify install directories
install(TARGETS incc DESTINATION lib)
install(DIRECTORY include/ DESTINATION include/incc)