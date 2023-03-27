#include <iostream>



int main()
{
    int value = -42;
    int abs_value = (value >= 0) ? value : -value;

    std::cout << "Value: " << value << '\n';
    std::cout << "Abs: " << abs_value << '\n';
    return 0;
}








