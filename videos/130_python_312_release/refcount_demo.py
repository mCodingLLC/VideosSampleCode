import sys

def main():
    my_list = [1, 2, 3]
    print(sys.getrefcount(my_list)) # 2
    use_list(my_list)

def use_list(lst):
    print(sys.getrefcount(lst)) # 3


if __name__ == "__main__":
    main()
