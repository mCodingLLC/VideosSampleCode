import sys

def main():
    count = sys.getrefcount(None)
    print(f"0b{count:b}")


if __name__ == "__main__":
    main()
