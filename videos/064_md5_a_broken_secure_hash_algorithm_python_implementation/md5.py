import tempfile
from io import BytesIO
from typing import BinaryIO

import numpy as np

shift = [7, 12, 17, 22, 7, 12, 17, 22, 7, 12, 17, 22, 7, 12, 17, 22,
         5, 9, 14, 20, 5, 9, 14, 20, 5, 9, 14, 20, 5, 9, 14, 20,
         4, 11, 16, 23, 4, 11, 16, 23, 4, 11, 16, 23, 4, 11, 16, 23,
         6, 10, 15, 21, 6, 10, 15, 21, 6, 10, 15, 21, 6, 10, 15, 21]
sines = np.abs(np.sin(np.arange(64) + 1))  # "nothing up my sleeve" randomness
sine_randomness = [int(x) for x in np.floor(2 ** 32 * sines)]
# K = [
#     0xd76aa478, 0xe8c7b756, 0x242070db, 0xc1bdceee,
#     0xf57c0faf, 0x4787c62a, 0xa8304613, 0xfd469501,
#     0x698098d8, 0x8b44f7af, 0xffff5bb1, 0x895cd7be,
#     0x6b901122, 0xfd987193, 0xa679438e, 0x49b40821,
#     0xf61e2562, 0xc040b340, 0x265e5a51, 0xe9b6c7aa,
#     0xd62f105d, 0x02441453, 0xd8a1e681, 0xe7d3fbc8,
#     0x21e1cde6, 0xc33707d6, 0xf4d50d87, 0x455a14ed,
#     0xa9e3e905, 0xfcefa3f8, 0x676f02d9, 0x8d2a4c8a,
#     0xfffa3942, 0x8771f681, 0x6d9d6122, 0xfde5380c,
#     0xa4beea44, 0x4bdecfa9, 0xf6bb4b60, 0xbebfbc70,
#     0x289b7ec6, 0xeaa127fa, 0xd4ef3085, 0x04881d05,
#     0xd9d4d039, 0xe6db99e5, 0x1fa27cf8, 0xc4ac5665,
#     0xf4292244, 0x432aff97, 0xab9423a7, 0xfc93a039,
#     0x655b59c3, 0x8f0ccc92, 0xffeff47d, 0x85845dd1,
#     0x6fa87e4f, 0xfe2ce6e0, 0xa3014314, 0x4e0811a1,
#     0xf7537e82, 0xbd3af235, 0x2ad7d2bb, 0xeb86d391]

md5_block_size = 64
md5_digest_size = 16


def left_rotate(x: int, y: int) -> int:
    """
    Rotate the bits of x by y places, as if x and y are 32-bit unsigned integers.

    >>> left_rotate(0b11111111000000001010101011001100, 1) == \
                    0b11111110000000010101010110011001
    True
    """
    return ((x << (y & 31)) | ((x & 0xffffffff) >> (32 - (y & 31)))) & 0xffffffff


def bit_not(x: int) -> int:
    """
    The bitwise complement of x if x were represented as a 32-bit unsigned integer.

    >>> bit_not(0b11111111000000001010101011001100) == \
                0b00000000111111110101010100110011
    True
    """
    return 4294967295 - x


"""
Mixing functions. 
Each of F, G, H, I has the following property.
Given: all the bits of all the inputs are independent and unbiased,
Then: the bits of the output are also independent and unbiased.
"""


def F(b: int, c: int, d: int) -> int:
    return d ^ (b & (c ^ d))


def G(b: int, c: int, d: int) -> int:
    return c ^ (d & (b ^ c))


def H(b: int, c: int, d: int) -> int:
    return b ^ c ^ d


def I(b: int, c: int, d: int) -> int:
    return c ^ (b | bit_not(d))


mixer_for_step = [F for _ in range(16)] + [G for _ in range(16)] + [H for _ in range(16)] + [I for _ in range(16)]

"""
These are all permutations of [0, ..., 15].
"""

