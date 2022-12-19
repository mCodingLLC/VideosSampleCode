from __future__ import annotations


class Node:
    def __init__(self, *children: Node, data=None):
        self.children = list(children)
        self.data = data

    def __repr__(self):
        return f'({self.data})'


# initial recursive implementation
def print_parent_then_children(node: Node):
    print(node)
    for child in node.children:
        print_parent_then_children(child)


# first try using stack
def print_parent_then_children(node: Node):
    stack = [node]

    while stack:
        node = stack.pop()
        print(node)
        for child in node.children:
            stack.append(child)


# fixed issue with order of pushing onto stack
def print_parent_then_children(node: Node):
    stack = [node]

    while stack:
        node = stack.pop()
        print(node)
        for child in reversed(node.children):
            stack.append(child)


# recursive implementation with max depth
def print_parent_then_children(node: Node, max_depth=-1):
    print(node)
    if max_depth == 0:
        return
    for child in node.children:
        print_parent_then_children(child, max_depth - 1)


# stack version with max depth
def print_parent_then_children(node: Node, max_depth=-1):
    stack = [(node, max_depth)]
    while stack:
        node, max_depth = stack.pop()
        print(node)
        if max_depth == 0:
            continue
        for child in reversed(node.children):
            stack.append((child, max_depth - 1))


# factor out the iteration
def walk_parent_then_children(node: Node, max_depth=-1):
    stack = [(node, max_depth)]
    while stack:
        node, max_depth = stack.pop()
        yield node
        if max_depth == 0:
            continue
        for child in reversed(node.children):
            stack.append((child, max_depth - 1))


# decoupled implementation
def print_parent_then_children(node: Node, max_depth=-1):
    for node in walk_parent_then_children(node, max_depth):
        print(node)


# root -> child 0 -> child 1 -> ...
def long_tree_example():
    root = Node(data="root")
    node = root
    for n in range(1000):
        new = Node(data=f"child {n}")
        node.children.append(new)
        node = new

    print_parent_then_children(root)


#            root
#    child 0      child 1
# 0-0  0-1  0-2
def small_example():
    root = Node(
        Node(
            Node(data="child 0-0"),
            Node(data="child 0-1"),
            Node(data="child 0-2"),
            data="child 0",
        ),
        Node(data="child 1"),
        data="root",
    )

    print_parent_then_children(root)
    print(list(walk_parent_then_children(root, max_depth=1)))


def main():
    small_example()
    long_tree_example()


if __name__ == '__main__':
    main()
