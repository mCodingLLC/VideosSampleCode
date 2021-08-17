#include <iostream>

int i = 0;

void func()
{
    std::cout << i << '\n';
    int i = 1;
    std::cout << i << '\n';
}

int main()
{
    func();
    return 0;
}