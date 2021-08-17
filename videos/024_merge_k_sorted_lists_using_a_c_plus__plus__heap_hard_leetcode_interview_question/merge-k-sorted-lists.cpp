#include <iostream>
#include <vector>
#include <algorithm>
#include <initializer_list>

struct ListNode
{
    int val;
    ListNode *next;
    ListNode() : val(0), next(nullptr) {}
    ListNode(int x) : val(x), next(nullptr) {}
    ListNode(int x, ListNode *next) : val(x), next(next) {}

    static ListNode *new_list(std::initializer_list<int> v)
    {
        return new_list(v.begin(), v.end());
    }

    template <typename RAIter>
    static ListNode *new_list(RAIter begin, RAIter end)
    {
        ListNode dummy;
        ListNode *curr = &dummy;
        while (begin != end)
        {
            const auto next = new ListNode(*begin++);
            curr->next = next;
            curr = next;
        }
        curr->next = nullptr;
        return dummy.next;
    }

    static void delete_list(ListNode *node)
    {
        while (node != nullptr)
        {
            auto next = node->next;
            delete node;
            node = next;
        }
    }

    void print()
    {
        ListNode *curr = this;
        while (curr)
        {
            std::cout << curr->val << " -> ";
            curr = curr->next;
        }
        std::cout << "X\n";
    }
};
class Solution
{
public:
    ListNode *mergeKLists(std::vector<ListNode *> &lists)
    {
        lists.erase(std::remove(lists.begin(), lists.end(), nullptr), lists.end());
        if (lists.size() == 0)
        {
            return nullptr;
        }

        const auto comp = [](ListNode *first, ListNode *second) {
            return first->val > second->val;
        };

        std::make_heap(lists.begin(), lists.end(), comp);

        ListNode dummy;
        ListNode *curr = &dummy;

        while (lists.size() > 1)
        {
            std::pop_heap(lists.begin(), lists.end(), comp);
            const auto min = lists.back();
            curr->next = min;
            curr = min;
            if (min->next != nullptr)
            {
                lists.back() = min->next;
                std::push_heap(lists.begin(), lists.end(), comp);
            }
            else
            {
                lists.pop_back();
            }
        }

        // lists.size() == 1
        curr->next = lists.back();
        return dummy.next;
    }
};

int main()
{
    ListNode *x = ListNode::new_list({1, 3, 5});
    ListNode *y = ListNode::new_list({2, 4, 6, 7, 8, 9, 10});
    ListNode *z = ListNode::new_list({0});

    std::vector<ListNode *> lists{x, y, z, nullptr, nullptr};
    ListNode *merged = Solution().mergeKLists(lists);
    merged->print();

    ListNode::delete_list(merged);
    return 0;
}