round_1_perm = [i for i in range(16)]  # [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
round_2_perm = [(5 * i + 1) % 16 for i in range(16)]  # [1, 6, 11, 0, 5, 10, 15, 4, 9, 14, 3, 8, 13, 2, 7, 12]
round_3_perm = [(3 * i + 5) % 16 for i in range(16)]  # [5, 8, 11, 14, 1, 4, 7, 10, 13, 0, 3, 6, 9, 12, 15, 2]
round_4_perm = [(7 * i) % 16 for i in range(16)]  # [0, 7, 14, 5, 12, 3, 10, 1, 8, 15, 6, 13, 4, 11, 2, 9]

msg_idx_for_step = round_1_perm + round_2_perm + round_3_perm + round_4_perm


class MD5State:
    def __init__(self):
        self.length: int = 0
        self.state: tuple[int, int, int, int] = (0x67452301, 0xefcdab89, 0x98badcfe, 0x10325476)
        self.n_filled_bytes: int = 0
        self.buf: bytearray = bytearray(md5_block_size)

    def digest(self) -> bytes:
        return b''.join(x.to_bytes(length=4, byteorder='little') for x in self.state)

    def hex_digest(self) -> str:
        return self.digest().hex()

    def process(self, stream: BinaryIO) -> None:
        assert self.n_filled_bytes < len(self.buf)

        view = memoryview(self.buf)
        while bytes_read := stream.read(md5_block_size - self.n_filled_bytes):
            view[self.n_filled_bytes:self.n_filled_bytes + len(bytes_read)] = bytes_read
            if self.n_filled_bytes == 0 and len(bytes_read) == md5_block_size:
                self.compress(self.buf)
                self.length += md5_block_size
            else:
                self.n_filled_bytes += len(bytes_read)
                if self.n_filled_bytes == md5_block_size:
                    self.compress(self.buf)
                    self.length += md5_block_size
                    self.n_filled_bytes = 0

    def finalize(self) -> None:
        assert self.n_filled_bytes < md5_block_size

        self.length += self.n_filled_bytes
        self.buf[self.n_filled_bytes] = 0b10000000
        self.n_filled_bytes += 1

        n_bytes_needed_for_len = 8

        if self.n_filled_bytes + n_bytes_needed_for_len > md5_block_size:
            self.buf[self.n_filled_bytes:] = bytes(md5_block_size - self.n_filled_bytes)
            self.compress(self.buf)
            self.n_filled_bytes = 0

        self.buf[self.n_filled_bytes:] = bytes(md5_block_size - self.n_filled_bytes)
        bit_len_64 = (self.length * 8) % (2 ** 64)
        self.buf[-n_bytes_needed_for_len:] = bit_len_64.to_bytes(length=n_bytes_needed_for_len,
                                                                 byteorder='little')
        self.compress(self.buf)

    def compress(self, msg_chunk: bytearray) -> None:
        assert len(msg_chunk) == md5_block_size  # 64 bytes, 512 bits
        msg_ints = [int.from_bytes(msg_chunk[i:i + 4], byteorder='little') for i in range(0, md5_block_size, 4)]
        assert len(msg_ints) == 16

        a, b, c, d = self.state

        for i in range(md5_block_size):
            bit_mixer = mixer_for_step[i]
            msg_idx = msg_idx_for_step[i]
            a = (a + bit_mixer(b, c, d) + msg_ints[msg_idx] + sine_randomness[i]) % (2 ** 32)
            a = left_rotate(a, shift[i])
            a = (a + b) % (2 ** 32)
            a, b, c, d = d, a, b, c

        self.state = (
            (self.state[0] + a) % (2 ** 32),
            (self.state[1] + b) % (2 ** 32),
            (self.state[2] + c) % (2 ** 32),
            (self.state[3] + d) % (2 ** 32),
        )


def md5(s: bytes) -> bytes:
    state = MD5State()
    state.process(BytesIO(s))
    state.finalize()
    return state.digest()


def md5_file(file: BinaryIO) -> bytes:
    state = MD5State()
    state.process(file)
    state.finalize()
    return state.digest()


