import sys

def my_trace(frame, event, arg):
    print(f"Event: {event}")
    return my_trace

def main():
    for x in range(5):
        print(x)

if __name__ == "__main__":
    sys.settrace(my_trace)
    main()

