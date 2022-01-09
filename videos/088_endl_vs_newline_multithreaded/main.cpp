#include <iostream>
#include <thread>
#include <fstream>
#include <syncstream> // C++20
//#include <mutex> // for C++11 through C++17

//std::mutex write_mutex; // for C++11 through C++17


void worker(int start, int stop, std::ostream &os) {
    for (int i = start; i < stop; ++i) {
//        C++11 - C++17 solutions
//        const std::lock_guard<std::mutex> lock{write_mutex}; // C++11
//        const std::scoped_lock lock{write_mutex}; // C++17
//        os << "thread: " << std::this_thread::get_id() << "; work: " << i;
//        os << '\n';

//        C++20 solution
        std::osyncstream out{os};
        out << "thread: " << std::this_thread::get_id() << "; work: " << i;
        out << '\n';
    }
}

void example(std::ostream &os) {
//    jthread is C++20
    std::jthread t1(worker, 10000, 20000, std::ref(os));
    std::jthread t2(worker, 20000, 30000, std::ref(os));

//    C++11 through C++17
//    std::thread t1(worker, 10000, 20000, std::ref(os));
//    std::thread t2(worker, 20000, 30000, std::ref(os));
//    t2.join();
//    t1.join();
}


int main() {
    std::ofstream file{"out.txt"};
    example(file);
    return 0;
}
