#include <iostream>
#include <unordered_map>
#include <utility>
#include <vector>
#include <array>
#include <algorithm>
#include <iomanip>
#include <memory>
#include <iterator>
#include <bit>
#include <string_view>
#include <thread>
#include <syncstream>

// nooby things in C++

// 1. using namespace std; (confusing bc experts do this in presentations)
void using_namespace_std() {
//    using namespace std;
    // not that bad in a function...
    // error-prone inside your own cpp files
    // annoying to force on others by putting in header files

    using std::string;
    string s{"hello, world!"};
}


// 2. using std::endl instead of just \n, especially in a loop
void print_range(int start, int end) {
    for (auto i = start; i != end; ++i)
        std::cout << i << std::endl; // flushes
//        std::cout << i << '\n';

}


// 3. using for loop by index when range-for expresses intent better
void train_model(const std::vector<int> &data, auto &model) {
    for (std::size_t i = 0; i < data.size(); ++i) {
        model.update(data[i]);
    }

    for (const auto &x: data)
        model.update(x);

    std::for_each(data.cbegin(), data.cend(), [&model](const auto &x) {
        model.update(x);
    }); //not an improvement
}

//4.  using a loop when a std algorithm already exists for it
void know_your_algorithms() {
    const std::vector<int> data = {-1, -3, -5, 8, 15, -1};

    // find the index of the first positive element
    std::size_t first_pos_idx;
    for (std::size_t i = 0; i < data.size(); ++i) {
        if (data[i] > 0) {
            first_pos_idx = i;
            break;
        }
    }
    // use first_pos_idx

    const auto is_positive = [](const auto &x) {
        return x > 0;
    };
    auto first_pos_it = std::find_if(
            data.cbegin(),
            data.cend(),
            is_positive);
    // or ranges even better
    // use first_pos_it
}


// 5. using C style array when std::array would work
void f(int *arr, int n) {
    // bad
}

template<std::size_t size>
void better_f(std::array<int, size> &arr) {
    // now it is impossible to pass the wrong size
    // but perhaps consider using iterators or C++ span instead
}


void using_c_array() {
    const int n = 256;
//    int arr[n] = {0}; // zero initialize
//    // use arr
//    f(arr, n);


    std::array<int, n> arr{}; // zero initialize
    // can still use
    // f(arr.data, arr.size);
    better_f(arr);
}


// 6. any use of reinterpret_cast
template<typename T>
void print_bytes(const T &input, std::ostream &os = std::cout) {
    auto *bytes = reinterpret_cast<const std::byte *>(&input);
    os << "[";
    os << std::hex << std::noshowbase;
    for (std::size_t i = 0; i < sizeof(T); ++i) {
        if (i != 0)
            os << " ";
        os << std::setfill('0') << std::setw(2);
        os << static_cast<int>(bytes[i]);
    }
    os << "]\n";
}

template<typename T>
void print_bytes_cpp20(const T &input, std::ostream &os = std::cout) {
    using bytearray = std::array<std::byte, sizeof(T)>;
    const auto &bytes = std::bit_cast<bytearray, T>(input);
    os << "[";
    os << std::hex << std::noshowbase;
    for (std::size_t i = 0; i < sizeof(T); ++i) {
        if (i != 0)
            os << " ";
        os << std::setfill('0') << std::setw(2);
        os << static_cast<int>(bytes[i]);
    }
    os << "]\n";
}


void any_use_of_reinterpret_cast() {
    long long x = 0;
    auto xp = reinterpret_cast<char *>(x); // technically ok, but can point anywhere in memory
    auto x2 = reinterpret_cast<long long>(xp); // ok but not guaranteed to be 0

    int *p = nullptr;
    auto p_int = reinterpret_cast<std::uintptr_t>(p);
    auto q = reinterpret_cast<int *>(p_int);


    float y = .123f;
    long i = *(long *) &y; // Sorry famous Quake III inv_sqrt code, this is UB unless compiled with -fno-strict-aliasing
    // ...
    y = *(float *) &i;


}


// 7. any casting away const with const_cast
const std::string &
more_frequent(const std::unordered_map<std::string, int> &word_counts,
              const std::string &word1,
              const std::string &word2) {
//    return word_counts[word1] > word_counts[word2] ? word1 : word2;
    auto &counts = const_cast<std::unordered_map<std::string, int> &>(word_counts);
    return counts[word1] > counts[word2] ? word1 : word2;

//    return word_counts.at(word1) > word_counts.at(word2) ? word1 : word2;
}

// 8. not knowing std::unordered_map operator[] inserts element if it doesn't exist
std::unordered_map<std::string, int>
count_words(const std::vector<std::string> words) {
    std::unordered_map<std::string, int> counts;
    for (const auto &word: words)
        counts[word]++; // counts[word] default constructs value to 0 if it doesn't exist
    return counts;
}

