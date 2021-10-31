#include <benchmark/benchmark.h>
#include "common.h"

#include <stdexcept>

constexpr std::size_t max_len = 32;
constexpr std::size_t seed = 1;


void quick_sort(auto first, auto last) {
    if (first == last) {
        return;
    }
    auto pivot = *std::next(first, std::distance(first, last) / 2);
    auto middle1 = std::partition(first, last, [pivot](const auto &em) { return em < pivot; });
    auto middle2 = std::partition(middle1, last, [pivot](const auto &em) { return !(pivot < em); });
    quick_sort(first, middle1);
    quick_sort(middle2, last);
}

void bubble_sort(auto first, auto last) {
    for (auto i = first; i != last; ++i) {
        for (auto j = first; j < i; ++j) {
            if (*i < *j) {
                std::iter_swap(i, j);
            }
        }
    }
}

void merge_sort(auto first, auto last) {
    if (last - first > 1) {
        auto middle = first + (last - first) / 2;
        merge_sort(first, middle);
        merge_sort(middle, last);
        std::inplace_merge(first, middle, last);
    }
}

void insertion_sort(auto first, auto last) {
    for (auto i = first; i != last; ++i) {
        std::rotate(std::upper_bound(first, i, *i), i, i + 1);
    }
}

static void BM_SortBase(benchmark::State &state, auto sort) {
    auto len = state.range(0);
    auto distrib = std::uniform_int_distribution(-100000, 100000);
    const auto v0 = get_random_vec(len, seed, distrib);
    auto v = v0;

    for (auto _: state) {
        v = v0;
        sort(v.begin(), v.end());
        benchmark::ClobberMemory();
    }

    if (!std::is_sorted(v.begin(), v.end())) {
        throw std::runtime_error("bad sort");
    }

    auto bytes = len * sizeof(int);
    state.SetBytesProcessed(bytes * state.iterations());
    state.counters["bytes_used"] = benchmark::Counter(bytes,
                                                      benchmark::Counter::kDefaults,
                                                      benchmark::Counter::OneK::kIs1024);
    state.counters["n"] = state.range(0);
}

static void BM_QuickSort(benchmark::State &state) {
    using It = std::vector<int>::iterator;
    BM_SortBase(state, quick_sort < It, It > );
    state.SetLabel("quick");
}

static void BM_BubbleSort(benchmark::State &state) {
    using It = std::vector<int>::iterator;
    BM_SortBase(state, bubble_sort < It, It > );
    state.SetLabel("bubble");
}

static void BM_MergeSort(benchmark::State &state) {
    using It = std::vector<int>::iterator;
    BM_SortBase(state, merge_sort < It, It > );
    state.SetLabel("merge");
}


static void BM_InsertionSort(benchmark::State &state) {
    using It = std::vector<int>::iterator;
    BM_SortBase(state, insertion_sort < It, It > );
    state.SetLabel("insertion");
}

static void BM_StdSort(benchmark::State &state) {
    using It = std::vector<int>::iterator;
    BM_SortBase(state, std::sort<It>);
    state.SetLabel("std::sort");
}

BENCHMARK(BM_QuickSort)->RangeMultiplier(2)->Range(2, max_len);
BENCHMARK(BM_BubbleSort)->RangeMultiplier(2)->Range(2, max_len);
BENCHMARK(BM_MergeSort)->RangeMultiplier(2)->Range(2, max_len);
BENCHMARK(BM_InsertionSort)->RangeMultiplier(2)->Range(2, max_len);
BENCHMARK(BM_StdSort)->RangeMultiplier(2)->Range(2, max_len);



BENCHMARK_MAIN();