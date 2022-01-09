cmake_minimum_required(VERSION 3.18)
project(endl_does_not_sync)

set(CMAKE_CXX_STANDARD 20)
find_package(Threads REQUIRED)

add_executable(endl_does_not_sync main.cpp)
target_link_libraries(endl_does_not_sync ${CMAKE_THREAD_LIBS_INIT})