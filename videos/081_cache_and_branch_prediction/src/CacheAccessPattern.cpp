#include <benchmark/benchmark.h>

#include "common.h"


auto get_perm(std::size_t len, std::size_t seed) {
    std::vector<std::size_t> indices(len);
    std::iota(indices.begin(), indices.end(), 0); // fill with 0 ... n-1
    std::shuffle(indices.begin(), indices.end(), std::mt19937(seed));
    return indices;
}


struct S {
    int x;
    int y;
};

void what_is_cache(S s) {
    auto x = s.x;
    auto y = s.y;
}


auto get_sum(auto const &v, auto const &indices) {
    int sum = 0;
    for (auto i: indices) {
        sum += v[i];
    }
    return sum;
}


auto get_sum_list(auto const &l) {
    int sum = 0;
    for (auto x: l) {
        sum += x;
    }
    return sum;
}

constexpr std::size_t max_len = 1 << 21;
constexpr std::size_t seed = 0;

static void BM_AccessLinearly(benchmark::State &state) {
    auto len = state.range(0);
    auto distrib = std::uniform_int_distribution(-10000, 10000);
    auto v = get_random_vec(len, seed, distrib);
    std::vector<std::size_t> indices(v.size());
    std::iota(indices.begin(), indices.end(), 0); // fill with 0 ... n-1
    for (auto _: state) {
        benchmark::DoNotOptimize(get_sum(v, indices));
    }
    auto bytes = 2 * len * sizeof(int);
    state.SetBytesProcessed(bytes * state.iterations());
    state.counters["bytes_used"] = benchmark::Counter(bytes,
                                                      benchmark::Counter::kDefaults,
                                                      benchmark::Counter::OneK::kIs1024);
    state.counters["n"] = state.range(0);
    state.SetLabel("vector inorder");
}


static void BM_AccessRandom(benchmark::State &state) {
    auto len = state.range(0);
    auto distrib = std::uniform_int_distribution(-10000, 10000);
    auto v = get_random_vec(state.range(0), seed, distrib);
    auto indices = get_perm(len, seed); // random permutation of 0 ... n-1

    for (auto _: state) {
        benchmark::DoNotOptimize(get_sum(v, indices));
    }

    auto bytes = 2 * len * sizeof(int);
    state.SetBytesProcessed(bytes * state.iterations());
    state.counters["bytes_used"] = benchmark::Counter(bytes,
                                                      benchmark::Counter::kDefaults,
                                                      benchmark::Counter::OneK::kIs1024);
    state.counters["n"] = state.range(0);
    state.SetLabel("vector random");
}

static void BM_AccessList(benchmark::State &state) {
    auto len = state.range(0);
    auto distrib = std::uniform_int_distribution(-10000, 10000);
    auto l = get_random_list(state.range(0), seed, distrib);

    for (auto _: state) {
        benchmark::DoNotOptimize(get_sum_list(l));
    }

    auto bytes = 2 * len * sizeof(int);
    state.SetBytesProcessed(bytes * state.iterations());
    state.counters["bytes_used"] = benchmark::Counter(bytes,
                                                      benchmark::Counter::kDefaults,
                                                      benchmark::Counter::OneK::kIs1024);
    state.counters["n"] = state.range(0);
    state.SetLabel("list");
}


template<typename Vec>
void matrix_multiply_ijk(Vec const &a, Vec const &b, Vec &out, int const N) {
    std::fill(out.begin(), out.end(), 0);
    for (int i = 0; i < N; ++i) {
        for (int j = 0; j < N; ++j) {
            // out_ij += a_ik * b_kj;
            for (int k = 0; k < N; ++k) {
                out[N * i + j] += a[N * i + k] * b[N * k + j];
            }
        }
    }
}


template<typename Vec>
void matrix_multiply_ikj(Vec const &a, Vec const &b, Vec &out, int const N) {
    std::fill(out.begin(), out.end(), 0);
    for (int i = 0; i < N; ++i) {
        for (int k = 0; k < N; ++k) {
            for (int j = 0; j < N; ++j) {
                out[N * i + j] += a[N * i + k] * b[N * k + j];
            }
        }
    }
}