def test_md5():
    assert md5(b"").hex() == 'd41d8cd98f00b204e9800998ecf8427e'
    assert md5(b"a").hex() == '0cc175b9c0f1b6a831c399e269772661'
    assert md5(b"abc").hex() == '900150983cd24fb0d6963f7d28e17f72'
    assert md5(b"message digest").hex() == 'f96b697d7cb7938d525a2f31aaf161d0'
    assert md5(b"abcdefghijklmnopqrstuvwxyz").hex() == 'c3fcd3d76192e4007dfb496cca67e13b'
    assert md5(b"ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789").hex() == 'd174ab98d277d9f5a5611c2c9f419d9f'
    assert md5(b"12345678901234567890123456789012345678901234567890123456789012345678901234567890").hex() == '57edf4a22be3c955ac49da2e2107b67a'
    assert md5(b"The quick brown fox jumps over the lazy dog").hex() == '9e107d9d372bb6826bd81d3542a419d6'
    assert md5(b"The quick brown fox jumps over the lazy dog.").hex() == 'e4d909c290d0fb1ca068ffaddf22cbd0'

    with tempfile.TemporaryFile('w+b') as f:
        f.write(b"The quick brown fox jumps over the lazy dog")
        f.seek(0)
        assert md5_file(f).hex() == '9e107d9d372bb6826bd81d3542a419d6'


def test_collision():
    m0 = [
        0x4d, 0xc9, 0x68, 0xff, 0x0e, 0xe3, 0x5c, 0x20, 0x95, 0x72, 0xd4, 0x77, 0x7b, 0x72, 0x15, 0x87,
        0xd3, 0x6f, 0xa7, 0xb2, 0x1b, 0xdc, 0x56, 0xb7, 0x4a, 0x3d, 0xc0, 0x78, 0x3e, 0x7b, 0x95, 0x18,
        0xaf, 0xbf, 0xa2, 0x00, 0xa8, 0x28, 0x4b, 0xf3, 0x6e, 0x8e, 0x4b, 0x55, 0xb3, 0x5f, 0x42, 0x75,
        0x93, 0xd8, 0x49, 0x67, 0x6d, 0xa0, 0xd1, 0x55, 0x5d, 0x83, 0x60, 0xfb, 0x5f, 0x07, 0xfe, 0xa2,
    ]

    m1 = [
        0x4d, 0xc9, 0x68, 0xff, 0x0e, 0xe3, 0x5c, 0x20, 0x95, 0x72, 0xd4, 0x77, 0x7b, 0x72, 0x15, 0x87,
        0xd3, 0x6f, 0xa7, 0xb2, 0x1b, 0xdc, 0x56, 0xb7, 0x4a, 0x3d, 0xc0, 0x78, 0x3e, 0x7b, 0x95, 0x18,
        0xaf, 0xbf, 0xa2, 0x02, 0xa8, 0x28, 0x4b, 0xf3, 0x6e, 0x8e, 0x4b, 0x55, 0xb3, 0x5f, 0x42, 0x75,
        0x93, 0xd8, 0x49, 0x67, 0x6d, 0xa0, 0xd1, 0xd5, 0x5d, 0x83, 0x60, 0xfb, 0x5f, 0x07, 0xfe, 0xa2,
    ]

    # m0 different from m1 in only two places, 0x00 -> 0x02 at (2, 3) and 0x55 -> 0xd5 at (3, 7)

    bz0 = bytes(m0)
    bz1 = bytes(m1)

    assert len(bz0) == md5_block_size
    assert len(bz1) == md5_block_size

    expected_md5_hex = "008ee33a9d58b51cfeb425b0959121c9"

    assert bz0 != bz1
    assert md5(bz0).hex() == expected_md5_hex
    assert md5(bz1).hex() == expected_md5_hex


def types_of_attacks():
    def collision_attack():  # < 1s to compute
        bz0 = bytes(...)
        bz1 = bytes(...)
        assert md5(bz0) == md5(bz1)
        return bz0, bz1

    def chosen_prefix_attack(prefix0: bytes, prefix1: bytes, suffix: bytes):  # hours to a few days to compute
        bz0 = bytes(...)
        bz1 = bytes(...)
        assert md5(prefix0 + bz0 + suffix) == md5(prefix1 + bz1 + suffix)

    def second_preimage_attack(bz0: bytes):  # none publicly known, 2**123 theoretical time
        bz1 = bytes(...)
        assert md5(bz1) == md5(bz0)
        return bz1

    def preimage_attack(hash: bytes):  # none publicly known, 2**123 theoretical time
        bz0 = bytes(...)
        assert md5(bz0) == hash
        return bz0


def main():
    test_md5()
    test_collision()


if __name__ == '__main__':
    main()
