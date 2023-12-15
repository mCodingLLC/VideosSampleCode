import inspect
import sys

import cloud_imports

cloud_imports.add_gh_repo("mCodingLLC", "prime_sieve", "master")
# cloud_imports.add_repo("https://example.com/your_repo")

import prime_sieve.list


def main():
    primes = prime_sieve.list.PrimeListSieve()

    print(f"{primes[:100]=}")

    print(sys.meta_path)
    print(inspect.getsource(prime_sieve.list))
    print(f"{prime_sieve.list.__file__=}")


if __name__ == "__main__":
    main()
