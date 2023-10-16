# Example from PEP 688

import inspect

# Implements __buffer__, __release_buffer__
class MyBuffer:
    def __init__(self, data: bytes):
        self.data = bytearray(data)
        self.view = None

    def __buffer__(self, flags: int) -> memoryview:
        if flags != inspect.BufferFlags.FULL_RO:
            raise TypeError("Only BufferFlags.FULL_RO supported")
        if self.view is not None:
            raise RuntimeError("Buffer already held")
        self.view = memoryview(self.data)
        return self.view

    def __release_buffer__(self, view: memoryview) -> None:
        assert self.view is view  # guaranteed to be true
        self.view.release()
        self.view = None

    def extend(self, b: bytes) -> None:
        if self.view is not None:
            raise RuntimeError("Cannot extend held buffer")
        self.data.extend(b)

def main():
    buffer = MyBuffer(b"capybara")

    # __buffer__ called here in memoryview:
    #    vvvvvvvvvvvvvvvvvv
    with memoryview(buffer) as view: 
        view[0] = ord("C")
        # __release_buffer__ called exiting with block

    # buffer now contains b"Capybara"

if __name__ == "__main__":
    main()