// 9. ignoring const correctness
void print_vec_one_per_line(std::vector<int> &arr) { // arr should be const
    for (const auto &x: arr) {
        std::cout << x << '\n';
    }
}

// 10. string literal lifetime
const char *string_literal_lifetimes() {
//    char *hello = "hello!"; // not since C++11, literal has type const char[7]
//    std::cout << hello << '\n';
//    hello[0] = 'H'; // UB, hopefully crash

//    const char *hello = "hello!"; // now required after C++11
//    std::cout << hello << '\n';
//    hello[0] = 'H'; // would require const_cast, UB

    char hello[] = "hello!"; // totally fine, makes a copy
    std::cout << hello << '\n';
    hello[0] = 'H'; // totally fine, modified the copy
    std::cout << hello << '\n';


    return "string literals"; // fine, string literals guaranteed to live for the entire life of the program
}


// 11. not knowing about structured bindings
void loop_map_items() {
    std::unordered_map<std::string, std::string> colors = {
            {"RED",   "#FF0000"},
            {"GREEN", "#00FF00"},
            {"BLUE",  "#0000FF"}
    };

    for (const auto &pair: colors) {
        std::cout << "name: " << pair.first << ", hex: " << pair.second << '\n';
    }

    for (const auto&[name, hex]: colors) {
        std::cout << "name: " << name << ", hex: " << hex << '\n';
    }

}


struct S {
    int a;
    std::string s;
};

S get_S() {
    S my_S = {0, "subscribe"};
    // whatever
    return my_S;
}

void use_S() {
//    const auto [a, s] = get_S();

    const auto e = get_S();
    const auto &a = e.a;
    const auto &s = e.s;

    const auto&[b, t] = e;

//    const auto &e2 = e;
//    const auto &b = e2.a;
//    const auto &t = e2.s;
}


// 12. using out-parameters to return multiple values, (instead return a struct)
void get_values_out_params(const int n, int &out1, int &out2) {
    // do stuff
    out1 = n;
    out2 = n + 1;
}


struct Values {
    int x, y;
};

Values // add constexpr for next point
get_values_return_struct(const int n) {
    return {n, n + 1};
}

auto
get_values_return_anon_struct(const int n) {
    struct V {
        int x, y;
    };

    return V{n, n + 1};
}


void use_values() {
//    auto values = get_values_return_struct(5); // NO COPY is made due to RVO!
//    std::cout << values.x << '\n';
//    std::cout << values.y << '\n';

    auto[x, y] = get_values_return_struct(5);
    std::cout << x << '\n';
    std::cout << y << '\n';

}

// 13. doing work at runtime that could be done at compile time (constexpr)
constexpr int sum_of_1_to_n(const int n) {
    return n * (n + 1) / 2;
}

void uses_sum() {
    const int limit = 1000;
    auto triangle_n = sum_of_1_to_n(limit);
    // use triangle_n...
}

// 14. not marking a destructor virtual (unless class is final)
class BaseWithNonvirtualDestructor {
public:
    void foo() {
        std::cout << "do foo\n";
    }

    virtual ~BaseWithNonvirtualDestructor() {
        std::cout << "called base destructor\n";
    }
};

class Derived : public BaseWithNonvirtualDestructor {
public:
    ~Derived() override {
        std::cout << "called derived destructor\n";
    }
};

void consume_base(std::unique_ptr<BaseWithNonvirtualDestructor> p) {
    p->foo();
    // deletes p when done
}

void base_with_nonvirtual_destructor() {
    auto derived = std::make_unique<Derived>();
//    Derived d;
    consume_base(std::move(derived)); // takes ownership and deletes when done
}


// 15. not knowing class members are guaranteed initialized in order they are declared, not in order of initializer list
template<typename T>
class View {
public:
    View(T *start, std::size_t size) : m_start{start}, m_end{m_start + size} {
        std::cout << "view constructor: " << m_start << "," << m_end << '\n';
    }

private:
    T *m_start; //initialization order is order listed here
    T *m_end;
};

void class_member_initialization_order() {
    View<std::byte> v(nullptr, 1);
}


// 16. not knowing the difference between default and value initialization
void default_vs_value_initialization() {

    // default initialized, contains garbage
    int x;
    int *x2 = new int;


    // value initialized, contains 0
    int y{};
    int *y2 = new int{};
    int *y3 = new int();

    //    int y0(); // WARNING: function declaration, not creating int!



    struct S {
        int n, m;
        std::string s;

        S() {
            std::cout << "constructor\n";
        }
    };

    // don't explain the rules, just say it depends on constructor, etc.
    S my_s; // default initialized, contains {garbage, garbage, empty string}
    std::cout << my_s.n << " " << my_s.m << " \"" << my_s.s << "\"\n";

    S my_s2{}; // value initialized, contains {0, 0, empty string} if you don't define constructor
    std::cout << my_s2.n << " " << my_s2.m << " \"" << my_s2.s << "\"\n";


//    S my_sf(); // function declaration!
}


