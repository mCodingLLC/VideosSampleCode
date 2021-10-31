#include <benchmark/benchmark.h>
#include "common.h"


constexpr std::size_t max_len = 1 << 20;
constexpr std::size_t seed = 1;

static void BM_VectorFindIndexBinary(benchmark::State &state) {
    auto len = state.range(0);
    auto v = get_random_vec(len, seed, std::uniform_int_distribution(-100000, 100000));
    std::sort(v.begin(), v.end());
    auto mid = v.begin() + v.size() / 2;


    for (auto _: state) {
        benchmark::DoNotOptimize(std::lower_bound(mid - state.range(0) / 2, mid + state.range(0) / 2, 0));
    }
}


static void BM_VectorFindIndexLinear(benchmark::State &state) {
    auto len = state.range(0);
    auto v = get_random_vec(len, seed, std::uniform_int_distribution(-100000, 100000));
    std::sort(v.begin(), v.end());
    auto mid = v.begin() + v.size() / 2;

    for (auto _: state) {
        benchmark::DoNotOptimize(
                std::find_if(
                        mid - state.range(0) / 2,
                        mid + state.range(0) / 2,
                        [](const auto x) { return x >= 0; })
        );
    }
}


BENCHMARK(BM_VectorFindIndexBinary)->RangeMultiplier(2)->Range(2, max_len);
BENCHMARK(BM_VectorFindIndexLinear)->RangeMultiplier(2)->Range(2, max_len);

BENCHMARK_MAIN();