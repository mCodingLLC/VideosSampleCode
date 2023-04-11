#include <iostream>
#include <memory>
#include <utility>
#include <vector>

template <class T>
class unique_ptr {
   public:
    unique_ptr() noexcept : unique_ptr{nullptr} {}
    explicit unique_ptr(T *ptr) noexcept : m_ptr{ptr} {}

    unique_ptr(const unique_ptr &) = delete;
    unique_ptr &operator=(const unique_ptr &) = delete;

    unique_ptr(unique_ptr &&other) noexcept : m_ptr{other.release()} {}

    unique_ptr &operator=(unique_ptr &&other) noexcept {
        if (this != &other) {
            reset(other.release());
        }
        return *this;
    }

    explicit operator bool() const noexcept { return static_cast<bool>(m_ptr); }

    T *get() const noexcept { return m_ptr; }
    T *operator->() const noexcept { return m_ptr; }
    T &operator*() const noexcept { return *m_ptr; }

    T *release() noexcept { return std::exchange(m_ptr, nullptr); }

    void reset(T *ptr = nullptr) noexcept {
        T *old = std::exchange(m_ptr, ptr);
        if (old) {
            delete old;
        }
    }

    ~unique_ptr() noexcept {
        if (m_ptr) {
            delete m_ptr;
        }
    }

   private:
    T *m_ptr;
};

template <class T, class... Args>
unique_ptr<T> make_unique(Args &&...args) {
    return unique_ptr<T>(new T(std::forward<Args>(args)...));
}

struct Widget {
    int val;

    explicit Widget(int val) : val{val} {
        std::cout << "ctor: " << val << '\n';
    }

    virtual ~Widget() noexcept { std::cout << "dtor: " << val << '\n'; }
};

void use_widget(const Widget *w) {
    std::cout << "yep, that's a widget: " << w->val << '\n';
}

void use_widget(const Widget &w) {
    std::cout << "yep, that's a widget: " << w.val << '\n';
}

void vector_raw_example() {
    std::vector<Widget *> widgets;
    const std::size_t count = 5;
    widgets.reserve(count);
    for (std::size_t i = 0; i < count; ++i) {
        widgets.push_back(new Widget(i));
    }

    for (const auto &widget : widgets) {
        use_widget(widget);
    }

    delete widgets.back();
    widgets.pop_back();

    Widget *last = widgets.back();
    widgets.pop_back();

    std::cout << "last element was " << last->val << '\n';

    delete last;

    for (std::size_t i = 0; i < widgets.size(); ++i) {
        delete widgets[i];
    }
}

void vector_example() {
    std::vector<unique_ptr<Widget>> widgets;
    const std::size_t count = 5;
    widgets.reserve(count);
    for (std::size_t i = 0; i < count; ++i) {
        widgets.push_back(unique_ptr<Widget>(new Widget(i)));
        // widgets.push_back(make_unique<Widget>(i));
    }

    for (const auto &widget : widgets) {
        use_widget(widget.get());
        use_widget(*widget);
    }

    widgets.pop_back();  // automatically deleted

    unique_ptr<Widget> last = std::move(widgets.back());
    widgets.pop_back();

    std::cout << "last element was " << last->val << '\n';
}

int main() {
    int *xp = new int(42);
    *xp = 0;
    delete xp;

    auto yp = std::make_unique<int>(42);
    *yp = 0;

    vector_example();
    return 0;
}
