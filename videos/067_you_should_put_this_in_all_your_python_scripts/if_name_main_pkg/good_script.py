# print("good scripts don't do i/o when you import them :)")


def useful_function(x):
    return x * x


class UsefulClass:
    def __init__(self, x):
        self.x = x


def main(args=None):
    for i in range(7):
        print(useful_function(i))


if __name__ == '__main__':
    main()
