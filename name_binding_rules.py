def f():
    print(x)

def g():
    print(x)
    x = 1

y = 0
def h():
    print(y)

def j():
    print(y)
    y = 1

def main():
    f()

if __name__ == '__main__':
   main()
