from typing import TypeVar

T = TypeVar('T', str, bytes, bytearray)

def removeprefix(s: T, prefix: T) -> T:
    if s.startswith(prefix):
        return s[len(prefix):]
    else:
        return s[:]

def removesuffix(s: T, suffix: T) -> T:
    if suffix and s.endswith(suffix):
        return s[:-len(suffix)]
    else:
        return s[:]

def test_removeprefix():
    assert removeprefix('abctest', 'abc') == 'test'
    assert removeprefix('abctest', 'def') == 'abctest'
    assert removeprefix('abctest', '') == 'abctest'
    assert removeprefix('', 'def') == ''
    assert removeprefix('', '') == ''

    assert removeprefix(b'abctest', b'abc') == b'test'
    assert removeprefix(b'abctest', b'def') == b'abctest'
    assert removeprefix(b'abctest', b'') == b'abctest'
    assert removeprefix(b'', b'def') == b''
    assert removeprefix(b'', b'') == b''

    assert removeprefix(bytearray(b'abctest'), bytearray(b'abc')) == bytearray(b'test')
    assert removeprefix(bytearray(b'abctest'), bytearray(b'def')) == bytearray(b'abctest')
    assert removeprefix(bytearray(b'abctest'), bytearray(b'')) == bytearray(b'abctest')
    assert removeprefix(bytearray(b''), bytearray(b'def')) == bytearray(b'')
    assert removeprefix(bytearray(b''), bytearray(b'')) == bytearray(b'')

    x = bytearray(b'123')
    y = removeprefix(x, bytearray(b'abc'))
    assert y == x
    assert y is not x

    print('passed')


if __name__ == '__main__':
    # removesuffix files example
    files: list[str] = ['paint.exe', 'word.exe', 'virus.exe', 'not-modified-example']
    #files = [x.removesuffix('.exe') for x in files]
    print(files)

    # bytes Response example
    print(b'Response: DATA'.removeprefix(b'Response: '))

    # NOT rstrip and lstrip
    files = [x.rstrip('.exe') for x in files]
    print(files)

    # sample implementation, tests first!
    test_removeprefix()

