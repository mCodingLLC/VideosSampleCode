class Solution:
    def isMatch(self, s: str, p: str, s_idx: int = 0, p_idx: int = 0) -> bool:
        if p_idx == len(p):
            return s_idx == len(s)

        while p_idx < len(p) - 1:
            if p[p_idx + 1] == "*":
                n = 0
                while s_idx + n < len(s) and (p[p_idx] == "." or p[p_idx] == s[s_idx + n]):
                    n += 1
                while n >= 0:
                    if self.isMatch(s, p, s_idx + n, p_idx + 2):
                        return True
                    n -= 1
                return False
            else:
                if s_idx < len(s) and (p[p_idx] == "." or p[p_idx] == s[s_idx]):
                    s_idx += 1
                    p_idx += 1
                else:
                    return False
        return s_idx == len(s) - 1 and (p[p_idx] == "." or p[p_idx] == s[s_idx])


def main():
    tests = [
        ('', '', True),
        ('', '.*', True),
        ('a', '.*', True),
        ('asdf', '.*', True),
        ('a', 'a', True),
        ('a', 'b', False),
        ('', 'a*', True),
        ('a', 'a*', True),
        ('aaaaaa', 'a*', True),
        ('aaaaab', 'a*', False),
        ('hello', 'hel*o', True),
        ('hello', 'hes*o', False),
        ('aaaaabbaabb', 'a*b*a*bb', True),
    ]
    soln = Solution()
    for s, p, expected in tests:
        actual = soln.isMatch(s, p)
        if actual != expected:
            print(f'failed: {s=} {p=} {actual=} {expected=}')


if __name__ == '__main__':
    main()
