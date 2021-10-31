#include <benchmark/benchmark.h>
#include "common.h"




template<typename Vec, typename Real = typename Vec::value_type>
auto get_product(Vec const &v, Real thresh) {
    Real p = 1.0;
    for (auto x: v) {
        Real f = x > thresh? 2 : 1.5;
        p *= f * x;
    }
    return p;
}



constexpr std::size_t len = 1024;
constexpr std::size_t seed = 0;

static void BM_BranchPercentage(benchmark::State &state) {
    auto distrib = std::uniform_real_distribution();
    auto v = get_random_vec(len, seed, distrib);
    double thresh = state.range(0) * .01;

    for (auto _: state) {
        benchmark::DoNotOptimize(get_product(v, thresh));
        benchmark::ClobberMemory();
    }

    auto bytes = len * sizeof(double);
    state.SetBytesProcessed(bytes * state.iterations());
    state.counters["thresh"] = state.range(0);
}


BENCHMARK(BM_BranchPercentage)->DenseRange(0, 100, 5);


BENCHMARK_MAIN();