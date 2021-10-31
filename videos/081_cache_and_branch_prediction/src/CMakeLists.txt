set(CMAKE_CXX_STANDARD 20)

include(CheckIPOSupported)
check_ipo_supported(RESULT supported OUTPUT error)

add_executable(BigOhNo VectorFindIndex.cpp common.h)
add_executable(CacheAccessPatterns CacheAccessPattern.cpp common.h)
add_executable(BranchPrediction BranchPrediction.cpp common.h)
add_executable(SmallSortingComparison SmallSortingComparison.cpp common.h)

if (supported)
    message(STATUS "IPO / LTO enabled")
    set_property(TARGET BigOhNo PROPERTY INTERPROCEDURAL_OPTIMIZATION TRUE)
    set_property(TARGET CacheAccessPatterns PROPERTY INTERPROCEDURAL_OPTIMIZATION TRUE)
    set_property(TARGET BranchPrediction PROPERTY INTERPROCEDURAL_OPTIMIZATION TRUE)
    set_property(TARGET SmallSortingComparison PROPERTY INTERPROCEDURAL_OPTIMIZATION TRUE)
else ()
    message(STATUS "IPO / LTO not supported: <${error}>")
endif ()

target_link_libraries(BigOhNo benchmark::benchmark)
target_link_libraries(CacheAccessPatterns benchmark::benchmark)
target_link_libraries(BranchPrediction benchmark::benchmark)
target_link_libraries(SmallSortingComparison benchmark::benchmark)
