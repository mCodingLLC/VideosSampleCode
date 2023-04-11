cmake_minimum_required(VERSION 3.16...3.23)

project(UNIQUE_PTR_EXAMPLE)

add_executable(main main.cpp)
set_target_properties(
    main PROPERTIES
    CXX_STANDARD 20
    CXX_EXTENSIONS OFF
)