// 17. using magic numbers in formulas
float energy(float m) {
    constexpr float SPEED_OF_LIGHT = 299792458.0;
//    return m * 299792458.0 * 299792458.0;

}


// 18. attempting to add or remove elements from a container while looping over it (probably UB)
void modify_while_iterating() {
    std::vector<int> v{1, 2, 3, 4};

//    for (auto x : v) {
//        v.push_back(x);
//    }


//    for (auto it = v.begin(), end = v.end() ; it != end; ++it) {
//        v.push_back(*it);
//    }

//    std::copy(v.begin(), v.end(), std::back_inserter(v));


//    const std::size_t size = v.size();
//    for (std::size_t i = 0; i < size; ++i)
//        v.push_back(v[i]);


    for (auto x: v) {
        std::cout << x;
    }
    std::cout << '\n';
}


// 19. returning std::move of a local variable
std::vector<int> make_vector(const int n) {
    std::vector<int> v{1, 2, 3, 4, 5};
    // populate vec more

    std::vector<int> w{1, 2};

    if (n == 0)
        return std::move(v);
    else
        return std::move(w);

//    return std::move(v); // NEVER
//    return v;
}

// 20. not understanding std::move doesnt move anything
template<typename T>
constexpr std::remove_reference_t<T> &&
move(T &&value) noexcept {
    return static_cast<std::remove_reference_t<T> &&>(value);
}
// cast_to_rvalue (or cast_to_xvalue)



// 21. not knowing evaluation order is not guaranteed LTR
void g(int a, int b, int c) {
    std::cout << a << ' ' << b << ' ' << c << '\n';
}

void function_evaluation_order_not_guaranteed() {
    std::string s = "but i have heard it works even if you don't believe in it";

    //guaranteed a evaluated before b in a.b as of c++17
    s.replace(0, 4, "")
            .replace(s.find("even"), 4, "only")
            .replace(s.find("don't"), 6, "");

    std::string expected = "i have heard it works only if you believe in it";
    std::cout << s << '\n';
    std::cout << expected << '\n';
    std::cout << (s == expected) << '\n';

    //however, even in c++20, order of args in a(b1, b2, b3) not guaranteed
    int i = 0;
    const auto inc_i = [&i]() -> int {
        return ++i;
    };

    g(inc_i(), inc_i(), inc_i()); // all permutations of 1 2 3 are allowed to be printed
}


// 22. using heap allocations when stack would have been fine
struct Record {
    int id;
    std::string name;
};

void unnecessary_heap_allocations() {
    Record *customer = new Record{0, "James"};
    Record *other = new Record{1, "Someone"};

    // do work

    delete customer;
    delete other;
}


// 23. not knowing about unique_ptr and shared_ptr
struct Metadata {
    std::byte magic;
    std::size_t size;
    std::array<char, 20> name;
    std::array<char, 200> description;
    // other fields
};

Metadata *read_metadata(const std::ifstream &file) {
    auto *data = new Metadata{};

    // read fields from file

    return data;
}


// 24. constructing a unique_ptr directly instead of using make_unique
void f(std::unique_ptr<int> a, std::unique_ptr<float> b) {

}

void constructing_a_unique_ptr_directly() {
    // REAL issue prior to C++17
    f(std::unique_ptr<int>(new int{}),
      std::unique_ptr<float>(new float{})); // could leak prior to C++17
    f(std::make_unique<int>(),
      std::make_unique<float>()); // cannot leak

    struct SomeLongName {
        int n, m;
        std::string s;

        // not needed in C++20 to make make_unique work
        SomeLongName(int n, int m, std::string s) : n{n}, m{m}, s{std::move(s)} {
        }
    };

    auto int_val = std::make_unique<int>();
    auto shared_int_val = std::make_shared<int>();
    auto val = std::make_unique<SomeLongName>(0, 0, "hello"); // forwards args to constructor
    auto val2 = std::unique_ptr<SomeLongName>(new SomeLongName(0, 0, "hello")); // longer rand uses new
}


//  25. any use of new or delete (outside of learning or defining container type), (malloc or free also)
class Widget {
public:
    Widget() : meta{new Metadata{}} {
        // whatever
    }

    virtual ~Widget() {
        delete meta;
    }

private:
    Metadata *meta;
};

class BetterWidget {
public:
    BetterWidget() : meta{std::make_unique<Metadata>()} {
        // whatever
    }

private:
    std::unique_ptr<Metadata> meta;
};


