#include <array>
#include <vector>
#include <queue>
#include <utility>

// only needed for running tests
#include <iostream>
#include <chrono>

// Leetcode probably should have used these instead...
//
// struct Building {
//     int left;
//     int right;
//     int height;
// };
//
// struct Point {
//     int x;
//     int y;
// };

class Solution
{
public:
    using Building = std::array<int, 3>;
    using Point = std::array<int, 2>;

    // using Building = std::vector<int>;
    // using Point = std::vector<int>;

private:
    struct BuildingRightAndHeight
    {
        int right;
        int height;

        explicit constexpr BuildingRightAndHeight(const Building &building) noexcept
            : right{building[1]}, height{building[2]} {}
    };

    class CompareHeight
    {
    public:
        bool operator()(const BuildingRightAndHeight first, const BuildingRightAndHeight second) noexcept
        {
            return first.height < second.height;
        };
    };
    using PriorityQueue = std::priority_queue<BuildingRightAndHeight,
                                              std::vector<BuildingRightAndHeight>,
                                              CompareHeight>;

    static inline int
    getLeft(const Building &building) noexcept { return building[0]; }

    // static inline int
    // getRight(const Building &building) noexcept { return building[1]; }

    // static inline int
    // getHeight(const Building &building) noexcept { return building[2]; }

    static inline int
    getX(const Point &skyline_element) noexcept { return skyline_element[0]; }

    static inline int
    getY(const Point &skyline_element) noexcept { return skyline_element[1]; }

    // precondition: active is nonempty (=> skyline nonempty)
    // precondition: right of tallest is > right of back of skyline
    // postcondition: active is empty or right of tallest is > right of back of skyline
    static void
    popTallestUntilRightExceedsCurrentTallestRightAndUpdateSkyline(PriorityQueue &active,
                                                                   std::vector<Point> &skyline)
    {
        // here we use that active's top will choose the building with rightmost endpoint
        // if multiple buildings are the tallest
        const int tallest_right = active.top().right;

        // ensures if active is nonempty that right of new tallest is > back of new skyline
        while (!active.empty() && active.top().right <= tallest_right)
            active.pop();

        updateSkyline(tallest_right, maxActiveHeight(active), skyline);
    }

    static int
    maxActiveHeight(PriorityQueue &active) noexcept
    {
        return active.empty() ? 0 : active.top().height;
    }

    static void
    updateSkyline(const int x, const int y, std::vector<Point> &skyline)
    {
        if (skyline.empty() || y != getY(skyline.back()))
            skyline.push_back({x, y});
    }

public:
    // Returns the skyline formed by the given buildings.
    // Buildings are represented [left, right, height]
    // skyline is represented by [x, y] at jump points
    // precondition: buildings.size() >= 1
    // precondition: buildings sorted by left coordinate
    static std::vector<Point>
    getSkyline(const std::vector<Building> &buildings)
    {
        // "active" buildings are those that have intersected the current x value
        // and either still intersect the current x value or have not been the tallest remaining yet
        // Reserve enough space for all buildings to be active, but in practice
        // the number of active buildings will not scale with the number of buildings
        std::vector<BuildingRightAndHeight> active_data;
        active_data.reserve(buildings.size());
        PriorityQueue active(CompareHeight{}, std::move(active_data));

        // Skyline to return. Each building may contribute at most 2 skyline points
        // so at most one resizing will be used.
        std::vector<Point> skyline;
        skyline.reserve(2 * buildings.size());

        for (auto it = buildings.begin(); it != buildings.end(); /* updated in loop */)
        {
            const int current_x = getLeft(*it);
            while (!active.empty() && active.top().right < current_x)
                popTallestUntilRightExceedsCurrentTallestRightAndUpdateSkyline(active, skyline);

            while (it != buildings.end() && getLeft(*it) == current_x)
                active.push(BuildingRightAndHeight{*it++});
            updateSkyline(current_x, maxActiveHeight(active), skyline);
        }

        while (!active.empty())
            popTallestUntilRightExceedsCurrentTallestRightAndUpdateSkyline(active, skyline);

        return skyline;
    }
};

template <typename VecVec>
void printVecVec(const VecVec &vecvec)
{
    for (const auto &vec : vecvec)
    {
        std::cout << '{';
        for (const auto &elem : vec)
            std::cout << elem << ',';
        std::cout << "}, ";
    }
    std::cout << '\n';
}

using Building = Solution::Building;
using Point = Solution::Point;

void assertEqualSkylines(
    const std::vector<Building> &input,
    const std::vector<Point> &actual,
    const std::vector<Point> &expected)
{
    if (actual != expected)
    {
        std::cout << "FAILED\n";
        if (input.size() < 20 && actual.size() < 20 && expected.size() < 20)
        {
            std::cout << "input:    ";
            printVecVec(input);
            std::cout << "actual:   ";
            printVecVec(actual);
            std::cout << "expected: ";
            printVecVec(expected);
        }
    }
}