template<typename Vec>
void matrix_multiply_jik(Vec const &a, Vec const &b, Vec &out, int const N) {
    std::fill(out.begin(), out.end(), 0);
    for (int j = 0; j < N; ++j) {
        for (int i = 0; i < N; ++i) {
            for (int k = 0; k < N; ++k) {
                out[N * i + j] += a[N * i + k] * b[N * k + j];
            }
        }
    }
}


template<typename Vec>
void matrix_multiply_jki(Vec const &a, Vec const &b, Vec &out, int const N) {
    std::fill(out.begin(), out.end(), 0);
    for (int j = 0; j < N; ++j) {
        for (int k = 0; k < N; ++k) {
            for (int i = 0; i < N; ++i) {
                out[N * i + j] += a[N * i + k] * b[N * k + j];
            }
        }
    }
}

template<typename Vec>
void matrix_multiply_kij(Vec const &a, Vec const &b, Vec &out, int const N) {
    std::fill(out.begin(), out.end(), 0);
    for (int k = 0; k < N; ++k) {
        for (int i = 0; i < N; ++i) {
            for (int j = 0; j < N; ++j) {
                out[N * i + j] += a[N * i + k] * b[N * k + j];
            }
        }
    }
}

template<typename Vec>
void matrix_multiply_kji(Vec const &a, Vec const &b, Vec &out, int const N) {
    std::fill(out.begin(), out.end(), 0);
    for (int k = 0; k < N; ++k) {
        for (int j = 0; j < N; ++j) {
            for (int i = 0; i < N; ++i) {
                out[N * i + j] += a[N * i + k] * b[N * k + j];
            }
        }
    }
}

using MatrixMultiplyIntFunction = decltype(&matrix_multiply_ikj<std::vector<int>>);

static void BM_MatrixMultiplyBase(benchmark::State &state, MatrixMultiplyIntFunction mult) {
    int N = 64;
    auto len = N * N;
    auto distrib = std::uniform_int_distribution(-10000, 10000);
    auto a = get_random_vec(len, seed, distrib);
    auto b = get_random_vec(len, seed + 1, distrib);
    auto result = decltype(a)(len);

    for (auto _: state) {
        mult(a, b, result, N);
        benchmark::ClobberMemory();
    }

    auto bytes = 3 * len * sizeof(int);
    state.SetBytesProcessed(bytes * state.iterations());
}

static void BM_MatrixMultiplyIJK(benchmark::State &state) {
    BM_MatrixMultiplyBase(state, &matrix_multiply_ijk);
    state.SetLabel("ijk");
}

static void BM_MatrixMultiplyIKJ(benchmark::State &state) {
    BM_MatrixMultiplyBase(state, &matrix_multiply_ikj);
    state.SetLabel("ikj");
}

static void BM_MatrixMultiplyJIK(benchmark::State &state) {
    BM_MatrixMultiplyBase(state, &matrix_multiply_jik);
    state.SetLabel("jik");
}

static void BM_MatrixMultiplyJKI(benchmark::State &state) {
    BM_MatrixMultiplyBase(state, &matrix_multiply_jki);
    state.SetLabel("jki");
}

static void BM_MatrixMultiplyKIJ(benchmark::State &state) {
    BM_MatrixMultiplyBase(state, &matrix_multiply_kij);
    state.SetLabel("kij");
}

static void BM_MatrixMultiplyKJI(benchmark::State &state) {
    BM_MatrixMultiplyBase(state, &matrix_multiply_kji);
    state.SetLabel("kji");
}

BENCHMARK(BM_MatrixMultiplyIJK);
BENCHMARK(BM_MatrixMultiplyIKJ);
BENCHMARK(BM_MatrixMultiplyJIK);
BENCHMARK(BM_MatrixMultiplyJKI);
BENCHMARK(BM_MatrixMultiplyKIJ);
BENCHMARK(BM_MatrixMultiplyKJI);
BENCHMARK(BM_AccessLinearly)->RangeMultiplier(2)->Range(64, max_len);
BENCHMARK(BM_AccessRandom)->RangeMultiplier(2)->Range(64, max_len);
BENCHMARK(BM_AccessList)->RangeMultiplier(2)->Range(64, max_len);

BENCHMARK_MAIN();