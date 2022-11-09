#include <iostream>
#include <utility>

struct S {
    int x;

    explicit S(int x) : x{x} { std::cout << "construct S(" << x << ")\n"; }

    S(const S& other) : x{other.x} { std::cout << "copy S(" << x << ")\n"; }
    // S(const S& other) = delete;

    // S(S&& other) : x{other.x} { std::cout << "move S(" << x << ")\n"; }
    // S(S&& other) = delete;
};

S make_value(int x) {
    // RVO (return value optimization, guaranteed c++17)
    return S(S(S(S(x))));
}

S make_double_value(int x) {
    // NRVO (named return value optimization, not guaranteed)
    S s(x);
    s.x = 2 * x;
    return s;
}

S no_elision(int x) {
    S s1(x);
    S s2(x);
    if (x > 0) {
        return s1;
    } else {
        return s2;
    }
}

S maybe_elision(int x) {
    // compiler can elide, clang and msvc do, gcc does not
    if (x > 0) {
        S s1(x);
        return s1;
    } else {
        S s2(x);
        return s2;
    }
}

int main() {
    S s = maybe_elision(21);
    std::cout << "answer: " << s.x << '\n';
    return 0;
}