// 26. more generally, any attempt at manual resource management (e.g. using fopen instead of RAII type)
void read_from_a_file(char *name) {
    FILE *fp = fopen(name, "r");
    // ... work with file, EXCEPTION?
    fclose(fp);

//    std::ifstream input{name};
    // work with the file
    // no need to close, RAII
}


// 27. thinking all pointers "should" be smart pointers.
std::shared_ptr<int> max(std::shared_ptr<int> a, std::shared_ptr<int> b) {
    return *a > *b ? std::move(a) : std::move(b);
}

const int *max(const int *a, const int *b) { // convention is raw pointers are non owning, no need to delete
    return *a > *b ? a : b;
}

// 28. returning a shared_ptr when you aren't SURE it's going to be shared (unique can convert to shared when needed)
// shared pointers are EXPENSIVE
struct Pizza {
    Pizza(float diameter, std::vector<std::string> toppings) :
            m_diameter{diameter}, m_toppings{std::move(toppings)} {}

    float m_diameter; // inches
    std::vector<std::string> m_toppings;
};

std::shared_ptr<Pizza> make_shared_pepperoni_pizza(float diameter) {
    std::vector<std::string> toppings = {"red sauce", "cheese", "pepperoni"};
    return std::make_shared<Pizza>(diameter, std::move(toppings)); // why shared?
}

std::unique_ptr<Pizza> make_unique_pepperoni_pizza(float diameter) {
    std::vector<std::string> toppings = {"red sauce", "cheese", "pepperoni"};
    return std::make_unique<Pizza>(diameter, std::move(toppings));
}

void convert_unique_to_shared_is_easy_and_cheap() {
    auto pizza = make_unique_pepperoni_pizza(16.0f);

    std::shared_ptr<Pizza> shared_pizza = std::move(pizza);
    std::shared_ptr<Pizza> shared_pizza2 = make_unique_pepperoni_pizza(16.0f); // easy
}


// 29. not knowing that shared_ptr is NOT thread-safe
struct Noisy {
    int x;

    Noisy() : x{0} {

    }

    ~Noisy() {
        std::osyncstream{std::cout} << "Deleted from thread " << std::this_thread::get_id() << '\n';
    }
};


void worker(std::shared_ptr<Noisy> noisy) {
//    static std::mutex compute_mutex;

    for (int i = 0; i < 5; ++i) {
//        std::lock_guard lock(compute_mutex);
        for (int j = 0; j < 10000; ++j) {
            noisy->x++;
        }
        std::osyncstream{std::cout} << "Thread " << std::this_thread::get_id() << " executing: " << noisy->x << "\n";
    }
}


void shared_ptr_is_NOT_threadsafe() {
    std::osyncstream{std::cout} << "Main thread " << std::this_thread::get_id() << " executing\n";

    auto noisy = std::make_shared<Noisy>();
    std::jthread t2(worker, noisy);
    std::jthread t1(worker, noisy);
    noisy.reset();// main thread done with object
}


// 30. confusing const pointer/ref with pointer/ref to const
void const_pointer_vs_pointer_to_const() {
    int x = 0;
    int y = 0;

    int *ptr = &x;
    *ptr = 1; // x == 1
    ptr = &y; // point to y
    *ptr = 2; // y == 2

    const int *ptr_to_const = &x;
    int const *ptr_to_const2 = &x;
    // *ptr_to_const = 1; // NOT ALLOWED
    ptr_to_const = &y; // point to y
    // *ptr_to_const = 2 // STILL NOT ALLOWED

    int *const const_ptr = &x;
    *const_ptr = 1; // x == 1
//    const_ptr = &y; // NOT ALLOWED

    const int *const const_ptr_to_const = &x;
    int const *const const_ptr_to_const2 = &x;
    // *const_ptr_to_const = 1; // NOT ALLOWED
    // const_ptr_to_const = &y; // NOT ALLOWED

    const int &const_reference = x;
    int const &const_reference2 = x;
    // const_reference = 1; // NOT ALLOWED


//    int & const not_allowed = x; // all references are const, not allowed
}

// 31. BONUS not using or ignoring compiler warnings

int main() {
//    std::cout << "Hello, World!" << std::endl;
//    print_bytes("Hello, World!");
//
//    print_bytes(.1L);
//    print_bytes(.2L);
//
//    print_bytes_cpp20("Hello, World!");
//    print_bytes_cpp20(.1L);
//    print_bytes_cpp20(.2L);

//    string_literal_lifetimes();
//    base_with_nonvirtual_destructor();
//    class_member_initialization_order();
//    default_vs_value_initialization();
//    function_evaluation_order_not_guaranteed();
//    modify_while_iterating();
//    shared_ptr_is_NOT_threadsafe();

    return 0;
}