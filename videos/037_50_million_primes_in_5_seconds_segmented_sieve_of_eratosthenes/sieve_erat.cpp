#include <string>
#include <vector>
#include <iostream>
#include <fstream>
#include <exception>
#include <cstdlib>
#include <algorithm>

using Int = uint64_t;

template <typename T, typename = std::enable_if_t<std::is_integral_v<T> && std::is_unsigned_v<T>>>
constexpr T largest_squarable()
{
    return (static_cast<T>(1) << (std::numeric_limits<T>::digits >> 1)) - static_cast<T>(1);
}

constexpr Int smallest_multiple_of_n_geq_m(const Int n, const Int m)
{
    if (m % n == 0)
    {
        return m;
    }
    return m + (n - (m % n));
}

class SegmentedPrimes
{
public:
    SegmentedPrimes() : primes{2, 3, 5, 7}, end_segment{1}, is_prime_buffer{}
    {
    }

    void reserve(const std::size_t n)
    {
        primes.reserve(n);
    }

    std::size_t size() const
    {
        return primes.size();
    }

    Int nth_prime(const std::size_t n) const
    {
        return primes[n];
    }

    Int count_primes_leq(const Int n) const
    {
        return std::upper_bound(primes.begin(), primes.end(), n) - primes.begin();
    }

    void push_back_until_size_geq(const Int n)
    {
        while (primes.size() < n)
        {
            push_back_next_segment_of_primes();
        }
    }

    void push_back_until_max_geq(const Int n)
    {
        while (primes.back() < n)
        {
            push_back_next_segment_of_primes();
        }
    }

    /*
        push_back new primes in the range [p_k^2, p_{k+n}^2) to the primes vector, where k == end_segment and n is at least 1
        The range [p_k^2, p_{k+n}^2) is sieved by [p_0, ..., p_{k+n-1}]
        because if a composite number n has all prime factors >= p_{k+n}, then n >= p_{k+n}^2.
        Precondition: primes contains all primes in the range [2, p_k^2) and no more before writing.
        Postcondition: primes contains all primes in the range [2, p_{k+n}^2) and no more.
    */
    void push_back_at_most_n_segments_of_primes(const std::size_t n)
    {
        const std::size_t n_segments = std::min(n, primes.size() - 1 - end_segment);

        const Int p = primes[end_segment];
        const Int q = primes[end_segment + n_segments];

        if (p > largest_squarable<Int>() || q > largest_squarable<Int>())
        {
            throw std::overflow_error("square");
        }
        const Int segment_min = p * p;
        const Int segment_max = q * q - 1;

        std::size_t segment_len = static_cast<std::size_t>(segment_max - segment_min + 1); // >= 4p+4

        is_prime_buffer.clear();
        is_prime_buffer.resize(segment_len, 1);

        for (std::size_t i = 0; i <= end_segment + n_segments; ++i)
        {
            const Int test_prime = primes[i];
            const Int start = smallest_multiple_of_n_geq_m(test_prime, segment_min);

            for (std::size_t idx = static_cast<std::size_t>(start - segment_min); idx < is_prime_buffer.size(); idx += test_prime)
            {
                is_prime_buffer[idx] = 0;
            }
        }

        for (std::size_t i = 0; i < is_prime_buffer.size(); ++i)
        {
            if (is_prime_buffer[i])
            {
                primes.push_back(i + segment_min);
            }
        }
        end_segment += n_segments;
    }

    void push_back_next_segment_of_primes()
    {
        push_back_at_most_n_segments_of_primes(1);
    }

    auto get_primes() const -> const std::vector<Int> &
    {
        return primes;
    }

private:
    std::vector<Int> primes; // primes is all primes in [2, p_k^2) where k == last_segment
    std::size_t end_segment;
    std::vector<int> is_prime_buffer;
};

void write_segment(const std::vector<Int> &primes, const std::size_t start, const std::size_t end,
                   std::ostream &out)
{
    return;
    for (std::size_t i = start; i != end; ++i)
    {
        out << primes[i] << '\n';
    }
}

void write_first_n_primes(const std::size_t n, std::ostream &out)
{
    SegmentedPrimes primes;
    try
    {
        // primes.reserve(n);
        primes.push_back_until_size_geq(n);
    }
    catch (const std::bad_alloc &)
    {
        if (primes.size() < n)
        {
            std::cerr << "Error: not enough memory, only able to compute " << primes.size() << " primes" << std::endl;
            write_segment(primes.get_primes(), 0, primes.size(), out);
            std::exit(EXIT_FAILURE);
        }
    }
    catch (const std::length_error &)
    {
        if (primes.size() < n)
        {
            std::cerr << "Error: not enough memory, only able to compute " << primes.size() << " primes" << std::endl;
            write_segment(primes.get_primes(), 0, primes.size(), out);
            std::exit(EXIT_FAILURE);
        }
    }
    catch (const std::overflow_error &)
    {
        std::cerr << "Error: overflow detected, quitting early with " << primes.size() << " primes" << std::endl;
        write_segment(primes.get_primes(), 0, primes.size(), out);
        std::exit(EXIT_FAILURE);
    }

    write_segment(primes.get_primes(), 0, n, out);
}

void usage()
{
    std::cerr << "usage: sieve_erat.exe n_primes [filename]" << std::endl;
}

int main(int argc, char *argv[])
{
    if (argc < 2 || argc > 3)
    {
        usage();
        return EXIT_FAILURE;
    }

    std::size_t how_many = std::stoul(std::string(argv[1]));

    // std::ostream *out_ptr = nullptr;
    // std::ofstream out;
    // if (argc == 3)
    // {
    //     out.open(argv[2]);
    //     if (!out.is_open())
    //     {
    //         std::cerr << "Error: could not open file for writing" << std::endl;
    //         return EXIT_FAILURE;
    //     }
    //     out_ptr = &out;
    // }
    // else
    // {
    //     out_ptr = &std::cout;
    // }

    // write_first_n_primes(how_many, *out_ptr);
    SegmentedPrimes primes;
    primes.push_back_until_size_geq(how_many);
    return EXIT_SUCCESS;
}