int main()
{
    std::cout << "Running tests...\n";
    auto test_start = std::chrono::steady_clock::now();
    std::chrono::steady_clock::time_point start, end;
    auto duration = end - start;

    std::vector<Building> input = {{5, 10, 7}};
    start = std::chrono::steady_clock::now();
    std::vector<Point> actual = Solution::getSkyline(input);
    end = std::chrono::steady_clock::now();
    duration += (end - start);
    std::vector<Point> expected = {{5, 7}, {10, 0}};
    assertEqualSkylines(input, actual, expected);

    input = {{2, 9, 10}, {3, 7, 15}, {5, 12, 12}, {15, 20, 10}, {19, 24, 8}};
    start = std::chrono::steady_clock::now();
    actual = Solution::getSkyline(input);
    end = std::chrono::steady_clock::now();
    duration += (end - start);
    expected = {{2, 10}, {3, 15}, {7, 12}, {12, 0}, {15, 10}, {20, 8}, {24, 0}};
    assertEqualSkylines(input, actual, expected);

    input = {{0, 2, 3}, {2, 5, 3}};
    start = std::chrono::steady_clock::now();
    actual = Solution::getSkyline(input);
    end = std::chrono::steady_clock::now();
    duration += (end - start);
    expected = {{0, 3}, {5, 0}};
    assertEqualSkylines(input, actual, expected);

    input = {{0, 2, 3}, {2, 5, 4}};
    start = std::chrono::steady_clock::now();
    actual = Solution::getSkyline(input);
    end = std::chrono::steady_clock::now();
    duration += (end - start);
    expected = {{0, 3}, {2, 4}, {5, 0}};
    assertEqualSkylines(input, actual, expected);

    input = {{0, 2, 3}, {2, 5, 2}};
    start = std::chrono::steady_clock::now();
    actual = Solution::getSkyline(input);
    end = std::chrono::steady_clock::now();
    duration += (end - start);
    expected = {{0, 3}, {2, 2}, {5, 0}};
    assertEqualSkylines(input, actual, expected);

    input = {{0, 2147483647, 2147483647}};
    start = std::chrono::steady_clock::now();
    actual = Solution::getSkyline(input);
    end = std::chrono::steady_clock::now();
    duration += (end - start);
    expected = {{0, 2147483647}, {2147483647, 0}};
    assertEqualSkylines(input, actual, expected);

    input = {{1, 2, 1}, {1, 2, 2}, {1, 2, 3}};
    start = std::chrono::steady_clock::now();
    actual = Solution::getSkyline(input);
    end = std::chrono::steady_clock::now();
    duration += (end - start);
    expected = {{1, 3}, {2, 0}};
    assertEqualSkylines(input, actual, expected);

    input = {{1, 5, 1}, {2, 3, 1}};
    start = std::chrono::steady_clock::now();
    actual = Solution::getSkyline(input);
    end = std::chrono::steady_clock::now();
    duration += (end - start);
    expected = {{1, 1}, {5, 0}};
    assertEqualSkylines(input, actual, expected);

    input = {{1, 5, 1}, {2, 5, 1}};
    start = std::chrono::steady_clock::now();
    actual = Solution::getSkyline(input);
    end = std::chrono::steady_clock::now();
    duration += (end - start);
    expected = {{1, 1}, {5, 0}};
    assertEqualSkylines(input, actual, expected);

    input = {{1, 5, 1}, {2, 6, 1}};
    start = std::chrono::steady_clock::now();
    actual = Solution::getSkyline(input);
    end = std::chrono::steady_clock::now();
    duration += (end - start);
    expected = {{1, 1}, {6, 0}};
    assertEqualSkylines(input, actual, expected);

    input = {{1, 5, 2}, {2, 3, 1}};
    start = std::chrono::steady_clock::now();
    actual = Solution::getSkyline(input);
    end = std::chrono::steady_clock::now();
    duration += (end - start);
    expected = {{1, 2}, {5, 0}};
    assertEqualSkylines(input, actual, expected);

    input = {{1, 5, 1}, {2, 3, 2}};
    start = std::chrono::steady_clock::now();
    actual = Solution::getSkyline(input);
    end = std::chrono::steady_clock::now();
    duration += (end - start);
    expected = {{1, 1}, {2, 2}, {3, 1}, {5, 0}};
    assertEqualSkylines(input, actual, expected);

    input = {{1, 5, 1}, {2, 5, 3}, {3, 5, 2}};
    start = std::chrono::steady_clock::now();
    actual = Solution::getSkyline(input);
    end = std::chrono::steady_clock::now();
    duration += (end - start);
    expected = {{1, 1}, {2, 3}, {5, 0}};
    assertEqualSkylines(input, actual, expected);

    input = {{1, 2, 1}, {2, 3, 1}, {4, 5, 1}};
    start = std::chrono::steady_clock::now();
    actual = Solution::getSkyline(input);
    end = std::chrono::steady_clock::now();
    duration += (end - start);
    expected = {{1, 1}, {3, 0}, {4, 1}, {5, 0}};
    assertEqualSkylines(input, actual, expected);

    input = {};
    expected = {};
    for (int i = 0; i < 100000; ++i)
    {
        input.push_back({2 * i, 2 * i + 1, 1});
        expected.push_back({2 * i, 1});
        expected.push_back({2 * i + 1, 0});
    }
    start = std::chrono::steady_clock::now();
    actual = Solution::getSkyline(input);
    end = std::chrono::steady_clock::now();
    duration += (end - start);
    assertEqualSkylines(input, actual, expected);

    auto test_end = std::chrono::steady_clock::now();
    auto diff = std::chrono::duration_cast<std::chrono::milliseconds>(test_end - test_start);
    std::cout << "Total test time: " << diff.count() << " ms\n";
    diff = std::chrono::duration_cast<std::chrono::milliseconds>(duration);
    std::cout << "Time in getSkyline: " << diff.count() << " ms\n";
}