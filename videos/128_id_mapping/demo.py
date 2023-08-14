# my_dict = {}
#
# not_hashable = [1, 2, 3]
# my_dict[not_hashable] = ...  # ERROR
#
# val = my_dict[not_hashable]


def set_in(set_mem, x):
    idx = hash(x) % len(set_mem)
    link = set_mem[idx]
    while link is not None:
        if link.value == x:
            return True
        link = link.next
    return False


class UnsafeList(list):
    def __hash__(self):
        return hash(tuple(self))


x = UnsafeList([1, 2, 3])
my_dict = {x: "subscribe"}
x[0] = 0


# print(my_dict[x])  # KeyError!


class Hashable:
    pass
    # __hash__ defined automatically
    # __eq__ defined automatically


class NotHashable:
    def __eq__(self, other):
        return self is other

    # __hash__ set to None automatically


class SadSet:
    def __init__(self):
        self.data = []

    def add(self, value):
        if value not in self.data:
            self.data.append(value)

    def remove(self, value):
        if value in self.data:
            self.data.remove(value)

    def __contains__(self, value):
        return value in self.data

    def __len__(self):
        return len(self.data)

    def __iter__(self):
        return iter(self.data)


class A:
    pass


x = A()
print(id(x))  # 2086544423440

del x
y = A()
print(id(y))  # 2086544423440 (SAME!)

from id_mapping import IdMapping, IdSet

d = IdMapping()

my_list = [1, 2, 3]
d[my_list] = "subscribe"
my_list[0] = 0

s = d[my_list]
assert s == "subscribe"  # SUCCESS!

collection = IdSet()

n = 257
collection.add(n)
collection.add(n)

print(collection)  # {257}
