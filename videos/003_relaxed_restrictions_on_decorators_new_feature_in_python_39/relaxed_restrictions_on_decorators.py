import time


def timed(f):
    def timed_f(*args, **kwargs):
        start = time.perf_counter()
        value = f(*args, **kwargs)
        elapsed = time.perf_counter() - start
        print(elapsed)
        return value

    return timed_f


@timed
def expensive_f():
    return sum(i ** 2 for i in range(1000000))


# expensive_f = timed(expensive_f)

class Button:
    def on_clicked(self):
        print('You clicked me')

    def register_on_clicked(self, f):
        self.on_clicked = f
        return f


buttons = [Button() for _ in range(10)]


@buttons[3].register_on_clicked
def print_hello():
    print('hello')


if __name__ == '__main__':
    print(expensive_f())

    for button in buttons:
        button.on_clicked()
