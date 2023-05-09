#include <cstdlib>
#include <iostream>
#include <memory>
#include <utility>
#include <vector>

template <class T>
struct DefaultDelete {
    void operator()(T *ptr) { delete ptr; }
};

template <class T, class D = DefaultDelete<T>>
class unique_ptr {
   public:
    unique_ptr() noexcept : unique_ptr{nullptr} {}
    explicit unique_ptr(T *ptr) noexcept : m_ptr{ptr}, m_deleter{} {}
    unique_ptr(T *ptr, const D &deleter) noexcept
        : m_ptr{ptr}, m_deleter{deleter} {}
    unique_ptr(T *ptr, D &&deleter) noexcept
        : m_ptr{ptr}, m_deleter{std::move(deleter)} {}

    unique_ptr(const unique_ptr &) = delete;
    unique_ptr &operator=(const unique_ptr &) = delete;

    unique_ptr(unique_ptr &&other) noexcept
        : m_ptr{other.release()}, m_deleter{std::move(other.m_deleter)} {}

    unique_ptr &operator=(unique_ptr &&other) noexcept {
        if (this != &other) {
            reset(other.release());
            m_deleter = std::move(other.m_deleter);
        }
        return *this;
    }

    explicit operator bool() const noexcept { return static_cast<bool>(m_ptr); }

    T *get() const noexcept { return m_ptr; }
    T *operator->() const noexcept { return m_ptr; }
    T &operator*() const noexcept { return *m_ptr; }

    D &get_deleter() noexcept { return m_deleter; }
    const D &get_deleter() const noexcept { return m_deleter; }

    T *release() noexcept { return std::exchange(m_ptr, nullptr); }

    void reset(T *ptr = nullptr) noexcept {
        T *old = std::exchange(m_ptr, ptr);
        if (old) {
            m_deleter(old);
        }
    }

    ~unique_ptr() noexcept {
        if (m_ptr) {
            m_deleter(m_ptr);
        }
    }

   private:
    [[no_unique_address]] D m_deleter; // use [[msvc::no_unique_address]] on Windows
    T *m_ptr;
};

void basic_example() {
    int *xp = new int(42);
    *xp = 0;
    delete xp;

    auto yp = std::make_unique<int>(42);
    *yp = 0;
}

int *some_c_func() {
    int *xp = (int *)malloc(sizeof(int));
    if (!xp) {
        puts("malloc failed, yeeting self X(\n");
        exit(1);
    }
    *xp = 42;
    return xp;
}

struct FreeDeleter {
    void operator()(void *ptr) { free(ptr); }
};

template <class T>
using c_unique_ptr_t = std::unique_ptr<T, FreeDeleter>;

c_unique_ptr_t<int> some_c_func_wrapper() {
    return c_unique_ptr_t<int>(some_c_func());
}

void c_library_example() {
    int *xp = some_c_func();
    std::cout << "x is " << *xp << '\n';
    free(xp);  // must be called

    // auto yp = std::unique_ptr<int, decltype([](void *ptr) { free(ptr); })>(some_c_func()); // OK but wordy
    // auto yp = std::unique_ptr<int, FreeDeleter>(some_c_func()); // OK, but requires caller to remember
    // auto yp = std::unique_ptr<int, decltype(&free)>(some_c_func(), free);  // dont do this! wasted 8 bytes
    // auto yp = std::unique_ptr<int, void (*)(void *)>(some_c_func(), free);  // dont do this! wasted 8 bytes
    // auto yp = c_unique_ptr_t<int>(some_c_func()); // OK, but requires caller to remember
    // c_unique_ptr_t<int> yp(some_c_func()); // OK, but requires caller to remember
    auto yp = some_c_func_wrapper();

    std::cout << "size of yp is " << (sizeof yp) << '\n';
    std::cout << "y is " << *yp << '\n';
}

void allocator_example() {
    std::allocator<int> alloc;

    auto dealloc = [](int *ptr) { std::allocator<int>().deallocate(ptr, 1); };
    auto xp = unique_ptr<int, decltype(dealloc)>(alloc.allocate(1), dealloc);
    *xp = 42;

    std::cout << alignof(decltype(xp)) << '\n';
    std::cout << "size of xp is " << (sizeof xp) << '\n';
    std::cout << "x is " << *xp << '\n';
}

int main() {
    basic_example();
    c_library_example();
    allocator_example();
    return 0;
}
