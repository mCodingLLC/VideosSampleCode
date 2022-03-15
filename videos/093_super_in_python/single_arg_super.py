import random


class A:
    def f(self):
        print("A", self)


class B(A):
    def f(self):
        print("B", self)


class C(B):
    def f(self):
        print("C", self)


def late_binding_example():
    sup = super(B)
    bs = [B(), C()]

    # possible that choice is made very far from when sup, and bs are defined
    choice = random.choice(bs)
    sup.__get__(choice).f()


def main():
    late_binding_example()


if __name__ == '__main__':
    main()
