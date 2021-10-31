cmake_minimum_required(VERSION 3.18)
project (BigOhNo)

message("Build type: ${CMAKE_BUILD_TYPE}")

add_subdirectory(extern)
add_subdirectory(src)
