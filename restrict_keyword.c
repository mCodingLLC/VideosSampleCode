// Compile with
// gcc --std=c17 -O3 restrict_keyword.c

#include <stdlib.h>   // malloc, free, size_t
#include <stdio.h>    // printf
#include <stdint.h>   // uint64_t
#include <inttypes.h> // print format for uint64_t

void *memcpy(void *restrict dst, const void *restrict src, size_t n);
void *memmove(void *dst, const void *src, size_t n);

void add_sub(int *x, int *y, int *amount)
{
    *x += *amount;
    *y -= *amount;
}

//precondition: dst, src1, src2 do not overlap
void vector_add(int64_t *restrict dst, const int64_t *src1, const int64_t *src2, size_t n)
{
    for (size_t i = 0; i < n; i++)
        dst[i] = src1[i] + src2[i];
}

void vector_add_allow_overlapping(int64_t *dst, const int64_t *src1, const int64_t *src2, size_t n)
{
    for (size_t i = 0; i < n; i++)
        dst[i] = src1[i] + src2[i];
}

void fib_upto_n(int64_t *dst, size_t n)
{
    dst[0] = 0;
    if (n == 0)
        return;
    dst[1] = 1;
    if (n == 1)
        return;
    vector_add_allow_overlapping(dst + 2, dst, dst + 1, n - 2);
}

void print_n(const int64_t *arr, size_t n)
{
    for (size_t i = 0; i < n; i++)
        printf("%" PRId64 "\n", arr[i]);
}

int main()
{
    size_t n = 10;
    int64_t *fibs = malloc((sizeof *fibs) * n);
    fib_upto_n(fibs, n);
    print_n(fibs, n);
    free(fibs);
    return 0;
}
