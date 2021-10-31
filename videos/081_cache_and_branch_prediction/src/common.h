#ifndef BIGOHNO_COMMON_H
#define BIGOHNO_COMMON_H

#include <random>
#include <vector>
#include <list>
#include <numeric>
#include <algorithm>


template<typename Container, typename Dist>
auto get_random(std::size_t len, std::size_t seed, Dist distrib) {
    std::mt19937 gen(seed);
    Container v(len);

    auto get_rand_value = [&]() {
        return distrib(gen);
    };

    std::generate(v.begin(), v.end(), get_rand_value);
    return v;
}

template<typename Dist>
auto get_random_vec(std::size_t len, std::size_t seed, Dist distrib) {
    return get_random<std::vector<typename Dist::result_type>, Dist>(len, seed, distrib);
}

template<typename Dist>
auto get_random_list(std::size_t len, std::size_t seed, Dist distrib) {
    return get_random<std::list<typename Dist::result_type>, Dist>(len, seed, distrib);
}



#endif //BIGOHNO_COMMON_H
